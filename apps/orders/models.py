from django.db import models
from django.core.validators import MaxValueValidator


class Order(models.Model):
    PAY_STATE_CHOICES = (
        ('결제완료', 0),
        ('결제취소', 1)
    )

    ORDER_STATE_CHOICES = (
        ('결제취소', 0),
        ('상품준비중', 1),
        ('상품출고', 2),
        ('배송중', 3),
        ('배송완료', 4)
    )

    id = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now_add=True, verbose_name='주문날짜')
    pay_state = models.CharField(max_length=4, choices=PAY_STATE_CHOICES, verbose_name='결제상태')
    order_state = models.CharField(max_length=5, default=0, choices=ORDER_STATE_CHOICES, verbose_name='주문상태')
    quantity = models.PositiveIntegerField(default=1, verbose_name='수량')
    product_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='상품 가격')
    coupon_discount = models.DecimalField(default=0.0, max_digits=10, decimal_places=3, null=True,
                                          verbose_name = '쿠폰 할인금액')
    total_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, verbose_name='총 주문금액')
    buyr_name = models.CharField(max_length=10, null=True, verbose_name='구매자')
    buyr_city = models.CharField(max_length=20, verbose_name='구매자 도시')
    buyr_country = models.CharField(max_length=5, verbose_name='구매자 국가코드')
    buyr_zipx = models.CharField(max_length=20, verbose_name='구매자 우편번호')
    vccode = models.CharField(max_length=10, verbose_name='나라별 decode')
    delivery_num = models.CharField(null=True, max_length=10, verbose_name='송장번호')
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='배송비', null=True)
    coupon = models.ForeignKey('coupons.Coupon', on_delete=models.SET_NULL, db_column = 'coupon', null=True,
                               verbose_name='쿠폰',)
    start_at = models.DateField(auto_now_add=True, verbose_name='주문시작일자')
    end_at = models.DateField(auto_now=True, verbose_name='주문종료일자')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return str(self.id)
