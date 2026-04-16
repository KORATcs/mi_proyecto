from src.modelos.personajes.personaje import Personaje
from excepciones.excepciones import JefeNoDerrotadoError
"""Clase Padre de todas las subclases de los Jefes. Cada nivel/realidad va a tener un jefe unico oblgiatorio
Cada uno de ellos, va a tener un nombre, vida y ataques especiales unicos y diferentes. Lo unico basico es su 
golpe comun que quita siempre 2 corazones"""

class Jefe(Personaje):

    def __init__(self, nombre, vida, habilidad_otorgada):
        """Constructor con atributos heredados: nombre y vida, mas su atrivbuos propios: ataque comun y 
        habilidad otorgada al derrotar a este jefe"""
        super().__init__(nombre)
        self._vida = vida
        self.ataque = 2 #TODOS LOS JEFES QUITAN 2 CORAZONES CON SU GOLPE COMUN
        self.habilidad_otorgada = habilidad_otorgada #habilidad que se le otorga a Hoku al derrotar a este jefe
    
    def otorgar_recompensa(self, personaje):
        # VALIDACIÓN: ¿Sigue vivo el jefe?
        if self.estaVivo():
            raise JefeNoDerrotadoError(f"No puedes obtener la recompensa, {self.nombre} sigue vivo.")
            
        personaje.desbloquear_habilidad(self.habilidad_otorgada)
        return self.habilidad_otorgada
    