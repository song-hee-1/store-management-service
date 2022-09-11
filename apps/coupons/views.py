from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Coupon
from .serializers import CouponSerializer, CouponTypeSerializer, ClaimedCouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()


class CouponTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CouponTypeSerializer
    queryset = Coupon.objects.all()


class ClaimedCouponViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimedCouponSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        return Response(status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        return Response(status.HTTP_404_NOT_FOUND)
