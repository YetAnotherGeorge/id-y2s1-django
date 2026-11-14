import datetime
import urllib.parse
import threading
import django
import django.http
from typing import * # type: ignore
# local_imports
from ..data_ro import formateaza_data_ro, FORMAT_IMPLICIT

class Accesare:
   _next_id: int = 0 # static 
   _id_lock: threading.Lock = threading.Lock() # static 
   
   id: int
   url: str
   parametri: Dict[str, Any]
   data: datetime.datetime

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
      return urllib.parse.urlparse(self.url).path or "/"

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