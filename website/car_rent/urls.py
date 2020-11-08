from django.urls import path

from .views import CarList, CreateAndEditTheCar, SelectRenter

app_name = 'car_rent'

urlpatterns = [
    path('', CarList.as_view(), name='list'),
    path('set_renter/<int:car_pk>/', SelectRenter.as_view(), name='set_renter'),
    path('car/', CreateAndEditTheCar.as_view(), name='create_car'),
    path('car/<int:car_pk>', CreateAndEditTheCar.as_view(), name='edit_car')
]
