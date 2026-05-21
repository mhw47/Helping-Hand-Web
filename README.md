# 🤝 Helping Hand

A healthcare services marketplace web application that connects patients with qualified healthcare staff for nursing care, home care, and one-time medical services.

## Overview

Helping Hand is a Django-based platform where patients can browse healthcare professionals, book services, and manage appointments — while agency managers can register and manage their staff profiles.

### Key Features

- **Service Booking** — Book nursing care, home care, or one-time medical services
- **Staff Discovery** — Browse qualified healthcare staff with ratings, specializations, and availability
- **Smart Pricing** — Automatic pricing with tiered discounts (daily, weekly, monthly)
- **Role-Based Access** — Separate dashboards for patients and agency managers
- **Booking Lifecycle** — Full status tracking from pending → confirmed → in-progress → completed
- **Reviews & Ratings** — Patients can rate and review staff after completed bookings

## Tech Stack

| Layer       | Technology            |
|-------------|-----------------------|
| Backend     | Django 4.2+           |
| Database    | PostgreSQL            |
| Auth        | Django session-based  |
| Environment | python-dotenv         |
| Images      | Pillow                |

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

```bash
# Clone the repository
git clone https://github.com/mhw47/Helping-Hand-Web.git
cd Helping-Hand-Web

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env       # Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

## Project Structure

```
Helping-Hand-Web/
├── core/                  # Main application
│   ├── models.py          # User, StaffProfile, Booking, Review
│   ├── views.py           # Request handlers
│   ├── urls.py            # URL routing
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin panel configuration
│   ├── managers.py        # Custom model managers
│   ├── pricing.py         # Pricing calculation engine
│   ├── validators.py      # Phone & pincode validators
│   └── mixins.py          # Reusable view mixins
├── helpinghand/           # Django project settings
├── templates/             # HTML templates
├── static/                # Static assets (CSS, JS, images)
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## License

This project is proprietary. All rights reserved.
