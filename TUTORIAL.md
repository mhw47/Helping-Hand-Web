# 📚 Helping Hand — Comprehensive Tutorial Guide

> A step-by-step guide for understanding, setting up, developing, and extending the **Helping Hand** healthcare marketplace application.

---

## Table of Contents

1. [Introduction & Project Overview](#1-introduction--project-overview)
2. [Prerequisites & Environment Setup](#2-prerequisites--environment-setup)
3. [Installation & First Run](#3-installation--first-run)
4. [Understanding the Project Structure](#4-understanding-the-project-structure)
5. [Core Concepts — Django MTV Pattern](#5-core-concepts--django-mtv-pattern)
6. [Data Models Deep Dive](#6-data-models-deep-dive)
7. [Views & URL Routing](#7-views--url-routing)
8. [Forms & User Input](#8-forms--user-input)
9. [Authentication & Authorization](#9-authentication--authorization)
10. [The Pricing Engine](#10-the-pricing-engine)
11. [Templates & Frontend](#11-templates--frontend)
12. [Django Admin Panel](#12-django-admin-panel)
13. [Custom Managers & QuerySets](#13-custom-managers--querysets)
14. [Running Tests](#14-running-tests)
15. [Common Development Tasks](#15-common-development-tasks)
16. [Troubleshooting & FAQ](#16-troubleshooting--faq)
17. [Extending the Application](#17-extending-the-application)
18. [Glossary](#18-glossary)

---

## 1. Introduction & Project Overview

### What is Helping Hand?

**Helping Hand** is a healthcare services marketplace that connects **patients** needing home healthcare services with **agency managers** who manage certified healthcare staff. Think of it as an "Uber for home healthcare."

### What does the app do?

| For Patients | For Agency Managers |
|-------------|-------------------|
| Browse nursing, home care & one-time services | Register and manage staff profiles |
| Book services with transparent, auto-calculated pricing | Review incoming bookings |
| Upload medical discharge documents | Accept bookings and assign staff |
| Track booking status from pending → completed | Monitor service delivery |
| Leave reviews and ratings after completion | View reviews and ratings |

### Technology at a Glance

```
┌──────────────────────────────────────────────┐
│  Frontend: Django Templates + Tailwind CSS   │
│           + HTMX + Lucide Icons              │
├──────────────────────────────────────────────┤
│  Backend:  Django 4.2+ (Python)              │
│           Class-Based Views                  │
│           Custom Managers & QuerySets        │
├──────────────────────────────────────────────┤
│  Database: PostgreSQL                        │
│           4 Models, strict relational schema │
├──────────────────────────────────────────────┤
│  Auth:     Django session-based              │
│           2 roles: Patient, Agency Manager   │
└──────────────────────────────────────────────┘
```

### Migration Background

This application was migrated from a React/Firebase frontend. The original source references are:
- `Webpage/src/data/mockData.js` → `StaffProfile` model
- `Webpage/src/context/AuthContext.jsx` → `User` model
- `Webpage/src/pages/BookingPage.jsx` → `Booking` model
- `Webpage/src/lib/pricing.js` → `core/pricing.py`

---

## 2. Prerequisites & Environment Setup

### Required Software

| Software | Version | Purpose | Download |
|----------|---------|---------|----------|
| **Python** | 3.10+ | Runtime for Django | [python.org](https://www.python.org/downloads/) |
| **PostgreSQL** | 14+ | Database server | [postgresql.org](https://www.postgresql.org/download/) |
| **pip** | Latest | Python package manager | Included with Python |
| **Git** | Any | Version control | [git-scm.com](https://git-scm.com/) |

### Verify Your Setup

Open a terminal and check each tool:

```bash
# Check Python
python --version
# Expected: Python 3.10.x or higher

# Check pip
pip --version
# Expected: pip 23.x or higher

# Check PostgreSQL
psql --version
# Expected: psql (PostgreSQL) 14.x or higher

# Check Git
git --version
# Expected: git version 2.x.x
```

### Understanding Virtual Environments

A virtual environment isolates your project's Python packages from the system Python. This prevents version conflicts between projects.

```bash
# Why virtual environments matter:
# Project A needs Django 4.2
# Project B needs Django 5.0
# Without venv, they'd conflict!
# With venv, each project has its own copy.
```

---

## 3. Installation & First Run

### Step 1: Clone the Repository

```bash
git clone https://github.com/mhw47/Helping-Hand-Web.git
cd Helping-Hand-Web
```

### Step 2: Create a Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Your prompt should now show (venv) at the beginning
```

> 💡 **Tip:** You'll need to activate the virtual environment every time you open a new terminal window.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Django` — Web framework
- `psycopg2-binary` — PostgreSQL adapter
- `python-dotenv` — Environment variable management
- `django-extensions` — Developer utilities
- `Pillow` — Image processing (for staff photos)

### Step 4: Set Up the Database

#### 4a. Create the PostgreSQL Database

```bash
# Using the PostgreSQL CLI
createdb helpinghand

# Or using psql
psql -U postgres
CREATE DATABASE helpinghand;
\q
```

#### 4b. Configure Environment Variables

Create a `.env` file in the project root (or copy the example):

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
# Security Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=helpinghand
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

> ⚠️ **Security:** Never commit the `.env` file to version control. It's already in `.gitignore`.

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

This creates all database tables based on the models defined in `core/models.py`. You should see output like:

```
Operations to perform:
  Apply all migrations...
Running migrations:
  Applying core.0001_initial... OK
  ...
```

### Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. Remember these credentials!

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

### Step 8: Visit the Application

Open your browser and visit:

| URL | What You'll See |
|-----|----------------|
| `http://localhost:8000/` | 🏠 Landing page with hero section, services, pricing |
| `http://localhost:8000/services/` | 📋 Detailed service listings |
| `http://localhost:8000/support/` | ❓ FAQ accordion |
| `http://localhost:8000/auth/register/` | 📝 Patient registration |
| `http://localhost:8000/auth/register/?role=agency` | 📝 Agency registration |
| `http://localhost:8000/auth/login/` | 🔐 Login page |
| `http://localhost:8000/admin/` | 🔧 Django admin panel |
| `http://localhost:8000/book/nursing/` | 📅 Book nursing care (requires login) |

🎉 **Congratulations!** The application is running.

---

## 4. Understanding the Project Structure

```
Helping-Hand-Web/
│
├── manage.py                  # Django CLI entry point (you run commands with this)
├── .env                       # Environment variables (NOT in git)
├── .gitignore                 # Files excluded from version control
├── requirements.txt           # Python dependencies
├── ARCHITECTURE.md            # Detailed architecture documentation
├── README.md                  # Project overview
│
├── helpinghand/               # 🔧 Django project configuration
│   ├── __init__.py            # Python package marker
│   ├── settings.py            # ⭐ All Django settings (database, auth, etc.)
│   ├── urls.py                # Root URL router (delegates to core/urls.py)
│   ├── wsgi.py                # WSGI entry point (for production)
│   ├── asgi.py                # ASGI entry point (for async)
│   └── test_settings.py       # Test database overrides (SQLite)
│
├── core/                      # 🏥 Main application code
│   ├── __init__.py            # Python package marker
│   ├── apps.py                # App configuration
│   ├── models.py              # ⭐ Data models (User, StaffProfile, Booking, Review)
│   ├── views.py               # ⭐ Request handlers (7 view classes)
│   ├── urls.py                # App URL patterns (7 routes)
│   ├── forms.py               # ⭐ Form classes (5 forms)
│   ├── admin.py               # Admin panel customization
│   ├── managers.py            # Custom QuerySets for complex queries
│   ├── pricing.py             # Pricing calculation engine
│   ├── validators.py          # Phone and PIN code validators
│   ├── decorators.py          # @patient_required, @agency_required
│   ├── mixins.py              # CBV permission mixins
│   ├── migrations/            # Database schema versions (auto-generated)
│   └── tests/                 # Test suite
│       ├── __init__.py
│       ├── test_models.py     # Model and pricing tests
│       └── test_auth.py       # Authentication tests
│
├── templates/                 # 🎨 HTML templates
│   ├── base.html              # Master layout (inherited by all pages)
│   ├── core/                  # App-specific templates
│   │   ├── landing.html       # Home page
│   │   ├── services.html      # Services listing
│   │   ├── support.html       # FAQ page
│   │   ├── book.html          # Booking form page
│   │   ├── _navbar.html       # Reusable navbar partial
│   │   └── _footer.html       # Reusable footer partial
│   └── auth/                  # Authentication templates
│       ├── login.html         # Login page
│       └── register.html      # Registration page
│
├── static/                    # 📁 Static assets
│   └── css/
│       └── style.css          # Custom design system
│
└── venv/                      # Virtual environment (NOT in git)
```

### What goes where?

| I want to... | Edit this file |
|-------------|---------------|
| Add a new database field | `core/models.py` |
| Add a new page/route | `core/views.py` + `core/urls.py` + `templates/core/` |
| Change form validation | `core/forms.py` |
| Change how pricing works | `core/pricing.py` |
| Add admin features | `core/admin.py` |
| Change the site layout | `templates/base.html` |
| Add custom styles | `static/css/style.css` |
| Change database connection | `.env` or `helpinghand/settings.py` |
| Add a new Python dependency | `requirements.txt` |

---

## 5. Core Concepts — Django MTV Pattern

Django uses the **MTV** (Model-Template-View) pattern, which is similar to **MVC** (Model-View-Controller) but with different terminology:

| Django Term | MVC Equivalent | What it does |
|------------|---------------|-------------|
| **Model** | Model | Defines data structure and business logic |
| **Template** | View | Renders the HTML that users see |
| **View** | Controller | Handles requests, processes data, returns responses |

### How a request flows through the application:

```
  Browser sends request
       ↓
  URL Router matches pattern     (core/urls.py)
       ↓
  View processes the request     (core/views.py)
       ↓
  Model fetches/saves data       (core/models.py)
       ↓
  Template renders HTML          (templates/)
       ↓
  Browser displays the page
```

### Example: When someone visits the landing page

1. **URL Router** (`core/urls.py`): `path('', views.LandingView.as_view(), name='landing')` matches `/`
2. **View** (`core/views.py`): `LandingView.get_context_data()` builds the context with services, stats, pricing, testimonials
3. **Template** (`templates/core/landing.html`): Renders the HTML using the context data
4. **Response**: The rendered HTML is sent back to the browser

---

## 6. Data Models Deep Dive

### Overview

The application has **4 models** that work together:

```
User ──────────────────────────────────────────────────────────────
  │                                                                 
  ├── (role=patient) ──creates──→ Booking ──has one──→ Review       
  │                                  ↑                              
  └── (role=agency) ──manages──→ StaffProfile ──assigned to──┘      
```

### Model 1: User

**Location:** `core/models.py` (lines 53–133)

The `User` model extends Django's built-in `AbstractUser` to add healthcare-specific fields:

```python
class User(AbstractUser):
    # Two roles
    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        AGENCY = 'agency', 'Agency Manager'

    # Core fields
    role = models.CharField(choices=Role.choices, default=Role.PATIENT)
    phone = models.CharField(max_length=15, unique=True)
    profile_complete = models.BooleanField(default=False)

    # Address fields (filled during profile completion)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)

    # Convenience properties
    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT

    @property
    def is_agency(self):
        return self.role == self.Role.AGENCY
```

**Key Points:**
- `AUTH_USER_MODEL = 'core.User'` in settings replaces Django's default User
- Phone number is unique and used for contact (NOT for authentication)
- `profile_complete` tracks whether the user has filled in their address

### Model 2: StaffProfile

**Location:** `core/models.py` (lines 139–249)

Represents a healthcare staff member managed by an agency:

```python
class StaffProfile(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(choices=Gender.choices)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18)])
    photo = models.ImageField(upload_to='staff_photos/', blank=True)

    # Flexible lists stored as JSON
    specializations = models.JSONField(default=list)  # ["Nursing Care", "Post-Surgery"]
    service_types = models.JSONField(default=list)    # ["nursing", "homecare"]

    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(default=Decimal('0.0'))
    available = models.BooleanField(default=True, db_index=True)

    # Belongs to an agency
    agency = models.ForeignKey(User, related_name='staff_profiles',
                               limit_choices_to={'role': User.Role.AGENCY})
```

**Key Points:**
- `JSONField` allows flexible lists without a separate table
- `limit_choices_to` ensures only agency users can own staff profiles
- `available` is indexed for fast filtering

### Model 3: Booking

**Location:** `core/models.py` (lines 255–554)

The central transaction model with **6 lifecycle states**:

```python
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        REVIEWING = 'reviewing'
        CONFIRMED = 'confirmed'
        IN_PROGRESS = 'in-progress'
        COMPLETED = 'completed'
        CANCELLED = 'cancelled'

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(User, limit_choices_to={'role': 'patient'})
    staff = models.ForeignKey(StaffProfile, null=True, blank=True)
    service_type = models.CharField(choices=ServiceType.choices)

    # Auto-computed pricing
    base_rate = models.DecimalField(default=Decimal('0'))
    total_cost = models.DecimalField(default=Decimal('0'))
```

**Business Rules enforced in `clean()`:**
1. Staff gender must match patient gender
2. Staff must support the booking's service type

**Automations in `save()`:**
1. Auto-generate unique `booking_id` (e.g., `BK-a1b2c3d4`)
2. Auto-compute pricing (tiered discounts)
3. Auto-set initial status (pending or reviewing based on discharge file)

### Model 4: Review

**Location:** `core/models.py` (lines 561–600)

One review per completed booking:

```python
class Review(models.Model):
    booking = models.OneToOneField(Booking,
                                  limit_choices_to={'status': 'completed'})
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
```

**Key Points:**
- `OneToOneField` ensures exactly one review per booking
- Reviews can only be created for completed bookings (enforced in `clean()`)

### Working with Models in the Shell

```bash
# Start Django shell
python manage.py shell_plus  # (requires django-extensions)

# Create a user
user = User.objects.create_user(
    username='john_patient',
    password='securepass123',
    role='patient',
    phone='9876543210',
    first_name='John',
    last_name='Doe'
)

# Check role
user.is_patient  # True
user.is_agency   # False

# Create a staff profile (requires an agency user)
agency = User.objects.create_user(
    username='care_agency', password='pass123',
    role='agency', phone='1234567890'
)
staff = StaffProfile.objects.create(
    name='Nurse Priya', gender='female', age=28,
    specializations=['Nursing Care', 'Post-Surgery'],
    service_types=['nursing', 'onetime'],
    hourly_rate=1500, agency=agency
)

# Query available staff
StaffProfile.objects.available()
StaffProfile.objects.matching('female', 'nursing')
```

---

## 7. Views & URL Routing

### URL Patterns

All URL patterns are defined in two files:

**Root Router** (`helpinghand/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Everything else goes to core
]
```

**App Router** (`core/urls.py`):
```python
urlpatterns = [
    path('',                    LandingView.as_view(),       name='landing'),
    path('services/',           ServicesView.as_view(),       name='services'),
    path('support/',            SupportView.as_view(),        name='support'),
    path('book/<str:service_type>/', BookingCreateView.as_view(), name='book_service'),
    path('auth/login/',         CustomLoginView.as_view(),   name='login'),
    path('auth/register/',      RegisterView.as_view(),      name='register'),
    path('auth/logout/',        CustomLogoutView.as_view(),  name='logout'),
]
```

### Understanding Class-Based Views (CBVs)

All views in this project use Django's **Class-Based Views**. Here's what each base class provides:

| Base Class | Purpose | HTTP Methods |
|-----------|---------|-------------|
| `TemplateView` | Render a template with context data | GET |
| `FormView` | Display and process a form | GET, POST |
| `CreateView` | Create a new model instance | GET, POST |
| `LoginView` | Handle user login | GET, POST |
| `LogoutView` | Handle user logout | POST |

### View Walkthrough: LandingView

```python
class LandingView(TemplateView):
    template_name = 'core/landing.html'  # Which template to render

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Build service cards with pricing
        ctx['services'] = [_build_service_context(c) for c in SERVICE_CARDS]

        # Statistics for the hero section
        ctx['stats'] = [
            {'value': '2,500+', 'label': 'Happy Patients', 'icon': 'users'},
            ...
        ]

        # How-it-works steps
        ctx['steps'] = [
            {'num': '01', 'title': 'Browse Services', ...},
            ...
        ]

        # Pricing rates and testimonials
        ctx['pricing_rates'] = _build_pricing_rates()
        ctx['testimonials'] = TESTIMONIALS

        return ctx  # This dict is passed to the template
```

**What happens:**
1. User visits `/` → URL router maps to `LandingView`
2. Django calls `get_context_data()` → builds a dictionary of data
3. Django renders `core/landing.html` with that data
4. Template uses `{{ services }}`, `{{ stats }}`, etc. to display the data

### View Walkthrough: RegisterView

```python
class RegisterView(FormView):
    template_name = 'auth/register.html'
    success_url = reverse_lazy('landing')

    def get_role(self):
        # Read ?role= from the URL query string
        role = self.request.GET.get('role', 'patient')
        return role if role in ('patient', 'agency') else 'patient'

    def get_form_class(self):
        # Different form for different roles
        if self.get_role() == 'agency':
            return AgencyRegistrationForm
        return PatientRegistrationForm

    def form_valid(self, form):
        user = form.save()           # Create the user
        login(self.request, user)    # Log them in immediately
        messages.success(...)        # Show a welcome message
        return redirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        # Already logged in? Go to landing page
        if request.user.is_authenticated:
            return redirect('landing')
        return super().dispatch(request, *args, **kwargs)
```

### View Walkthrough: BookingCreateView

```python
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'core/book.html'
    success_url = reverse_lazy('landing')

    def get_initial(self):
        # Pre-fill form with user's saved info
        user = self.request.user
        return {
            'patient_name': user.get_full_name(),
            'phone': user.phone,
            'address': user.address,
            'city': user.city,
            'pincode': user.pincode,
        }

    def form_valid(self, form):
        # Set the patient and service type automatically
        form.instance.patient = self.request.user
        form.instance.service_type = self.kwargs.get('service_type')
        messages.success(self.request, 'Booking placed successfully!')
        return super().form_valid(form)
```

### Using Named URLs in Templates

```html
<!-- Link to services page -->
<a href="{% url 'services' %}">View Services</a>

<!-- Link to register as patient -->
<a href="{% url 'register' %}?role=patient">Sign Up</a>

<!-- Link to book nursing service -->
<a href="{% url 'book_service' 'nursing' %}">Book Nursing Care</a>

<!-- Link to login -->
<a href="{% url 'login' %}">Log In</a>
```

---

## 8. Forms & User Input

### Form Classes Overview

| Form | File | Purpose |
|------|------|---------|
| `PatientRegistrationForm` | `core/forms.py` | Patient sign-up |
| `AgencyRegistrationForm` | `core/forms.py` | Agency manager sign-up |
| `HelpingHandLoginForm` | `core/forms.py` | Custom styled login |
| `ProfileCompletionForm` | `core/forms.py` | Fill in address details |
| `BookingForm` | `core/forms.py` | Create a new booking |

### How Forms Work

**Step 1: Define the form class**
```python
class BookingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'input-field', 'type': 'date'})
    )

    class Meta:
        model = Booking
        fields = [
            'patient_name', 'patient_gender', 'patient_age',
            'symptoms', 'illnesses', 'conditions',
            'start_date', 'duration_days',
            'address', 'city', 'pincode', 'phone',
            'discharge_file'
        ]
```

**Step 2: Use it in a view**
```python
class BookingCreateView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    # Django handles GET (display empty form) and POST (validate + save)
```

**Step 3: Render in a template**
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}          <!-- Render all fields -->
    <button type="submit">Book Now</button>
</form>

<!-- Or render individual fields -->
<div>
    <label for="{{ form.patient_name.id_for_label }}">Patient Name</label>
    {{ form.patient_name }}
    {{ form.patient_name.errors }}
</div>
```

### Validation Layers

The app validates user input at 4 levels:

1. **Form field validation** — `required`, `max_length`, email format
2. **Custom validators** (`validators.py`) — phone must be 10 digits, PIN must be 6 digits
3. **Model `clean()`** — business rules (gender matching, service type compatibility)
4. **Model `save()`** — auto-processing (generate ID, compute pricing, set status)

### Custom Validators

```python
# validators.py
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must be exactly 10 digits.',
)

pincode_validator = RegexValidator(
    regex=r'^\d{6}$',
    message='Pin code must be exactly 6 digits.',
)
```

These are used in model fields:
```python
phone = models.CharField(max_length=15, validators=[phone_validator])
```

---

## 9. Authentication & Authorization

### How Authentication Works

The app uses Django's built-in **session-based authentication**:

1. User submits username + password
2. Django checks credentials against the database
3. If valid, creates a session cookie → user is "logged in"
4. Every subsequent request includes the cookie → Django knows who the user is

### Registration Flow

```
Visit /auth/register/?role=patient
  → PatientRegistrationForm displayed
  → Fill in: username, first_name, last_name, phone, email, password1, password2
  → POST → form validates → user created with role=PATIENT
  → Auto-login → redirect to landing page
```

```
Visit /auth/register/?role=agency
  → AgencyRegistrationForm displayed
  → Fill in: username, first_name, last_name, phone, password1, password2
  → POST → form validates → user created with role=AGENCY
  → Auto-login → redirect to landing page
```

### Login/Logout

```python
# Settings that control auth behavior
LOGIN_URL = '/auth/login/'            # Where unauthenticated users are sent
LOGIN_REDIRECT_URL = '/dashboard/'     # Where users go after login
LOGOUT_REDIRECT_URL = '/'             # Where users go after logout
```

### Role-Based Access Control

The app provides **two ways** to restrict access by role:

#### For Function-Based Views: Decorators

```python
from core.decorators import patient_required, agency_required

@patient_required
def my_patient_view(request):
    # Only patients can access this
    pass

@agency_required
def staff_management(request):
    # Only agency managers can access this
    pass

@profile_complete_required
def booking_view(request):
    # Only users with completed profiles
    pass
```

#### For Class-Based Views: Mixins

```python
from core.mixins import PatientRequiredMixin, AgencyRequiredMixin

class PatientDashboard(PatientRequiredMixin, TemplateView):
    template_name = 'core/patient_dashboard.html'
    # Only patients can access

class StaffManagement(AgencyRequiredMixin, ListView):
    model = StaffProfile
    # Only agency managers can access
```

#### How They Work Under the Hood

```python
# Decorator (decorators.py)
def patient_required(view_func):
    @wraps(view_func)
    @login_required                    # Step 1: Must be logged in
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_patient:  # Step 2: Must be a patient
            raise PermissionDenied(...)  # Returns 403 Forbidden
        return view_func(request, *args, **kwargs)
    return _wrapped

# Mixin (mixins.py)
class PatientRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_patient    # Same check

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(...)        # 403 for wrong role
        return super().handle_no_permission()  # Redirect to login
```

---

## 10. The Pricing Engine

### How Pricing Works

**Location:** `core/pricing.py`

The pricing system uses a tiered discount model based on booking duration:

| Duration | Tier | Discount |
|----------|------|----------|
| 1–6 days | Daily | 0% |
| 7–29 days | Weekly | 10% off |
| 30+ days | Monthly | 25% off |

### Service Rates

| Service | Daily Rate |
|---------|-----------|
| Nursing Care | ₹1,500/day |
| Home Care | ₹1,000/day |
| One-Time Service | ₹500 (flat, always 1 day) |

### Pricing Calculation Examples

```python
from core.pricing import calculate_price, format_currency

# Example 1: 5 days of nursing (daily tier, no discount)
result = calculate_price('nursing', 5)
# base_rate = ₹1,500
# subtotal  = 5 × ₹1,500 = ₹7,500
# discount  = 0%
# total     = ₹7,500

# Example 2: 14 days of nursing (weekly tier, 10% discount)
result = calculate_price('nursing', 14)
# base_rate = ₹1,500
# subtotal  = 14 × ₹1,500 = ₹21,000
# discount  = 10% → ₹2,100
# total     = ₹18,900

# Example 3: 30 days of home care (monthly tier, 25% discount)
result = calculate_price('homecare', 30)
# base_rate = ₹1,000
# subtotal  = 30 × ₹1,000 = ₹30,000
# discount  = 25% → ₹7,500
# total     = ₹22,500

# Example 4: One-time service (always flat rate)
result = calculate_price('onetime', 1)
# total = ₹500 (no discount possible)

# Format as currency
format_currency(18900)  # → '₹18,900'
```

### Where Pricing Happens

Pricing is **automatically computed** every time a booking is saved:

```python
# In Booking.save() (models.py)
def save(self, *args, **kwargs):
    if not self.booking_id:
        self.booking_id = self._generate_booking_id()
    self._compute_pricing()    # ← Recalculates every save!
    if not self.pk:
        self._determine_initial_status()
    super().save(*args, **kwargs)
```

This means:
- Creating a booking → pricing is calculated
- Changing duration → pricing is recalculated
- Changing service type → pricing is recalculated

---

## 11. Templates & Frontend

### Template Inheritance

All pages inherit from `templates/base.html`, which provides the common layout:

```html
<!-- base.html provides: -->
- HTML boilerplate (<html>, <head>, <body>)
- Tailwind CSS (CDN)
- HTMX (for AJAX-like interactions)
- Lucide Icons
- Google Fonts (Inter, DM Sans)
- Navbar (via {% include "core/_navbar.html" %})
- Flash messages
- Footer (via {% include "core/_footer.html" %})

<!-- Child templates override blocks: -->
{% block title %}Page Title{% endblock %}
{% block meta_description %}SEO description{% endblock %}
{% block content %}Page-specific HTML{% endblock %}
{% block extra_head %}Additional CSS/JS{% endblock %}
{% block extra_scripts %}Page-specific scripts{% endblock %}
```

### Creating a New Page (Tutorial)

**Step 1:** Create the template (`templates/core/about.html`):

```html
{% extends "base.html" %}

{% block title %}About Us{% endblock %}
{% block meta_description %}Learn about Helping Hand healthcare services{% endblock %}

{% block content %}
<section class="py-20 px-6">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-4xl font-bold">About Helping Hand</h1>
        <p class="mt-4 text-lg text-gray-600">
            {{ description }}
        </p>
    </div>
</section>
{% endblock %}
```

**Step 2:** Create the view (`core/views.py`):

```python
class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['description'] = 'We are a healthcare marketplace...'
        return ctx
```

**Step 3:** Add the URL pattern (`core/urls.py`):

```python
urlpatterns = [
    ...
    path('about/', views.AboutView.as_view(), name='about'),
]
```

**Step 4:** Link to it from other pages:

```html
<a href="{% url 'about' %}">About Us</a>
```

### HTMX — Dynamic Updates Without JavaScript

HTMX lets you add AJAX-like behavior with just HTML attributes:

```html
<!-- Example: Load content dynamically -->
<div hx-get="/api/staff-list/" hx-trigger="load" hx-target="#staff-container">
    Loading...
</div>
<div id="staff-container"></div>

<!-- Example: Submit form without page reload -->
<form hx-post="/book/nursing/" hx-target="#result">
    {% csrf_token %}
    ...
    <button type="submit">Book Now</button>
</form>
```

### Tailwind CSS Usage

The project uses Tailwind CSS via CDN in "Play" mode. Common patterns:

```html
<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    ...
</div>

<!-- Card component -->
<div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
    ...
</div>

<!-- Button styling -->
<button class="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition">
    Click Me
</button>
```

### Custom CSS Classes

The project defines custom classes in `static/css/style.css`:

- `input-field` — Styled form inputs
- `icon-bg-teal`, `icon-bg-blue`, `icon-bg-purple` — Colored icon backgrounds
- `gradient-teal`, `gradient-blue`, `gradient-purple` — Gradient decorations
- `animate-fade-in-up` — Fade-in animation for flash messages

---

## 12. Django Admin Panel

### Accessing the Admin

1. Visit `http://localhost:8000/admin/`
2. Log in with your superuser credentials

### What You Can Do

| Section | Actions |
|---------|---------|
| **Users** | View all users, filter by role, edit profile fields, change passwords |
| **Staff Profiles** | Add/edit staff, toggle availability directly from list, view ratings |
| **Bookings** | View all bookings, filter by status/type/date, view auto-computed pricing |
| **Reviews** | View reviews, filter by rating, reviews also shown inline within bookings |

### Admin Customizations

The app customizes the admin with:

```python
# User Admin — extra fields for role and contact
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_name', 'phone', 'role', 'profile_complete']
    list_filter = ['role', 'profile_complete', 'is_active']

# Staff Profile Admin — toggle availability from list
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_editable = ['available']  # Checkbox directly in the list!

# Booking Admin — read-only pricing, inline reviews
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ['booking_id', 'base_rate', 'total_cost', ...]
    inlines = [ReviewInline]  # Show review within booking detail
    date_hierarchy = 'created_at'  # Date-based navigation
```

### Adding Test Data via Admin

1. **Create an agency user**: Users → Add → set role to "Agency Manager"
2. **Create staff profiles**: Staff Profiles → Add → assign to the agency
3. **Create a booking**: Bookings → Add → select patient and service type
4. **Observe auto-pricing**: Notice how pricing fields are auto-computed!

---

## 13. Custom Managers & QuerySets

### What Are Custom Managers?

Django's default manager (`Model.objects`) only provides basic CRUD. Custom managers add **domain-specific query methods** that can be chained:

### Booking Queries

```python
# All active bookings (not completed/cancelled)
Booking.objects.active()

# All past bookings
Booking.objects.past()

# Bookings for a specific patient
Booking.objects.active().for_patient(request.user)

# Bookings assigned to an agency's staff
Booking.objects.for_agency(agency_user)

# Filter by service type
Booking.objects.active().by_service_type('nursing')

# Bookings needing discharge document review
Booking.objects.needs_review()

# Chain them together!
Booking.objects.active().for_patient(user).by_service_type('nursing')
```

### Staff Profile Queries

```python
# All available staff
StaffProfile.objects.available()

# Find matching staff for a booking
StaffProfile.objects.matching('female', 'nursing')
# Returns: available female staff who provide nursing care and are 18+
```

### How Managers Are Implemented

```python
# managers.py
class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=['pending', 'confirmed', 'in-progress', 'reviewing'])

    def past(self):
        return self.filter(status__in=['completed', 'cancelled'])

    def for_patient(self, user):
        return self.filter(patient=user)

# The manager exposes all QuerySet methods
BookingManager = BookingQuerySet.as_manager()
```

---

## 14. Running Tests

### Test Structure

```
core/tests/
├── __init__.py
├── test_models.py    # Model logic, pricing, business rules
└── test_auth.py      # Registration, login, logout, permissions
```

### Running Tests

```bash
# Run ALL tests (uses SQLite, no PostgreSQL required)
python manage.py test core.tests --settings=helpinghand.test_settings

# Run only model tests
python manage.py test core.tests.test_models --settings=helpinghand.test_settings

# Run only auth tests
python manage.py test core.tests.test_auth --settings=helpinghand.test_settings

# Run with verbose output
python manage.py test core.tests --settings=helpinghand.test_settings -v 2
```

### What the Tests Cover

**test_models.py:**
- User creation and role properties (`is_patient`, `is_agency`)
- StaffProfile validation (age ≥ 18, valid service types)
- Booking ID generation (format: `BK-xxxxxxxx`)
- Pricing calculation (all tiers, edge cases)
- Status determination (pending vs. reviewing)
- Gender matching enforcement
- Review constraints (completed bookings only, 1:1)

**test_auth.py:**
- Patient and agency registration
- Auto-role assignment on save
- Login with valid/invalid credentials
- Redirect behavior after login/logout
- Role-based access control (403 for wrong role)
- Form validation (phone, username, required fields)

### Writing a New Test

```python
# core/tests/test_models.py
from django.test import TestCase
from core.models import User, Booking

class BookingTests(TestCase):
    def setUp(self):
        """Create test data used by multiple tests."""
        self.patient = User.objects.create_user(
            username='testpatient', password='pass123',
            role='patient', phone='9876543210'
        )

    def test_booking_id_format(self):
        """Booking IDs should start with 'BK-' followed by 8 hex chars."""
        booking = Booking.objects.create(
            patient=self.patient,
            service_type='nursing',
            patient_name='Test Patient',
            patient_gender='male',
            patient_age=25,
            start_date='2026-06-01',
            duration_days=7,
            address='123 Test St',
            city='Mumbai',
            pincode='400001',
            phone='9876543210',
        )
        self.assertTrue(booking.booking_id.startswith('BK-'))
        self.assertEqual(len(booking.booking_id), 11)  # BK- + 8 chars
```

---

## 15. Common Development Tasks

### Adding a New Model Field

```python
# 1. Add the field in core/models.py
class Booking(models.Model):
    ...
    notes = models.TextField(blank=True, default='')  # New field

# 2. Create a migration
python manage.py makemigrations core

# 3. Apply the migration
python manage.py migrate

# 4. Optionally add to admin (core/admin.py)
# 5. Optionally add to forms (core/forms.py)
```

### Adding a New URL Route

```python
# 1. Create the view in core/views.py
class DashboardView(PatientRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

# 2. Add URL in core/urls.py
path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

# 3. Create the template in templates/core/dashboard.html
{% extends "base.html" %}
{% block content %}
<h1>Dashboard</h1>
{% endblock %}
```

### Adding a New Form

```python
# 1. Define the form in core/forms.py
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'input-field', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
        }

# 2. Use in a view
class ReviewCreateView(PatientRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'core/review.html'
    ...
```

### Checking Database State

```bash
# Open Django shell
python manage.py shell_plus

# Count records
User.objects.count()
Booking.objects.count()

# View all bookings with status
Booking.objects.values_list('booking_id', 'status', 'total_cost')

# Check pricing for a specific booking
b = Booking.objects.get(booking_id='BK-abc12345')
print(f"Service: {b.service_type}")
print(f"Duration: {b.duration_days} days")
print(f"Tier: {b.pricing_tier}")
print(f"Total: ₹{b.total_cost}")
```

### Resetting the Database

```bash
# Drop and recreate (WARNING: deletes all data!)
dropdb helpinghand
createdb helpinghand
python manage.py migrate
python manage.py createsuperuser
```

---

## 16. Troubleshooting & FAQ

### Common Errors

#### "FATAL: database 'helpinghand' does not exist"

```bash
# Solution: Create the database
createdb helpinghand
# Then run migrations
python manage.py migrate
```

#### "django.db.utils.OperationalError: could not connect to server"

```bash
# Solution: Make sure PostgreSQL is running
# Windows:
net start postgresql-x64-14

# macOS:
brew services start postgresql

# Check your .env file has correct credentials
```

#### "ModuleNotFoundError: No module named 'django'"

```bash
# Solution: Activate your virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

#### "You have 'X' unapplied migration(s)"

```bash
# Solution: Apply pending migrations
python manage.py migrate
```

#### "UNIQUE constraint failed: core_user.phone"

This means a user with that phone number already exists. Each phone number must be unique.

#### Merge conflict markers in source files (`<<<<<<<`, `=======`, `>>>>>>>`)

The codebase currently has unresolved git merge conflicts. See the **ARCHITECTURE.md Section 17** for details on which files are affected and how to resolve them.

### Useful Django Commands

```bash
# Start development server
python manage.py runserver

# Create database tables
python manage.py migrate

# Create a new migration after model changes
python manage.py makemigrations core

# Create a superuser
python manage.py createsuperuser

# Open interactive Python shell with Django context
python manage.py shell_plus

# Run tests
python manage.py test core.tests --settings=helpinghand.test_settings

# Show all URL patterns
python manage.py show_urls    # (requires django-extensions)

# Check for issues
python manage.py check

# Show SQL for a migration
python manage.py sqlmigrate core 0001
```

---

## 17. Extending the Application

### Planned Features (Not Yet Implemented)

Based on the codebase structure, these features are partially scaffolded:

1. **Patient Dashboard** — View active/past bookings, submit reviews
2. **Agency Dashboard** — Manage staff, view incoming bookings
3. **Profile Completion Page** — Address form after registration
4. **Staff Assignment** — Agency assigns staff to pending bookings
5. **Booking Status Updates** — Confirm, start, complete bookings

### Architecture for New Features

When adding a new feature, follow this pattern:

```
1. Model (core/models.py)     → Define data structures
2. Migration                   → Update database schema
3. Manager (core/managers.py)  → Add query shortcuts
4. Form (core/forms.py)       → Build input forms
5. View (core/views.py)       → Handle requests
6. URL (core/urls.py)         → Map URLs to views
7. Template (templates/)       → Render HTML
8. Admin (core/admin.py)      → Add admin support
9. Test (core/tests/)          → Write tests
```

### Example: Adding a Patient Dashboard

**1. View:**
```python
# core/views.py
class PatientDashboardView(PatientRequiredMixin, TemplateView):
    template_name = 'core/patient_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['active_bookings'] = Booking.objects.active().for_patient(user)
        ctx['past_bookings'] = Booking.objects.past().for_patient(user)
        return ctx
```

**2. URL:**
```python
# core/urls.py
path('dashboard/', views.PatientDashboardView.as_view(), name='dashboard'),
```

**3. Template:**
```html
{% extends "base.html" %}
{% block title %}My Dashboard{% endblock %}

{% block content %}
<section class="py-12 px-6">
    <h1 class="text-3xl font-bold">My Bookings</h1>

    <h2 class="text-xl mt-8">Active</h2>
    {% for booking in active_bookings %}
    <div class="bg-white rounded-xl p-4 shadow mb-4">
        <p><strong>{{ booking.booking_id }}</strong> — {{ booking.get_service_type_display }}</p>
        <p>Status: {{ booking.get_status_display }}</p>
        <p>Total: ₹{{ booking.total_cost }}</p>
    </div>
    {% empty %}
    <p class="text-gray-500">No active bookings.</p>
    {% endfor %}

    <h2 class="text-xl mt-8">Past</h2>
    {% for booking in past_bookings %}
    <div class="bg-white rounded-xl p-4 shadow mb-4">
        <p><strong>{{ booking.booking_id }}</strong> — {{ booking.get_status_display }}</p>
    </div>
    {% endfor %}
</section>
{% endblock %}
```

---

## 18. Glossary

| Term | Definition |
|------|-----------|
| **CBV** | Class-Based View — Django views written as Python classes |
| **FBV** | Function-Based View — Django views written as functions |
| **CSRF** | Cross-Site Request Forgery — a security attack; Django protects against it |
| **HTMX** | A library for AJAX-like behavior using HTML attributes |
| **Mixin** | A class that provides methods to other classes via multiple inheritance |
| **Migration** | A Python file that describes changes to the database schema |
| **ORM** | Object-Relational Mapping — Python code that translates to SQL |
| **QuerySet** | A lazy, chainable representation of a database query |
| **Tailwind CSS** | A utility-first CSS framework |
| **MTV** | Model-Template-View — Django's architecture pattern |
| **INR** | Indian Rupee — the currency used in the pricing system |
| **Lucide** | An open-source icon library used for UI icons |
| **psycopg2** | The PostgreSQL adapter for Python |
| **Pillow** | Python imaging library for handling image uploads |
| **Decorator** | A function that wraps another function to add behavior |

---

*Tutorial guide for the Helping Hand College codebase.*
*Generated: May 2026*
