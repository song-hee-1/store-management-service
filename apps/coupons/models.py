from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Coupon(models.Model):
    type = models.ForeignKey('CouponType', db_column='type', on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'coupon'

    def __str__(self):
        return self.code


class CouponType(models.Model):
    """
    배송비 할인 : 0
    정액 할인 : 1
    % 할인 : 2
    """
    type = models.PositiveIntegerField()

    class Meta:
        db_table = 'coupon_type'


# 발급된 쿠폰의 사용내역 열람을 위해 사용된 쿠폰 테이블 추가
class ClaimedCoupon(models.Model):
    redeemed = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'claimed_coupon'
