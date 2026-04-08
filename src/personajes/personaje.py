from src.excepciones.excepciones import DanioInvalidoError, PersonajeMuertoError, ObjetivoMuertoError

class Personaje():
    """CLASE BASE (PADRE) que va a tener un constructor unicamente con un NOMBRE"""

    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_estado(self):
        """Metodo que muesta el Estado del personaje (su nombre, su vida actual y su ataque basico)"""
        if self.estaVivo() == True:
            print(f"Nombre: {self.nombre} - Vida: {self._vida} - Ataque basico: {self.ataque}")
        else:
            print(f"{self.nombre} esta muerto")

    def estaVivo(self):
        """Metodo que muestra si un personaje esta vivo o muerto"""
        if self._vida > 0:
            return True
        return False
    
    def atacar(self, Enemigo):
            # VALIDACIÓN: ¿El atacante está vivo?
            if not self.estaVivo():
                raise PersonajeMuertoError(f"{self.nombre} está muerto y no puede atacar.")
            
            # VALIDACIÓN: ¿El objetivo está vivo?
            if not Enemigo.estaVivo():
                raise ObjetivoMuertoError(f"{Enemigo.nombre} ya está muerto.")

            print(f"{self.nombre} ataca a {Enemigo.nombre}")
            return Enemigo.recibir_danio(self.ataque)

    def recibir_danio(self, danio):
            # VALIDACIÓN: ¿Daño negativo?
            if danio < 0:
                raise DanioInvalidoError("El daño no puede ser un valor negativo.")
                
            self._vida -= danio
            if self._vida < 0: self._vida = 0
            
            print(f"{self.nombre} recibe {danio} de daño. Vida restante: {self._vida}")
            return self.estaVivo()