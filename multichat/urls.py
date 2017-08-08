from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import homeadmin,create_stuff_user, simple, complex, landing,illness,register,user_login
from django.conf.urls import include


urlpatterns = [
    url(r'^$', landing),
    url(r'^login/$', user_login),
    url(r'^register/$', register),
    url(r'^illness/$', illness),

    url(r'^$', landing),
    url(r'^simple/(?P<id>\d+)$', simple),
   
    
    url(r'^complex/(?P<id>\d)$', complex),
    url(r'^chat/', include('chat.urls')),

    url(r'^index_admin/$', homeadmin),
    url(r'^admin/', admin.site.urls),
    url(r'^addstuff/',create_stuff_user),





]
