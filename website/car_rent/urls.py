from django.urls import path

from .views import CarList, SelectRenter, EditTheCar

app_name = 'car_rent'

urlpatterns = [
# Просмотр профиля
    path('', CarList.as_view(), name='list'),
    path('set_renter/<int:car_pk>/', SelectRenter.as_view(), name='set_renter'),
    path('create_car/', EditTheCar.as_view(), name='create_car'),
    path('edit_car/<int:pk>', EditTheCar.as_view(), name='edit_car')
]
