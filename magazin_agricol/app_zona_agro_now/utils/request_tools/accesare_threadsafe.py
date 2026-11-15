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
   ip_client: str | None
   url: str
   query_string: str
   parametri: Dict[str, Any]
   data: datetime.datetime

   def __init__(self, ip_client: str | None, url: str = "", query_string: str = "", parametri: dict[str, str | list[object]] | None = None):
      # Seteaza id - thread safe
      with self._id_lock:
         self.id = Accesare._next_id
         Accesare._next_id += 1
   
      self.ip_client = ip_client
      self.url = url
      self.query_string = query_string
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
      """Returneaza data in romana sau sectiunea HTML ceruta."""
      if tip == "zi":
         return f"<section><h2>Data si ora</h2><p>Data: {formateaza_data_ro(self.data, format)}</p></section>"
      if tip == "timp":
         return f"<section><h2>Data si ora</h2><p>Ora: {formateaza_data_ro(self.data, '%H:%M:%S')}</p></section>"
      return formateaza_data_ro(self.data, format)

   def string_url(self) -> str:
      """Intreg url-ul, inclusiv query string."""
      return self.url + ("?" + self.query_string if self.query_string else "")

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
      parametri: Dict[str, Any] = {}
      for key in request.GET:
         values = request.GET.getlist(key)
         parametri[key] = values[0] if len(values) == 1 else values
      
      return Accesare(
         ip_client=getattr(request, "ip_client", None),
         url=request.path,
         query_string=request.META.get("QUERY_STRING", ""),
         parametri=parametri,
      )