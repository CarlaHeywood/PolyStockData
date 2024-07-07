# backend/serializers.py

# Convert the python model/objects into JSON compatible data
from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
