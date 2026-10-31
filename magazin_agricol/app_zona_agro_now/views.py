from django.http import HttpResponse
import datetime

def index(request):
	return HttpResponse("""
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


def info(request) -> HttpResponse:
   return HttpResponse(f"""
      <!doctype html>
      <html lang="ro">
      <head>
         <meta charset="utf-8">
         <title>Informatii despre server</title>
      </head>
      <body>
         <h1>Informatii despre server</h1>
         <br>
      </body>
      </html>
   """)