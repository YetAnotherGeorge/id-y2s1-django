import django.http
import datetime
from typing import Tuple
from threading import Lock
from urllib.parse import urlparse
from .utils.data_ro import formateaza_data_ro, FORMAT_IMPLICIT

class Accesare:
   _next_id = 0
   _id_lock = Lock()

   def __init__(self, ip_client: str | None, url: str = "", parametri: dict[str, str | list[object]] | None = None):
      # Seteaza id - thread safe
      with self._id_lock:
         self.id = Accesare._next_id
         Accesare._next_id += 1
   
      self.ip_client = ip_client
      self.url = url
      self.parametri = {} if parametri is None else parametri
      self.data = datetime.datetime.now()

   def lista_parametri(self) -> list[Tuple[str, object | None]]:
      """dict to tuple

      Returns:
         list[Tuple[str, object | None]]: 
      """
      lp = []
      for k, v in self.parametri.items():
         if v is None:
            lp.append((k, None))
         else:
            lp.append((k, v))
      return lp
   
   def calculeaza_data(self, format: str = FORMAT_IMPLICIT, tip: str = "") -> str:
      """Data accesarii in romana. Pentru tip "zi" sau "timp" returneaza sectiunea HTML; altfel stringul simplu."""
      if tip == "zi":
         return f"<section><h2>Data</h2><p>{formateaza_data_ro(self.data, FORMAT_IMPLICIT)}</p></section>"
      if tip == "timp":
         return f"<section><h2>Ora</h2><p>{formateaza_data_ro(self.data, '%H:%M:%S')}</p></section>"
      return formateaza_data_ro(self.data, format)

   def string_url(self) -> str:
      """Intreg url-ul, inclusiv query string."""
      return self.url

   def pagina(self) -> str:
      """Doar calea paginii (fara domeniu sau parametri), ex: / sau /info."""
      return urlparse(self.url).path or "/"

   def __str__(self) -> str:
      campuri = {
         "id": self.id,
         "ip_client": self.ip_client,
         "string_url": self.string_url(),
         "pagina": self.pagina(),
         "calculeaza_data": self.calculeaza_data(),
         "lista_parametri": self.lista_parametri(),
      }
      return "\n".join(f"{nume}: {valoare}" for nume, valoare in campuri.items())
   
   @staticmethod
   def din_cerere(request: django.http.HttpRequest) -> Accesare:
      """static request factory method

      Args:
         request (HttpRequest): The incoming HTTP request object.

      Returns:
         Accesare: An instance of the Accesare class representing the request details.
      """
      return Accesare(
         ip_client=getattr(request, "ip_client", None),
         url=request.path,
         parametri=request.GET.dict(),
      )

def index(request: django.http.HttpRequest) -> django.http.HttpResponse:
   print(request.accesare) # type: ignore lab 1 - 9: print this
   return django.http.HttpResponse("""
      <!doctype html>
      <html lang="ro">
      <head>
         <meta charset="utf-8">
         <title>Magazin agricol</title>
      </head>
      <body>
         <h1>Magazin de produse tehnice utile în agricultură</h1>
         <p>Proiectul va consta într-un magazin de produse tehnice utile în agricultură: motocoase, accesorii și piese de schimb pentru unelte de cosit, motosape, motocultivatoare, despicătoare de lemne și tocătoare de crengi.</p>
         <p>Site-ul va conține o pagină de login și sign up, unde utilizatorii se vor putea înregistra folosind o adresă de email, un nume și o parolă.</p>
         <p>După logare, utilizatorii vor putea:</p>
         <ul>
            <li>să vizualizeze produsele disponibile;</li>
            <li>să filtreze produsele după categorie, interval de preț și stoc;</li>
            <li>să adauge produse într-un coș virtual.</li>
         </ul>
      </body>
      </html>
   """)


def info(request: django.http.HttpRequest) -> django.http.HttpResponse:
   accesare = request.accesare # type: ignore
   print(accesare)

   tip = request.GET.get("data", "")
   if tip in ("zi", "timp"):
      sectiuni = accesare.calculeaza_data(tip=tip)
   else:
      sectiuni = accesare.calculeaza_data(tip="zi") + accesare.calculeaza_data(tip="timp")

   return django.http.HttpResponse(f"""
      <!doctype html>
      <html lang="ro">
      <head>
         <meta charset="utf-8">
         <title>Informatii despre server</title>
      </head>
      <body>
         <h1>Informatii despre server</h1>
         {sectiuni}
      </body>
      </html>
   """)