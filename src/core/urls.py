from django.conf.urls import url
from core.views import HomePageView, RegisterFormView, my_login_view
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^login$', my_login_view, {'template_name': 'core/login.html'}, name="login"),
    url(r'^logout$', logout, name="logout"),
    url(r'^registration', RegisterFormView.as_view(), {'template_name': 'core/registration.html'}, name="registration"),
]