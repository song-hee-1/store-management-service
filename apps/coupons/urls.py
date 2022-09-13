from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CouponViewSet, CouponTypeViewSet, ClaimedCouponViewSet

router = DefaultRouter()
router.register('coupons', viewset=CouponViewSet, basename='coupon')
router.register('coupons-type', viewset=CouponTypeViewSet, basename='coupon-type')
router.register('claimed-coupons', viewset=ClaimedCouponViewSet, basename='cliamed-coupon')

urlpatterns = [
    path('', include(router.urls)),
]
