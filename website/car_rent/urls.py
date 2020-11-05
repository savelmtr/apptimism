from django.urls import path

from .views import CarList, SelectRenter

app_name = 'car_rent'

urlpatterns = [
# Просмотр профиля
    path('', CarList.as_view(), name='list'),
    path('set_renter/<int:car_pk>/', SelectRenter.as_view(), name='select_renter')

]
