import requests
from twilio.rest import Client
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alphavantage_key = "JU1R5UV853KCN5ZE"
alphavantage_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": alphavantage_key,
}
# Finding the data from the day before and the day before that
# Need to make sure we only find week days as stock market is closed on weekends
x = 1
one_day_ago = dt.datetime.now()-dt.timedelta(x)
if one_day_ago.weekday() == 6:
    x = 3
    one_day_ago = dt.datetime.now()-dt.timedelta(x)
elif one_day_ago.weekday() == 5:
    x = 2
    one_day_ago = dt.datetime.now() - dt.timedelta(x)
two_days_ago = dt.datetime.now()-dt.timedelta(x+1)
if two_days_ago.weekday() == 6:
    two_days_ago = one_day_ago-dt.timedelta(3)
temp = str(one_day_ago.day)
if one_day_ago.day < 10:
    temp = "0" + temp
one_day_ago = str(one_day_ago.year) + "-" + str(one_day_ago.month) + "-" + temp
temp = str(two_days_ago.day)
if two_days_ago.day < 10:
    temp = "0" + temp
two_days_ago = str(two_days_ago.year) + "-" + str(two_days_ago.month) + "-" + temp


alphavantage_Endpoint = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(alphavantage_Endpoint, params=alphavantage_params)
data = response.json()
one_day_ago_data = data["Time Series (Daily)"][one_day_ago]["4. close"]
two_days_ago_data = data["Time Series (Daily)"][two_days_ago]["4. close"]
difference = float(one_day_ago_data) - float(two_days_ago_data)
difference = (difference / float(two_days_ago_data)) * 100

# If the value change is greater than 5%
if abs(difference) >= 5:
    news_key = "6f43485da225467dab60877f691f7ed3"
    news_params = {
        "apiKey": news_key,
        "q": "Tesla",
        "language": "en",
        "pageSize": 3,
    }
    news_Endpoint = "https://newsapi.org/v2/everything?"
    response = requests.get(news_Endpoint, params=news_params)
    news_data = response.json()


    # Send a seperate message with the percentage change and each article's title and description to your phone number.

    auth_token = "b6c4853914709f5b5f63d99231e8c538"
    account_sid = "ACb7e90c6ccd256cb7392f753d439dac20"
    client = Client(account_sid, auth_token)
    if difference < 0:
        symb = "🔻"
    else:
        symb = "🔺"
    for x in range(0, 3):
        message = client.messages.create(
            from_='+18559260376',
            body=f"TSLA: {symb}{abs(difference)}%\n"
                 f"Headline: {news_data['articles'][x]['title']}\n"
                 f"Brief: {news_data['articles'][x]['description']}",
            to="+16337693359"
        )
        print(message.sid)

