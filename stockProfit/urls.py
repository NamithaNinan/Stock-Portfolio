from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^update/', views.update),
    url(r'^delete/', views.delete),  
    url(r'^chart$', views.home), 
    #url(r'^charts$', views.historyData), 
    url(r'^chartit$', views.weather_chart_view),
]
