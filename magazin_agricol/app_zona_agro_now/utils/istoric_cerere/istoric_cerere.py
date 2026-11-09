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
   cereri_count_max: int = 10000
   cereri: list[IstoricCerere] = []
   
   @staticmethod
   def adauga_cerere(cerere: IstoricCerere):
      """ Adauga cerere; thread safe """
      with IstoricCereri.lck:
         if len(IstoricCereri.cereri) >= IstoricCereri.cereri_count_max:
            IstoricCereri.cereri.pop(0)
         IstoricCereri.cereri.append(cerere)
   

   @staticmethod
   def to_html_table(idx_start_inc: int | None = None, idx_end_exc: int | None = None, step: int | None = None) -> str:
      """ Randeaza (o submultime) din istoric ca un un tabel HTML """
      rows: str = ""
      
      # selecteaza submultimea target
      cereri_sel: list = IstoricCereri.cereri[
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
   