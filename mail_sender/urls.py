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
    url(r'^froala_editor/', include('froala_editor.urls'))
]
