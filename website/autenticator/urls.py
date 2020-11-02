from django.urls import path

from .views import (ActivationComplete, ActivationPage, LoginPage,
                    PasswordChangeDonePage, PasswordChangePage,
                    PasswordResetCompletePage, PasswordResetConfirmPage,
                    PasswordResetDonePage, PasswordResetPage,
                    RegistrationComplete, RegistrationPage)

app_name = 'auth'

urlpatterns = [
# Логин
    path('login/', LoginPage.as_view(), name='login'),

# Регистрация пользователей
    path('register/', RegistrationPage.as_view(), name='registration'),
    path('register/complete/', RegistrationComplete.as_view(), name='registration_complete'),
    path('activate/<activation_key>/', ActivationPage.as_view(), name='activation'),
    path('activate/complete/', ActivationComplete.as_view(), name = 'activation_complete'),

# Смена и сброс пароля
    path('password_change/', PasswordChangePage.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDonePage.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetPage.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDonePage.as_view(), name='password_reset_done'),
    path('password_reset/complete/', PasswordResetCompletePage.as_view(), name='password_reset_complete'),
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmPage.as_view(), name='password_reset_confirm'),
]
