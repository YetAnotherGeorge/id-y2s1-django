import datetime
import re

ZILE = ("Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică")
ZILE_SCURT = ("Lun", "Mar", "Mie", "Joi", "Vin", "Sâm", "Dum")
LUNI = ("Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie")
LUNI_SCURT = ("Ian", "Feb", "Mar", "Apr", "Mai", "Iun", "Iul", "Aug", "Sep", "Oct", "Nov", "Dec")

FORMAT_IMPLICIT = "%A, %-d %B %Y"

def formateaza_data_ro(data: datetime.datetime, format: str = FORMAT_IMPLICIT) -> str:
   """Ca strftime, dar %A, %a, %B si %b sunt returnate in limba romana."""
   inlocuiri = {
      "A": ZILE[data.weekday()],
      "a": ZILE_SCURT[data.weekday()],
      "B": LUNI[data.month - 1],
      "b": LUNI_SCURT[data.month - 1],
      "-d": str(data.day),
   }
   # celelalte coduri raman neschimbate pentru strftime
   format_ro = re.sub(r"%(\-d|[AaBb])", lambda m: inlocuiri.get(m.group(1), m.group(0)), format)
   return data.strftime(format_ro)