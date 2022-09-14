from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Order
from apps.deliveries.models import CountryCode, DeliveryCost
from apps.coupons.models import Coupon
from .serializers import OrderSerializer
from .utils import get_current_rate_of_exchange


class DateFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['start_at', 'end_at']


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(
                Q(id__icontains=q) | Q(date__icontains=q) | Q(pay_state__icontains=q) | Q(quantity__icontains=q) |
                Q(price__icontains=q) | Q(buyr_name__icontains=q) | Q(buyr_city__icontains=q) |
                Q(buyr_country__icontains=q) | Q(buyr_zipx__icontains=q) | Q(vccode__icontains=q) |
                Q(delivery_num__icontains=q)
            )
        return queryset

    filter_backends = [DjangoFilterBackend]
    filterset_class = DateFilter

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        buyr_country_code = data['buyr_country']
        quantity = data['quantity']

        # 입력받은 country code로 country name 가져옴
        country_name = CountryCode.objects.filter(country_code=buyr_country_code).values()[0]['country_name']

        if country_name:
            # 나라별로 수량에 맞는 배송비를 가져옴
            delivery_cost_per_quantity = DeliveryCost.objects.filter(quantity=quantity)
            delivery_cost = delivery_cost_per_quantity.values()[0][country_name]

            if country_name != 'South Korea':
                current_rate_of_exchange = get_current_rate_of_exchange(request)
                delivery_cost = round(delivery_cost / current_rate_of_exchange, 4)
        else:
            message = {"ERROR": "에러가 발생하였습니다. 입력된 국가 코드가 유효하지 않습니다"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        coupon = data['coupon']
        coupon_id = coupon.id
        product_price = data['product_price']
        coupon_discount = 0
        total_price = 0

        if coupon:
            coupon_type = Coupon.objects.get(id=coupon_id).type.type
            coupon_value = Coupon.objects.get(id=coupon_id).value

            if coupon_type == 1:
                coupon_discount += delivery_cost
            elif coupon_type == 2:
                coupon_discount = coupon_value
                product_price -= coupon_discount
            else:
                coupon_discount = product_price * coupon_value

        total_price = product_price + delivery_cost - coupon_discount

        if total_price < 0:
            total_price = 0

        self.perform_create(serializer, delivery_cost, coupon_discount, total_price)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, delivery_cost=None, coupon_discount=None, total_price=None):
        serializer.save(delivery_cost=delivery_cost, coupon_discount=coupon_discount, total_price=total_price)
