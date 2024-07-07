# InvestWise.py
Personal stock analyzer web app to identify the best investment in your watchlist.
Using Polygon.io API to collect stock data from previous close date.

<a href="http://3.84.164.56:5003/">Demo Link</a>

```
$ pip3 install polygon-api-client
```

https://polygon-api-client.readthedocs.io/en/latest/

##### Commands: 
```console
            python3 -m venv /polygon
            sudo pip3 install virtualenv
            source venv/bin/activate
            pip3 list     # List packages 
            pip3 install django # In venv and outside of venv
            django-admin --version
            pip3 install -r requirements.txt            
    (venv)  python manage.py migrate
    (venv)  python manage.py makemigrations
    (venv)  python3 manage.py runserver
```

To create a new migration file:
```
  python3 manage.py makemigrations --empty myapp --name myname
```
<br>

##### Screenshot
<p align="center">
  <img src="https://raw.githubusercontent.com/CarlaHeywood/PolyStockData/main/Screenshot.png" width="100%">
</p>

<br>

##### Terminal output at python manage.py
This takes several minutes
<p align="center">
  <img src="https://raw.githubusercontent.com/CarlaHeywood/PolyStockData/main/TerminalOutput.png" width="100%">
</p>

<!-- Inspiration -->
<!-- 
https://www.tradingview.com/widget/advanced-chart/
https://ui.aceternity.com/components/infinite-moving-cards
https://ui.aceternity.com/components/background-boxes

https://www.cnn.com/markets
https://nasdaq.com/
https://crypo-nextjs.netlify.app/
https://jiade.dexignlab.com/php/demo/coin-details.php
https://finlab-python-django-crypto-trading-ui-admin-dashboard-template.dexignlab.com/banking/
https://www.investopedia.com/stocks-4427785
 -->