import django
import django.http
import django.shortcuts
from typing import Any, Mapping

def view_contact(request: django.http.HttpRequest) -> django.http.HttpResponse:
    return django.shortcuts.render(request, "contact.html")