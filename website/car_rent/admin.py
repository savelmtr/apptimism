from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass

class CarInline(admin.TabularInline):
    model = Car
    extra = 3