from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from .forms import UserEditForm
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class Profile(View):
    
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):

        cars = request.user.car_set.all()
        
        return render(request, self.template_name, {'cars': cars})


@method_decorator(login_required, name='dispatch')
class EditProfile(View):

    form_class = UserEditForm

    success_url = reverse_lazy('users:profile')

    template_name = 'users/edit_profile.html'


    def get(self, request, *args, **kwargs):

        form = self.form_class(instance=request.user)
        
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid():

            form.save()

            return HttpResponseRedirect(success_url)

        return render(request, self.template_name, {'form': form})
