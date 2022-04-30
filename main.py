import asyncio
import aiohttp


def mono_upd(currency, result_dict, api):
    if currency['currencyCodeA'] == 840:
        if currency['rateSell'] > result_dict['USD']['sell']['value']:
            result_dict['USD']['sell']['bank'] = api
            result_dict['USD']['sell']['value'] = currency['rateSell']
        if currency['rateBuy'] > result_dict['USD']['buy']['value']:
            result_dict['USD']['buy']['bank'] = api
            result_dict['USD']['buy']['value'] = currency['rateBuy']
    if currency['currencyCodeA'] == 978:
        if currency['rateSell'] > result_dict['EUR']['sell']['value']:
            result_dict['EUR']['sell']['bank'] = api
            result_dict['EUR']['sell']['value'] = currency['rateSell']
        if currency['rateBuy'] > result_dict['EUR']['buy']['value']:
            result_dict['EUR']['buy']['bank'] = api
            result_dict['EUR']['buy']['value'] = currency['rateBuy']


def privat_upd(currency, result_dict, api):
    if currency['ccy'] == 'USD':
        if float(currency['sale']) > result_dict['USD']['sell']['value']:
            result_dict['USD']['sell']['bank'] = api
            result_dict['USD']['sell']['value'] = float(currency['sale'])
        if float(currency['buy']) > result_dict['USD']['buy']['value']:
            result_dict['USD']['buy']['bank'] = api
            result_dict['USD']['buy']['value'] = float(currency['buy'])
    if currency['ccy'] == 'EUR':
        if float(currency['sale']) > result_dict['EUR']['sell']['value']:
            result_dict['EUR']['sell']['bank'] = api
            result_dict['EUR']['sell']['value'] = float(currency['sale'])
        if float(currency['buy']) > result_dict['EUR']['buy']['value']:
            result_dict['EUR']['buy']['bank'] = api
            result_dict['EUR']['buy']['value'] = float(currency['buy'])


async def get_currency_rates(api, api_dict, result_dict, session):
    response = await session.request(method='GET', url=api_dict[api])
    currency_dict = await response.json()
    if api == 'monobank':
        for currency in currency_dict:
            mono_upd(currency, result_dict, api)
    if api == 'privatbank':
        for currency in currency_dict:
            privat_upd(currency, result_dict, api)


async def main():
    result_dict = {
        'EUR': {
            'buy': {
                'bank': '',
                'value': 0,
            },
            'sell': {
                'bank': '',
                'value': 0,
            },
        },
        'USD': {
            'buy': {
                'bank': '',
                'value': 0,
            },
            'sell': {
                'bank': '',
                'value': 0,
            },
        }
    }
    api_dict = {'monobank': 'https://api.monobank.ua/bank/currency',
                'privatbank': 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11',
                }

    connector = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        await asyncio.gather(*[get_currency_rates(api, api_dict, result_dict, session) for api in api_dict])

    print(result_dict)


if __name__ == '__main__':
    asyncio.run(main())
