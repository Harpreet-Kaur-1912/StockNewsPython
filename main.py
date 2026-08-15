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


# ---------------- STOCK DATA ---------------- #

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(
    url=STOCK_ENDPOINT,
    params=stock_params
)

response.raise_for_status()

data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]


# Yesterday closing price
yesterday_stock_price = float(
    data_list[0]["4. close"]
)

print("Yesterday:", yesterday_stock_price)


# Day before yesterday closing price
day_before_yesterday = float(
    data_list[1]["4. close"]
)

print("Day before yesterday:", day_before_yesterday)


# Difference
difference = abs(
    yesterday_stock_price - day_before_yesterday
)

print("Difference:", difference)


# Percentage difference
percentage_difference = (
    difference / day_before_yesterday
) * 100

print("Percentage difference:", percentage_difference)


# ---------------- NEWS ---------------- #

if percentage_difference > 1:

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    response = requests.get(
        url=NEWS_ENDPOINT,
        params=news_params
    )

    response.raise_for_status()

    articles = response.json()["articles"]

    article_response = articles[:3]


    formatted_articles = [
        f"Headline: {article['title']}\n"
        f"Brief: {article['description']}"
        for article in article_response
    ]

    print(formatted_articles)


    # ---------------- EMAIL ---------------- #

    email_body = "\n\n".join(formatted_articles)

    subject = (
        f"{STOCK_NAME} Stock Alert - "
        f"{percentage_difference:.2f}% move"
    )

    message = (
        f"Subject: {subject}\n\n"
        f"{STOCK_NAME} moved "
        f"{percentage_difference:.2f}%.\n\n"
        f"{email_body}"
    )


    with smtplib.SMTP(
        "smtp.gmail.com",
        port=587
    ) as connection:

        connection.starttls()

        connection.login(
            user=MY_EMAIL,
            password=EMAIL_PASSWORD
        )

        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=message
        )

    print("Email sent successfully!")

else:
    print("Stock did not move more than 1%. No email sent.")
