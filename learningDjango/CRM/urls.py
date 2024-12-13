from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('password-reset-request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-verify/', views.password_reset_verify, name='password_reset_verify'),
]
