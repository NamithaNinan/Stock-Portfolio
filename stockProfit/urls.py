from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^update/', views.update),
    url(r'^delete/', views.delete),  
    url(r'^charts$', views.queryDB), 
    url(r'^historyData$', views.historyData), 
   	url(r'^test$', views.queryDB),
   	url(r'^ethical$', views.ethicalStrategy),
]
