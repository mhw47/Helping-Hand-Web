"""
URL configuration for the core application.
"""

from django.urls import path

from . import views

urlpatterns = [
    # ── Public Pages ───────────────────────────────────────────────────────
    path('', views.LandingView.as_view(), name='landing'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('support/', views.SupportView.as_view(), name='support'),

    # ── Services / Booking ───────────────────────────────────────────────────
    path('book/<str:service_type>/', views.BookingCreateView.as_view(), name='book_service'),

    # ── Authentication & Dashboard ──────────────────────────────────────────
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/logout/', views.CustomLogoutView.as_view(), name='logout'),

    # ── API ────────────────────────────────────────────────────────────────
    path('api/chatbot/', views.ChatbotAPIView.as_view(), name='chatbot_api'),
]
