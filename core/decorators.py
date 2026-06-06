"""
Permission decorators for function-based views.

Usage:
    @patient_required
    def my_patient_view(request):
        ...

    @agency_required
    def staff_management(request):
        ...
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def patient_required(view_func):
    """
    Decorator that requires the user to be authenticated AND a patient.

    Chains with @login_required so unauthenticated users get redirected
    to the login page. Authenticated non-patients get 403.
    """
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_patient:
            raise PermissionDenied(
                'This page is only accessible to patient accounts.'
            )
        return view_func(request, *args, **kwargs)
    return _wrapped



def profile_complete_required(view_func):
    """
    Decorator that requires the user's profile to be complete.

    Redirects to profile completion if profile_complete is False.
    """
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.profile_complete:
            from django.shortcuts import redirect
            return redirect('complete_profile')
        return view_func(request, *args, **kwargs)
    return _wrapped
