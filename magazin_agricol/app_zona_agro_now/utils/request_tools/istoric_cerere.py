from collections.abc import Callable
from threading import Lock


class IstoricCerere:
   requested_page: str
   timestamp: str # format iso 8601
   ip_client: str
   ip_x_forwarded_for: str | None 
   
   def __init__(self, requested_page: str, timestamp: str, ip_client: str, ip_x_forwarded_for: str | None):
      self.requested_page = requested_page
      self.timestamp = timestamp
      self.ip_client = ip_client
      self.ip_x_forwarded_for = ip_x_forwarded_for
      
   def to_html_str(self) -> str:
      return f"""<tr>
         <td>{self.requested_page}</td>
         <td>{self.timestamp}</td>
         <td>{self.ip_client}</td>
         <td>{self.ip_x_forwarded_for or ''}</td>
      </tr>"""
      

class IstoricCereri:
   """ Clasa statica pentru gestionarea istoricului cererilor - thread safe """
   lck: Lock = Lock()
   cereri_total_count: int = 0 # total req since server start
   
   cereri_count_max: int = 10000
   cereri: list[IstoricCerere] = []
   
   @staticmethod
   def adauga_cerere(cerere: IstoricCerere):
      """ Adauga cerere; thread safe """
      with IstoricCereri.lck:
         if len(IstoricCereri.cereri) >= IstoricCereri.cereri_count_max:
            IstoricCereri.cereri.pop(0)
         IstoricCereri.cereri.append(cerere)
         IstoricCereri.cereri_total_count += 1
   
   @staticmethod
   def to_html_table(idx_start_inc: int | None = None, idx_end_exc: int | None = None, step: int | None = None) -> str:
      """ Randeaza (o submultime) din istoric ca un un tabel HTML """
      rows: str = ""
      
      # selecteaza submultimea target
      cereri_sel: list[IstoricCerere]
      
      with IstoricCereri.lck:
         cereri_sel = IstoricCereri.cereri[
            (idx_start_inc if idx_start_inc is not None else 0)
            :(idx_end_exc if idx_end_exc is not None else len(IstoricCereri.cereri))
            :(step if step is not None else 1)
      ]
      
      with IstoricCereri.lck:
         rows = "".join(c.to_html_str() for c in cereri_sel)
         
      return f"""
         <table>
            <tr><th>Requested Page</th><th>Timestamp</th><th>IP Client</th><th>IP X-Forwarded-For</th></tr>
            {rows}
         </table>
      """
      
   @staticmethod
   def to_html_table_array(cereri_idx: list[int]) -> str:
      """ Randeaza (o submultime) din istoric ca un un tabel HTML """
      rows: str = ""
      
      # selecteaza submultimea target
      cereri_sel: list = [IstoricCereri.cereri[i] for i in cereri_idx if 0 <= i < len(IstoricCereri.cereri)]
      
      with IstoricCereri.lck:
         rows = "".join(c.to_html_str() for c in cereri_sel)
         
      return f"""
         <table>
            <tr><th>Requested Page</th><th>Timestamp</th><th>IP Client</th><th>IP X-Forwarded-For</th></tr>
            {rows}
         </table>
      """
   
   @staticmethod
   def get_grouped(group_selector: Callable[[IstoricCerere], str]) -> dict[str, list[IstoricCerere]]:
      """ Grupeaza cererile dupa criteriul dat de group_selector """
      grouped: dict[str, list[IstoricCerere]] = {}
      with IstoricCereri.lck:
         for cerere in IstoricCereri.cereri:
            key = group_selector(cerere)
            if key not in grouped:
               grouped[key] = []
            grouped[key].append(cerere)
      return grouped