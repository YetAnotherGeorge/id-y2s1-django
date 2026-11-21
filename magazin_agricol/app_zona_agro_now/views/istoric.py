import django.http
import django.shortcuts

# local_imports
from ..utils.request_tools.accesare_threadsafe import Accesare
from ..utils.request_tools.istoric_cerere import IstoricCerere, IstoricCereri

def view_istoric(request: django.http.HttpRequest) -> django.http.HttpResponse:
   """
   [VIEW] 
   Returneaza pagina cu istoricul magazinului agricol.
   Va calcula cea mai putin si cea mai accesata pagina
   """
   ic: dict[str, list[IstoricCerere]] = IstoricCereri.get_grouped(lambda c: c.requested_page)
   ic_top = ""
   ic_top_count = None
   
   ic_bottom = ""
   ic_bottom_count = None
   
   for page, cereri_list in ic.items():
      count = len(cereri_list)
      if ic_top_count is None or count > ic_top_count:
         ic_top_count = count
         ic_top = page
      if ic_bottom_count is None or count < ic_bottom_count:
         ic_bottom_count = count
         ic_bottom = page
   
   
   return django.shortcuts.render(request, 'istoric.html', {
      'ic_top': ic_top, 'ic_top_count': ic_top_count, 
      'ic_bottom': ic_bottom, 'ic_bottom_count': ic_bottom_count
   })
