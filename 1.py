#1

from sympy import *
import scipy.integrate as integrate
import numpy as np
from math import factorial
from time import process_time


#Nasobeni matice pomoci knihovny numpy
start = process_time()
matice = [[25, 1092, 2151], [60, 985, 1345], [5, 5456, 3541]]
vysledek = np.array(matice)*12
konec = process_time()

print("Pomocí knihovny Numpy:")
print(f"Matice je {vysledek} a výpočet trval: {(konec - start)} sekund")

#vlastni reseni 
start = process_time()
matice = [[25, 1092, 2151], [60, 985, 1345], [5, 5456, 3541]]
for i in range(len(matice)):
    for j in range(len(matice[0])):
        matice[i][j] = matice[i][j]*12
konec = process_time()

print("Vlastní řešení:")
print(f"Matice je {matice} a výpočet trval: {(konec - start)} sekund")


#Skalarni soucin pomoci knihovny numpy
start = process_time()
a = np.array([4, 2, 12])
b = np.array([2, 7, 17])
vysledek = sum(a*b)
konec = process_time()

print("Pomocí knihovny Numpy:")
print(f"Skalarní soucčn je: {vysledek} a výpočet trval: {(konec - start)} sekund")

#vlastni reseni 
start = process_time()
vysledek = 0
a = (4, 2, 12)
b = (2, 7, 17)
for i in range(len(a)):
    vysledek += a[i]*b[i]
konec = process_time()

print("Vlastní řešení:")
print(f"Skalární součin je: {vysledek} a vypočet trval: {(konec - start)} sekund")
print("\n")


#Vypocet faktorialu pomoci knihovny math
start = process_time()
x = 142364
vysledek = factorial(x)
konec = process_time()
vysledek = str(vysledek)

print("Pomocí knihovny Math:")
print(f"Faktorial z čísla {x} je {vysledek[:10]} a výpočet trval: {(konec - start)} sekund")

#vlastni reseni
start = process_time()
x = 142364
vysledek = 1
for i in range(1, x+1):
    vysledek = vysledek * i 
konec = process_time()
vysledek = str(vysledek)

print("Vlastní řešení:")
print(f"Faktorial z čísla {x} je {vysledek[:10]} a výpočet trval: {(konec - start)} sekund")
print("\n")

 
#Integrace pomoci knihovny scipy
start = process_time()
vysledek = integrate.quad(lambda x: (3*x**2-6*x+3), 1, 5)
konec = process_time()

print("Pomocí knihovny Scipy:")
print(f"Výpočet integrace je: {vysledek[0]} a výpocčet trval: {(konec - start)} sekund")

#vlastni reseni
def f(x):
    return (3*x**2-6*x+3)

start = process_time()
vysledek = 0
a = 1
b = 5
dx = 0.0001
while a < b:
    vysledek += dx * (f(a) + f((a+dx)))/2
    a += dx
konec = process_time()

print("Vlastní řešeni:")
print(f"Výpočet integrace je: {vysledek} a výpočet trval: {(konec - start)} sekund")
print("\n")


#derivace pomoci knihovny sympy 
def derivace_sym(funkce, promenna, hodnota):
    promenna = symbols("x")
    derivace = diff(funkce, promenna)
    return (derivace.subs(x, hodnota)).doit()
    
start = process_time()
x = symbols('x')
funkce = 5*x**3-7*x**2+8*x-14
vysledek = derivace_sym(funkce, x, 7)

konec = process_time()

print("Pomocí knihovny Sympy:")
print(f"Derivace je {vysledek} a výpočet trval: {(konec - start)} sekund")

#vlastni reseni
def f(x):
    return 5*x**3-7*x**2+8*x-14

def derivace(funkce, hodnota, h=0.001):
    return (funkce(hodnota+h) - funkce(hodnota))/h

start = process_time()
vysledek = derivace(f, 7)
konec = process_time()

print("Vlastní řešení:")
print(f"Derivace je {vysledek} a výpočet trval: {(konec - start)} sekund")
print("\n")