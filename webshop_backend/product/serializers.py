# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields from the Product model

    def validate(self, attrs):
        # Add any custom validation logic here
        if attrs['price'] <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        if attrs['rating'] < 0 or attrs['rating'] > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        if attrs['stock'] < 1:
            raise serializers.ValidationError('Stock must be greater than zero.')
        return attrs