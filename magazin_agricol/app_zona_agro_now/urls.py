from django.urls import path, re_path

from .views import index, misc, istoric, despre

urlpatterns = [
   path("", index.view_index, name="home"),
   path("info/", misc.view_info, name="info"),
   path("log/", misc.view_log, name="log"),
   re_path(r"^accesare(?P<id>[0-9]+)$", misc.view_accesare, name="accesare"),
   path("istoric/", istoric.view_istoric, name="istoric"),
   path("despre/", despre.view_despre, name="despre")
]