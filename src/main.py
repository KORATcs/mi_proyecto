#VIDEOJUEGO DE PLATAFORMAS
#IMPORTACIONES
from personajes.enemigos.enemigos import Enemigo
from personajes.protagonista.hoku import Hoku
from personajes.enemigos.bichiluz import Bichiluz
from personajes.enemigos.perruga import Perruga
from personajes.enemigos.hibrido import Hibrido
from personajes.enemigos.medaña import Medaña
from personajes.jefes.cabra_de_fuego import CabraDeFuego

#PERSONAJE PRINCIPAL "HOKU"
"""Pequeño extraterrestre, hibrido, similar a un zorro del desierto, 
que puede consumir habilidades de los jefes para avanzar por los mundos"""
Hoku = Hoku() #unico protagonista

#ENEMIGOS
"""Pequeños enemigos que pueden o no atacar a Hoku. Estan esparcidos por todo el nivel.
Son sencillos de derrotar, pueden evitarse igualmente."""
enemigo = Bichiluz() #enemigo que se mantiene en su lugar
enemigo2 = Perruga() #enemigo con recorrido automatico, huele el suelo como un perro en busqueda de presas
enemigo3 = Medaña() #como toda araña es timido, esta en su cueva o rincon, pero si alguien se acerca no duda en protegerse
enemigo4 = Hibrido() #es mas violento que el resto, pero no es tan complejo de vencer

#JEFE
jefe = CabraDeFuego()

#LLAMADO DE LAS FUNCIONES
Hoku.mostrar_estado()
jefe.mostrar_estado()
enemigo.mostrar_estado()
enemigo2.mostrar_estado()
enemigo3.mostrar_estado()
enemigo4.mostrar_estado()

