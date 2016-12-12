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
            db = client.cmpe285_StockEngine
            collection = db.live_data_value

            #date = now.strftime("%Y-%m-%d %H:%M:%S")
            date = datetime.datetime.now()
            # Create the document to add
            data = {"symbol": company, "date": date, "price": curr_stock_price}

            # Add the document
            objId = collection.insert_one(data).inserted_id

        except Exception, exc:
            print "Exc: " + str(exc)
            print "Incorrect symbol entered. Quitting"
            looping = 0
    else :
        print "Not connected to internet."

# ethical GOOG AAPL JCI ADBE NVDA
# Value QCOM CI TWX TMUS EXPE
# Growth CTSH KORS DKS NVDA TSLA
# Index: COST AMZN NFLX OM FB
# Quality: GIS INTC CSCO WMT BA

symList  = ["GOOG", "AAPL", "JCI", "ADBE", "NVDA",
            "QCOM", "CI", "TWX", "TMUS", "EXPE",
            "CTSH", "KORS", "DKS", "NKE", "TSLA",
            "COST", "AMZN", "NFLX", "XOM", "FB",
            "GIS", "INTC", "CSCO", "WMT", "BA"]

startTime = time.time() 
for t in range(10):
    stop = 0
    for i in range(len(symList)):

        sym = symList[i] 
        print "Running the function now for " + sym
        storeLiveData(sym)
        currTime = time.time()
        if currTime > startTime + 55:
            stop = 1
            break
    if stop == 1:
        break

