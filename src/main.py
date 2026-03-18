#VIDEOJUEGO DE PLATAFORMAS
from personajes.personaje import Personaje
from personajes.enemigos import Enemigo
from personajes.hoku import Hoku
from personajes.jefe import Jefe

#PERSONAJE PRINCIPAL "HOKU"
#Pequeño extraterrestre, hibrido, similar a un zorro del desierto, que puede consumir habilidades de los jefes para avanzar por los mapas.
Hoku = Hoku()

#ENEMIGOS
#Pequeños enemigos que pueden o no atacar a Hoku. Estan esparcidos por todo el nivel. 
#Son sencillos de derrotar, pueden evitarse igualmente.
enemigo = Enemigo("Bichito de Luz", 150) #pequeño insecto brillant
enemigo2 = Enemigo("Larva Curvada", 150) #larva gigante con varias curvas
enemigo3 = Enemigo("Araña Letal", 300) #araña venenosa
enemigo4 = Enemigo("Polilla X", 250) #polilla gigante
enemigo5 = Enemigo("Hibrido", 400) #gatito fisionado con una medusa

#JEFE PRINCIPAL DEL NIVEL
#Es un jefe que va a tener que derrotarse obligatoriamente para consumir su poder y avanzar al siguiente nivel.
jefe = Jefe("Ala Mayor", 2000) #VA A SER UN AVE FENIX

#LLAMADO DE LAS FUNCIONES
#Hoku.mostrar_estado()