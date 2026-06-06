"""
Django Admin configuration for the Helping Hand application.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, StaffProfile, Booking, Review


# ═══════════════════════════════════════════════════════════════════════════════
# USER ADMIN
# ═══════════════════════════════════════════════════════════════════════════════

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Extended User admin with healthcare-specific fields."""

    list_display = [
        'username', 'get_full_name', 'phone', 'role',
        'profile_complete', 'is_active', 'date_joined',
    ]
    list_filter = ['role', 'profile_complete', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'phone', 'email']
    ordering = ['-date_joined']

    # Add custom fields to the admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Contact', {
            'fields': ('role', 'phone', 'alternate_phone'),
        }),
        ('Address', {
            'fields': ('address', 'address_line2', 'city', 'state', 'pincode'),
            'classes': ('collapse',),
        }),
        ('Profile Status', {
            'fields': ('profile_complete',),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Contact', {
            'fields': ('role', 'phone'),
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name() or '—'
    get_full_name.short_description = 'Full Name'


# ═══════════════════════════════════════════════════════════════════════════════
# STAFF PROFILE ADMIN
# ═══════════════════════════════════════════════════════════════════════════════

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    """Admin for managing healthcare staff profiles."""

    list_display = ['name', 'gender', 'age', 'get_service_types', 'hourly_rate', 'rating', 'review_count', 'available']
    list_filter = ['gender', 'available']
    search_fields = ['name', 'specializations']
    list_editable = ['available']
    ordering = ['-rating', 'name']

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'gender', 'age', 'photo'),
        }),
        ('Professional Details', {
            'fields': ('specializations', 'service_types', 'hourly_rate'),
        }),
        ('Performance', {
            'fields': ('rating', 'review_count', 'available'),
        }),
    )

    def get_service_types(self, obj):
        return ', '.join(obj.service_types) if obj.service_types else '—'
    get_service_types.short_description = 'Service Types'


# ═══════════════════════════════════════════════════════════════════════════════
# BOOKING ADMIN
# ═══════════════════════════════════════════════════════════════════════════════

class ReviewInline(admin.StackedInline):
    """Inline review display within a booking."""
    model = Review
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin for managing healthcare bookings."""

    list_display = [
        'booking_id', 'patient_name', 'service_type', 'status',
        'start_date', 'duration_days', 'total_cost', 'staff', 'created_at',
    ]
    list_filter = ['status', 'service_type', 'created_at']
    search_fields = ['booking_id', 'patient_name', 'patient__username', 'city']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = [
        'booking_id', 'base_rate', 'discount_percentage',
        'discount_amount', 'subtotal', 'total_cost', 'pricing_tier',
        'created_at', 'updated_at',
    ]
    inlines = [ReviewInline]

    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_id', 'patient', 'staff', 'status'),
        }),
        ('Service Details', {
            'fields': ('service_type', 'start_date', 'duration_days'),
        }),
        ('Patient Information', {
            'fields': ('patient_name', 'patient_gender', 'patient_age'),
        }),
        ('Medical Details', {
            'fields': ('symptoms', 'illnesses', 'conditions', 'discharge_file'),
            'classes': ('collapse',),
        }),
        ('Service Address', {
            'fields': ('address', 'city', 'pincode', 'phone'),
        }),
        ('Pricing (Auto-Computed)', {
            'fields': (
                'base_rate', 'discount_percentage', 'discount_amount',
                'subtotal', 'total_cost', 'pricing_tier',
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# REVIEW ADMIN (standalone)
# ═══════════════════════════════════════════════════════════════════════════════

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin for viewing reviews."""

    list_display = ['booking', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['booking__booking_id', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
