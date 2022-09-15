from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.coupons.models import Coupon, CouponType


class CouponTestCase(APITestCase):
    """ Coupon Viewset action(list, create, retrieve ,update,partial_update, destory)이 정상 작동하는지 확인하기 위한 테스트 """

    def setUp(self):
        coupon_instance = CouponType.objects.create(type=1)
        CouponType.objects.create(type=2)
        CouponType.objects.create(type=3)
        Coupon.objects.create(
            code= "TESTCOUPONCODE", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=3000,
            active=True, type=coupon_instance)

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


class CouponValidateTestCase(APITestCase):
    """쿠폰 생성시 유효성이 정상적으로 검사되는지 확인하기 위한 테스트"""

    def setUp(self):
        coupon_type_1 = CouponType.objects.create(type=1)
        coupon_type_2 = CouponType.objects.create(type=2)
        coupon_type_3 = CouponType.objects.create(type=3)

    def test_create_coupon_false_validate_to(self):
        data = {
            "code": "TESTESETTESTSETETS",
            "valid_from": "2022-09-13",
            "valid_to": "2022-09-14",
            "value": 0,
            "active": True,
            "type": 1
        }
        response = self.client.post(reverse('coupon-list'), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_coupon_false_value(self):
        data = {
            "code": "TESTESETTESTSETETS",
            "valid_from": "2022-09-14",
            "valid_to": "2022-09-20",
            "value": 1.1,
            "active": True,
            "type": 3
        }
        response = self.client.post(reverse('coupon-list'), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
