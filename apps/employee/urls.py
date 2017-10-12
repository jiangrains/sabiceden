from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^account/signin$', views.signin, name = 'signin'),
    url(r'^account/exit$', views.exit, name = 'exit'),
    url(r'^account/checktoken$', views.checktoken, name = 'checktoken'),
]