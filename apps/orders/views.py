from django.db.models import Q

from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


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
                Q(delivery_num__icontains=q) | Q(start_at__icontains=q) | Q(end_at__icontains=q)
            )
        return queryset
