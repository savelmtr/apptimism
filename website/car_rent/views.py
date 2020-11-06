from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from .models import Car
from django.shortcuts import render
from .decorators import staff_member_required_with_attrs
from django.http import HttpResponse
from .forms import CarEditForm

User = get_user_model()



@method_decorator(staff_member_required_with_attrs, name='dispatch')
class CarList(ListView):

    model = Car

    def post(self, request, *args, **kwargs):
        try:
            Car.objects.get(pk=request.POST['car_pk']).renter = None
        except Exception as e:
            print(e)
            return self.get(request, *args, **kwargs)
        return super().post(self, request, *args, **kwargs)


@method_decorator(staff_member_required_with_attrs, name='dispatch')
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

        try:
            user = User.objects.get(pk=int(request.POST['renter']))
            car = Car.objects.get(pk=self.car_pk)
            car.renter = user
            car.save()
        except Exception as e:
            print(e)
            return HttpResponse(f'Exception: {e}')
        return render(request, self.template_name, self.get_context_data())


@method_decorator(staff_member_required_with_attrs, name='dispatch')
class EditTheCar(DetailView):

    model = Car
    template_name = 'car_rent/car_edit.html'
    form_class = CarEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'object' in context:
            form = CarEditForm(instance=context['object'])
        else:
            form = CarEditForm()
        context['form'] = form
        return context