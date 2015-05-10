from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/*', views.login_user, name='login'),
    url(r'^logout/*', views.logout_user, name='logout'),
    url(r'^upload/*', views.upload_tournament, name='upload_tournament'),
    url(r'^$', views.index, name='index'),
]