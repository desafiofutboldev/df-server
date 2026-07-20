from time import sleep
from DFServer import ReaccionServer
from DFServer.DFBaseServer import DFBaseServer

server = ReaccionServer()
server.start()

lastScreen = None

while True:
    currentScreen = server.currentScreen

    if currentScreen != lastScreen:
        if currentScreen == DFBaseServer.DFGenericScreens.idle:
            print("Pantalla: idle")
        elif currentScreen == DFBaseServer.DFGenericScreens.calibracion:
            print("Pantalla: calibración")

        lastScreen = currentScreen

    sleep(0.2)
