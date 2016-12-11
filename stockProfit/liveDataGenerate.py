import requests
import pymongo
import time
import datetime
import json
from requests.auth import HTTPDigestAuth
from pymongo import MongoClient
from googlefinance import getQuotes
import socket
from array import *


def internet(host="8.8.8.8", port=53, timeout=3):

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False


def storeLiveData (symbol):

    company = symbol

    if(internet()):
        
        try:
            now = datetime.datetime.now()
            data = getQuotes(company)
            #open_stock_price = float(data[0]['PreviousClosePrice'])
            curr_stock_price = float(data[0]['LastTradeWithCurrency'])

            client = MongoClient()
            db = client.testLiveData
            collection = db.testLiveTable

            date = now.strftime("%Y-%m-%d %H:%M:%S")
            # Create the document to add
            data = {"symbol": company, "date": date, "price": curr_stock_price}

            # Add the document
            objId = collection.insert_one(data).inserted_id


            #value_change = curr_stock_price - open_stock_price
            #perc_change = value_change / open_stock_price
            #print "Output:"
            #print "========"
            #print now.strftime("%Y-%m-%d %H:%M")
            #var = "Stock Price: %.3f" % curr_stock_price
            #print var
            #var = "Value Change: %.3f" % value_change
            #print var
            #var = "Percentage Change: %.3f%%" % perc_change
            #print var
            #print ""
        except Exception, exc:
            print "Exc: " + str(exc)
            print "Incorrect symbol entered. Quitting"
            looping = 0
    else :
        print "Not connected to internet."

# ethical GOOG AAPL JCI ADBE PBW
# Value QCOM CI TWX TMUS EXPE
# Growth CTSH KORS DKS NVDA TSLA
# Index: COST AMZN NFLX OM FB
# Quality: GIS INTC CSCO WMT BA

symList  = ["GOOG", "AAPL", "JCI", "ADBE", "PBW",
            "QCOM", "CI", "TWX", "TMUS", "EXPE",
            "CTSH", "KORS", "DKS", "NVDA", "TSLA",
            "COST", "AMZN", "NFLX", "XOM", "FB",
            "GIS", "INTC", "CSCO", "WMT", "BA"]

for i in range(len(symList)):

    sym = symList[i] 
    print "Running the function now for " + sym
    storeLiveData(sym)
