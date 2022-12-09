from .views import RegisterAPI
from django.urls import path, include
from knox import views as knox_views

from .views import (
    RegisterAPI,
    LoginAPI,
    ChangePasswordView,
    reset_password, 
    # RequestPasswordResetEmail,
)


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('rest_password/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', reset_password, name='reset-email'),
    # path('password-reset/<userid64>/<token>/', PasswordTokenCheckAPI.as_view(), name='reset-password'),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]