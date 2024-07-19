import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API = "MY_NEWS_KEY"
ALPHA_API = "MY_ALPHA_KEY"
TWILIO_SID = "MY_TWILIO_SID"
TWILIO_AUTH_TOKEN = "MY_TWILIO_AUTH_TOKEN"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
alpha_data = response.json()["Time Series (Daily)"]
alpha_data_list = [value for (key, value) in alpha_data.items()]
yesterday_data = alpha_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = alpha_data_list[1]
day_before_yesterday_close_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_close_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+12016901566",
            to="+972528770100"
        )