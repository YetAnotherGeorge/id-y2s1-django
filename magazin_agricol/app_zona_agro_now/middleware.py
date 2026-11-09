from .utils.istoric_cerere import istoric_cerere

from .views import Accesare

# Folosit in magazin_agricol\magazin_agricol\settings.py, in MIDDLEWARE
class AccesareMiddleware:
   def __init__(self, get_response):
      self.get_response = get_response

   def __call__(self, request):
      request.ip_client = request.META.get("REMOTE_ADDR") # todo: X-forwarded-for in caz de LB
      request.accesare = Accesare.din_cerere(request)
      
      c_info: istoric_cerere.IstoricCerere = istoric_cerere.IstoricCerere(
         requested_page=request.path,
         timestamp=request.accesare.data.isoformat(),
         ip_client=request.ip_client,
         ip_x_forwarded_for=request.META.get("HTTP_X_FORWARDED_FOR")
      )
      istoric_cerere.IstoricCereri.adauga_cerere(c_info)
      
      return self.get_response(request)