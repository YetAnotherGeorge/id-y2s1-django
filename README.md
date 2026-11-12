# id-y2s1-django
Proiect Dezvoltarea Aplicatiilor Web - Site Produse Agricole


## Tasks - Done
Lab 1 - 1 
   - Document google docs
   - Initializare proiect
Lab 1 - 2
Lab 1 - 3
Lab 1 - 4: Middleware Accesare
Lab 1 - 5: string_url, pagina
lab 1 - 6 
lab 1 - 7: utils: data_ro.py
lab 1 - 8: custom middleware for ip
lab 1 - 9 
lab 1 - 10: data param

lab 2 - 1:
   Sa se scrie o pagină /log care afiseaza toate cererile către paginile din site (prima pagina, info si chiar, e însăși, log). Pagina poate primi si parametrul ultimele cu o valoare numerică întreagă (altfel pagina va afișa un mesaj de eroare). Se vor afișa ultimele n accesări unde n e valoarea parametrului ultimele. Dacă se cere o valoare mai mare decât numărul de accesări, se vor afișa toate și la final un mesaj de eroare cu textul "Exista doar k accesari fata de n accesari cerute", înlocuind k și n cu valorile corespunzătoare.

   http://127.0.0.1:8000/log/?ultimele=4

lab 2 - 2
   Pagina /log poate primi ca parametru și accesari cu valoarea "nr" (string) (/log?accesari=nr) caz în care va afișa o secțiune suplimentară care afișeaza numarul de accesari de cand a fost pornit serverul (in sesiunea curenta). Se mai pot da si parametrii iduri care primește o enumerare de id-uri separate prin virgula și dubluri, implicit cu valoarea false (deci daca lipsește din query string  e considerat false). Parametrul iduri poate sa apare de mai multe ori: /log?iduri=2,3&iduri=5&iduri=4,2,1 
   In această situație se vor afișa accesarile cu id-urile 2,3,5,4,1 (în această ordine, 2 nefiind afișat a doua oară). Dacă parametrul dubluri e setat la true, se afișează și 2.
