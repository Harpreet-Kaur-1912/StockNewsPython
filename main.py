import requests
import smtplib
import os

STOCK_NAME = "SMCI"
COMPANY_NAME = "Super Micro Computer"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_PASSWORD = os.environ.get("PASSWORD")

FROM_EMAIL = "hkaur19121989@gmail.com"
TO_EMAIL = "harpreet.kaur.9012@gmail.com"

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

stock_data = response.json()

if "Time Series (Daily)" not in stock_data:
    print(stock_data)
    raise Exception("Stock data was not returned correctly.")

data = stock_data["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]


yesterday_stock_price = float(
    data_list[0]["4. close"]
)

day_before_yesterday = float(
    data_list[1]["4. close"]
)

print("Yesterday closing price:", yesterday_stock_price)
print("Day before yesterday closing price:", day_before_yesterday)


# ---------------- PERCENTAGE CHANGE ---------------- #

difference = abs(
    yesterday_stock_price - day_before_yesterday
)

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

    news_data = response.json()

    articles = news_data["articles"]

    top_three_articles = articles[:3]


    formatted_articles = [
        f"Headline: {article['title']}\n"
        f"Brief: {article['description']}"
        for article in top_three_articles
    ]


    email_body = "\n\n".join(formatted_articles)


    # ---------------- EMAIL ---------------- #

    subject = (
        f"{STOCK_NAME} Stock Alert - "
        f"{percentage_difference:.2f}% move"
    )

    message = (
        f"Subject: {subject}\n\n"
        f"{STOCK_NAME} moved "
        f"{percentage_difference:.2f}% between the last two trading days.\n\n"
        f"{email_body}"
    )


    with smtplib.SMTP(
        "smtp.gmail.com",
        port=587
    ) as connection:

        connection.starttls()

        connection.login(
            user=FROM_EMAIL,
            password=EMAIL_PASSWORD
        )

        connection.sendmail(
            from_addr=FROM_EMAIL,
            to_addrs=TO_EMAIL,
            msg=message
        )


    print("Email sent successfully!")

else:
    print("Stock did not move more than 1%. No email sent.")
