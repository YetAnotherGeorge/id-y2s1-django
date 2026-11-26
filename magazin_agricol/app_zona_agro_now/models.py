from datetime import date
from django.db import models
from django.utils import timezone

# Cerinte:
# >= 5 campuri NULL (descriere, sigla, tara_origine, website_oficial, tara, garantie_luni);
# >= 1 camp UNIQUE (Categorie.nume, BrandUtilaj.nume, Furnizor.nume_companie, Moneda.cod_iso);
# >= 1 camp URLField/EmailField/SlugField (BrandUtilaj.website_oficial - URLField);
# >= 2 modele cu Meta.ordering (Produs, Categorie, ImagineProdus);
# >= 1 camp cu choices (Produs.tensiune_alimentare: '12V', '24V', 'N/A');
# >= 4 campuri cu default, min 1 cu blank=True (culoare, necesita_montaj_autorizat, stoc_disponibil, tensiune_alimentare, este_original_oem, timp_livrare_zile, este_principala);
# >= 5 campuri cu help_text (pret_bani, modele_compatibile, culoare, sigla, curs_schimb_ron, numar_ordine);
# >= 1 camp datetime cu default data adaugarii (Produs.data_adaugare - DateTimeField auto_now_add/default);
# >= 5 campuri cu error_messages (Produs.nume, Produs.pret_bani, Categorie.nume, BrandUtilaj.nume, BrandUtilaj.website_oficial, Moneda.cod_iso);
# >= 5 constrangeri models.Q (pret_bani > 0, stoc_disponibil >= 0, garantie_luni >= 0, timp_livrare_zile > 0, curs_schimb_ron > 0, numar_ordine >= 1);
# >= 4 campuri indexate db_index/Meta.indexes (Produs.nume, Produs.pret_bani, Produs.tensiune_alimentare, Produs.data_adaugare);
# >= 1 camp ImageField/FileField (ImagineProdus.cale_fisier - ImageField)

# TODO: explain why Tabel 06 is a weak entity