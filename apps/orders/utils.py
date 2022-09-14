import requests
from decimal import Decimal
from django.conf import settings


def get_current_rate_of_exchange(request):
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

    params = {
        'authkey': settings.RATE_OF_EXCHANGE_API_KEY,
        'data': "AP01"
    }

    response = requests.get(url=url, params=params).json()

    try:
        deal_base_r = response[-1]['deal_bas_r']
        replace_comma_deal_base_r = deal_base_r.replace(",", "")
        current_rate_of_exchange = Decimal(replace_comma_deal_base_r)
    except:
        current_rate_of_exchange = 1200
    finally:
        return current_rate_of_exchange
