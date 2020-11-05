from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import Car
from django.shortcuts import render


User = get_user_model()



@method_decorator(login_required, name='dispatch')
class CarList(ListView):

    model = Car


class SelectRenter(ListView):

    model = User
    template_name = 'car_rent/select_renter.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['car'] = Car.objects.get(pk=self.car_pk)
        return context

    def get(self, request, *args, **kwargs):
        self.car_pk = kwargs['car_pk']
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        user = User.objects.get(pk=int(request.POST['renter']))
        car = Car.objects.get(pk=kwargs['car_pk'])
        self.object_list = User.objects.all()
        self.car_pk = kwargs['car_pk']

        # Сделать блок try...escept
        car.renter = user
        car.save()
        return render(request, self.template_name, self.get_context_data())