import django
import django.http
import django.shortcuts
from typing import Any, Mapping

def view_cos_cumparaturi(request: django.http.HttpRequest) -> django.http.HttpResponse:
    return django.shortcuts.render(request, "in_lucru.html", {"pageName": "Coș de Cumpărături"})