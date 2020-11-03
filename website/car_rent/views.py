from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Car

@method_decorator(login_required, name='dispatch')
class CarList(ListView):

	model = Car
