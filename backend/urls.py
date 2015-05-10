from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/*', views.login_user, name='login'),
    url(r'^logout/*', views.logout_user, name='logout'),
    url(r'^upload/*', views.upload_tournament, name='upload_tournament'),
    url(r'^view_player/(?P<pop_id>[0-9]+)/*', views.view_player, name='view_player'),
    url(r'^$', views.index, name='index'),
]