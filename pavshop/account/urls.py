from django.urls import path, re_path
from . import views
 
app_name = "account"
urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('register/', views.register_view, name="register_view"),
    path('load-cities/', views.load_cities_view, name='load_cities_view'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,33})/$', views.activate_view, name='activate_view'),
]
