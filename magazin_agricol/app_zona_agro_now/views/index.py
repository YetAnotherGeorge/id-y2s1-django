import django
import django.http
import django.shortcuts


def view_index(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """
   [VIEW] Index page
   """
   return django.shortcuts.render(request, "index.html")