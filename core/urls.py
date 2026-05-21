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

    # ── Authentication ─────────────────────────────────────────────────────
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/logout/', views.CustomLogoutView.as_view(), name='logout'),
]
