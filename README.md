## Pasi pentru utilizarea aplicatiei

1. Pentru a porni aplicatia, rulati scriptul **`aplicatie.py`**.
2. In meniul din partea stanga se regasesc mai multe butoane, organizate in trei categorii: **"Generare"**, **"Intrebari utilizator"** si **"Acasa"**.

## Butoanele din categoria "Generare"

- Categoria **"Generare"** contine patru butoane, corespunzatoare fiecarui tip de intrebare: **"MinMax"**, **"Nash"**, **"CSP"** si **"Search"**.
- Apasarea unui buton deschide fereastra specifica tipului de problema selectat.
- Pentru a incepe generarea intrebarilor, introduceti numarul dorit in sectiunea **"Setari"**, apoi apasati butonul **"Genereaza"**.
- Dupa generare, va fi afisata intrebarea corespunzatoare, iar sectiunea **"Raspuns"** va deveni activa, permitand introducerea solutiei.
- Pentru a valida raspunsul, apasati butonul **"Evalueaza"**. Aplicatia va oferi feedback sub forma scorului obtinut, a explicatiei si a raspunsului corect.
- Butonul **"Urmatoarea"** permite trecerea la intrebarea urmatoare, iar **"Inapoi"** revine la intrebarea anterioara.
- Daca doriti sa generati intrebari noi, apasati din nou pe butonul "Genereaza"

## Butoanele din categoria "Intrebari utilizator"

- Aceasta categorie contine doua butoane, destinate adresarii intrebarilor de tip **MinMax** si **Nash**: **"Intreaba MinMax"** si **"Intreaba Nash"**.
- Apasarea unui buton deschide fereastra specifica tipului de problema selectat.
- Introduceti intrebarea conform instructiunilor afisate. Instanta problemei trebuie furnizata in formatul cerut.

### Template-uri pentru intrebari de tip MinMax

Structura generala este: [instanta] [intrebare]

**Exemple:**
1. `aleatoriu Care va fi valoarea radacinii?`  
   (cuvantul *aleatoriu* va genera automat o instanta aleatorie)
2. `3; 3,1,5,2; 2,2,2; Care este numarul minim de frunze evaluate?`

**Formatul instantei:** adancime; valorile frunzelor; structura arborelui;

### Template-uri pentru intrebari de tip Nash

Structura generala este: [instanta] [intrebare]

**Exemple:**
1. `aleatoriu Cate echilibre Nash sunt?`
2. `[[ (1,1) (2,2) ] [ (3,3) (2,1) ]]; [A1, B1]; [A2, B2]; Care sunt echilibrele Nash pure?`
3. `aleatoriu Care sunt strategiile dominante pentru jucatorul 1?`
4. `aleatoriu Care sunt strategiile dominante pentru jucatorul 2?`

**Formatul instantei:** matricea de payoff-uri; [strategiile jucatorului 1]; [strategiile jucatorului 2];

## Butonul din categoria "Acasa"

- Apasarea acestui buton va redirectioneaza catre fereastra principala a aplicatiei.
