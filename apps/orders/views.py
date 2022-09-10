from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


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
