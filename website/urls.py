from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^shows/popular', views.popular, name="popular-view"),
    url(r'^shows/browse', views.browse, name="browse-view"),
    url(r'^shows/unwatched', views.unwatched, name="unwatched-view"),
    url(r'^shows/my', views.my_shows, name="my-shows-view"),
    url(r'^shows/(\d+)$', views.show_details, name="shows-view"),
    url(r'^shows/', views.popular, name="shows-default-view"),
    url(r'^user/login/', views.login_user, name="login-view"),
    url(r'^user/reset/', views.reset, name="reset-view"),
    url(r'^user/sign_up/', views.signup, name="signup-view"),
    url(r'^user/profile/', views.profile, name="profile-view"),
    url(r'^user/logout/', logout, {'next_page': '/'}),
    url(r'^$', views.index, name="main-view"),
]