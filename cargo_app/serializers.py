from .models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ( 'name', 'quantity', 'cat_price')

#class TrackSerializer(serializers.ModelSerializer):
#    class Meta:
    