import argparse
import aiohttp
import asyncio

async def fetch_exchange_rates(date):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to fetch data for date {date}")

async def get_exchange_rates(days):
    today = datetime.date.today()
    exchange_rates = []

    for i in range(days):
        date = today - datetime.timedelta(days=i)
        data = await fetch_exchange_rates(date.strftime("%d.%m.%Y"))
        
        eur = None
        usd = None

        for rate in data['exchangeRate']:
            if rate['currency'] == 'EUR':
                eur = {
                    'sale': float(rate['saleRate']),
                    'purchase': float(rate['purchaseRate'])
                }
            elif rate['currency'] == 'USD':
                usd = {
                    'sale': float(rate['saleRate']),
                    'purchase': float(rate['purchaseRate'])
                }

        if eur is not None and usd is not None:
            exchange_rates.append({date.strftime("%d.%m.%Y"): {'EUR': eur, 'USD': usd}})
    
    return exchange_rates

if __name__ == "__main__":
    import datetime

    parser = argparse.ArgumentParser()
    parser.add_argument("days", type=int, default=2, nargs='?', help="Кількість днів")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    rates = loop.run_until_complete(get_exchange_rates(args.days))
    print(rates)
