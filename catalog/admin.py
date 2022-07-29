from django.contrib import admin
from .models import DishType, Status, Dish

admin.site.register(Dish)
admin.site.register(Status)
admin.site.register(DishType)

