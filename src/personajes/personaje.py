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
        """Metodo que primero verifica si el enemigo esta con vida o no. Si es True, se va a proceder al ataque,
        de lo contrario solo se va a mostrar el mensaje de que "tal enemigo esta muerto"""
        if Enemigo.estaVivo() == True:
            print(f"{self.nombre} ataca a {Enemigo.nombre}")
            return Enemigo.recibir_danio(self.ataque)
        else:
            if Enemigo.nombre == "Cabra de Fuego":
                self.desbloquear_habilidad(Enemigo.habilidad_otorgada)
                print(f"{Enemigo.nombre} esta muerto. Hoku ha desbloqueado la habilidad: {Enemigo.habilidad_otorgada}")
            else:
                print(f"{Enemigo.nombre} esta muerto")

    def recibir_danio(self, danio):
        """Metodo que recibe el danio del ataque enemigo y lo resta a la vida del personaje. 
        Si el danio es mayor a la vida actual, la vida se va a quedar en 0"""
        self._vida -= danio

        if self._vida < 0:
            self._vida = 0

        print(f"{self.nombre} recibe {danio} de danio")
        print(f"Vida restante: {self._vida}")

        return self._vida > 0