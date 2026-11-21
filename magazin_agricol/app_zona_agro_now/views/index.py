import django
import django.http
from django.shortcuts import render


def view_index(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """
   [VIEW] Index page
   """
   return render(request, "index.html")