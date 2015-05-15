from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/?', views.login_user, name='login'),
    url(r'^logout/?', views.logout_user, name='logout'),
    url(r'^change_password/?', views.change_password, name='change_password'),
    url(r'^upload/?', views.upload_tournament, name='upload_tournament'),
    url(r'^choose_avatar/?', views.choose_avatar, name='choose_avatar'),
    url(r'^view_player/(?P<pop_id>[0-9]+)/?', views.view_player, name='view_player'),
    url(r'^tournaments/(?P<pop_id>[0-9]+)/?', views.player_tournaments, name='player_tournaments'),
    url(r'^tournaments/?', views.tournaments, name='tournaments'),
    url(r'^tournament/(?P<tournament_id>[0-9]+)/?', views.view_tournament, name='view_tournament'),
    url(r'^$', views.index, name='index'),
]