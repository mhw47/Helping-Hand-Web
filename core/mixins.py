"""
Permission mixins for class-based views.

Usage:
    class DashboardView(PatientRequiredMixin, TemplateView):
        template_name = 'core/dashboard.html'

    class StaffManagementView(AgencyRequiredMixin, ListView):
        model = StaffProfile
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class PatientRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin that requires the user to be logged in AND have a 'patient' role.

    Redirects unauthenticated users to the login page.
    Raises 403 Forbidden for authenticated users with wrong role.
    """

    def test_func(self):
        return self.request.user.is_patient

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(
                'This page is only accessible to patient accounts.'
            )
        return super().handle_no_permission()


class AgencyRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin that requires the user to be logged in AND have an 'agency' role.

    Redirects unauthenticated users to the login page.
    Raises 403 Forbidden for authenticated users with wrong role.
    """

    def test_func(self):
        return self.request.user.is_agency

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(
                'This page is only accessible to agency manager accounts.'
            )
        return super().handle_no_permission()


class ProfileCompleteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin that requires the user's profile to be complete.

    Redirects to the profile completion page if profile_complete is False.
    """

    profile_incomplete_url = '/auth/complete-profile/'

    def test_func(self):
        return self.request.user.profile_complete

    def handle_no_permission(self):
        if self.request.user.is_authenticated and not self.request.user.profile_complete:
            from django.shortcuts import redirect
            return redirect(self.profile_incomplete_url)
        return super().handle_no_permission()
