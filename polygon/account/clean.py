#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stock analyzer using Python and polygon.io API
@author: Carla Heywood
"""

# pip install polygon-api-client

# import modules
import django
from polygon import *
import os, requests, json, datetime, time
from datetime import date, timedelta
import sqlite3 as sql

# api key from config
from apikey import polygonAPIkey, keystr

headers = {}      
params = {}

watchlist = ['AAPL','ADP','AIG','AVGO','BAC','BBY','CL','COST','ESS','GE','GS','HD','HPQ','IBM','INTC','JEPI','JNJ','JPM','KO','LOW','MCD','MMM','MSFT','NEE','NVDA','O','PEP','PG','QCOM','QYLD','SCHD','SPGI','SPY','SYY','TGT','UWMC','VFC','VOO','VTI','VZ','WFC','WMT','XOM']

print("*******************************")
print("*                             *")
print("*           Welcome!          *")
print("*                             *")
print("*******************************")

# API calls to access stock data
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

                    if r2.status_code == 403:
                        print("Not Authorized..")
                        time.sleep(5)

                    if r2.status_code == 429:
                        print("Please wait...")
                        time.sleep(15)

                    if r2.status_code == 200:
                        print("Dividends Complete!")
                        for stockd in dividends['results']: # Shows last 10 dividend payouts
                            symbol = stockd['ticker']
                            cash_amount = stockd['cash_amount']
                            divfrequency = stockd['frequency']
                            pay_date = stockd['pay_date']
                            declaration_date = stockd['declaration_date']
                            ex_dividend_date = stockd['ex_dividend_date']
                            print(str(symbol) + ": " + str(closep) + " | D: " + str(cash_amount) + " | F: " + str(divfrequency) + " | PD: " + str(pay_date) + " | ExD: " + str(ex_dividend_date))
    return r2.status_code

if load_stockdata():
    print("All Stock Data Loaded Successfully. Thank You!")
else:
    print("Not sure what happened here...")