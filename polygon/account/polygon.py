#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Historical stock price data in python with polygon.io API
@author: Carla Heywood
"""

# pip install polygon-api-client

# import modules
from polygon import *
import pandas as pd
import os, requests, json, datetime, time
from datetime import date, timedelta

# api key from config
from apikey import polygonAPIkey, keystr
# OR just assign your API as a string variable
# polygonIkeAPy = 'polygonIkeAPy'

# headers = {'Authorization': '4US5e1obpxTqaWTTG6c6qGiHeK6O6TG3'}      
headers = {}      
params = {}

holidays = ["2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-03","2023-07-04","2023-09-04","2023-11-23","2023-11-24","2023-12-25","2024-01-01","2023-01-16","2023-02-20","2023-04-07","2023-05-29","2023-06-19","2023-07-03","2023-07-04","2023-09-04","2023-11-23","2023-11-24","2023-12-25","2024-01-01"]
watchlist = ['AAPL','ADP','AIG','AVGO','BAC','BBY','CL','COST','ESS','GE','GS','HD','HPQ','IBM','INTC','JEPI','JNJ','JPM','KO','LOW','MCD','MMM','MSFT','NEE','NVDA','O','PEP','PG','QCOM','QYLD','SCHD','SPGI','SPY','SYY','TGT','UWMC','VFC','VOO','VTI','VZ','WFC','WMT','XOM']
timeframe = date.today() - timedelta(days=1)# have to check for dates the market is open. -1 to make sure weekday() is in range also can only view previous days details 
# daynum = date.today().day # day of the month 
weekdayint = timeframe.weekday() # day of the week 
# print("Weekday Int:" + str(weekdayint))
# print(timeframe) 

def set_timeframe(timeframe):
    if weekdayint >= 5 :
        print("It's a weekend. Checking previous days...")
        if weekdayint == 5: # it's saturday
            timeframe = timeframe - timedelta(days=1)
            print("Saturday - 1 day: " + str(timeframe))
            return(timeframe) 
        else:  # it's sunday
            timeframe = timeframe - timedelta(days=2)
            print("Sunday - 2 days: " + str(timeframe))
            return(timeframe)
    else: 
        if weekdayint < 5 and timeframe in holidays: # It is a weekday / Check for a holiday
            print("Happy Holiday! Checking previous days...")
            timeframe = timeframe - timedelta(days=1)
            set_timeframe(timeframe) 

        if weekdayint < 5:
            print("Today: "  + str(date.today()))
            # print(str(timeframe)) 
            return(timeframe) # Using yesterday's numbers for free

# https://stackoverflow.com/questions/42037593/third-party-api-integration-in-python-django
# def load_polygondata ():

with requests.Session() as s:
    print("******** Welcome Home! ********")
    for ticker in watchlist:
        # 
        # DETAILS V3
        # 
        print("StockDetailsV3 Loading... // ", ticker)
        url4 = str("https://api.polygon.io/v3/reference/tickers/" + str(ticker) + "?apiKey=" + polygonAPIkey)
        r4 = s.get(url4, headers=headers, params=params)
        # print("Stock Details V3: Code " + str(r3.status_code))
        # print(stock['T'] + " : loading...")
        stockdetailsv3 = json.loads(r4.content)

        if r4.status_code == 403:
            print("Not Authorized..")
            time.sleep(5)

        if r4.status_code == 429:
            print("Please wait...")
            time.sleep(15)

        if r4.status_code == 200:
            if stockdetailsv3['results']['branding']:
                brandicon = stockdetailsv3['results']['branding']['icon_url'] + keystr
                brandlogo = stockdetailsv3['results']['branding']['logo_url'] + keystr
            else:
                brandicon = stockdetailsv3['results']['branding']['icon_url'] + keystr
                brandlogo = stockdetailsv3['results']['branding']['logo_url'] + keystr

            description = stockdetailsv3['results']['description']
            # print("description: " + description)
            print("StockDetailsV3 Complete!")

            # 
            # PREVIOUS CLOSE 
            # 
            print("PreviousClose Loading...")
            url3 = str("https://api.polygon.io/v2/aggs/ticker/" + str(ticker) + "/prev?adjusted=true&apiKey=" + polygonAPIkey)
            r3 = s.get(url3, headers=headers, params=params)
            # print("Previous Close (OHLC): Code " + str(r3.status_code))
            # print(stock['T'] + " : loading...")
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
                        # con = sql.connect("db.sqlite3")
                        # cur = con.cursor()
                        # cur.execute("SELECT symbol FROM account_stock WHERE previous_date = ?", (previous_date,))
                        # expired_stocks = cur.fetchall()
                        
                        # if expired_stocks == []:
                        #     print("All info is up to date.")
                        #     print(expired_stocks)
                        #     con.close()
                        #     return home(request)
                        #     time.sleep(5)
                        #     break

                        # else:
                        #     print("Need to update expired stocks...Proceeding")
                        #     print(expired_stocks[0][0])
                    closep = price['c']
                    # closep = previousclose['results']['c']
                    print("PreviousClose Complete!")

                    # time.sleep(12) # 5 reqests per minute for free

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
                        # print("Made it")
                        # dividends = json.loads(r2.content)
                        for stockd in dividends['results']: # Shows last 10 dividend payouts
                            symbol = stockd['ticker']
                            # closep = stock['c']
                            cash_amount = stockd['cash_amount']
                            divfrequency = stockd['frequency']
                            pay_date = stockd['pay_date']
                            declaration_date = stockd['declaration_date']
                            ex_dividend_date = stockd['ex_dividend_date']
                            # print(str(symbol) + ": " + str(closep) + " | D: " + str(cash_amount) + " | F: " + str(divfrequency) + " | PD: " + str(pay_date) + " | ExD: " + str(ex_dividend_date))
    print("Complete!")
            # else:
            #     continue