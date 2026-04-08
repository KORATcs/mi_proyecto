# <p align="center"> HOKU </p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Library-Pygame-green?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Status-In_Development-orange?style=for-the-badge" />
</p>

---

## 👋 $\color{lightpink}{\text{Presentación}}$

> [!NOTE]
> ### 👩‍💻 Sobre la Autora
> Hola, mi nombre es **Camila Guadalupe Simon**. Este es mi proyecto final para la materia **Laboratorio Avanzado de la Programación** (Julio 2026), de la carrera Desarrollo de Software. Mi intención es que este mundo siga creciendo hasta dar el salto a motores como **Godot Engine**.

---

## 📖 $\color{lightblue}{\text{Hoku - Sinopsis}}$

> [!IMPORTANT]
> ### 🌌 El Equilibrio de los Multiversos
> En un universo donde realidades alternas coexisten, los ancestros de la especie de **Hoku** protegen runas que mantienen el equilibrio universal. Tras el ataque de una nube bestial que arrebató las runas y la vida de los guardianes, el caos se desató en todas las realidades. 
> 
> **Hoku**, con su alma valiente, ha salido en busca de la nube para recuperar lo perdido. En su camino no solo encontrará desastres; ganará la gratitud de criaturas híbridas, nuevas habilidades y el corazón de muchos.

---

## 🚀 $\color{lightgreen}{\text{Características del Proyecto}}$

* **Arquitectura MVC:** Separación estricta entre la lógica (Modelos) y la representación visual (Vistas).
* **Gráficos Procedurales:** Personajes dibujados 100% mediante código con `Pygame`.
* **Sistema de Combate:** Detección de rango de ataque dinámico y colisiones sólidas. 
* **Bestiario Híbrido:** Criaturas únicas como la *Perruga*, la *Medania* y el jefe *Cabra de Fuego*.

---

## 🎮 $\color{violet}{\text{Instrucciones de Juego}}$

### ⌨️ Mandos y Controles
| Acción | Hoku (Protagonista) | Jefe (Cabra de Fuego) |
| :--- | :--- | :--- |
| **Moverse** | `W` `A` `S` `D` | `↑` `↓` `←` `→` |
| **Atacar** | `Espacio` | (Encuentro Cercano) |

> [!TIP]
> **Rango de combate:** El ataque solo es válido si la distancia entre personajes es menor a **100px**.

---

## 🛠️ $\color{orange}{\text{Desarrollo e Instalación}}$

### ⚙️ Requisitos
* **Python 3.12** o superior.
* **Pip** instalado.

### 📦 Configuración del entorno

### 1. Clonar el repositorio:
```bash
git clone [https://github.com/KORATcs/mi_proyecto.git](https://github.com/KORATcs/mi_proyecto.git)

### 2. Crear un entorno virtual
Para evitar conflictos con otras librerias, crea un entorno aislado:

# En Linux o macOS:
python3 -m venv venv
source venv/bin/activate

# En Windows:
python -m venv venv
venv\Scripts\activate

### 3. Instalar Dependencias
Instala la libreria pase para el motor del juego

pip install pygame

### 🎮 Instrucciones de Juego
Instala la librería base para el motor gráfico:

python3 main.py


| Acción | Hoku (Protagonista) | Jefe (Cabra de Fuego) |
| :--- | :--- | :--- |
| **Moverse** | `W` `A` `S` `D` | `↑` `↓` `←` `→` |
| **Atacar** | `Espacio` | (Encuentro Cercano) |


### Estructura del MVC

mi_proyecto/
├── main.py                # Director de orquesta (Bucle principal)
├── src/
│   ├── modelos/           # Lógica pura: Clases, Vida, Daño (Cerebro)
│   │   └── personajes/
│   └── vistas/            # Gráficos: Dibujos de Pygame y Colores (Cuerpo)
│       └── personaje_grafico.py
└── README.md              # Documentación del proyecto

### 🛠️ Tecnologías
Lenguaje: Python 🐍

Motor: Pygame 🕹️

Paradigma: Programación Orientada a Objetos (POO)

### 🌟 Créditos
Desarrollado con mucha dedicación y café por Camila (Hoku Team).
¡Gracias por explorar este mundo de híbridos! nwn


