import requests
import connect
from datetime import datetime, timedelta, date

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
    "apikey": connect.API_KEY
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
print(yesterday_date)
news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday_date,
    "sortBy": "popularity",
    "apiKey": connect.NEWS_KEY
}

news_url = 'https://newsapi.org/v2/everything'
nr = requests.get(news_url, params=news_parameters)
news_data = nr.json()

print(STOCK)
print(str(f"{round(stock_change)}%"))
print(news_data["articles"][0]["title"])
print(news_data["articles"][0]["description"])


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
