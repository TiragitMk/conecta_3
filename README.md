# Conecta 4 (o conecta 3)

3 en raya en un tablero 4x4, con múltiples niveles de dificultad y oponentes que aprenden de las jugadas.
Cuestionario en la raíz del repositorio.

## Requisitos

- Python 3.13 o superior
- [uv](https://docs.astral.sh/uv/getting-started/installation/), en uv.lock el resto de dependencias.

## Instalación

```bash
git clone https://github.com/TiragitMk/conecta_3.git
uv sync
```

## Ejecución

```bash
uv run -m conecta_4.conecta4
```

## Cómo jugar

Este juego simula un conecta4 con reglas un poco diferentes. Las fichas se colocan en las diferentes columnas, simulando gravedad.
La elección de jugadas será por tanto entre las diferentes columnas. El primero que alcance una racha de 3 fichas consecutivas
de su mismo tipo en vertical, horizontal, o diagonal, ganará la partida.

No se puede colocar ficha en una columna del tablero que ya está llena, y si el tablero completo se llena sin haber ganador,
se llegará al empate.

El jugador será prompteado para escoger entre partidas Jugador contra IA o partidas IA contra IA.
Si el jugador escoge jugar por sí mismo, se le dará a elegir un nivel de dificultad para la IA. Hay 3 niveles de dificultad:
* **Fácil**: La IA escoge aleatoriamente entre las diferentes casillas posibles.
* **Medio**: La IA puede predecir de manera básica si una jugada le gana o le pierde la partida con un poco de antelación.
* **Difícil**: La IA aprende de sus errores cuando pierde, almacena jugadas, las recataloga y mejora para las próximas partidas.
El aprendizaje se mantiene mientras el juego se encuentre abierto, la memoria no es persistente.

**_Controles_**:

El juego al completo transcurre en la terminal con comandos escritos. Se darán instrucciones durante el desarrollo del juego.

- `s` `n` - Sí / No.
- `0`, `1`, `2`... - Escoger opción.
- `Enter` - Ingresar comando.

Una vez se ha comenzado el game loop, no se puede parar hasta que acabe la partida. Si 
se quiere parar el juego en medio de partida, se debe parar manualmente pulsando `ctrl`+`c` en la terminal.
Ingresar comandos u opciones no contempladas entre las alternativas dispuestas no dará resultado alguno.

**_Cosas a tener en cuenta:_**

* La memoria de la IA que aprende no es persistente.
* Hay un fichero de constantes de ajustes `src/conecta_4/settings.py`. Cambiar estos ajustes puede generar problemas de jugabilidad,
ya que el juego está adaptado de momento para estos ajustes.

## Estructura del proyecto

El proyecto se ha desarrollado con una única librería/módulo, `src/conecta_4`.
En esta librería se ubica el código fuente al completo.

El único fichero que contiene funciones puras es `list_utils.py`. El resto de ficheros hacen uso de objetos (como módulo propio)
que se encuentran en el propio código fuente y cuyo uso se extiende a lo largo de todo el proyecto.

También se puede encontrar un directorio `tests/` en el que se encuentran diversos tests de desarrollo, para usar `pytest`.