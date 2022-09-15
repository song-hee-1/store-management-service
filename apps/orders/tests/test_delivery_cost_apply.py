from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.orders.models import Order
from apps.coupons.models import Coupon, CouponType
from apps.deliveries.models import DeliveryCost, CountryCode


class DeliveryCostTestCase(APITestCase):
    """구매 국가, 구매 갯수에 따른 배송비 적용을 확인하기 위한 테스트"""

    def setUp(self):
        coupon_type_1 = CouponType.objects.create(type=1)
        coupon_type_2 = CouponType.objects.create(type=2)
        coupon_type_3 = CouponType.objects.create(type=3)

        coupon_1 = Coupon.objects.create(
            code="TESTCOUPONCODE1", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=0,
            active=True, type=coupon_type_1)
        coupon_2 = Coupon.objects.create(
            code="TESTCOUPONCODE2", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=3000,
            active=True, type=coupon_type_2)
        coupon_3 = Coupon.objects.create(
            code="TESTCOUPONCODE3", valid_from="2022-09-14 04:29:00", valid_to="2022-09-20 04:29:00", value=0.50,
            active=True, type=coupon_type_3)

        CountryCode.objects.create(country_idx=221, country_code="US", country_dcode="+1", country_name="USA")
        CountryCode.objects.create(country_idx=37, country_code="CA", country_dcode="+1", country_name="Canada")
        DeliveryCost.objects.create(
            id=1, quantity=1, Australia=26000, Brazil=38300, Canada=34370, China=25970, France=31070, Germany=36220,
            Hong_kong=24250, Indonesia=21200, Japan=25470, Malaysia=19820, New_Zealand=26000, Philippines=20550,
            Russia=37070, Singapore=17550, Spain=33720, Taiwan=19720, Thailand=20970, UK=38070, USA=33370,
            Vietnam=18970, Cambodia=21500, Laos=21500, Macao=21500, Mongolia=21500, Myanmar=21500, Bangladesh=22000,
            Bhutan=22000, Brunei_Darussala=22000, India=22000, Maldives=22000, Nepal=22000, Sri_Lanka=22000,
            Albania=32500, Armenia=32500, Austria=32500, Azerbaijan=32500, Bahrain=32500, Belarus=32500, Belgium=32500,
            Bulgaria=32500, Bosnia_And_Herzegovina=32500, Croatia=32500, Cyprus=32500, Czech_Rep=32500, Denmark=32500,
            Estonia=32500, Finland=32500, Georgia=32500, Greece=32500, Hungary=32500, Iran=32500, Ireland=32500,
            Israel=32500, Jordan=32500, Kazakhstan=32500, Latvia=32500, Luxembourg=32500, Macedonia=32500,
            Netherlands=32500, Norway=32500, Oman=32500, Pakistan=32500, Poland=32500, Portugal=32500, Qatar=32500,
            Romania=32500, Saudi_Arabia=32500, Slovakia=32500, Slovenia=32500, Sweden=32500, Switzerland=32500,
            Turkey=32500, Ukraine=32500, United_Arab_Emirates=32500, Uzbekistan=32500, Algeria=36000,
            Antiless_Netherlands=36000, Argentina=36000, Botswana=36000, Cape_Verde=36000, Chile=36000,
            Costa_Rica=36000, Cuba=36000, Djibouti=36000, Dominican_Republic=36000, Ecuador=36000, Egypt=36000,
            Eritrea=36000, Ethiopia=36000, Fiji=36000, Kenya=36000, Lesotho=36000, Mauritius=36000, Mexico=36000,
            Morocco=36000, Mozambique=36000, Nigeria=36000, Panama=36000, Peru=36000, Rwanda=36000, Tanzania=36000,
            Tunisia=36000, Zambia=36000
        )
        DeliveryCost.objects.create(
            id=2, quantity=2, Australia=32000, Brazil=46500, Canada=40620, China=29620, France=36620, Germany=42370,
            Hong_kong=26750, Indonesia=24500, Japan=29120, Malaysia=23370, New_Zealand=30500, Philippines=23250,
            Russia=44120, Singapore=21250, Spain=40370, Taiwan=22870, Thailand=23620, UK=44120, USA=42620,
            Vietnam=21620,
            Cambodia=23500, Laos=23500, Macao=23500, Mongolia=23500, Myanmar=23500, Bangladesh=25000, Bhutan=25000,
            Brunei_Darussala=25000, India=25000, Maldives=25000, Nepal=25000, Sri_Lanka=25000, Albania=36500,
            Armenia=36500, Austria=36500, Azerbaijan=36500, Bahrain=36500, Belarus=36500, Belgium=36500, Bulgaria=36500,
            Bosnia_And_Herzegovina=36500, Croatia=36500, Cyprus=36500, Czech_Rep=36500, Denmark=36500, Estonia=36500,
            Finland=36500, Georgia=36500, Greece=36500, Hungary=36500, Iran=36500, Ireland=36500, Israel=36500,
            Jordan=36500, Kazakhstan=36500, Latvia=36500, Luxembourg=36500, Macedonia=36500, Netherlands=36500,
            Norway=36500, Oman=36500, Pakistan=36500, Poland=36500, Portugal=36500, Qatar=36500, Romania=36500,
            Saudi_Arabia=36500, Slovakia=36500, Slovenia=36500, Sweden=36500, Switzerland=36500, Turkey=36500,
            Ukraine=36500, United_Arab_Emirates=36500, Uzbekistan=36500, Algeria=42000, Antiless_Netherlands=42000,
            Argentina=42000, Botswana=42000, Cape_Verde=42000, Chile=42000, Costa_Rica=42000, Cuba=42000,
            Djibouti=42000,
            Dominican_Republic=42000, Ecuador=42000, Egypt=42000, Eritrea=42000, Ethiopia=42000, Fiji=42000,
            Kenya=42000,
            Lesotho=42000, Mauritius=42000, Mexico=42000, Morocco=42000, Mozambique=42000, Nigeria=42000, Panama=42000,
            Peru=42000, Rwanda=42000, Tanzania=42000, Tunisia=42000, Zambia=42000
        )

        Order.objects.create(
            pay_state="결제완료",
            order_state="상품준비중",
            quantity=1,
            product_price=10000,
            buyr_name="한핑핑",
            buyr_city="미국 어딘가",
            buyr_country="US",
            buyr_zipx="12345",
            vccode="12345",
        )

    def test_delivery_cost_per_quantity(self):
        us_quantity_1 = {
            "pay_state": "결제완료",
            "order_state": "상품준비중",
            "quantity": 1,
            "product_price": 10000,
            "buyr_name": "한핑핑",
            "buyr_city": "미국 어딘가",
            "buyr_country": "US",
            "buyr_zipx": "12345",
            "vccode": "12345",
            "coupon": 1
        }

        us_quantity_2 = {
            "pay_state": "결제완료",
            "order_state": "상품준비중",
            "quantity": 2,
            "product_price": 10000,
            "buyr_name": "한핑핑",
            "buyr_city": "미국 어딘가",
            "buyr_country": "US",
            "buyr_zipx": "12345",
            "vccode": "12345",
            "coupon": 1
        }

        # 미국에서 1개 구입시
        response = self.client.post(reverse('order-list'), us_quantity_1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        us_delivery_cost_1 = float(response.data["delivery_cost"])

        # 미국에서 2개 구입시
        response = self.client.post(reverse('order-list'), us_quantity_2)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        us_delivery_cost_2 = float(response.data["delivery_cost"])

        # 1개 구입시와 2개 구입시의 배송비는 다르고, 2개 구입시의 배송비가 더 큼
        self.assertTrue(us_delivery_cost_1 != us_delivery_cost_2)
        self.assertTrue(us_delivery_cost_2 > us_delivery_cost_1)

    def test_delivery_cost_per_country(self):
        canada_data = {
            "pay_state": "결제완료",
            "order_state": "상품준비중",
            "quantity": 1,
            "product_price": 10000,
            "buyr_name": "한핑핑2",
            "buyr_city": "캐나다 어딘가",
            "buyr_country": "CA",
            "buyr_zipx": "12345",
            "vccode": "12345",
            "coupon": 1
        }

        us_data = {
            "pay_state": "결제완료",
            "order_state": "상품준비중",
            "quantity": 1,
            "product_price": 10000,
            "buyr_name": "한핑핑",
            "buyr_city": "미국 어딘가",
            "buyr_country": "US",
            "buyr_zipx": "12345",
            "vccode": "12345",
            "coupon": 1
        }

        response = self.client.post(reverse('order-list'),  canada_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        canada_delivery_cost = float(response.data["delivery_cost"])

        response = self.client.post(reverse('order-list'), us_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        us_delivery_cost = float(response.data["delivery_cost"])

        # 캐나다(34370)와 미국(33370)의 배송비는 다르고, 캐나다의 배송비가 더 큼
        self.assertTrue(canada_delivery_cost != us_delivery_cost)
        self.assertTrue(canada_delivery_cost > us_delivery_cost)
