#VIDEOJUEGO DE PLATAFORMAS
#IMPORTACIONES
from src. personajes.enemigos.enemigos import Enemigo
from src. personajes.protagonista.hoku import Hoku
from src. personajes.enemigos.bichiluz import Bichiluz
from src. personajes.enemigos.perruga import Perruga
from src. personajes.enemigos.hibrido import Hibrido
from src. personajes.enemigos.medania import Medania
from src. personajes.jefes.cabra_de_fuego import CabraDeFuego
from src. personajes.npc.fuego_fatuo import FuegoFatuo
from src. interactuable.interactuable import Interactuable
from src. objetos.palancas import Palancas
from src. objetos.puertas import Puertas

#PERSONAJE PRINCIPAL "HOKU"
"""Pequenio extraterrestre, hibrido, similar a un zorro del desierto, 
que puede consumir habilidades de los jefes para avanzar por los mundos"""
Hoku = Hoku() #unico protagonista

#ENEMIGOS
"""Pequenios enemigos que pueden o no atacar a Hoku. Estan esparcidos por todo el nivel.
Son sencillos de derrotar, pueden evitarse igualmente."""
Bichiluz = Bichiluz() #enemigo que se mantiene en su lugar
Perruga = Perruga() #enemigo con recorrido automatico, huele el suelo como un perro en busqueda de presas
Medania = Medania() #como toda arania es timido, esta en su cueva o rincon, pero si alguien se acerca no duda en protegerse
Hibrido = Hibrido() #es mas violento que el resto, pero no es tan complejo de vencer

#JEFE
"""Enemigo mas poderoso, que se encuentra al final de cada mundo. Para avanzar al siguiente mundo, 
Hoku debe derrotar al jefe y consumir su habilidad especial"""
jefe = CabraDeFuego()

#PERSONAJES NO JUGABLES
FuegoFatuo = FuegoFatuo() #NPC que se encuentra en el mundo 1, ayuda a Hoku a atravesar la grieta que se encuentra en una cumbre

#OBJETOS
palanca = Palancas()
puerta = Puertas()

#===================================================== INVOCACIONES =====================================================================================
#Perruga.ataque_especial(Hoku)
#Hibrido.ataque_especial(Hoku)

#FuegoFatuo.interactuar(Hoku)
#palanca.interactuar(Hoku)
#puerta.interactuar(Hoku)

Hoku.atacar(jefe)
jefe.otorgar_recompensa(Hoku)
Hoku.lanzar_habilidad(jefe.habilidad_otorgada, Bichiluz)