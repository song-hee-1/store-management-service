from rest_framework import viewsets

from .models import Coupon
from .serializers import CouponSerializer, CouponTypeSerializer


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()


class CouponTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CouponTypeSerializer
    queryset = Coupon.objects.all()
