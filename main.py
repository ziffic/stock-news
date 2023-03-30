import requests
import connect
# from datetime import datetime, timedelta, date
# from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": connect.STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()["Time Series (60min)"]
data_list = [value for (key, value) in data.items()]

# Get yesterday's closing stock price
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
diff_percent = difference / yesterday_closing_price * 100
print(diff_percent)

if diff_percent > 5:
    print("Get News!")

# news_parameters = {
#     "q": COMPANY_NAME,
#     "from": yesterday_date,
#     "sortBy": "popularity",
#     "apiKey": connect.NEWS_API_KEY
# }

# nr = requests.get(NEWS_ENDPOINT, params=news_parameters)
# news_data = nr.json()

# client = Client(connect.ACCOUNT_SID, connect.AUTH_TOKEN)

# for n in range(3):
#     text_body = f"{STOCK}"
#     print(STOCK)
#     print(str(f"{round(stock_change)}%"))
#     print(news_data["articles"][n]["title"])
#     print(news_data["articles"][n]["description"])

    # message = client.messages \
    #     .create(body="Test", from_='+18662711651', to='+17143231961')
