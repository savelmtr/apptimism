from django.urls import path

from .views import ProfileView

app_name = 'users'

urlpatterns = [
# Просмотр профиля
    path('login/', ProfileView.as_view(), name='profile'),

]
