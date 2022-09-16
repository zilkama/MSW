#8
"""
Zadání:
Numerická derivace je velice krátké téma. V hodinách jste se dozvěděli o nejvyužívanějších typech numerické derivace (dopředná, zpětná, centrální). Jedno z neřešených témat na hodinách byl problém volby kroku. V praxi je vhodné mít krok dynamicky nastavitelný. Algoritmům tohoto typu se říká derivace s adaptabilním krokem. Cílem tohoto zadání je napsat program, který provede numerickou derivaci s adaptabilním krokem pro vámi vybranou funkci. Proveďte srovnání se statickým krokem a analytickým řešením.

"""

#vypočty derivací
def for_derivate(f, x0, k):
    return(f(x0+k) - f(x0))/k

def back_derivate(f, x0, k):
    return (f(x0) - f(x0-k))/k

def cent_derivate(f, x0, k):
    return(f(x0+k) - f(x0-k))/(2*k)

def for_derivate_adaptive(f, x0, k_adaptive):
    return (f(x0+k_adaptive) - f(x0))/k_adaptive

def back_derivate_adaptive(f, x0, k_adaptive):
    return (f(x0) - f(x0-k_adaptive))/k_adaptive

def cent_derivate_adaptive(f, x0, k_adaptive):
    return (f(x0+k_adaptive) - f(x0-k_adaptive))/(2*k_adaptive)

#Funkce

f = lambda x: x**3 + 1
x0 = 4
k = 0.2
k_adaptive = float(input("Zadej adaptivní krok: "))

#mezi výsledky
forder = for_derivate(f, x0, k)
backder = back_derivate(f, x0, k)
centder = cent_derivate(f, x0, k)
forada = for_derivate_adaptive(f, x0, k_adaptive)
backada = back_derivate_adaptive(f, x0, k_adaptive)
centada = cent_derivate_adaptive(f, x0, k_adaptive)

print(f"Bez kroků dopředu: {forder}, s krokem dopředu: {forada}")
print(f"Bez kroků dopředu: {backder}, s krokem dopředu: {backada}")
print(f"Bez kroků dopředu: {centder}, s krokem dopředu: {centada}")
