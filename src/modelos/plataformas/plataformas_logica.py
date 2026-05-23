class Plataforma:
    """
    Modelo lógico de una plataforma.
    Guarda posición, tamaño y propiedades físicas.
    """

    def __init__(self, x, y, ancho, alto, solida=True):

        self.x     = x
        self.y     = y
        self.ancho = ancho
        self.alto  = alto

        # Si es sólida el jugador no puede atravesarla
        self.solida = solida