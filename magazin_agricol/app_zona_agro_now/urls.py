from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="home"),
   path("info/", views.info, name="info"),
   path("log/", views.istoric_cereri, name="log")
]