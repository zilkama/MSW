#3
"""
Zadání:
Důležitou částí studia na přírodovědecké fakultě je podobor matematiky zvaný lineární algebra. Poznatky tohoto oboru jsou základem pro oblasti jako zpracování obrazu,  strojové učení nebo návrh mechanických soustav s definovanou stabilitou. Základní úlohou v lineární algebře je nalezení neznámých v soustavě lineárních rovnic. Na hodinách jste byli obeznámeni s přímou a iterační metodou pro řešení soustav lineárních rovnic. Vaším úkolem je vytvořit graf, kde na ose x bude velikost čtvercové matice a na ose y průměrný čas potřebný k nalezení uspokojivého řešení. Cílem je nalézt takovou velikost matice, od které je výhodnější využít iterační metodu.

"""

import numpy as nmp
from numpy import array, diag, mean
import time
import matplotlib.pyplot as plt

#Jacobiho metoda 
def jacobiho_metoda(A, b, niteraci, x0):
    x = x0
    D = nmp.diag(A)
    L = nmp.tril(A, k = -1)
    U = nmp.triu(A, k = 1)
    for i in range(niteraci):
        x = (b - nmp.matmul((L + U),x))/D
        if (nmp.allclose(x, vysledek_gaussovy_metody, rtol=1e-8, atol=1e-9,)) == True: 
            break
    return x

#Gaussova metoda 
def gaussova_metoda(A,b):
    x = nmp.linalg.solve(A, b)
    return x

casG1 = [ ]
casJ1 = [ ]
casG2 = [ ]
casJ2 = [ ]

#tvorba rady rovnic
h = input ("Zadejte velikost ctvercove matice = " ) 
print("Zvolena velikost ctvercove matice je :", h)
h = int(h)

for M in range (h-1):
    M = M + 2
    a = nmp.ones(M) 
    array
    
    #diagonalni matice
    A1 = nmp.diagflat([a])
    diag
    
    #jednotkova matice
    A2 = nmp.ones((M, M), dtype=int)
    array
   
    #jednotkova + diagonalni matice
    A = A1 + A2
    
    #tvorba matice prava strana
    b1 = nmp.ones(M)
    array
    b = b1*(M+1)
    
    #opakovani vypoctu
    for v in range (100):
        x0 = nmp.ones(len(A))
        
        #vypocty + cas pro Gaussovu metodu
        gstart = time.perf_counter()
        vysledek_gaussovy_metody = gaussova_metoda(A,b)
        gend = time.perf_counter()
        g = gend - gstart
        g = round(1000000*g)
        
        #vypocty + cas pro Jacobiho metodu
        jstart = time.perf_counter()
        vysledek_jacobiho_metody = jacobiho_metoda(A,b,100,x0)
        jend = time.perf_counter()
        j = jend - jstart
        j = round(1000000*j)
    
        casG1.append(g)
        casJ1.append(j)

    PG = mean(casG1)
    PJ = mean(casJ1)
    casG1 = [ ]
    casJ1 = [ ]
    casG2.append(PG)   
    casJ2.append(PJ)   

#vysledny graf
fig, ax = plt.subplots ()
line = plt.plot(casG2, label = "Gaussova eliminace")
line = plt.plot(casJ2, label = "Jacobiho iteracni metoda")
plt.title(r"Potrebny cas k vypoctu dane linearni soustavy rovnic")
plt.xlabel('Velikost ctvercove matice')
plt.ylabel('Doba vypoctu [10^-6 s]')

ax.legend(loc=2)

plt.show() 
