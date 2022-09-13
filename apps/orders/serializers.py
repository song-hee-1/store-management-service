from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['delivery_cost']

    # def create(self, validated_data):
    #     buyr_country_code = validated_data.pop('buyr_country')
    #
    #     return Order.objects.create(buyr_country = buyr_country_code, **validated_data)
