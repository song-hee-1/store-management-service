from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    type = models.ForeignKey('CouponType', db_column='type', on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    num_available = models.PositiveIntegerField(null=True)
    num_used = models.IntegerField(default=0)

    class Meta:
        db_table = 'coupon'

    def __str__(self):
        return self.code

    # def can_use(self):
    #     active = True
    #
    #     # if self.active == False:
    #     #     active = False
    #
    #     if self.num_used >= self.num_available != 0:
    #         active = False
    #
    #     return active
    #
    # def use(self):
    #     self.num_used = self.num_used + 1
    #
    #     if self.num_used == self.num_available:
    #         self.active = False
    #
    #     self.save()


class CouponType(models.Model):
    """
    배송비 할인 : 0
    정액 할인 : 1
    % 할인 : 2
    """
    type = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'coupon_type'
