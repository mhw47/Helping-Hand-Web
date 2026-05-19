"""
Custom model managers and querysets for the Helping Hand application.
"""

from django.db import models


class BookingQuerySet(models.QuerySet):
    """Custom queryset for Booking model with commonly-used filters."""

    def active(self):
        """Bookings that are currently active (not completed or cancelled)."""
        return self.filter(
            status__in=['pending', 'confirmed', 'in-progress', 'reviewing']
        )

    def past(self):
        """Bookings that are completed or cancelled."""
        return self.filter(
            status__in=['completed', 'cancelled']
        )

    def for_patient(self, user):
        """All bookings for a specific patient."""
        return self.filter(patient=user)

    def for_agency(self, user):
        """All bookings assigned to staff managed by a specific agency."""
        return self.filter(staff__agency=user)

    def by_service_type(self, service_type):
        """Filter by service type."""
        return self.filter(service_type=service_type)

    def needs_review(self):
        """Bookings awaiting discharge document review."""
        return self.filter(status='reviewing')


<<<<<<< HEAD
# Auto-proxies all QuerySet methods to the Manager — no manual delegation needed.
BookingManager = BookingQuerySet.as_manager()
=======
class BookingManager(models.Manager):
    """Custom manager that uses BookingQuerySet."""

    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def past(self):
        return self.get_queryset().past()

    def needs_review(self):
        return self.get_queryset().needs_review()
>>>>>>> c33abf1 (Reworked the whole architecture with Django & PostgreSQL)


class StaffProfileQuerySet(models.QuerySet):
    """Custom queryset for StaffProfile model."""

    def available(self):
        """Only staff members who are currently available."""
        return self.filter(available=True)

    def by_gender(self, gender):
        """Filter by gender."""
        return self.filter(gender=gender)

    def by_service_type(self, service_type):
        """
        Filter by service type stored in JSONField list.

        Uses a DB-agnostic approach: fetches candidates and filters in Python,
        since JSONField __contains is not supported on SQLite.
        On PostgreSQL in production, you could optimize this with __contains.
        """
        pks = [
            obj.pk for obj in self.all()
            if service_type in (obj.service_types or [])
        ]
        return self.filter(pk__in=pks)

    def matching(self, patient_gender, service_type):
        """
        Find available staff matching both gender and service type.
        Mirrors the React findMatchingStaff() function from mockData.js.
        """
        base_qs = (
            self.available()
            .by_gender(patient_gender)
            .filter(age__gte=18)
        )
        # Filter by service type (JSONField list containment)
        pks = [
            obj.pk for obj in base_qs
            if service_type in (obj.service_types or [])
        ]
        return base_qs.filter(pk__in=pks)


<<<<<<< HEAD
# Auto-proxies all QuerySet methods to the Manager — no manual delegation needed.
StaffProfileManager = StaffProfileQuerySet.as_manager()
=======
class StaffProfileManager(models.Manager):
    """Custom manager that uses StaffProfileQuerySet."""

    def get_queryset(self):
        return StaffProfileQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def matching(self, patient_gender, service_type):
        return self.get_queryset().matching(patient_gender, service_type)
>>>>>>> c33abf1 (Reworked the whole architecture with Django & PostgreSQL)
