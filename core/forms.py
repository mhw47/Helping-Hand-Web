"""
Forms for the Helping Hand application.

Phase 3: Authentication — Registration and Login forms.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class BaseRegistrationForm(UserCreationForm):
    """
    Shared registration form for all user roles.

    Contains common fields (name, phone, username, passwords) and widget
    styling. Subclasses only need to set ROLE and add role-specific fields.
    """

    ROLE = None  # Subclasses MUST override

    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'First name',
            'id': 'reg-first-name',
            'autocomplete': 'given-name',
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Last name',
            'id': 'reg-last-name',
            'autocomplete': 'family-name',
        }),
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': '10-digit phone number',
            'id': 'reg-phone',
            'inputmode': 'numeric',
            'autocomplete': 'tel',
        }),
        help_text='Your primary contact number (10 digits).',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone',
                  'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Choose a username',
                'id': 'reg-username',
                'autocomplete': 'username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the password fields once for all roles
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Create a password',
            'id': 'reg-password1',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Confirm password',
            'id': 'reg-password2',
            'autocomplete': 'new-password',
        })

    def save(self, commit=True):
        """Set role from the class-level ROLE constant."""
        user = super().save(commit=False)
        user.role = self.ROLE
        if commit:
            user.save()
        return user


class PatientRegistrationForm(BaseRegistrationForm):
    """Registration form for Patient accounts. Adds optional email."""

    ROLE = User.Role.PATIENT

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Email address (optional)',
            'id': 'reg-email',
            'autocomplete': 'email',
        }),
    )

    class Meta(BaseRegistrationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'phone', 'email',
                  'password1', 'password2']


class AgencyRegistrationForm(BaseRegistrationForm):
    """Registration form for Agency Manager accounts."""

    ROLE = User.Role.AGENCY


class HelpingHandLoginForm(AuthenticationForm):
    """
    Styled login form using Django's built-in AuthenticationForm.
    """

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Username',
            'id': 'login-username',
            'autocomplete': 'username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password',
            'id': 'login-password',
            'autocomplete': 'current-password',
        }),
    )


class ProfileCompletionForm(forms.ModelForm):
    """
    Form for completing a user's profile after registration.
    Covers address details — mirrors the React SignupPage.jsx flow.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'address_line2',
                  'city', 'state', 'pincode', 'alternate_phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Last name',
            }),
            'address': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'House / Flat No., Street Name',
                'rows': 2,
                'style': 'resize: none; min-height: 60px;',
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Landmark, Area, Colony',
            }),
            'city': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'City',
            }),
            'state': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'State',
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '6-digit PIN code',
                'inputmode': 'numeric',
            }),
            'alternate_phone': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '10-digit number (optional)',
                'inputmode': 'numeric',
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_complete = True
        if commit:
            user.save()
        return user
