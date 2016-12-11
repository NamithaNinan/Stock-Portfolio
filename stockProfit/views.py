from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from models import Employees
from models import StockValues
from django.template import RequestContext
from models import Post
import datetime
import requests
from requests.auth import HTTPDigestAuth
import json
import time
import quandl
from chartit import DataPool, Chart
from models import MonthlyWeather


def index(request):
    if request.method == 'POST':
       # save new post
       title = request.POST['title']
       content = request.POST['content']

       post = Post(title=title)
       post.last_update = datetime.datetime.now() 
       post.content = content
       post.save()

    # Get all posts from DB
    posts = Post.objects
    context = {'Posts': posts}
    return render(request, 'stockProfit/index.html', context)


def update(request):
    id = eval("request." + request.method + "['id']")
    post = Post.objects(id=id)[0]
    
    if request.method == 'POST':
        # update field values and save to mongo
        post.title = request.POST['title']
        post.last_update = datetime.datetime.now() 
        post.content = request.POST['content']
        post.save()
        template = 'stockProfit/index.html'
        params = {'Posts': Post.objects} 

    elif request.method == 'GET':
        template = 'stockProfit/update.html'
        params = {'post':post}
   
    return render(request, template, params)
                              

def delete(request):
    id = eval("request." + request.method + "['id']")

    if request.method == 'POST':
        post = Post.objects(id=id)[0]
        post.delete() 
        template = 'stockProfit/index.html'
        params = {'Posts': Post.objects} 
    elif request.method == 'GET':
        template = 'stockProfit/delete.html'
        params = { 'id': id } 

    return render(request, template, params)

    return render(request, "stockProfit/home.html")

def home(request):
    return render(request, "stockProfit/home.html")

def chart(request):
    company = ['GOOG', 'AAPL', 'YHOO']
    
    for i in range(len(company)):
        stockValues = StockValues(company[i])

        url = "https://www.quandl.com/api/v3/datasets/WIKI/"+company[i]+".json?api_key=Qj3hVb4abNZYbdEFxp27"
        myResponse=requests.get(url)
        if(myResponse.ok):
            jData = json.loads(myResponse.content)
            stock_price = jData["dataset"]["data"][0][1]
            value_change = jData["dataset"]["data"][0][4]-jData["dataset"]["data"][0][1]
            percentage_change=(value_change/stock_price)*100
            name = jData["dataset"]["name"]
            print "Current date and time is "+time.strftime("%c")+time.strftime(" %Z")
            print "Company name is "+name
            print "Company stock price is ",stock_price
            print "Value change is ",value_change
            print "Percentage change  is ",percentage_change,"%"
            stockValues.name=name
            stockValues.price = stock_price
            stockValues.valuechange = value_change

            stockValues.save()
   
    return render(request, "stockProfit/charts.html") 

    

def historyData (request):


    symList  = ["GOOG", "AAPL", "JCI", "ADBE", "NVDA",
                "QCOM", "CI", "TWX", "TMUS", "EXPE",
                "CTSH", "KORS", "DKS", "NVDA", "TSLA",
                "COST", "AMZN", "NFLX", "XOM", "FB",
                "GIS", "INTC", "CSCO", "WMT", "BA"]

    for j in range(len(symList)):
        company = symList[j]
        for i in range(5):
            stockValues = StockValues(company)

            url = "https://www.quandl.com/api/v3/datasets/WIKI/"+company+".json?api_key=Qj3hVb4abNZYbdEFxp27";
            myResponse=requests.get(url)
            if(myResponse.ok):
                jData = json.loads(myResponse.content)
                date = jData["dataset"]["data"][i][0]
                stock_price = jData["dataset"]["data"][i][1]

                stockValues.date = date;
                stockValues.name=jData["dataset"]["name"]
                #stockValues.symbol = company
                stockValues.price = stock_price
                #stockValues.valuechange = value_change
                stockValues.save()
   
    return render(request, "stockProfit/charts.html")


# This is for chartit tutorial. Add all other proj code above this

def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': MonthlyWeather.objects.all()},
              'terms': [
                'month',
                'temp']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
        datasource = weatherdata,
        series_options =
            [{'options':{
                'type': 'line',
                'stacking': False},
            'terms':{
                'month': 'temp'
                }}],
        chart_options =
            {'title': {
                'text': 'Weather Data of City'},
            'xAxis': {
                'title': {
                    'text': 'Month Name'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response({'weatherchart': cht})