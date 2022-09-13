import requests
from django.conf import settings


def get_current_rate_of_exchange(request):

    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

    params = {
        'authkey': settings.RATE_OF_EXCHANGE_API_KEY,
        'data': "AP01"
    }

    response = requests.get(url=url, params=params).json()
    current_rate_of_exchange = response[-1]['deal_bas_r']
    return current_rate_of_exchange
