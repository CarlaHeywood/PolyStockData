# backend/models.py
import json
import sqlite3 as sql
from django.db import models
from django_mysql.models import ListCharField

# Create your models for the database here. Each class is a new table
# https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types

def watchlist_from_db():
    """
        Retrieves all ticker/stock symbols found in DB
        Returns Watchlist: type array
    """
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT symbol FROM backend_stock")
    results = cur.fetchall()
    watchlist = []
    count = 0
    for record in results:
        watchlist.append(results[count][0])
        count += 1
    # print(watchlist)
    con.close()
    return watchlist

def add_stock_db(stock):
    """
       Create new record for individual stock 
    """
    stock = Stock.objects.create(symbol = stock.symbol,
        stock_name = stock.stock_name,
        stock_type = stock.stock_type,
        weburl = stock.weburl,
        closep = stock.closep,
        previous_date = stock.previous_date,
        brandicon = stock.brandicon,
        brandlogo = stock.brandlogo,
        description = stock.description,
        cash_amount = stock.cash_amount,
        divfrequency = stock.divfrequency,
        pay_date = stock.pay_date,
        declaration_date = stock.declaration_date,
        ex_dividend_date = stock.ex_dividend_date)
    
    # print(stock.symbol, "New Stock Added to DB Successfully!")
    return stock

def get_allstocks_db():
    """
        Returns all stock objects with all details found in DB
    """
    return Stock.objects.all()

def get_stockdetails_db(symbol):
    """
        Search DB for stockdetails.
        If not found, show the stock symbol it was looking for 
        Return Stock: type Object
    """
    # print(symbol,": Searching Database...")
    # print("get_stockdetails: ", symbol)

    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * FROM backend_stock WHERE symbol = ?", (symbol,))
    result = cur.fetchone()
    # print("get_stockdetails result: \n ",result)
    con.close()

    if result is None:
        print("NOT Found in DB: ", symbol)
        return None

    # print("Found in DB: \n", result)
    # print("Found in DB")
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
    """
        User object for user accounts
    """
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    username = models.CharField(max_length=16)
    watchlist = models.TextField(default=['AAPL','UMWC','JEPI', 'PG','O'])

    def load_watchlist_from_db(self, watchlist):
        """ 
            Load watchlist from DB for User
        """
        con = sql.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("SELECT symbol FROM backend_stock")
        results = cur.fetchall()
        count = 0
        for record in results:
            watchlist.append(results[count][0])
            count += 1
        # print(watchlist)
        con.close()
        return watchlist

class Stock (models.Model):
    """
        Stock object for database 
    """
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
    # related_companies = models.ManyToManyField(
        # 'self.symbol', symmetrical=False, blank=True)
    related_tickers = models.TextField(
        default=['AAPL', 'UMWC', 'JEPI', 'PG', 'O'])

    def __str__(self):
        overview = f'{self.symbol} : {self.closep} | D: {self.cash_amount} | F: {self.divfrequency} | PD: {self.pay_date} | ExD: {self.ex_dividend_date} | PD: {self.previous_date}'
        return overview

