import requests
import connect
from twilio.rest import Client

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

difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(difference / yesterday_closing_price * 100)

if abs(diff_percent) > .5:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": connect.NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{COMPANY_NAME}: {up_down}{diff_percent}%\n"
                          f"Headline: {article['title']} \n"
                          f"Brief: {article['description']}" for article in articles]

    client = Client(connect.TWILIO_SID, connect.TWILIO_AUTH_TOKEN)

    # for article in articles:
    #     message = client.messages.create(
    #         body=article,
    #         from_='+18662711651',
    #         to='+17143231961'
    #     )
