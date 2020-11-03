from django.urls import path

from .views import CarList

app_name = 'car_rent'

urlpatterns = [
# Просмотр профиля
    path('list/', CarList.as_view(), name='list'),
    path('set_renter/', SetRenter.as_view(), name='set_renter')

]
