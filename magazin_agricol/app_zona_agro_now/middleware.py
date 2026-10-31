from .views import Accesare


class AccesareMiddleware:
   def __init__(self, get_response):
      self.get_response = get_response

   def __call__(self, request):
      request.ip_client = request.META.get("REMOTE_ADDR") # todo: X-forwarded-for in caz de LB
      request.accesare = Accesare.din_cerere(request)
      return self.get_response(request)