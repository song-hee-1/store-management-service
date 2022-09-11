from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CouponViewSet, CouponTypeViewSet

router = DefaultRouter()
router.register('coupons', viewset=CouponViewSet, basename='coupon')
router.register('coupons-type', viewset=CouponTypeViewSet, basename='coupon-type')

urlpatterns = [
    path('', include(router.urls)),
]
