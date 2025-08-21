from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView, name='logout'),
    path('password/reset/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/reset/confirm/<uidb64>/<token>/', ForgotPasswordConfirmView.as_view(), name='forgot_password_confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
]
