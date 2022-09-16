#5
"""
Zadání:
Vyhledávání hodnot, při kterých dosáhne zkoumaný signál vybrané hodnoty je důležitou součástí analýzy časových řad. Pro tento účel existuje spousta zajímavých metod. Jeden typ metod se nazývá ohraničené (například metoda půlení intervalu), při kterých je zaručeno nalezení kořenu avšak metody typicky konvergují pomalu. Druhý typ metod se nazývá neohraničené, které konvergují rychle, avšak svojí povahou nemusí nalézt řešení (metody využívající derivace). Vaším úkolem je vybrat tři různorodé funkce (například polynomiální, exponenciální/logaritmickou, harmonickou se směrnicí, aj.), které mají alespoň jeden kořen a nalézt ho jednou uzavřenou a jednou otevřenou metodou. Porovnejte časovou náročnost nalezení kořene a přesnost nalezení. 

"""

import numpy as nmp
from numpy import sin, log
import matplotlib.pyplot as pplt
from scipy.misc import derivative

#Funkce
lb1 = lambda x : x**3 - 1
lb2 = lambda x : -sin(3*x) + x
lb3 = lambda x : log(x**2) - 2

#bisekce, půlení intervalů
def zav_metoda(funkce, min0, max0, presnost=0.001):
    opak = 0
    min, max = min0, max0
    while abs(max-min) > presnost:
        koren = (max + min)/2
        if funkce(min)*funkce(max) < 0:
            max = koren
        else:
            min = koren
        opak += 1
    print(f"Opakování pro přesnost 0.001: {opak}")
    return koren

def vysledek_zav(funkce, min, max, koren, nazev):
    print(f"Kořen pro funkci je {koren}")
    print(f"Funkční hodnota v bodě je {funkce(koren)}")
    pplt.plot(nmp.linspace(min, max), funkce(nmp.linspace(min, max)), "r")
    pplt.plot(koren, funkce(koren), "bo")
    pplt.title(nazev)
    pplt.show()

vysledek_zav(lb1, 0.1, 10, zav_metoda(lb1, 0.1, 5), "x**3 - 1")
vysledek_zav(lb2, 0.1, 10, zav_metoda(lb2, 0.1, 1), "-sin(3*x) + x")
vysledek_zav(lb3, 0.1, 10, zav_metoda(lb3, 1, 3), "log(x**2) - 2")

#Newtonova metoda tečen (derivací)
def ote_metoda(funkce, bod, presnost=0.00001):
    opakovani = 0
    while abs(funkce(bod)) > presnost:
        koren = bod - (funkce(bod) / derivative(funkce, bod))
        bod = koren
        opakovani += 1
    koren = bod
    print(f"Opakovaní pro přesnost 0.001: {opakovani}")
    return koren

def vysledek_ote(funkce, min, max, koren, nazev):
    print(f"Kořen pro funkci je {koren}")
    print(f"Funkční hodnota v tomto bodě je {funkce(koren)}")
    pplt.plot(nmp.linspace(min, max), funkce(nmp.linspace(min, max)), "r")
    pplt.plot(koren, funkce(koren), "bo")
    pplt.title(nazev)
    pplt.show()

vysledek_ote(lb1, 0.1, 10, zav_metoda(lb1, 0.1, 5), "x**3 - 1")
vysledek_ote(lb2, 0.1, 10, zav_metoda(lb2, 0.1, 1), "-sin(3*x) + x")
vysledek_ote(lb3, 0.1, 10, zav_metoda(lb3, 1, 3), "log(x**2) - 2")
