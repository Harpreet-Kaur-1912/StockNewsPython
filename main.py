import requests
import smtplib
import os

STOCK_NAME = "SMCI"
COMPANY_NAME = "Super Micro Computer"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

MY_EMAIL = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"





STOCK_PARAMS = {"function": "TIME_SERIES_DAILY",
                "symbol": "SMCI",
                "apikey": STOCK_API_KEY }
response = requests.get(url=STOCK_ENDPOINT, params = STOCK_PARAMS)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_stock_price = data_list[0]["4. close"]
print(yesterday_stock_price)

day_before_yesterday = data_list[1]["4. close"]
print(day_before_yesterday)
difference = abs(float(yesterday_stock_price) - float(day_before_yesterday))
print(difference)

percentage_difference = (difference / float(yesterday_stock_price)) * 100
print(percentage_difference)

if percentage_difference > 1:
    news_params = { "apiKey" : NEWS_API_KEY,
   "qInTitle" : STOCK_NAME, }
    response = requests.get(url=NEWS_ENDPOINT, params = news_params)
    article = response.json()["articles"]
    print(article)
    article_response = article[:3]
    print(article_response)


    formatted_article = ["Headline:{article['title']}. \n Brief: {article['description']}" for article in article_response]
    print(formatted_article)


    client = Client(TWILIO_SID, TWILIO_TOKEN)

    for article in formatted_article:
      message = client.messages.create(
          body=article,
          from_="+17372508034",
          to="+12892337666"
      )













