from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView

from .forms import CarEditForm
from .models import Car
from .services import get_car_from_user, give_car_to_user

User = get_user_model()


@method_decorator(staff_member_required, name='dispatch')
class CarList(ListView):

    model = Car

    queryset = Car.objects.order_by('-pk')

    def post(self, request, *args, **kwargs):

        result = get_car_from_user(request.POST['car_pk'])
        if result:
            print(result)
            return HttpResponse(f'Exception: {result}')

        return super().get(self, request, *args, **kwargs)


@method_decorator(staff_member_required, name='dispatch')
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

        self.object_list = User.objects.all()
        self.car_pk = kwargs['car_pk']

        result = give_car_to_user(int(request.POST['renter']), self.car_pk)

        if result:
            print(result)
            return HttpResponse(f'Exception: {result}')
        return render(request, self.template_name, self.get_context_data())


@method_decorator(staff_member_required, name='dispatch')
class CreateAndEditTheCar(View):

    template_name = 'car_rent/car_edit.html'
    form_class = CarEditForm

    def get(self, request, car_pk=None, *args, **kwargs):
        if car_pk and Car.objects.filter(pk=car_pk).exists():
            car = Car.objects.get(pk=car_pk)
            form = self.form_class(instance=car)
            regime = 1
        else:
            form = self.form_class()
            regime = 0

        return render(
            request, self.template_name, {'form': form, 'message': '', 'regime': regime})

    def post(self, request, car_pk=None, *args, **kwargs):
        if car_pk and Car.objects.filter(pk=car_pk).exists():
            car = Car.objects.get(pk=car_pk)
            form = self.form_class(request.POST, instance=car)
            regime = 1
            msg = _('The car is successfully edited.')
        else:
            form = self.form_class(request.POST)
            regime = 1
            msg = _('The car is successfully added.')

        if form.is_valid():

            car_instance = form.save()

            return HttpResponseRedirect(
                reverse_lazy('car_rent:edit_car', kwargs={'car_pk': car_instance.pk}))

        return render(
            request, self.template_name, {'form': form, 'message': msg, 'regime': regime})
