import requests
from django.conf import settings


def get_current_rate_of_exchange(request):

    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

    params = {
        'authkey': settings.RATE_OF_EXCHANGE_API_KEY,
        'data': "AP01"
    }

    response = requests.get(url=url, params=params).json()
    deal_base_r = response[-1]['deal_bas_r']
    replace_comma_deal_base_r = deal_base_r.replace(",", "")

    current_rate_of_exchange = float(replace_comma_deal_base_r)
    return current_rate_of_exchange
