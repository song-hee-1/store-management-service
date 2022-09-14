from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.coupons.models import Coupon, CouponType
from apps.deliveires.models import CountryCode, DeliveryCost

class CouponTestCase(APITestCase):
    """ Coupon Viewset action(list, create, retrieve ,update,partial_update, destory)이 정상 작동하는지 확인하기 위한 테스트 """

    def setUp(self):
        coupon_type_1 = CouponType.objects.create(type=1)
        coupon_type_2 = CouponType.objects.create(type=2)
        coupon_type_3 = CouponType.objects.create(type=3)

        Coupon.objects.create(
            code= "TESTCOUPONCODE", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=3000,
            active=True, type=coupon_type_1)
        Coupon.objects.create(
            code= "TESTCOUPONCODE", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=3000,
            active=True, type=coupon_type_2)
        Coupon.objects.create(
            code= "TESTCOUPONCODE", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=3000,
            active=True, type=coupon_type_3)

        CountryCode.objects.create(country_idx=221, country_code="US", country_dcode="+1", country_name="USA")
        DeliveryCost.objects.create(id=1, quantity=1, USA=33370)
        DeliveryCost.objects.create(id=1, quantity=2, USA=42620)
        DeliveryCost.objects.create(id=1, quantity=3, USA=65750)

    def test_create_coupon(self):
        data = {
            "code": "TESTCOUPONCODE2",
            "valid_from": "2022-09-14 04:29:00",
            "valid_to": "2022-09-20 04:29:00",
            "value": 3000,
            "active": "true",
            "type": 1
        }

        response = self.client.post(reverse('coupon-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_couponlist(self):
        response = self.client.get(reverse('coupon-list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_get_coupon_retrieve(self):
        response = self.client.get(reverse('coupon-detail', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_update_coupon(self):
        update_data = {
            "code": "TESTCOUPONCODE2",
            "valid_from": "2022-09-14 04:29:00",
            "valid_to": "2022-09-20 04:29:00",
            "value": 2000,
            "active": "true",
            "type": 1
        }
        response = self.client.put(reverse('coupon-detail', kwargs={'pk': 1}), update_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_destory_coupon(self):
        response = self.client.delete(reverse('coupon-detail', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)