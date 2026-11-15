import django
import django.http
import django.shortcuts


def despre(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """
   [VIEW] despre page
   """
   return django.shortcuts.render(request, "despre.html")