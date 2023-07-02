from rest_framework import serializers
from .models.client import Order, Client
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):
    person_phone_number = serializers.CharField(write_only=True)
    producto = serializers.CharField(source='product_detail')
    specs = serializers.CharField(allow_blank=True)
    precio = serializers.DecimalField(source='price', max_digits=10, decimal_places=2, allow_null=True)
    cantidad = serializers.IntegerField(source='quantity')
    extra = serializers.CharField(source='extra_details', allow_blank=True)

    class Meta:
        model = Order
        fields = ['person_phone_number', 'producto', 'specs', 'precio', 'cantidad', 'extra']
        extra_kwargs = {
            'pickup_delivery': {'required': False, 'default': Order.PICKUP}
        }

    def validate_person_phone_number(self, value):
        return value  # We don't validate the client's existence here anymore.

    def create(self, validated_data):
        phone_number = validated_data.pop('person_phone_number')
        
        # If the Client does not exist, we'll create a User and then a Client associated with this User.
        if not Client.objects.filter(person_phone_number=phone_number).exists():
            try:
                user = User.objects.create_user(username=phone_number, password='default_password')  # Adjust as needed.
                client = Client.objects.create(user=user, person_phone_number=phone_number)
            except Exception as e:
                raise serializers.ValidationError({"user": f"Error when creating User or Client: {str(e)}"})
        else:
            client = Client.objects.get(person_phone_number=phone_number)

        return Order.objects.create(client=client, **validated_data)
