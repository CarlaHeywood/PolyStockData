from django.db import models
from django_mysql.models import ListCharField

# Create your models for the database here. Each class is a new table
# https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types

import sqlite3 as sql


def watchlist_from_db(): # works great check Dashboard
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT symbol FROM account_stock")
    results = cur.fetchall()
    watchlist = []
    count = 0 
    for record in results:
        watchlist.append(results[count][0])
        count += 1
    # print(watchlist)
    con.close()
    return watchlist

def get_stockdetails(symbol):
    # print("get_stockdetails: ", symbol)
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * FROM account_stock WHERE symbol = ?", (symbol,))
    result = cur.fetchone()
    # print("get_stockdetails result: \n ",result)
    con.close()
    if result == None:
        print("get_stockdetails:")
        print("Not Found in DB: ", symbol)
        return None
    else:
        print("get_stockdetails:")
        # print("Found in DB: \n", result)
        print("Found in DB")
        stock = Stock(symbol=result[1], 
                    closep=result[2], 
                    previous_date=result[3],
                    cash_amount=result[4], 
                    divfrequency=result[5], 
                    pay_date=result[6],
                    declaration_date=result[7],
                    ex_dividend_date=result[8],
                    stock_name=result[9],
                    stock_type=result[10],
                    weburl=result[11],
                    description=result[12],
                    brandicon=result[13],
                    brandlogo=result[14])
        return stock

class User (models.Model):
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    username = models.CharField(max_length=16)
    watchlist = models.TextField(default=['AAPL','UMWC','JEPI', 'PG','O'])

    def load_watchlist_from_db(watchlist):    
        con = sql.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("SELECT symbol FROM account_stock")
        results = cur.fetchall()
        count = 0 
        for record in results:
            watchlist.append(results[count][0])
            count += 1
        # print(watchlist)
        con.close()
        return watchlist

class Stock (models.Model):
    symbol = models.CharField(max_length=8)
    closep = models.CharField(max_length=10)
    previous_date = models.CharField(max_length=10)
    cash_amount = models.CharField(max_length=10)
    divfrequency = models.CharField(max_length=2)
    pay_date = models.CharField(max_length=10)
    declaration_date = models.CharField(max_length=10)
    ex_dividend_date = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=250)
    stock_type = models.CharField(max_length=250)
    weburl = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    brandicon = models.CharField(max_length=250)
    brandlogo = models.CharField(max_length=250)
    # dividendrate = models.FloatField()
    # dividendusd = models.FloatField()
    # low52 = models.FloatField()
    # high52 = models.FloatField()
    # buyitself = ((price) / (dividendusd) )*price
    # buy1k = models.FloatField()
    # numsharesbuy1k = 1000/dividendusd
    # rule72 = 72/dividendrate
    # oneyrate = models.FloatField()
    # fiveyrate = models.FloatField()
    # avgfiveyrate = fiveyrate/5
    # def __init__(self, symbol, closep, cash_amount, divfrequency, pay_date, declaration_date, ex_dividend_date):
    #     self.symbol = symbol
    #     self.closep = closep 
    #     self.cash_amount = cash_amount 
    #     self.divfrequency = divfrequency 
    #     self.pay_date = pay_date
    #     self.declaration_date = declaration_date
    #     self.ex_dividend_date = ex_dividend_date

    def __str__(self):
        overview = f'{self.symbol} : {self.closep} | D: {self.cash_amount} | F: {self.divfrequency} | PD: {self.pay_date} | ExD: {self.ex_dividend_date} | PD: {self.previous_date}'
        return overview