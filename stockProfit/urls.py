from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^update/', views.update),
    url(r'^delete/', views.delete),  
    url(r'^charts$', views.displayCurrVal), 
    url(r'^historyData$', views.historyData), 
   	url(r'^test$', views.displayCurrVal),
   	url(r'^ethical$', views.ethicalStrategy),
   	url(r'^growth$', views.growthStrategy),
   	url(r'^indexInvesting$', views.indexStrategy),
   	url(r'^quality$', views.qualityStrategy),
   	url(r'^value$', views.valueStrategy),
   	url(r'^livePortFolio$', views.livePortFolio),
]
