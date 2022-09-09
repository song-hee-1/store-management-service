from django.db import models
from django.core.validators import MaxValueValidator


class Order(models.Model):
    PAY_STATE_CHOICES = (
        ('결제완료', '0'),
        ('결제취소', '1')
    )
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now_add=True, verbose_name='주문날짜')
    pay_state = models.CharField(max_length=4, choices=PAY_STATE_CHOICES, verbose_name='결제상태')
    quantity = models.PositiveIntegerField(default=1, verbose_name='수량')
    price = models.IntegerField(validators=[MaxValueValidator(10000000)], verbose_name='상품 가격')
    buyr_name = models.CharField(max_length=10, null=True, verbose_name='구매자')
    buyr_city = models.CharField(max_length=20, verbose_name='구매자 도시')
    buyr_country = models.CharField(max_length=5, verbose_name='구매자 국가')
    buyr_zipx = models.CharField(max_length=20, verbose_name='구매자 우편번호')
    vccode = models.CharField(max_length=10, verbose_name='나라별 decode')
    delivery_num = models.CharField(null=True, max_length=10, verbose_name='송장번호')
    delivery_cost = models.ForeignKey('deliveries.DeliveryCost', null=True,
                                      db_column='delivery_cost', on_delete=models.PROTECT, verbose_name='배송비')
    coupon = models.ForeignKey('coupons.Coupon', verbose_name='쿠폰', on_delete=models.SET_NULL, null=True)
    start_at = models.DateTimeField(auto_now_add=True, verbose_name='주문시작일자')
    end_at = models.DateTimeField(auto_now=True, verbose_name='주문종료일자')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return str(self.id)
