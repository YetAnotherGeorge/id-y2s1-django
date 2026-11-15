import django
import django.http
import django.shortcuts
from typing import Any, Mapping
# local_imports
from ..utils.request_tools.accesare_threadsafe import Accesare
from ..utils.request_tools.istoric_cerere import IstoricCereri


def info(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """
   [VIEW] Task lab 1: /info
   Returneaza pagina simpla cu info despre server
   """
   
   accesare: Accesare = request.accesare # type: ignore
   # print(accesare)  # printat de middleware

   tip: str = request.GET.get("data", "")
   if tip == "zi":
      data_html = accesare.calculeaza_data(tip="zi")
   elif tip == "timp":
      data_html = accesare.calculeaza_data(tip="timp")
   else:
      data_html = accesare.calculeaza_data(tip="zi") + accesare.calculeaza_data(tip="timp")

   # Render page
   context: Mapping[str, Any] = {"data_html": data_html}
   return django.shortcuts.render(request, 'info.html', context)


def detalii_accesare(request: django.http.HttpRequest, id: str) -> django.http.HttpResponse:
   """extrage accesarea cu numarul dat de regex

   Args:
      request (django.http.HttpRequest): request
      id (str): din groupul regex

   Raises:
      django.http.Http404: daca cererea nu e gasita
   Returns:
      django.http.HttpResponse: pagina cu detalii despre accesare
   """
   index = int(id)
   with IstoricCereri.lck:
      cerere = IstoricCereri.cereri[index] if 0 <= index < len(IstoricCereri.cereri) else None
   if cerere is None:
      raise django.http.Http404("Accesarea nu exista.")

   return django.shortcuts.render(request, "accesare.html", {"cerere": cerere, "id": index})


def istoric_cereri(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """ 
   [VIEW] Cerinta lab 2: /log endpoint
   """
   with IstoricCereri.lck:
      cereri = list(IstoricCereri.cereri)
      total = IstoricCereri.cereri_total_count

   try:
      ultimele = int(request.GET.get("ultimele", len(cereri)))
      iduri = [int(value.strip()) for group in request.GET.getlist("iduri") for value in group.split(",")]
   except ValueError:
      return django.http.HttpResponseBadRequest("Parametrii ultimele si iduri trebuie sa fie numerici.")
   if ultimele < 0:
      return django.http.HttpResponseBadRequest("Parametrul ultimele nu poate fi negativ.")

   if iduri:
      if request.GET.get("dubluri", "").lower() != "true":
         iduri = list(dict.fromkeys(iduri))
   else:
      iduri = list(range(max(0, len(cereri) - ultimele), len(cereri)))
   randuri = [(index, cereri[index]) for index in iduri if 0 <= index < len(cereri)]

   tabela = request.GET.get("tabel")
   tabela = tabela.lower().strip() if tabela else None
   proprietati = ("id", "ip_client", "url", "query_string", "parametri", "data")
   coloane = list(proprietati) if tabela == "tot" else (tabela or "").split(",")
   coloane = [column.strip() for column in coloane if column.strip()]
   if any(column not in proprietati for column in coloane):
      return django.http.HttpResponseBadRequest("Proprietate tabel necunoscuta.")
   randuri_tabel = [
      [index if column == "id" else
       cerere.accesare.string_url() if column == "url" else
       getattr(cerere.accesare, column) for column in coloane]
      for index, cerere in randuri
   ]

   frecvente: dict[str, int] = {}
   for cerere in cereri:
      frecvente[cerere.requested_page] = frecvente.get(cerere.requested_page, 0) + 1
   cel_mai_mult = max(frecvente, key=lambda k: frecvente[k]) if frecvente else ""
   cel_mai_putin = min(frecvente, key=lambda k: frecvente[k]) if frecvente else ""
   parametri = [name for name, values in request.GET.lists() for _ in values]
   context: Mapping[str, Any] = {
      "randuri": randuri,
      "numar_cereri": total,
      "ultimele": ultimele,
      "prea_multe": not request.GET.getlist("iduri") and ultimele > total,
      "accesari": request.GET.get("accesari", "").lower(),
      "total_accesari": total,
      "detalii": [cerere.timestamp.replace("T", " ") for _, cerere in randuri],
      "parametri": parametri,
      "numar_parametri": len(parametri),
      "tabel_query": tabela,
      "coloane": [(column, column.replace("_", " ").title()) for column in coloane],
      "randuri_tabel": randuri_tabel,
      "pagina_top": cel_mai_mult,
      "pagina_top_count": frecvente.get(cel_mai_mult),
      "pagina_bottom": cel_mai_putin,
      "pagina_bottom_count": frecvente.get(cel_mai_putin),
   }
   return django.shortcuts.render(request, "log.html", context)
