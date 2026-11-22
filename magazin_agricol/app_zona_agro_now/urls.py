from django.urls import path, re_path

from .views import index, produse, cos_cumparaturi, despre, istoric, contact, misc

urlpatterns = [
   path("", index.view_index, name="home"),
   path("produse/", produse.view_produse, name="produse"),
   path("cos_cumparaturi/", cos_cumparaturi.view_cos_cumparaturi, name="cos_cumparaturi"),
   path("despre/", despre.view_despre, name="despre"),
   path("istoric/", istoric.view_istoric, name="istoric"),
   path("contact/", contact.view_contact, name="contact"),
   path("info/", misc.view_info, name="info"),
   path("log/", misc.view_log, name="log"),

   re_path(r"^accesare(?P<id>[0-9]+)$", misc.view_accesare, name="accesare"),
]