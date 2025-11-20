# Server genérico para DF

Este repo contiene:
* Un módulo de Python general, que inicializa y carga la plantilla de server, junto con las screens relevantes para el juego. Este modulo no se corre por sí mismo, sino que se hereda en una clase contenida en ```<Juego>Server.py``` que implementa los métodos necesarios para actualizar los gráficos del juego en cuestión.
* Un template ```/templates/totem.html``` que contiene las dos screens comunes a todos los juegos (idle y contador)
* Cuatro tipos de screens que aplican a diferentes juegos (especificados en 'Tipos de plantillas')

### Tipos de plantillas
Tipo 1: 
* tateti

Tipo 2: 
* ~~postes tiempo~~

Tipo 3: 
* postes pasadas
* aros basket
* arquero
* puntería
* reacción
* octógono
* autopase
* fuerza
* rampa

Tipo 4:
* potencia
* salto
* postes tiempo
* velocidad