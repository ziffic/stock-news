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


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": connect.STOCK_API_KEY
}

url = 'https://www.alphavantage.co/query'
r = requests.get(url, params=parameters)
data = r.json()
yesterday_data = f"{yesterday.year}-{make_double(yesterday.month)}-{make_double(yesterday.day)} 18:00:00"
day_before_data = f"{day_before.year}-{make_double(day_before.month)}-{make_double(day_before.day)} 18:00:00"
# print(yesterday_data)
# print(day_before_data)

yesterday_close = float(data["Time Series (60min)"][yesterday_data]["4. close"])
day_before_close = float(data["Time Series (60min)"][day_before_data]["4. close"])
# print(yesterday_close)
# print(day_before_close)

difference = yesterday_close - day_before_close
stock_change = (difference / yesterday_close) * 100
# print(stock_change)

if -5 >= stock_change >= 5:
    print("Get News!")

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# print(yesterday_date)
news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday_date,
    "sortBy": "popularity",
    "apiKey": connect.NEWS_API_KEY
}

news_url = 'https://newsapi.org/v2/everything'
nr = requests.get(news_url, params=news_parameters)
news_data = nr.json()

client = Client("AC8472eaddc77bfd632a39df070d64eb4b", "a8c4b634c22d11569aca799b0e5f595a")

for n in range(3):
    text_body = f"{STOCK}"
    print(STOCK)
    print(str(f"{round(stock_change)}%"))
    print(news_data["articles"][n]["title"])
    print(news_data["articles"][n]["description"])

    message = client.messages \
        .create(body="Test", from_='+18662711651', to='+17143231961')


# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height 
of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height 
of the coronavirus market crash.
"""
