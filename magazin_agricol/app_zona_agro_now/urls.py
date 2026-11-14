from django.urls import path, re_path

from .views import index, misc, istoric, despre

urlpatterns = [
   path("", index.index, name="home"),
   path("info/", misc.info, name="info"),
   path("log/", misc.istoric_cereri, name="log"),
   re_path(r"^accesare(?P<id>[0-9]+)$", misc.detalii_accesare, name="accesare"),
   path("istoric/", istoric.istoric, name="istoric"),
   path("despre/", despre.despre, name="despre")
]