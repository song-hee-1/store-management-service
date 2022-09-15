from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import Coupon, ClaimedCoupon, CouponType
from .serializers import CouponSerializer, CouponTypeSerializer, ClaimedCouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()

    @action(detail=True, methods=['put'])
    def redeem(self, request, pk=None, **kwargs):
        """
        쿠폰 사용(redeem)을 위한 endpoint
        """

        queryset = Coupon.objects.all()
        coupon = get_object_or_404(queryset, pk=pk)

        data = {
            'coupon': pk,
            'user': self.request.user.id,
        }

        serializer = ClaimedCouponSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CouponTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CouponTypeSerializer
    queryset = CouponType.objects.all()


class ClaimedCouponViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimedCouponSerializer
    queryset = ClaimedCoupon.objects.all()

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


class ClaimedCouponTypeView(APIView):
    def get(self, request):

        # 쿠폰 타입별로 할인 금액의 합
        # ClaimedCoupon.objects.values('coupon_id__type').annotate(Sum('coupon_discount'))

        # 쿠폰 타입별로 사용 횟수
        # ClaimedCoupon.objects.values('coupon_id__type').annotate(count=Count('coupon_id'))

        # 쿠폰 타입별로 사용 횟수와 할인 금액의 합
        annotate = ClaimedCoupon.objects.values('coupon_id__type').\
            annotate(claimed_count=Count('coupon_id'), claimed_discount_price=Sum('coupon_discount'))

        return Response(annotate)
