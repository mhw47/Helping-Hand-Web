"""
Core views for the Helping Hand application.

Phase 2: Static pages — Landing, Services, Support.
Phase 3: Authentication — Register, Login, Logout.
"""

import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import (
    PatientRegistrationForm,
    AgencyRegistrationForm,
    HelpingHandLoginForm,
)
from .pricing import SERVICE_RATES, format_currency


# ─── Helper: Build common context data ─────────────────────────────────────────

TESTIMONIALS = [
    {
        'name': 'Ramesh Gupta',
        'location': 'Mumbai',
        'rating': 5,
        'text': 'The nursing care for my father was exceptional. The staff was '
                'professional, caring, and always on time. Highly recommended!',
        'service': 'Nursing Care',
    },
    {
        'name': 'Kavita Reddy',
        'location': 'Pune',
        'rating': 5,
        'text': 'Helping Hand made it so easy to find a caregiver for my mother. '
                'The home care service exceeded our expectations.',
        'service': 'Home Care',
    },
    {
        'name': 'Suresh Iyer',
        'location': 'Thane',
        'rating': 4,
        'text': 'Quick and reliable one-time service. The staff was gentle and '
                'experienced with elderly care. Will book again.',
        'service': 'One-Time Service',
    },
    {
        'name': 'Anita Desai',
        'location': 'Navi Mumbai',
        'rating': 5,
        'text': 'Post-surgery nursing care was top-notch. The nurse was '
                'knowledgeable and made my recovery so much smoother.',
        'service': 'Nursing Care',
    },
]

FAQS = [
    {'q': 'How do I book a service?',
     'a': "Simply click 'Book Now', select your service type, fill in patient details, "
          "choose your dates, and confirm. It takes less than 5 minutes!",
     'cat': 'Booking'},
    {'q': 'What qualifications do your staff have?',
     'a': 'All our nursing staff are registered nurses with valid certifications. '
          'Home care staff undergo thorough background checks and training.',
     'cat': 'Staff'},
    {'q': 'Can I cancel my booking?',
     'a': 'Yes, you can cancel up to 24 hours before the scheduled start time for '
          'a full refund. Late cancellations may incur a fee.',
     'cat': 'Booking'},
    {'q': 'How is pricing calculated?',
     'a': 'Pricing is based on the service type and duration. We offer discounts '
          'for weekly (10% off) and monthly (25% off) bookings.',
     'cat': 'Pricing'},
    {'q': 'Do you match staff by gender?',
     'a': 'Yes, we strictly match male staff with male patients and female staff '
          'with female patients to ensure comfort.',
     'cat': 'Staff'},
    {'q': 'What areas do you serve?',
     'a': 'We currently serve major cities across Maharashtra, with plans to '
          'expand to other states.',
     'cat': 'General'},
    {'q': 'Is there a minimum age for patients?',
     'a': 'Yes, we provide care for patients aged 16 and above.',
     'cat': 'General'},
    {'q': 'What if I need to upload medical documents?',
     'a': 'You can upload a hospital discharge ticket during the booking process. '
          'Our team will review it.',
     'cat': 'Booking'},
]

SERVICE_CARDS = [
    {
        'key': 'nursing',
        'icon': 'stethoscope',
        'title': 'Nursing Care',
        'desc': 'Professional registered nurses providing medical care, medication '
                'management, wound care, and vital monitoring in the comfort of your home.',
        'bg_class': 'icon-bg-teal',
        'icon_class': 'icon-teal',
        'gradient_class': 'gradient-teal',
    },
    {
        'key': 'homecare',
        'icon': 'home',
        'title': 'Home Care',
        'desc': 'Dedicated caregivers assisting with daily living activities, '
                'providing companionship, and ensuring comfort for elderly family members.',
        'bg_class': 'icon-bg-blue',
        'icon_class': 'icon-blue',
        'gradient_class': 'gradient-blue',
    },
    {
        'key': 'onetime',
        'icon': 'hand-heart',
        'title': 'One-Time Services',
        'desc': 'Quick, on-demand assistance for specific tasks like bathing, '
                'diaper changes, and other elderly care needs without long-term commitments.',
        'bg_class': 'icon-bg-purple',
        'icon_class': 'icon-purple',
        'gradient_class': 'gradient-purple',
    },
]

SERVICE_FEATURES = {
    'nursing': [
        'Medication Administration', 'Wound Care & Dressing',
        'Vital Signs Monitoring', 'Post-Surgery Care',
        'IV Therapy & Injections', 'Chronic Disease Management',
    ],
    'homecare': [
        'Daily Living Assistance', 'Mobility Support',
        'Meal Preparation', 'Companionship',
        'Light Housekeeping', 'Exercise & Therapy Assistance',
    ],
    'onetime': [
        'Bathing Assistance', 'Diaper Changes',
        'Grooming & Hygiene', 'Feeding Assistance',
        'Bed Repositioning', 'Short-Term Emergency Care',
    ],
}


def _build_service_context(card):
    """Enrich a service card dict with pricing data."""
    rate = SERVICE_RATES[card['key']]
    daily = rate['daily']
    return {
        **card,
        'price': format_currency(daily),
        'daily_price': format_currency(daily),
        'weekly_price': format_currency(int(daily * Decimal('0.9'))),
        'monthly_price': format_currency(int(daily * Decimal('0.75'))),
    }


def _build_pricing_rates():
    """Build pricing rate list for the landing page pricing section."""
    rates = []
    for key, rate in SERVICE_RATES.items():
        daily = rate['daily']
        rates.append({
            'key': key,
            'label': rate['label'],
            'daily_formatted': format_currency(daily),
            'weekly_formatted': format_currency(int(daily * Decimal('0.9'))),
            'monthly_formatted': format_currency(int(daily * Decimal('0.75'))),
        })
    return rates


# ═══════════════════════════════════════════════════════════════════════════════
# VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

class LandingView(TemplateView):
    """Landing page with hero, services, how-it-works, pricing, testimonials."""

    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Services (summary cards)
        ctx['services'] = [_build_service_context(c) for c in SERVICE_CARDS]

        # Stats
        ctx['stats'] = [
            {'value': '2,500+', 'label': 'Happy Patients', 'icon': 'users'},
            {'value': '150+', 'label': 'Certified Staff', 'icon': 'user-check'},
            {'value': '12+', 'label': 'Cities Served', 'icon': 'award'},
            {'value': '4.8', 'label': 'Average Rating', 'icon': 'star'},
        ]

        # How it works
        ctx['steps'] = [
            {'num': '01', 'icon': 'search', 'title': 'Browse Services',
             'desc': 'Explore our range of nursing and home care services with transparent pricing.'},
            {'num': '02', 'icon': 'calendar-check', 'title': 'Book Online',
             'desc': 'Fill in patient details, choose your dates, and confirm your booking in minutes.'},
            {'num': '03', 'icon': 'user-check', 'title': 'Get Care',
             'desc': 'A matched, verified professional arrives at your doorstep ready to help.'},
        ]

        # Pricing rates
        ctx['pricing_rates'] = _build_pricing_rates()

        # Testimonials
        ctx['testimonials'] = TESTIMONIALS
        ctx['testimonials_json'] = json.dumps(TESTIMONIALS)

        return ctx


class ServicesView(TemplateView):
    """Detailed services page with features and pricing breakdowns."""

    template_name = 'core/services.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Detailed service cards with features and pricing
        detailed = []
        for card in SERVICE_CARDS:
            enriched = _build_service_context(card)
            enriched['features'] = SERVICE_FEATURES.get(card['key'], [])
            detailed.append(enriched)

        ctx['services_detailed'] = detailed

        # Highlights
        ctx['highlights'] = [
            {'icon': 'shield', 'title': 'Verified Staff',
             'desc': 'Background-checked and certified professionals'},
            {'icon': 'clock', 'title': '24/7 Availability',
             'desc': 'Round-the-clock service when you need it'},
            {'icon': 'star', 'title': 'Quality Assured',
             'desc': 'Rated 4.8/5 by thousands of families'},
        ]

        return ctx


class SupportView(TemplateView):
    """Support page with searchable FAQ accordion and contact info."""

    template_name = 'core/support.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['faqs'] = FAQS
        ctx['categories'] = ['All'] + sorted(set(f['cat'] for f in FAQS))
        return ctx


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH VIEWS — Phase 3
# ═══════════════════════════════════════════════════════════════════════════════

class RegisterView(FormView):
    """
    User registration view with role-based form selection.

    GET /auth/register/?role=patient   → PatientRegistrationForm
    GET /auth/register/?role=agency    → AgencyRegistrationForm
    """

    template_name = 'auth/register.html'
    success_url = reverse_lazy('landing')

    def get_role(self):
        """Get the selected role from query params, default to 'patient'."""
        role = self.request.GET.get('role', 'patient')
        if role not in ('patient', 'agency'):
            role = 'patient'
        return role

    def get_form_class(self):
        if self.get_role() == 'agency':
            return AgencyRegistrationForm
        return PatientRegistrationForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['role'] = self.get_role()
        return ctx

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f'Welcome to Helping Hand, {user.get_full_name() or user.username}! '
            f'Your account has been created successfully.'
        )
        return redirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        """Redirect already-authenticated users to the landing page."""
        if request.user.is_authenticated:
            return redirect('landing')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    Styled login view using Django's built-in LoginView.

    Redirects authenticated users away. On success, redirects to
    LOGIN_REDIRECT_URL (default: landing page).
    """

    template_name = 'auth/login.html'
    authentication_form = HelpingHandLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Welcome back, {self.request.user.get_full_name() or self.request.user.username}!'
        )
        return response


class CustomLogoutView(LogoutView):
    """
    Logout view — redirects to landing page with a success message.
    """

    next_page = reverse_lazy('landing')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

