import django
import django.http
import django.shortcuts
from django.template import context
from typing import * # type: ignore
# local_imports
from ..utils.data_ro import formateaza_data_ro, FORMAT_IMPLICIT
from ..utils.request_tools.accesare_threadsafe import Accesare
from ..utils.request_tools.istoric_cerere import IstoricCerere, IstoricCereri


def info(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """
   [VIEW] Task lab 1: /info
   Returneaza pagina simpla cu info despre server
   """
   
   accesare: Accesare = request.accesare # type: ignore
   # print(accesare)  # printat de middleware

   tip: str = request.GET.get("data", "")
   accTimeInfo: Mapping[str, Any] = {}
  
   if tip in ("zi", "timp"):
      if tip == "zi":
         accTimeInfo["zi"] = formateaza_data_ro(accesare.data, FORMAT_IMPLICIT)
      else:
         accTimeInfo["timp"] = formateaza_data_ro(accesare.data, "%H:%M:%S")
   else:
      accTimeInfo["zi"] = formateaza_data_ro(accesare.data, FORMAT_IMPLICIT)
      accTimeInfo["timp"] = formateaza_data_ro(accesare.data, "%H:%M:%S")

   # Render page
   context: Mapping[str, Any] = {
      "accTimeInfo": accTimeInfo
   }
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
   cerere: IstoricCerere | None = None
   with IstoricCereri.lck:
      id_cerut: int | Never = int(id)
      if 0 <= id_cerut < len(IstoricCereri.cereri):
         cerere = IstoricCereri.cereri[id_cerut]
      else: 
         cerere = None

   if cerere is None:
      raise django.http.Http404("Accesarea nu exista.")

   return django.shortcuts.render(request, "accesare.html", {"cerere": cerere})


def istoric_cereri(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """ 
   [VIEW] Cerinta lab 2: /log endpoint
   """
   try:
      with IstoricCereri.lck:
         cereri = list(IstoricCereri.cereri)
         total_accesari = IstoricCereri.cereri_total_count

      ultimele_raw = request.GET.get("ultimele")
      ultimele = int(ultimele_raw) if ultimele_raw is not None else len(cereri)
      iduri = request.GET.getlist("iduri")
      iduri_cerute = [valoare for grup in iduri for valoare in grup.split(",")]

      if iduri:
         iduri_selectate = [int(valoare) for valoare in iduri_cerute]
         iduri_tabel = iduri_selectate if request.GET.get("dubluri") else list(set(iduri_selectate))
      else:
         idx_start = max(0, len(cereri) - ultimele)
         iduri_selectate = list(range(idx_start, len(cereri)))
         iduri_tabel = iduri_selectate

      iduri_valide = [idx for idx in iduri_selectate if 0 <= idx < len(cereri)]
      cereri_tabel = [cereri[idx] for idx in iduri_tabel if 0 <= idx < len(cereri)]
      accesari = request.GET.get("accesari", "").lower()
      tabel_query = request.GET.get("tabel")
      tabel_query = tabel_query.lower().strip() if tabel_query is not None else None
      coloane = {"id", "url", "timestamp", "ip_client", "ip_x_forwarded_for"} if tabel_query == "tot" else {
         coloana.strip() for coloana in (tabel_query or "").split(",")
      }

      context = {
         "cereri": cereri_tabel,
         "numar_cereri": len(cereri),
         "ultimele": ultimele,
         "prea_multe": not iduri and ultimele > len(cereri),
         "iduri_cerute": iduri_cerute,
         "accesari": accesari,
         "total_accesari": total_accesari,
         "detalii": [cereri[idx].timestamp.replace("T", " ") for idx in iduri_valide],
         "parametri": request.GET.keys(),
         "numar_parametri": len(request.GET),
         "tabel_query": tabel_query,
         "coloane": coloane,
         "randuri": [(idx, cereri[idx]) for idx in iduri_valide],
      }
      return django.shortcuts.render(request, "log.html", context)
   except Exception as e:
      print(f"istoric_cereri exception: {e}")
      return django.http.HttpResponse("Eroare la procesarea istoricului cererilor.", status=500)
