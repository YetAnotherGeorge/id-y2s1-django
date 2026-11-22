import datetime
import django.http
import django.conf
from typing import Any

def date_firma(request: django.http.HttpRequest) -> dict[str, Any]:
    return {
        "firma": django.conf.settings.DATE_FIRMA,
        "an_curent": datetime.datetime.now().year
    }