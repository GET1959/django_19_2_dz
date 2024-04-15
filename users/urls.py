from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, \
    EmailConfirmationSentView, EmailConfirmedView, UserConfirmEmailView, \
    UserLoginView, UserForgotPasswordView, UserPasswordResetConfirmView, \
    AuthorizationRequest, PasswordRequestSent, PasswordChanged, PasswordGeneratedSent

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('pw_generated_sent', PasswordGeneratedSent.as_view(), name='pw_generated_sent'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/', UserPasswordResetConfirmView.as_view(), name='password_reseted'),
    path('auth_request/', AuthorizationRequest.as_view(), name='auth_request'),
    path('pw_request_sent/', PasswordRequestSent.as_view(), name='pw_request_sent'),
    path('pw_changed/', PasswordChanged.as_view(), name='pw_changed'),
]
