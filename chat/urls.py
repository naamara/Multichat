from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import homeadmin,create_stuff_user,landing,illness,register,user_login
from django.conf.urls import include
from chat.views import test, send, receive, sync, join, leave


urlpatterns = [
  
    url(r'^$', test),
    url(r'^send/$', send),
    url(r'^receive/$', receive),
    url(r'^sync/$', sync),

    url(r'^join/$', join),
    url(r'^leave/$', leave),





]