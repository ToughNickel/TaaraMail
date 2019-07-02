from django.conf.urls import url
from django.urls import include

from mail_sender import views

app_name = 'mail_sender'
urlpatterns = [
    # The home view ('/mail_sender/')
    url(r'^$', views.home, name='home'),
    # Explicit home ('/mail_sender/home/')
    url(r'^home/$', views.home, name='home'),
    url(r'^gettoken/$', views.gettoken, name='gettoken'),
    url(r'^mail/$', views.mail, name='mail'),
    url(r'^send/$', views.send, name='send'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^customise/$', views.customise, name='customise'),
    url(r'^confirm_gen/', views.confirm_gen, name='confirm_gen'),
    url(r'^customise_vlz/$', views.customise_vlz, name='customise_vlz'),
    url(r'^confirm_vlz/', views.confirm_vlz, name='confirm_vlz')
]
