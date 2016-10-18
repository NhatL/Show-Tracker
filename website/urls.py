from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^shows/popular', views.popular, name="popular-view"),
    url(r'^shows/browse', views.browse, name="browse-view"),
    url(r'^shows/unwatched', views.unwatched, name="unwatched-view"),
    url(r'^shows/my/episode', views.my_show_episode, name="my-shows-watch-view"),
    url(r'^shows/my/mark/(\d+)/all$', views.my_show_mark_all, name="my-shows-mark-all-view"),
    url(r'^shows/my/mark/(\d+)/(\d+)$', views.my_show_mark_season, name="my-shows-mark-season-view"),
    url(r'^shows/my/mark/(\d+)/(\d+)/unwatched$', views.my_show_mark_season_unwatched, name="my-shows-mark-season-unwatched-view"),
    url(r'^shows/my/remove/(\d+)$', views.my_shows_remove, name="my-shows-remove-view"),
    url(r'^shows/my/add/(\d+)$', views.my_shows_add, name="my-shows-add-view"),
    url(r'^shows/my', views.my_shows, name="my-shows-view"),
    url(r'^shows/(\d+)$', views.show_details, name="shows-view"),
    url(r'^shows/', views.popular, name="shows-default-view"),
    url(r'^user/login/', views.login_user, name="login-view"),
    url(r'^user/reset/', views.reset, name="reset-view"),
    url(r'^user/sign_up/', views.signup, name="signup-view"),
    url(r'^user/profile/', views.profile, name="profile-view"),
    url(r'^user/logout/', logout, {'next_page': '/'}, name="logout-view"),
    url(r'^$', views.index, name="main-view"),
]