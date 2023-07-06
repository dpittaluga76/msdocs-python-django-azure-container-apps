from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
import requests
import json

def send_to_botpedido(phone_number, free_text):
    url = 'https://botpedido-app-service.azurewebsites.net/set-free-text'
    data = {
        'person_phone_number': phone_number,
        'free_text': free_text,
        'api_key': "bosanova2023"
    }
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    person_phone_number = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    business_description = models.TextField()
    email = models.EmailField()
    requirement_description = models.TextField()
    intro = models.TextField(blank=True, null=True)
    free_text = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Client.objects.get(pk=self.pk)
            if orig.free_text != self.free_text: 
                # free_text field has changed
                send_to_botpedido(self.person_phone_number, self.free_text)
        
        super(Client, self).save(*args, **kwargs)


class Product(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    min_quantity = models.IntegerField()
    #  This is number of days.
    price_estimate = models.IntegerField(default=5)
    production_estimate = models.IntegerField(default=5)
    attribute_prefix = models.CharField(max_length=255)
    attribute_suffix = models.CharField(max_length=255)
    product_list_title = models.CharField(max_length=255)

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Order(models.Model):
    PICKUP = 'PU'
    DELIVERY = 'DE'

    PICKUP_DELIVERY_CHOICES = [
        (PICKUP, 'Pickup'),
        (DELIVERY, 'Delivery'),
    ]

    order_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    pickup_delivery = models.CharField(
        max_length=2,
        choices=PICKUP_DELIVERY_CHOICES,
        default=PICKUP,
    )
    product_detail = models.TextField()
    specs = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    extra_details = models.TextField(blank=True)
