"""
Custom validators for the Helping Hand application.

Ported from: Webpage/src/lib/validation.js
"""

from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must be exactly 10 digits.',
    code='invalid_phone',
)

pincode_validator = RegexValidator(
    regex=r'^\d{6}$',
    message='Pin code must be exactly 6 digits.',
    code='invalid_pincode',
)
