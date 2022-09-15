from django.utils.timezone import now

from rest_framework import serializers

from .models import Coupon, CouponType, ClaimedCoupon


class CouponSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if 'valid_to' in data:
            if data['valid_to'] < now():
                raise serializers.ValidationError("유효기간이 현재보다 과거입니다.")

        if 'type' in data:
            coupon = CouponType.objects.get(type=data['type'].type)
            if coupon.type == 3 and data['value'] > 1.0:
                raise serializers.ValidationError("할인율은 1.0 이하만 가능합니다. 100%를 초과할 수 없습니다.")

        return data

    class Meta:
        model = Coupon
        fields = '__all__'


class CouponTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponType
        fields = '__all__'


class ClaimedCouponSerializer(serializers.ModelSerializer):
    def validate(self):
        coupon = data['coupon']

        if coupon.valid_from and coupon.valid_from > now():
            raise serializers.ValidationError("쿠폰 사용이 아직 불가능합니다.")

        if coupon.valid_to and coupon.valid_to < now():
            raise serializers.ValidationError("쿠폰이 만료되었습니다.")

    class Meta:
        model = ClaimedCoupon
        fields = '__all__'
