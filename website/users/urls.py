from django.urls import path

from .views import EditProfile, Profile

app_name = 'users'

urlpatterns = [
    # Просмотр профиля
    path('', Profile.as_view(), name='profile'),
    path('edit_profile/', EditProfile.as_view(), name='edit'),

]
