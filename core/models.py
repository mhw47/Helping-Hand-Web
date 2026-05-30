"""
Core data models for the Helping Hand healthcare marketplace.

Migrated from React/Firebase (NoSQL + localStorage) to strict relational
Django ORM models backed by PostgreSQL.

Source references:
  - Webpage/src/data/mockData.js      → StaffProfile
  - Webpage/src/context/AuthContext.jsx → User
  - Webpage/src/pages/BookingPage.jsx   → Booking
  - Webpage/src/pages/DashboardPage.jsx → Booking statuses, Review
  - Webpage/src/lib/pricing.js          → Pricing computation in Booking.save()
  - Webpage/src/lib/validation.js       → Validators
"""

import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .managers import BookingManager, StaffProfileManager
from .pricing import calculate_price
from .validators import phone_validator, pincode_validator


# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
# SHARED ENUMS — used by StaffProfile, Booking, and views
# ═══════════════════════════════════════════════════════════════════════════════

class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'


class ServiceType(models.TextChoices):
    NURSING = 'nursing', 'Nursing Care'
    HOMECARE = 'homecare', 'Home Care'
    ONETIME = 'onetime', 'One-Time Service'


# ═══════════════════════════════════════════════════════════════════════════════
# USER MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class User(AbstractUser):
    """
    Custom User model supporting Patient and Agency Manager roles.

    Extends Django's AbstractUser to add healthcare-specific profile fields.
    Replaces the React AuthContext mock user with proper database-backed auth.

    Authentication: Django session-based (username + password).
    The phone field is retained for contact purposes but is NOT used for auth.
    """

    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        AGENCY = 'agency', 'Agency Manager'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PATIENT,
        db_index=True,
        help_text='Determines access permissions and dashboard views.',
    )

    # Contact info
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_validator],
        help_text='Primary phone number (10 digits).',
    )
    alternate_phone = models.CharField(
        max_length=15,
        blank=True,
        default='',
        validators=[phone_validator],
        help_text='Optional alternate contact number.',
    )

    # Address (populated during profile completion)
    address = models.TextField(
        blank=True,
        default='',
        help_text='House/Flat No., Street, Landmark.',
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='Additional address details.',
    )
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    pincode = models.CharField(
        max_length=6,
        blank=True,
        default='',
        validators=[pincode_validator],
    )

    profile_complete = models.BooleanField(
        default=False,
        help_text='Whether the user has completed profile setup.',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        display = self.get_full_name() or self.username
        return f'{display} ({self.get_role_display()})'

    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT

    @property
    def is_agency(self):
        return self.role == self.Role.AGENCY


# ═══════════════════════════════════════════════════════════════════════════════
# STAFF PROFILE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class StaffProfile(models.Model):
    """
    Healthcare staff member profile.

    Migrated from the mockStaff array in mockData.js.
    Each staff member belongs to an agency (ForeignKey to User with role='agency').
    Uses JSONField for specializations and service types (works on all DB backends).
    """

    # Use module-level Gender and ServiceType enums

    # Identity
    name = models.CharField(max_length=200)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18)],
        help_text='Staff must be at least 18 years old.',
    )
    photo = models.ImageField(
        upload_to='staff_photos/',
        blank=True,
        default='',
    )

    # Professional attributes
    specializations = models.JSONField(
        default=list,
        help_text='List of specializations, e.g. ["Nursing Care", "Post-Surgery"].',
    )
    service_types = models.JSONField(
        default=list,
        help_text='Service types this staff can provide, e.g. ["nursing", "onetime"].',
    )
    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Rate in INR per day.',
    )

    # Performance metrics
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal('0.0'),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    review_count = models.PositiveIntegerField(default=0)
    available = models.BooleanField(
        default=True,
        db_index=True,
        help_text='Whether the staff member is available for new bookings.',
    )

    # Ownership
    agency = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profiles',
        limit_choices_to={'role': User.Role.AGENCY},
        help_text='The agency that manages this staff member.',
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom manager
    objects = StaffProfileManager

    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'
        ordering = ['-rating', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_gender_display()}, {self.age})'

    def clean(self):
        super().clean()
        # Validate that service_types contain only valid choices
        valid_types = {choice[0] for choice in ServiceType.choices}
        if self.service_types:
            invalid = set(self.service_types) - valid_types
            if invalid:
                raise ValidationError({
                    'service_types': f'Invalid service types: {", ".join(invalid)}. '
                                     f'Must be one of: {", ".join(valid_types)}.'
                })


# ═══════════════════════════════════════════════════════════════════════════════
# BOOKING MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Booking(models.Model):
    """
    Central booking/transaction model for healthcare service requests.

    Enforces all business rules at the model level:
      - Patient age >= 16
      - Gender matching between patient and assigned staff
      - Automatic pricing calculation based on service type and duration
      - One-time services forced to 1 day duration
      - Auto 'reviewing' status when discharge file is uploaded

    Migrated from React's BookingPage.jsx localStorage-based booking system.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        REVIEWING = 'reviewing', 'Under Review'
        CONFIRMED = 'confirmed', 'Confirmed'
        IN_PROGRESS = 'in-progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    # Use module-level ServiceType enum

    # ── Booking Identifier ─────────────────────────────────────────────────
    booking_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
        help_text='Auto-generated booking ID (e.g., BK-a1b2c3d4).',
    )

    # ── Relationships ──────────────────────────────────────────────────────
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': User.Role.PATIENT},
    )
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
        help_text='Assigned staff member. Null until staff is matched.',
    )

    # ── Service Details ────────────────────────────────────────────────────
    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
    )

    # ── Patient Information ────────────────────────────────────────────────
    patient_name = models.CharField(max_length=200)
    patient_gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )
    patient_age = models.PositiveIntegerField(
        validators=[MinValueValidator(16)],
        help_text='Patient must be at least 16 years old.',
    )

    # ── Medical Information ────────────────────────────────────────────────
    symptoms = models.TextField(blank=True, default='')
    illnesses = models.TextField(blank=True, default='')
    conditions = models.TextField(blank=True, default='')
    discharge_file = models.FileField(
        upload_to='discharge_docs/%Y/%m/',
        blank=True,
        default='',
        help_text='Discharge summary document (PDF, JPG, PNG).',
    )

    # ── Schedule ───────────────────────────────────────────────────────────
    start_date = models.DateField()
    duration_days = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        help_text='Number of days for the service (max 365).',
    )

    # ── Service Address ────────────────────────────────────────────────────
    address = models.TextField(help_text='Full service address.')
    city = models.CharField(max_length=100)
    pincode = models.CharField(
        max_length=6,
        validators=[pincode_validator],
    )
    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],
        help_text='Contact phone for this booking.',
    )

    # ── Pricing (computed on save) ─────────────────────────────────────────
    base_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'),
        help_text='Daily rate before discount.',
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0'),
        help_text='Discount percentage (0.10 = 10%).',
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'),
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'),
        help_text='Total before discount.',
    )
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'),
        help_text='Final amount after discount.',
    )
    pricing_tier = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text='Pricing tier applied: daily, weekly, or monthly.',
    )

    # ── Status ─────────────────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    # ── Timestamps ─────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom manager
    objects = BookingManager

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['patient', 'status']),
        ]

    def __str__(self):
        return f'{self.booking_id} — {self.patient_name} ({self.get_service_type_display()})'

    def clean(self):
        """
        Model-level validation enforcing healthcare business rules.
        """
        super().clean()
        errors = {}

        # Rule: Gender matching — if staff is assigned, genders must match
        if self.staff and self.patient_gender:
            if self.staff.gender != self.patient_gender:
                errors['staff'] = (
                    f'Staff gender ({self.staff.get_gender_display()}) must match '
                    f'patient gender ({self.get_patient_gender_display()}).'
                )

        # Rule: Staff must support the booking's service type
        if self.staff and self.service_type:
            if self.service_type not in (self.staff.service_types or []):
                errors['staff'] = (
                    f'Staff member {self.staff.name} does not provide '
                    f'{self.get_service_type_display()} services.'
                )

        if errors:
            raise ValidationError(errors)

    def _generate_booking_id(self):
        """Generate a unique booking ID with BK- prefix."""
        short_uuid = uuid.uuid4().hex[:8]
        return f'BK-{short_uuid}'

    def _compute_pricing(self):
        """Compute and set all pricing fields based on service_type and duration_days."""
        # Force one-time services to 1 day
        if self.service_type == ServiceType.ONETIME:
            self.duration_days = 1

        pricing = calculate_price(self.service_type, self.duration_days)
        if pricing:
            self.base_rate = pricing['base_rate']
            self.discount_percentage = pricing['discount']
            self.discount_amount = pricing['discount_amount']
            self.subtotal = pricing['subtotal']
            self.total_cost = pricing['total']
            self.pricing_tier = pricing['tier']

    def _determine_initial_status(self):
        """Set initial status based on whether a discharge file is uploaded."""
        # Only set auto-status for new bookings (no pk yet) or pending bookings
        if not self.pk or self.status == self.Status.PENDING:
            if self.discharge_file:
                self.status = self.Status.REVIEWING
            elif self.status not in [s[0] for s in self.Status.choices]:
                self.status = self.Status.PENDING

    _PRICING_FIELDS = ('service_type', 'duration_days')

    def save(self, *args, **kwargs):
        """
        Override save to:
        1. Auto-generate booking_id for new bookings
        2. Compute pricing fields (only when relevant fields change)
        3. Determine initial status
        """
        is_new = not self.pk

        # Generate booking ID for new records
        if not self.booking_id:
            self.booking_id = self._generate_booking_id()
            # Ensure uniqueness (extremely unlikely collision, but be safe)
            while Booking.objects.filter(booking_id=self.booking_id).exists():
                self.booking_id = self._generate_booking_id()

        # Only recompute pricing for new bookings or when pricing fields change
        if is_new:
            self._compute_pricing()
        else:
            try:
                old = Booking.objects.only(*self._PRICING_FIELDS).get(pk=self.pk)
                if any(getattr(old, f) != getattr(self, f) for f in self._PRICING_FIELDS):
                    self._compute_pricing()
            except Booking.DoesNotExist:
                self._compute_pricing()

        # Determine status for new bookings
        if is_new:
            self._determine_initial_status()

        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """Whether this booking is currently active."""
        return self.status in [
            self.Status.PENDING,
            self.Status.CONFIRMED,
            self.Status.IN_PROGRESS,
            self.Status.REVIEWING,
        ]

    @property
    def has_discharge_file(self):
        """Whether a discharge document has been uploaded."""
        return bool(self.discharge_file)

    @property
    def end_date(self):
        """Computed end date based on start_date + duration_days."""
        if self.start_date:
            from datetime import timedelta
            return self.start_date + timedelta(days=self.duration_days - 1)
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# REVIEW MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Review(models.Model):
    """
    Patient review for a completed booking.

    One review per booking (OneToOneField).
    Migrated from the review modal in DashboardPage.jsx.
    """

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review',
        limit_choices_to={'status': Booking.Status.COMPLETED},
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars.',
    )
    comment = models.TextField(
        blank=True,
        default='',
        help_text='Optional review comment.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f'Review for {self.booking.booking_id} — {self.rating}★'

    def clean(self):
        super().clean()
        if self.booking_id and self.booking.status != Booking.Status.COMPLETED:
            raise ValidationError({
                'booking': 'Reviews can only be submitted for completed bookings.'
            })
