from django.contrib import admin
from .models.client import Order, Client  # Assuming 'MyModel' is your model's name.

admin.site.register(Order)
admin.site.register(Client)
