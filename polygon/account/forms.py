from django.shortcuts import render
from django.forms import *
from .models import *

from polygon import *
import pandas as pd
import os, requests, json, datetime, time
from datetime import datetime, date, timedelta
import sqlite3 as sql


class SearchForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol']

 