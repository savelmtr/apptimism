from django.urls import path

from .views import Profile, EditProfile

app_name = 'users'

urlpatterns = [
# Просмотр профиля
    path('profile/', Profile.as_view(), name='profile'),
    path('edit/', EditProfile.as_view(), name='edit'),

]
