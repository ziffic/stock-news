import requests
import connect
from datetime import datetime, timedelta, date
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

yesterday_date = date.today() - timedelta(days=1)
yesterday = datetime.today() - timedelta(days=1)
day_before = datetime.today() - timedelta(days=2)


def make_double(num):
    if num < 10:
        return f"0{num}"
    else:
        return num


parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": connect.API_KEY
}

url = 'https://www.alphavantage.co/query'
r = requests.get(url, params=parameters)
data = r.json()
yesterday_data = f"{yesterday.year}-{make_double(yesterday.month)}-{make_double(yesterday.day)} 18:00:00"
day_before_data = f"{day_before.year}-{make_double(day_before.month)}-{make_double(day_before.day)} 18:00:00"

yesterday_close = float(data["Time Series (60min)"][yesterday_data]["4. close"])
day_before_close = float(data["Time Series (60min)"][day_before_data]["4. close"])

difference = yesterday_close - day_before_close
stock_change = (difference / yesterday_close) * 100

if -5 >= stock_change >= 5:
    print("Get News!")

news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday_date,
    "sortBy": "popularity",
    "apiKey": connect.NEWS_KEY
}

news_url = 'https://newsapi.org/v2/everything'
nr = requests.get(news_url, params=news_parameters)
news_data = nr.json()

client = Client(connect.ACCOUNT_SID, connect.AUTH_TOKEN)

for n in range(3):
    text_body = f"{STOCK}"
    print(STOCK)
    print(str(f"{round(stock_change)}%"))
    print(news_data["articles"][n]["title"])
    print(news_data["articles"][n]["description"])

    message = client.messages \
        .create(body="Test", from_='+18662711651', to='+17143231961')
