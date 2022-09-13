from rest_framework import serializers

from .models import Coupon, CouponType, ClaimedCoupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponType
        fields = '__all__'


class ClaimedCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimedCoupon
        fields = '__all__'
