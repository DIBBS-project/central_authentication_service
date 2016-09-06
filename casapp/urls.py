from django.conf.urls import patterns, url

from casapp import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
    url(r'^authenticate/', views.authenticate, name="authenticate"),
)