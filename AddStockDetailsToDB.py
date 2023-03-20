#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stock analyzer using Python and polygon.io API

Read the data and output to terminal.
Data stored in sqlite3 database.  

@author: Carla Heywood
"""

# pip install polygon-api-client

# import modules
from polygon import *
import os, requests, json, datetime, time
from datetime import date, timedelta

# Database modules
from django.conf import settings
from django.db import models
from django.core.management import call_command
from django_mysql.models import ListCharField

# API key from config
from apikey import polygonAPIkey, keystr


# Set up Django settings
settings.configure(
    INSTALLED_APPS=[
        'AddStockDetailsToDB',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'Stocks.sqlite3'),
        },
    },
    SECRET_KEY='secret_key',
)

headers = {}      
params = {}

holidays = ["2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-03","2023-07-04","2023-09-04","2023-11-23","2023-11-24","2023-12-25","2024-01-01","2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-03","2023-07-04","2023-09-04","2023-11-23","2023-11-24","2023-12-25","2024-01-01"]
watchlist = ['AAPL','ADP','AIG','AVGO','BAC','BBY','CL','COST','ESS','GE','GS','HD','HPQ','IBM','INTC','JEPI','JNJ','JPM','KO','LOW','MCD','MMM','MSFT','NEE','NVDA','O','PEP','PG','QCOM','QYLD','SCHD','SPGI','SPY','SYY','TGT','UWMC','VFC','VOO','VTI','VZ','WFC','WMT','XOM']

# Database Model
class Stock (models.Model):
    symbol = models.CharField(max_length=8)
    description = models.CharField(max_length=1000)
    brandicon = models.CharField(max_length=250)
    brandlogo = models.CharField(max_length=250)
    closep = models.CharField(max_length=10)
    previous_date = models.CharField(max_length=10)
    cash_amount = models.CharField(max_length=10)
    divfrequency = models.CharField(max_length=2)
    pay_date = models.CharField(max_length=10)
    declaration_date = models.CharField(max_length=10)
    ex_dividend_date = models.CharField(max_length=10)
    
    def __str__(self):
        overview = f'{self.symbol} : {self.closep} | D: {self.cash_amount} | F: {self.divfrequency} | PD: {self.pay_date} | ExD: {self.ex_dividend_date} | PD: {self.previous_date}'
        return overview

# Create database tables
call_command('makemigrations')
call_command('migrate')

# https://stackoverflow.com/questions/42037593/third-party-api-integration-in-python-django

print("*******************************")
print("*                             *")
print("*        Welcome Home!        *")
print("*                             *")
print("*******************************")

def load_stockdata():
    with requests.Session() as s:
        for ticker in watchlist:
            # 
            # STOCK DETAILS V3
            # 
            print("StockDetailsV3 Loading... // ", ticker)
            url4 = str("https://api.polygon.io/v3/reference/tickers/" + str(ticker) + "?apiKey=" + polygonAPIkey)
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
                brandicon = stockdetailsv3['results']['branding']['icon_url'] + keystr
                brandlogo = stockdetailsv3['results']['branding']['logo_url'] + keystr
                description = stockdetailsv3['results']['description']
                print("StockDetailsV3 Complete!")

                # 
                # PREVIOUS CLOSE 
                # 
                print("PreviousClose Loading...")
                url3 = str("https://api.polygon.io/v2/aggs/ticker/" + str(ticker) + "/prev?adjusted=true&apiKey=" + polygonAPIkey)
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
                        previous_date = datetime.datetime.fromtimestamp(price['t']/1000).date()
                        closep = price['c']
                        print("PreviousClose Complete!")

                    # 
                    # DIVIDENDS 
                    # 
                    print("Dividends Loading...")
                    url2 = str("https://api.polygon.io/v3/reference/dividends?ticker=" + str(ticker) + "&limit=1&apiKey=" + polygonAPIkey)
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
                            # symbol = stockd['ticker']
                            # cash_amount = stockd['cash_amount']
                            # divfrequency = stockd['frequency']
                            # pay_date = stockd['pay_date']
                            # declaration_date = stockd['declaration_date']
                            # ex_dividend_date = stockd['ex_dividend_date']
                            # print(str(symbol) + ": " + str(closep) + " | D: " + str(cash_amount) + " | F: " + str(divfrequency) + " | PD: " + str(pay_date) + " | ExD: " + str(ex_dividend_date))
                            stock = Stock(symbol=stockd['ticker'], 
                                            description=description, 
                                            brandicon=brandicon, 
                                            brandlogo=brandlogo, 
                                            closep=closep, 
                                            cash_amount=stockd['cash_amount'], 
                                            previous_date=previous_date,
                                            divfrequency=stockd['frequency'], 
                                            pay_date=stockd['pay_date'],
                                            declaration_date=stockd['declaration_date'],
                                            ex_dividend_date=stockd['ex_dividend_date'])
                            print(stock)
    return r2.status_code

if load_stockdata():
    print("All Stock Data Loaded Successfully. Thank You!")
else:
    print("Not sure what happened here.....")