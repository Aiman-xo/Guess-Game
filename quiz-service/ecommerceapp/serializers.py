from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Product1,Category

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product1
        fields='__all__'

    def validate_price(self,value):
        if value < 0:
            raise ValidationError('price cannot be negative',status=400)
        return value
