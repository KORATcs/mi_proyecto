class Personaje():

    #clase base 

    def __init__(self, nombre):
        self.nombre = nombre
        self._vida = 100 #tiene 4 corazones (cada corazon son 25 puntos de vida - lo mismo que golpea un enemigo normal)
        self.ataque = 50

    def mostrar_estado(self): #MUESTRA NOMBRE, VIDA Y ATAQUE DEL PERSONAJE
        print(f"{self.nombre} - {self._vida} - {self.ataque}")

    def estaVivo(self): #MUESTRA SI ESTA VIVO O MUERTO || devuelve true cuando la vida es mayor a cero
        if self._vida > 0:
            return True
        return False

    def atacar(self, Enemigo): #METODO PARA ATACAR AL ENEMIGO/JEFE
        if Enemigo.estaVivo() == True:
            print(f"{self.nombre} ataca a {Enemigo.nombre}")
            return Enemigo.recibir_danio(self.ataque)
        else:
            print(f"{Enemigo.nombre} esta muerto")

    def recibir_danio(self, daño): #METODO PARA RECIBIR DAÑO || Se realiza gracias a que el atributo vida es privado
        self._vida -= daño

        if self._vida < 0:
            self._vida = 0

        print(f"{self.nombre} recibe {daño} de daño")
        print(f"Vida restante: {self._vida}")

        return self._vida > 0