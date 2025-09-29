import requests
import datetime
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCKS_API_KEY = "XIZJ9JTCZSSXX9IE"
NEWS_API_KEY = "b32b20f253c4445eace3640f56b62bd6"

TWILIO_SID = "OR189c7adc24c0c5fab317476410b1c4ca"

# Data for Tesla Stock
response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={STOCKS_API_KEY}")
data = response.json()

#Get yesterday's closing stock price

today_date = datetime.date.today()
today_date_string = str(today_date)

while today_date_string not in data["Time Series (Daily)"]:
    today_date -= datetime.timedelta(days=1)
    today_date_string = str(today_date)

# when exit while loop i have the valid time-data
yesterday_closing_price = data["Time Series (Daily)"][today_date_string]["4. close"] # aici avem toate datele care tin de ultima zi afisata din API (din Time Series (Daily) si ultima zi)
print("Ultima zi are pretul de inchidere = " + yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yesterday = today_date - datetime.timedelta(days=1)
day_after_yesterday_string = str(day_before_yesterday)
day_before_yesterday_closing_price = data["Time Series (Daily)"][day_after_yesterday_string]["4. close"]
print("Ziua de dinainte de ultima are pretul de inchidere = " + day_before_yesterday_closing_price)

#Find the positive difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
difference = round(difference, 2)
difference_abs = abs(difference)
print("Diferenta = " + str(difference))

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday

percentage = (difference_abs/float(day_before_yesterday_closing_price)) * 100

#If percentage is greater than 5

# if difference >= 0:
#     print(f"🔺{percentage}%")
#     if percentage > 1:
#         print("Get News")
# else:
#     print(f"🔻{percentage}%")
#     if percentage > 1:
#         print("Get News")

#use the News API to get articles related to the COMPANY_NAME.

if percentage > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    response_news = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response_news.json()["articles"]
    print(articles)


#create a list that contains the first 3 articles

three_articles = articles[:3]
print(three_articles)

#send a separate message with each article's title and description to your phone number.

#Create a new list of the first 3 articles

formated_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

#Send each article as a separate message via Twilio.

client = Client(TWILIO_SID)

for article in formated_articles:
    message = client.messages.create(
        body=article,
        from_="+15167306982",
        to="+40746253654"
    )