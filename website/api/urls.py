from django.urls import path

from .views import (AdminCarsView, GetAllUsers, LoginAPIView,
                    RegistrationAPIView, UserCarsView, UserView)

app_name = 'api'

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_registration'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('cars/', UserCarsView.as_view(), name='cars'),
    path('cars/<int:user_pk>', AdminCarsView.as_view(), name='cars'),
    path('users/', GetAllUsers.as_view(), name='users'),
    path('users/<int:user_pk>', UserView.as_view(), name='user'),
]
