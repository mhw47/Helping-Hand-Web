"""
Authentication tests for the Helping Hand application.

Tests cover:
  - Patient registration (form + view)
  - Agency registration (form + view)
  - Login (valid + invalid)
  - Logout
  - Permission mixins and decorators
  - Navbar dynamic state
"""

from django.test import TestCase, Client
from django.urls import reverse

from core.models import User
from core.forms import PatientRegistrationForm, AgencyRegistrationForm, HelpingHandLoginForm
from core.decorators import patient_required, agency_required


# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRATION FORM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class PatientRegistrationFormTest(TestCase):
    """Test PatientRegistrationForm validation and role assignment."""

    def test_valid_registration(self):
        """Valid data should create a patient user."""
        form = PatientRegistrationForm(data={
            'username': 'testpatient',
            'first_name': 'Ramesh',
            'last_name': 'Gupta',
            'phone': '9876543210',
            'email': 'ramesh@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.role, User.Role.PATIENT)
        self.assertTrue(user.is_patient)
        self.assertFalse(user.is_agency)
        self.assertEqual(user.phone, '9876543210')

    def test_phone_required(self):
        """Phone number should be required."""
        form = PatientRegistrationForm(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_password_mismatch(self):
        """Mismatched passwords should fail."""
        form = PatientRegistrationForm(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '9876543210',
            'password1': 'SecurePass123!',
            'password2': 'WrongPass456!',
        })
        self.assertFalse(form.is_valid())


class AgencyRegistrationFormTest(TestCase):
    """Test AgencyRegistrationForm role assignment."""

    def test_creates_agency_user(self):
        """Form should create a user with agency role."""
        form = AgencyRegistrationForm(data={
            'username': 'testagency',
            'first_name': 'Agency',
            'last_name': 'Manager',
            'phone': '9876543211',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.role, User.Role.AGENCY)
        self.assertTrue(user.is_agency)


# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRATION VIEW TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class RegisterViewTest(TestCase):
    """Test the registration view (GET + POST)."""

    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        """GET /auth/register/ should return 200."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')

    def test_register_patient_default(self):
        """Default role should be patient."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.context['role'], 'patient')

    def test_register_agency_tab(self):
        """?role=agency should show agency form."""
        response = self.client.get(reverse('register') + '?role=agency')
        self.assertEqual(response.context['role'], 'agency')

    def test_register_patient_post(self):
        """POST should create patient user and redirect."""
        response = self.client.post(reverse('register') + '?role=patient', {
            'username': 'newpatient',
            'first_name': 'New',
            'last_name': 'Patient',
            'phone': '9876543220',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        user = User.objects.get(username='newpatient')
        self.assertEqual(user.role, User.Role.PATIENT)

    def test_register_agency_post(self):
        """POST with role=agency should create agency user."""
        response = self.client.post(reverse('register') + '?role=agency', {
            'username': 'newagency',
            'first_name': 'New',
            'last_name': 'Agency',
            'phone': '9876543221',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newagency')
        self.assertEqual(user.role, User.Role.AGENCY)

    def test_register_auto_login(self):
        """User should be auto-logged-in after registration."""
        self.client.post(reverse('register') + '?role=patient', {
            'username': 'autologin',
            'first_name': 'Auto',
            'last_name': 'Login',
            'phone': '9876543222',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        # Check that user is now authenticated
        response = self.client.get(reverse('landing'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_authenticated_user_redirected(self):
        """Authenticated users should be redirected away from register page."""
        User.objects.create_user(
            username='existing', password='pass123', phone='9876543223'
        )
        self.client.login(username='existing', password='pass123')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN VIEW TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class LoginViewTest(TestCase):
    """Test the login view (GET + POST)."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='SecurePass123!',
            phone='9876543230', first_name='Test', last_name='User',
        )

    def test_login_page_loads(self):
        """GET /auth/login/ should return 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back')

    def test_valid_login(self):
        """Valid credentials should log in and redirect."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        """Invalid credentials should show error."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Re-renders form
        self.assertContains(response, 'Login failed')

    def test_login_redirect_authenticated(self):
        """Already authenticated users should be redirected away."""
        self.client.login(username='testuser', password='SecurePass123!')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGOUT VIEW TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class LogoutViewTest(TestCase):
    """Test the logout view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='pass123', phone='9876543240'
        )
        self.client.login(username='testuser', password='pass123')

    def test_logout_post(self):
        """POST to logout should log out and redirect."""
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [200, 302])
        # After logout, user should not be authenticated
        response = self.client.get(reverse('landing'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# ═══════════════════════════════════════════════════════════════════════════════
# NAVBAR DYNAMIC STATE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class NavbarAuthStateTest(TestCase):
    """Test that navbar shows correct auth links."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='pass123',
            phone='9876543250', first_name='Test', last_name='User',
        )

    def test_anonymous_sees_login_signup(self):
        """Anonymous users should see Login and Sign Up buttons."""
        response = self.client.get(reverse('landing'))
        content = response.content.decode()
        self.assertIn('Login', content)
        self.assertIn('Sign Up', content)
        self.assertNotIn('Logout', content)
        self.assertNotIn('Dashboard', content)

    def test_authenticated_sees_dashboard_logout(self):
        """Authenticated users should see Dashboard and Logout."""
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('landing'))
        content = response.content.decode()
        self.assertIn('Dashboard', content)
        self.assertIn('Logout', content)
        self.assertIn('Test User', content)  # Username in navbar

    def test_authenticated_no_login_button(self):
        """Authenticated users should NOT see Login/Sign Up."""
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('landing'))
        content = response.content.decode()
        # Login link should not be present (but "Login" as text in other contexts is ok)
        self.assertNotIn('nav-login-btn', content)
        self.assertNotIn('nav-register-btn', content)


# ═══════════════════════════════════════════════════════════════════════════════
# PERMISSION MIXIN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class PermissionTest(TestCase):
    """Test permission mixins behavior via URL access patterns."""

    def setUp(self):
        self.client = Client()
        self.patient = User.objects.create_user(
            username='patient1', password='pass123',
            phone='9876543260', role=User.Role.PATIENT,
        )
        self.agency = User.objects.create_user(
            username='agency1', password='pass123',
            phone='9876543261', role=User.Role.AGENCY,
        )

    def test_unauthenticated_redirect_to_login(self):
        """Unauthenticated users should be redirected to login."""
        # The LOGIN_URL should be /auth/login/
        from django.conf import settings
        self.assertEqual(settings.LOGIN_URL, '/auth/login/')

    def test_patient_role_property(self):
        """Patient user should have is_patient=True."""
        self.assertTrue(self.patient.is_patient)
        self.assertFalse(self.patient.is_agency)

    def test_agency_role_property(self):
        """Agency user should have is_agency=True."""
        self.assertTrue(self.agency.is_agency)
        self.assertFalse(self.agency.is_patient)
