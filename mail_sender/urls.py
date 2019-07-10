from django.conf.urls import url
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
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
    url(r'^confirm_vlz/', views.confirm_vlz, name='confirm_vlz'),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r"^upload_image$", views.upload_image, name="upload_image"),
    url(r"^upload_image_validation", views.upload_image_validation, name="upload_image_validation"),
]
'''+ static(settings.STATIC_URL, document_root=settings.STATIC_DIR) + static(settings.STATIC_PUBLIC_URL, document_root=settings.STATIC_PUBLIC_DIR)'''
