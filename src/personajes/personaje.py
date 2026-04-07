class Personaje():
    """CLASE BASE (PADRE) que va a tener un constructor unicamente con un NOMBRE"""

    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_estado(self):
        """Metodo que muesta el Estado del personaje (su nombre, su vida actual y su ataque basico)"""
        print(f"Nombre: {self.nombre} - Vida: {self._vida} - Ataque basico: {self.ataque}")

    def estaVivo(self):
        """Metodo que muestra si un personaje esta vivo o muerto"""
        if self._vida > 0:
            return True
        return False

    def atacar(self, Enemigo):
        """Metodo que primero verifica si el enemigo esta con vida o no. Si es True, se va a proceder al ataque,
        de lo contrario solo se va a mostrar el mensaje de que "tal enemigo esta muerto"""
        if Enemigo.estaVivo() == True:
            print(f"{self.nombre} ataca a {Enemigo.nombre}")
            return Enemigo.recibir_danio(self.ataque)
        else:
            print(f"{Enemigo.nombre} esta muerto")

    def recibir_danio(self, daño):
        self._vida -= daño

        if self._vida < 0:
            self._vida = 0

        print(f"{self.nombre} recibe {daño} de daño")
        print(f"Vida restante: {self._vida}")

        return self._vida > 0