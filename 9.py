#9
"""
Zadání:
V oblasti přírodních a sociálních věd je velice důležitým pojmem integrál, který představuje funkci součtů malých změn (počet nakažených covidem za čas, hustota monomerů daného typu při posouvání se v řetízku polymeru, aj.). Integraci lze provádět pro velmi jednoduché funkce prostou Riemannovým součtem, avšak pro složitější funkce je nutné využít pokročilé metody. Vaším úkolem je vybrat si 3 různorodé funkce (polynom, harmonická funkce, logaritmus/exponenciála) a vypočíst určitý integrál na dané funkci od nějakého počátku do nějakého konečného bodu. Porovnejte, jak si každá z metod poradila s vámi vybranou funkcí na základě přesnosti vůči analytickému řešení.

"""

import numpy as nmp
from numpy import sin, log
from scipy import integrate

#Funkce
def poly_fun(x):
    return x**3 - 3*x + 7

def harm_fun(x):
    return 2*sin(3*x)

def log_fun(x):
    return log(6*x) + (2/3)


#Vypočet
def riemannuv_ctverec(funkce, k, l):
    return integrate.quadrature(funkce, k, l)

def simpsonova_metoda(funkce, m, n, h=0.01):
    return integrate.simpson(funkce(nmp.arange(m, n+h, h)), nmp.arange(m, n+h, h))

def rombergova_metoda(funkce, o, p):
    return integrate.romberg(funkce, o, p)

#Výsledky
print("Polynomická Funkce")
print(f"Pomocí Riemannova čtverce {riemannuv_ctverec(poly_fun, 1, 2)[0]}")
print(f"Pomocí Simpsonovy metody {simpsonova_metoda(poly_fun, 1, 2)}")
print(f"Pomocí Rombergovy metody {rombergova_metoda(poly_fun, 1, 2)}")

print("Polynomická Funkce")
print(f"Pomocí Riemannova čtverce {riemannuv_ctverec(harm_fun, 1, 2)[0]}")
print(f"Pomocí Simpsonovy metody {simpsonova_metoda(harm_fun, 1, 2)}")
print(f"Pomocí Rombergovy metody {rombergova_metoda(harm_fun, 1, 2)}")

print("Polynomická Funkce")
print(f"Pomocí Riemannova čtverce {riemannuv_ctverec(log_fun, 1, 2)[0]}")
print(f"Pomocí Simpsonovy metody {simpsonova_metoda(log_fun, 1, 2)}")
print(f"Pomocí Rombergovy metody {rombergova_metoda(log_fun, 1, 2)}")
