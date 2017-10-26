from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import homeadmin,create_stuff_user, simple,simple2, complex, landing,illness,register,user_login,whyus,about,contact,our_team,our_team,how_it_works,orderdrugs,labtests,addcontact,payconsult
from django.conf.urls import include


urlpatterns = [
    url(r'^$', landing),
    url(r'^login/$', user_login),
    url(r'^register/$', register),
    url(r'^illness/$', illness),

    url(r'^$', landing),
    url(r'^simple/(?P<id>\d+)$', simple),

    url(r'^simple2/(?P<id>\d+)$', simple2),
   
    
    url(r'^complex/(?P<id>\d+)$', complex),
    url(r'^chat/', include('chat.urls')),

    url(r'^index_admin/$', homeadmin),
    url(r'^admin/', admin.site.urls),
    url(r'^addstuff/',create_stuff_user),
    url(r'^dashboard/', include('dash.urls')),

    url(r'^whyus/$', whyus),
    url(r'^about/$', about),
    url(r'^contact/$', contact),
    url(r'^how_it_works/$', how_it_works),
    url(r'^team/$', our_team),
    url(r'^orderdrugs/$', orderdrugs),
    url(r'^labtests/$', labtests),
    url(r'^addcontact/$', addcontact),
    
    url(r'^payconsult/$', payconsult)



]
