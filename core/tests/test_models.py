"""
Unit tests for the Helping Hand core models.

Tests cover:
  - User creation (Patient + Agency roles)
  - StaffProfile validation (age >= 18, service type choices)
  - Booking pricing computation (all three tiers)
  - Booking gender matching enforcement
  - Booking auto-status on discharge file upload
  - One-time service forced to 1 day
  - Review model (only on completed bookings)
"""

from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import User, StaffProfile, Booking, Review
from core.pricing import calculate_price, get_tier, format_currency


# ═══════════════════════════════════════════════════════════════════════════════
# PRICING ENGINE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class PricingEngineTest(TestCase):
    """Test the pricing calculation engine (ported from pricing.js)."""

    def test_daily_tier(self):
        """1-6 days should be daily tier with 0% discount."""
        tier = get_tier(5)
        self.assertEqual(tier['label'], 'daily')
        self.assertEqual(tier['discount'], Decimal('0'))

    def test_weekly_tier(self):
        """7-29 days should be weekly tier with 10% discount."""
        tier = get_tier(14)
        self.assertEqual(tier['label'], 'weekly')
        self.assertEqual(tier['discount'], Decimal('0.10'))

    def test_monthly_tier(self):
        """30+ days should be monthly tier with 25% discount."""
        tier = get_tier(30)
        self.assertEqual(tier['label'], 'monthly')
        self.assertEqual(tier['discount'], Decimal('0.25'))

    def test_nursing_daily_price(self):
        """Nursing care for 5 days = ₹1500 * 5 = ₹7500 (no discount)."""
        result = calculate_price('nursing', 5)
        self.assertEqual(result['base_rate'], Decimal('1500'))
        self.assertEqual(result['total'], Decimal('7500'))
        self.assertEqual(result['discount'], Decimal('0'))

    def test_nursing_weekly_price(self):
        """Nursing care for 7 days = ₹1500 * 7 = ₹10500 - 10% = ₹9450."""
        result = calculate_price('nursing', 7)
        self.assertEqual(result['subtotal'], Decimal('10500'))
        self.assertEqual(result['discount_amount'], Decimal('1050'))
        self.assertEqual(result['total'], Decimal('9450'))
        self.assertEqual(result['tier'], 'weekly')

    def test_homecare_monthly_price(self):
        """Home care for 30 days = ₹1000 * 30 = ₹30000 - 25% = ₹22500."""
        result = calculate_price('homecare', 30)
        self.assertEqual(result['subtotal'], Decimal('30000'))
        self.assertEqual(result['discount_amount'], Decimal('7500'))
        self.assertEqual(result['total'], Decimal('22500'))
        self.assertEqual(result['tier'], 'monthly')

    def test_onetime_price(self):
        """One-time service is always 1 day, ₹500, no discount."""
        result = calculate_price('onetime', 99)  # Duration arg ignored
        self.assertEqual(result['total'], Decimal('500'))
        self.assertEqual(result['days'], 1)
        self.assertEqual(result['discount'], Decimal('0'))

    def test_invalid_service_type(self):
        """Invalid service type returns None."""
        result = calculate_price('invalid', 5)
        self.assertIsNone(result)

    def test_format_currency(self):
        """Currency formatting should use INR symbol."""
        self.assertEqual(format_currency(1500), '₹1,500')
        self.assertEqual(format_currency(Decimal('9450')), '₹9,450')


# ═══════════════════════════════════════════════════════════════════════════════
# USER MODEL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class UserModelTest(TestCase):
    """Test custom User model creation and role properties."""

    def test_create_patient_user(self):
        """Create a patient user with all required fields."""
        user = User.objects.create_user(
            username='patient1',
            password='testpass123',
            phone='9876543210',
            role=User.Role.PATIENT,
            first_name='Ramesh',
            last_name='Gupta',
        )
        self.assertEqual(user.role, 'patient')
        self.assertTrue(user.is_patient)
        self.assertFalse(user.is_agency)
        self.assertEqual(str(user), 'Ramesh Gupta (Patient)')

    def test_create_agency_user(self):
        """Create an agency manager user."""
        user = User.objects.create_user(
            username='agency1',
            password='testpass123',
            phone='9876543211',
            role=User.Role.AGENCY,
        )
        self.assertTrue(user.is_agency)
        self.assertFalse(user.is_patient)

    def test_phone_uniqueness(self):
        """Phone numbers must be unique across all users."""
        User.objects.create_user(
            username='user1', password='pass123', phone='9876543210'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='user2', password='pass123', phone='9876543210'
            )

    def test_default_role_is_patient(self):
        """Default role should be Patient."""
        user = User.objects.create_user(
            username='default_user', password='pass123', phone='9876543212'
        )
        self.assertEqual(user.role, User.Role.PATIENT)

    def test_profile_complete_default_false(self):
        """Profile should not be complete by default."""
        user = User.objects.create_user(
            username='newuser', password='pass123', phone='9876543213'
        )
        self.assertFalse(user.profile_complete)


# ═══════════════════════════════════════════════════════════════════════════════
# STAFF PROFILE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class StaffProfileModelTest(TestCase):
    """Test StaffProfile model validation and manager queries."""

    def setUp(self):
        self.agency = User.objects.create_user(
            username='agency1', password='pass123',
            phone='9876543220', role=User.Role.AGENCY,
        )

    def test_create_staff(self):
        """Create a valid staff profile."""
        staff = StaffProfile.objects.create(
            name='Priya Sharma',
            gender='female',
            age=28,
            specializations=['Nursing Care', 'Post-Surgery'],
            service_types=['nursing'],
            hourly_rate=Decimal('1500'),
            rating=Decimal('4.8'),
            review_count=124,
            available=True,
            agency=self.agency,
        )
        self.assertEqual(str(staff), 'Priya Sharma (Female, 28)')
        self.assertEqual(staff.service_types, ['nursing'])

    def test_staff_age_minimum(self):
        """Staff under 18 should fail validation."""
        staff = StaffProfile(
            name='Young Person',
            gender='male',
            age=17,
            specializations=['Home Care'],
            service_types=['homecare'],
            hourly_rate=Decimal('1000'),
            agency=self.agency,
        )
        with self.assertRaises(ValidationError):
            staff.full_clean()

    def test_invalid_service_type(self):
        """Invalid service types should fail validation."""
        staff = StaffProfile(
            name='Test Staff',
            gender='male',
            age=25,
            specializations=['Test'],
            service_types=['invalid_type'],
            hourly_rate=Decimal('1000'),
            agency=self.agency,
        )
        with self.assertRaises(ValidationError):
            staff.full_clean()

    def test_matching_queryset(self):
        """Staff matching should filter by gender, service type, and availability."""
        StaffProfile.objects.create(
            name='Female Nurse', gender='female', age=28,
            specializations=['Nursing'], service_types=['nursing'],
            hourly_rate=Decimal('1500'), available=True, agency=self.agency,
        )
        StaffProfile.objects.create(
            name='Male Nurse', gender='male', age=30,
            specializations=['Nursing'], service_types=['nursing'],
            hourly_rate=Decimal('1500'), available=True, agency=self.agency,
        )
        StaffProfile.objects.create(
            name='Unavailable Nurse', gender='female', age=26,
            specializations=['Nursing'], service_types=['nursing'],
            hourly_rate=Decimal('1500'), available=False, agency=self.agency,
        )

        matches = StaffProfile.objects.matching('female', 'nursing')
        self.assertEqual(matches.count(), 1)
        self.assertEqual(matches.first().name, 'Female Nurse')


# ═══════════════════════════════════════════════════════════════════════════════
# BOOKING MODEL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class BookingModelTest(TestCase):
    """Test Booking model with pricing, validation, and status logic."""

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient1', password='pass123',
            phone='9876543230', role=User.Role.PATIENT,
        )
        self.agency = User.objects.create_user(
            username='agency1', password='pass123',
            phone='9876543231', role=User.Role.AGENCY,
        )
        self.female_nurse = StaffProfile.objects.create(
            name='Priya Sharma', gender='female', age=28,
            specializations=['Nursing Care'], service_types=['nursing'],
            hourly_rate=Decimal('1500'), available=True, agency=self.agency,
        )
        self.male_homecare = StaffProfile.objects.create(
            name='Rajesh Kumar', gender='male', age=32,
            specializations=['Home Care'], service_types=['homecare'],
            hourly_rate=Decimal('1000'), available=True, agency=self.agency,
        )

    def _create_booking(self, **kwargs):
        """Helper to create a booking with sensible defaults."""
        defaults = {
            'patient': self.patient,
            'service_type': 'nursing',
            'patient_name': 'Test Patient',
            'patient_gender': 'female',
            'patient_age': 45,
            'start_date': date.today() + timedelta(days=1),
            'duration_days': 7,
            'address': '123 Test Street',
            'city': 'Mumbai',
            'pincode': '400001',
            'phone': '9876543232',
        }
        defaults.update(kwargs)
        return Booking.objects.create(**defaults)

    def test_auto_booking_id(self):
        """Booking should auto-generate a BK-XXXXXXXX ID."""
        booking = self._create_booking()
        self.assertTrue(booking.booking_id.startswith('BK-'))
        self.assertEqual(len(booking.booking_id), 11)  # BK- + 8 hex chars

    def test_nursing_weekly_pricing(self):
        """Nursing for 7 days should compute weekly discount pricing."""
        booking = self._create_booking(
            service_type='nursing', duration_days=7
        )
        self.assertEqual(booking.base_rate, Decimal('1500'))
        self.assertEqual(booking.subtotal, Decimal('10500'))
        self.assertEqual(booking.discount_percentage, Decimal('0.10'))
        self.assertEqual(booking.discount_amount, Decimal('1050'))
        self.assertEqual(booking.total_cost, Decimal('9450'))
        self.assertEqual(booking.pricing_tier, 'weekly')

    def test_homecare_monthly_pricing(self):
        """Home care for 30 days should compute monthly discount pricing."""
        booking = self._create_booking(
            service_type='homecare', duration_days=30
        )
        self.assertEqual(booking.base_rate, Decimal('1000'))
        self.assertEqual(booking.total_cost, Decimal('22500'))
        self.assertEqual(booking.pricing_tier, 'monthly')

    def test_onetime_forced_single_day(self):
        """One-time service duration should be forced to 1 day regardless."""
        booking = self._create_booking(
            service_type='onetime', duration_days=99
        )
        self.assertEqual(booking.duration_days, 1)
        self.assertEqual(booking.total_cost, Decimal('500'))
        self.assertEqual(booking.discount_percentage, Decimal('0'))

    def test_gender_matching_validation(self):
        """Assigning a female staff to a male patient should fail validation."""
        booking = self._create_booking(
            patient_gender='male',
            staff=self.female_nurse,  # Female staff
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_gender_matching_valid(self):
        """Assigning a female staff to a female patient should pass."""
        booking = self._create_booking(
            patient_gender='female',
            staff=self.female_nurse,
        )
        booking.full_clean()  # Should not raise

    def test_service_type_matching_validation(self):
        """Staff must support the booking's service type."""
        booking = self._create_booking(
            service_type='nursing',
            patient_gender='male',
            staff=self.male_homecare,  # Only does homecare
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_default_status_pending(self):
        """New bookings without discharge file should be pending."""
        booking = self._create_booking()
        self.assertEqual(booking.status, 'pending')

    def test_discharge_file_sets_reviewing_status(self):
        """Booking with discharge file should auto-set to 'reviewing' status."""
        booking = self._create_booking(
            discharge_file='test_discharge.pdf'
        )
        self.assertEqual(booking.status, 'reviewing')

    def test_patient_age_minimum(self):
        """Patient under 16 should fail validation."""
        booking = self._create_booking(patient_age=15)
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_booking_active_property(self):
        """Active property should return True for non-terminal statuses."""
        booking = self._create_booking()
        self.assertTrue(booking.is_active)

        booking.status = Booking.Status.COMPLETED
        self.assertFalse(booking.is_active)

    def test_end_date_computation(self):
        """End date should be start_date + duration - 1."""
        start = date(2026, 6, 1)
        booking = self._create_booking(start_date=start, duration_days=7)
        self.assertEqual(booking.end_date, date(2026, 6, 7))

    def test_active_queryset(self):
        """Active queryset should only return non-terminal bookings."""
        b1 = self._create_booking(patient_name='Active')
        b2 = self._create_booking(patient_name='Completed')
        b2.status = Booking.Status.COMPLETED
        b2.save()

        active = Booking.objects.active()
        self.assertEqual(active.count(), 1)
        self.assertEqual(active.first().patient_name, 'Active')

    def test_past_queryset(self):
        """Past queryset should only return completed/cancelled bookings."""
        b1 = self._create_booking(patient_name='Active')
        b2 = self._create_booking(patient_name='Done')
        b2.status = Booking.Status.COMPLETED
        b2.save()

        past = Booking.objects.past()
        self.assertEqual(past.count(), 1)
        self.assertEqual(past.first().patient_name, 'Done')


# ═══════════════════════════════════════════════════════════════════════════════
# REVIEW MODEL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class ReviewModelTest(TestCase):
    """Test Review model validation."""

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient1', password='pass123',
            phone='9876543240', role=User.Role.PATIENT,
        )
        self.booking = Booking.objects.create(
            patient=self.patient,
            service_type='nursing',
            patient_name='Test Patient',
            patient_gender='female',
            patient_age=45,
            start_date=date.today(),
            duration_days=7,
            address='Test Address',
            city='Mumbai',
            pincode='400001',
            phone='9876543241',
            status=Booking.Status.COMPLETED,
        )

    def test_create_review(self):
        """Create a valid review for a completed booking."""
        review = Review.objects.create(
            booking=self.booking,
            rating=5,
            comment='Excellent service!',
        )
        self.assertEqual(str(review), f'Review for {self.booking.booking_id} — 5★')

    def test_rating_range(self):
        """Rating must be between 1 and 5."""
        review = Review(booking=self.booking, rating=6)
        with self.assertRaises(ValidationError):
            review.full_clean()

        review = Review(booking=self.booking, rating=0)
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_on_non_completed_booking(self):
        """Reviews should only be allowed on completed bookings."""
        self.booking.status = Booking.Status.PENDING
        self.booking.save()

        review = Review(booking=self.booking, rating=4)
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_one_review_per_booking(self):
        """Each booking can only have one review (OneToOneField)."""
        Review.objects.create(booking=self.booking, rating=5)
        with self.assertRaises(Exception):
            Review.objects.create(booking=self.booking, rating=3)
