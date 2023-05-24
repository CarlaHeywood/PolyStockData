"""
Create your views for handling HTTP Requests also anything where the html will directly interact with

- 1/22 working on load_stockdata. creating a record and django object. 
ERROR: Internal Server Error: AttributeError: 'NoneType' object has no attribute 'attname'
FIXED IT!! THe stock data is storing in the database properly now.
- I was able to add a couple pages and organize the Models and Views files but not the 
original function to call Polygon API has not worked since 5pm today. It's now 10pm. Not sure how it broke

"""
import os, requests, json, datetime, time, random
from datetime import datetime, date, timedelta

# import sqlite3 as sql

from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
from polygon import *
from .models import *

import subprocess



# api key from config 
# from apikey import *
# OR just assign your API as a string variable
polygonAPIkey = os.getenv('polygonAPIkey')

keystr = os.getenv('keystr')


# ImproperlyConfigured( django.core.exceptions.ImproperlyConfigured: Requested setting USE_I18N
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'account.settings')

# import modules

headers = {}     
params = {}

holidays = ["2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-03","2023-07-04","2023-09-04","2023-11-23","2023-11-24","2023-12-25","2024-01-01","2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-03","2023-07-04","2023-09-04","2023-11-23","2023-11-24","2023-12-25","2024-01-01"]
watchlist = ['AAPL','ADP','AIG','AVGO','BAC','BBY','CL','COST','ESS','GE','GS',
                 'HD','HPQ','IBM','INTC','JEPI','JNJ','JPM','KO','LOW','MCD','MMM','MSFT',
                 'NEE','NVDA','O','PEP','PG','QCOM','QYLD','SCHD','SPGI','SPY','SYY','TGT',
                 'UWMC','VFC','VOO','VTI','VZ','WFC','WMT','XOM']

# ------- START Render Templates to Pages --------    
def home(request):
    """
        Render Home page
    """
    # print("Home")
    data = get_allstocks_db()
    stocks = random.sample(sorted(data, key=lambda x: x.symbol), 3)
    # print(stocks)
    return render(request, 'home.html', {'stocks':stocks , 'current_year':datetime.now().year})

def dashboard(request):
    """
        Render Dashboard page
    """
    # print("Dashboard")
    data = get_allstocks_db()
    if data == '':
        print("No Data Found in Database.")
        data = ['AAPL','UMWC','JEPI', 'PG','O']
    # print(data)
    return render(request, 'dashboard.html', {'watchlist':data , 'current_year':datetime.now().year})

def profile(request):
    """
        Render Profile page
    """
    users = User()
    # print("Profile")
    return render(request, 'profile.html', {'users':users , 'current_year':datetime.now().year})

# def stockdetails(request, symbol=None):
#     """
#         Render stockdetails page for given stock symbol. 
#         If not found, shows what symbol it was looking for
#     """
#     if request.method == 'POST':
#         symbol = request.POST.get('searchsymbol', symbol)
#         print("Search Symbol: ", symbol)
#     if symbol:
#         if symbol in watchlist_from_db():
#             print("stockdetails: Found - ",symbol)
#             return render(request, 'stockdetails.html', {'stock': get_stockdetails_db(symbol)})
#         else:
#             print("stockdetails: Not Found - ", symbol)
#             return home(request)
#     else:
#         print("stockdetails: No Symbol")
#         return home(request)


def stockdetails(request,symbol):
    """
        Render individual Stock page
    """
    print("Loading stockdetails...")
    print(symbol)

    if request.method == 'POST': # SEARCH
        symbol = request.POST.get('searchsymbol', symbol)
        print("SEARCH: ", symbol)
    
    return render(request, 'stockdetails.html', {'stock': get_stockdetails_db(symbol), 'current_year':datetime.now().year})

# ------- END Render Templates to Pages ---------


# ------- START Pologon API calls ---------

# https://stackoverflow.com/questions/42037593/third-party-api-integration-in-python-django
def loadpolygondata(request):
    """
        Creates new Database records by calling polygon API.
        Need to check for duplicates to simply update existing records.
    """
    print("Fetching Polygon stock data....")

    Stock.objects.all().delete()

    with requests.Session() as s:
        for ticker in watchlist:
            # stock = Stock(symbol=ticker)
            # 
            # STOCK DETAILS V3 
            # 
            print("StockDetailsV3 Loading... // ", ticker)
            url4 = str("https://api.polygon.io/v3/reference/tickers/" + 
                       str(ticker) + "?apiKey=" + polygonAPIkey)
            r4 = s.get(url4, headers=headers, params=params)
            # print("Stock Details V3: Code " + str(r3.status_code))
            stockdetailsv3 = json.loads(r4.content)

            if r4.status_code == 403:
                print("Not Authorized..")
                time.sleep(5)

            if r4.status_code == 429:
                print("Please wait...")
                time.sleep(15)

            if r4.status_code == 200:
                stock_type = stockdetailsv3['results']['type']
                stock_name = stockdetailsv3['results']['name']

                if 'branding' in stockdetailsv3['results']:
                    if 'icon_url' in stockdetailsv3['results']['branding']:
                        brandicon = stockdetailsv3['results']['branding']['icon_url'] + keystr
                    if 'logo_url' in stockdetailsv3['results']['branding']:
                        brandlogo = stockdetailsv3['results']['branding']['logo_url'] + keystr
                else:
                    brandicon = "No Icon Available"
                    brandlogo = "No Logo Available"

                if 'homepage_url' in stockdetailsv3['results']:
                    weburl = stockdetailsv3['results']['homepage_url']
                else: 
                    weburl = "#"

                if 'description' in stockdetailsv3['results']:
                    description = stockdetailsv3['results']['description']
                else: 
                    description = "No Description "

                # description = stockdetailsv3['results']['description']
                print("StockDetailsV3 Complete!")

                # 
                # PREVIOUS CLOSE
                # 
                print("PreviousClose Loading...")
                url3 = str("https://api.polygon.io/v2/aggs/ticker/" + str(ticker) + 
                           "/prev?adjusted=true&apiKey=" + polygonAPIkey)
                r3 = s.get(url3, headers=headers, params=params)
                # print("Previous Close (OHLC): Code " + str(r3.status_code))
                previousclose = json.loads(r3.content)

                if r3.status_code == 403:
                    print("Not Authorized..")
                    time.sleep(5)

                if r3.status_code == 429:
                    print("Please wait...")
                    time.sleep(15)

                if r3.status_code == 200:
                    for price in previousclose['results']:
                        # print(price)
                        previous_date = datetime.fromtimestamp(price['t']/1000).date()
                        closep = price['c']
                        print("PreviousClose Complete!")

                    # 
                    # DIVIDENDS
                    # 
                    print("Dividends Loading...")
                    url2 = str("https://api.polygon.io/v3/reference/dividends?ticker=" + 
                               str(ticker) + "&limit=1&apiKey=" + polygonAPIkey)
                    r2 = s.get(url2, headers=headers, params=params)
                    dividends = json.loads(r2.content)
                    # print("Dividends Info: Code " + str(r2.status_code))
                    time.sleep(12) # 5 reqests per minute for free
                    # print(dividends)
                    if r2.status_code == 403:
                        print("Not Authorized..")
                        time.sleep(5)

                    if r2.status_code == 429:
                        print("Please wait...")
                        time.sleep(15)

                    if r2.status_code == 200:
                        print("Dividends Complete!")
                        for stockd in dividends['results']: # Shows last 10 dividend payouts
                            stock = Stock(symbol = stockd['ticker'],
                                                stock_name = stockdetailsv3['results']['name'],
                                                stock_type = stockdetailsv3['results']['type'],
                                                weburl = weburl,
                                                closep = closep,
                                                previous_date = previous_date,
                                                brandicon = brandicon,
                                                brandlogo = brandlogo,
                                                description = description,
                                                cash_amount = stockd['cash_amount'],
                                                divfrequency = stockd['frequency'],
                                                pay_date = stockd['pay_date'],
                                                declaration_date = stockd['declaration_date'],
                                                ex_dividend_date = stockd['ex_dividend_date'])
                            # print(str(symbol) + ": " + str(closep) + " |
                            # D: " + str(cash_amount) + " | F: " + str(divfrequency) +
                            # " | PD: " + str(pay_date) + " | ExD: " + str(ex_dividend_date))
                            print(stock)
        print("Complete!")
        return render(request, 'home.html',{'current_year':datetime.now().year})

def fetch_ALL_polystockdata(request):
    """
        Update database by deleting all records then 
        fetch updated stock details from Polygon API

        Delete all then Create new records 
    """
    Stock.objects.all().delete()



# ------- END Pologon API calls ---------
