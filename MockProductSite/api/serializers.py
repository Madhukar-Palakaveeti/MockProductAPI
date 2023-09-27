from rest_framework import serializers
from api.models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length = 200)
    price = serializers.IntegerField(required=False)
    rating = serializers.CharField(max_length=4, required=False)
    discount = serializers.CharField(max_length=11, required=False)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.discount = validated_data.get('discount', instance.discount)

        instance.save()
        return instance

