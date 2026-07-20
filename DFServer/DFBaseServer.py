from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread, Event
from time import sleep
from os import path
import os
from enum import Enum
from datetime import datetime, date    


class DFBaseServer():

    class DFBaseServerType(Enum):
        type1 = 'type1'
        type2 = 'type2'
        type3 = 'type3'
        type4 = 'type4'

    class DFGenericScreens(Enum):
        idle = 'idle'
        demoIdle = 'demoIdle'
        loading = 'loading'
        levelSelection = 'levelSelection'
        gameInoperative = 'gameInoperative'
        calibracion = 'calibracion'

    class DFType1Screens(Enum):
        playingP1 = 'playing-p1'
        playingP2 = 'playing-p2'
        finishedP1 = 'finished-p1'
        finishedP2 = 'finished-p2'
        finishedTie = 'finished-tie'

    class DFType2Screens(Enum): # not used anymore - TODO: delete from everywhere
        playing = 'playing'
        finishedNormal = 'finished-normal'
        finishedRecord = 'finished-record'

    class DFType3Screens(Enum):
        playing = 'playing'
        playingLowTime = 'playing-lowtime'
        finishedNormal = 'finished-normal'
        finishedRecord = 'finished-record'

    class DFType4Screens(Enum):
        playing = 'playing'
        finishedNormal = 'finished-normal'
        finishedRecord = 'finished-record'
        

    def openLog(self):
        actual = date.today().isoformat()
        now = datetime.now().strftime("%H:%M:%S")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "log.txt")

        with open(config_path, "a") as f:
            f.write(f"Dia: {actual}\n")
            f.write(f"Inicio: {now}\n") 

    def closeLog(self):
        now = datetime.now().strftime("%H:%M:%S")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "log.txt")

        with open(config_path, "a") as f:
            f.write(f"Finalizacion: {now}\n") 
            f.write("----------------------------\n")
        
    def __init__(
            self, 
            clientType : DFBaseServerType, 
            gameName : str, 
            gameUnit = None, 
            playingTitle = None, 
            host = '127.0.0.1', 
            port = 5000
            ):
        """
        This class is only meant to be inherited by the servers corresponding to each game, as it implements the common server functionality.

        Parameters:
        * clientType: the type of html client to load (1-4). It should be selected via the contained 'DFBaseServerType' class
        * gameName: the name the game will show when in idle state
        * gameUnit: the unit that will accompany the score of the user (does not apply to all games)
        * playingTitle: (only type 4) - the title that will accompany the playing screen
        * host (str): the URL in which the server will host the client
        * port (int): the port in which the server will host the client
        """

        if not isinstance(clientType, DFBaseServer.DFBaseServerType):
            raise ValueError("clientType must be of type 'DFBaseServerType'")

        self.__app = Flask(__name__)
        self._socketio = SocketIO(self.__app)
        self.__host = host
        self.__port = port
        self.__gameName = gameName
        self._gameUnit = gameUnit
        self.__clientType = clientType

        self.__serverRunning = False

        dir = path.join(path.dirname(path.abspath(__file__)),'screens_generic')
        with open(path.join(dir, 'screens_generic.html'),'r', encoding='utf-8') as f:
            self.__screens_content = f.read()
        with open(path.join(dir,f'screens_{clientType.value}.html'), 'r', encoding='utf-8') as f:
            self.__screens_content += f.read()

        @self.__app.route('/')
        def __renderTotem():
            return render_template('totem.html', screensContent = self.__screens_content, gameName = self.__gameName, gameUnit = gameUnit, playingTitle = playingTitle)
        self._level_event = Event()
        self._selected_level = None

        # Registrar evento SocketIO para recibir nivel
        @self._socketio.on('levelSelected')
        def _handle_level_selection(level):
            print(f'[Servidor] Nivel seleccionado: {level}')
            self._selected_level = int(level)
            self._level_event.set()

        # Registrar evento SocketIO para pedido de calibración (botón 'modo' con clave validada en el cliente)
        @self._socketio.on('calibrationRequested')
        def _handle_calibration_requested():
            print('[Servidor] Calibración solicitada')
            self.showCalibration()

        # Registrar evento SocketIO para salir de calibración (botón 'modo' en esa pantalla, sin clave)
        @self._socketio.on('calibrationExitRequested')
        def _handle_calibration_exit_requested():
            print('[Servidor] Salida de calibración solicitada')
            self.showIdle()

        # Al conectarse un cliente, se le informa la pantalla actual (evita que se quede en 'idle' si se conecta/recarga después de un cambio de pantalla)
        @self._socketio.on('connect')
        def _handle_connect():
            if hasattr(self, '_lastScreen'):
                self._socketio.emit('changeScreen', {'screenId': self._lastScreen.value})

    @property
    def currentScreen(self):
        """
        The screen currently being shown to the client (a DFGenericScreens or DFType<N>Screens member).
        """
        return self._lastScreen

    def __server(self):
        self._socketio.run(self.__app, self.__host, self.__port, use_reloader = False, allow_unsafe_werkzeug = True)

    def start(self):
        """
        Starts the already configured server. Only callable once.
        """
        if self.__serverRunning == False:
            self.__serverRunning = True
            self.__serverThread = Thread(target = self.__server)
            self.__serverThread.daemon = True
            self.__serverThread.start()
            self._lastScreen = DFBaseServer.DFGenericScreens.idle
            self.showIdle()
        else:
            raise RuntimeError('Server was already started')

    def showIdle(self):
        """
        Shows the idle screen. No parameters.
        """
        currScreen = DFBaseServer.DFGenericScreens.idle
        if currScreen != self._lastScreen:
            self._showScreen(currScreen)
            self._lastScreen = currScreen

    def showDemoIdle(self):
        """
        Shows the demo mode idle screen. No parameters.
        """
        currScreen = DFBaseServer.DFGenericScreens.demoIdle
        if currScreen != self._lastScreen:
            self._showScreen(currScreen)
            self._lastScreen = currScreen

    def showCalibration(self):
        """
        Shows the calibration screen (accessed via the 'modo' button on the idle screen). No parameters.
        """
        currScreen = DFBaseServer.DFGenericScreens.calibracion
        if currScreen != self._lastScreen:
            self._showScreen(currScreen)
            self._lastScreen = currScreen

    def showGameInoperative(self):
        """
        Shows the game inoperative (no connectivity / needs support) screen. No parameters.
        """
        currScreen = DFBaseServer.DFGenericScreens.gameInoperative
        if currScreen != self._lastScreen:
            self._showScreen(currScreen)
            self._lastScreen = currScreen

    def showCountdown(self, remainingSecs : int):
        """
        Shows the countdown screen.

        remainingSecs: the amount of time to be shown.
        """
        currScreen = DFBaseServer.DFGenericScreens.loading
        if currScreen != self._lastScreen:
            self._showScreen(currScreen)
            self._lastScreen = currScreen
        self._updateParam('countdownTimer',remainingSecs)

    def levelSelection(self) -> int:
        self._level_event.clear()

        currScreen = DFBaseServer.DFGenericScreens.levelSelection
        if currScreen != self._lastScreen:
            self._showScreen(currScreen)
            self._lastScreen = currScreen
        print("[Servidor] Esperando selección de nivel...")
        self._level_event.wait() 
        print(f"[Servidor] Nivel recibido: {self._selected_level}")
        return self._selected_level

    
    def _showScreen(self, screen : DFGenericScreens | DFType1Screens | DFType2Screens | DFType3Screens | DFType4Screens):
        """
        Shows a specific screen on the client. The screen must be provided via the builtin DF<...>Screens ('Generic' or 'TypeN' with N being the option selected at server setup)
        """
        if not (
            isinstance(screen, DFBaseServer.DFGenericScreens) or
            isinstance(screen, DFBaseServer.DFType1Screens) and self.__clientType == DFBaseServer.DFBaseServerType.type1 or
            isinstance(screen, DFBaseServer.DFType2Screens) and self.__clientType == DFBaseServer.DFBaseServerType.type2 or
            isinstance(screen, DFBaseServer.DFType3Screens) and self.__clientType == DFBaseServer.DFBaseServerType.type3 or
            isinstance(screen, DFBaseServer.DFType4Screens) and self.__clientType == DFBaseServer.DFBaseServerType.type4
            ):
            raise ValueError(f"'screen' must be of 'DFGenericScreens' or 'DF{self.__clientType.value}Screens' type")
        
        if self._lastScreen != screen:
            self._socketio.emit('changeScreen',{'screenId': screen.value})
            self._lastScreen = screen

    def _updateParam(self, paramClass : str, paramValue : any):
        """
        Abstraction provided to update a specific parameter with class 'paramClass' with the value 'paramVal' on the client. Does not guarantee that the relevant screen will be shown when updating.
        """
        self._socketio.emit('updateParam',{'paramClass':paramClass, 'paramValue': paramValue})

class DFType3Server(DFBaseServer):
    """
    Template for the games that use a type 3 server. Must be inherited by the class visible to the game and should not used directly.
    """
    def __init__(self, gameName : str, gameUnit : str, lowTimeThr : int = 15, host = '127.0.0.1', port = 5000):
        super().__init__(
            clientType = DFBaseServer.DFBaseServerType.type3,
            gameName = gameName,
            gameUnit = gameUnit,
            host = host, 
            port = port,
            )
        
        self.__lowTimeThr = lowTimeThr
    
    def showPlaying(self, score : int = -1, remainingSecs : int = -1):
        """
        Shows the active game screen. This function accepts both 'only score' or 'only remaining time' calls, but doesn't update the screen (only data) unless a valid 'remainingSecs' is provided.
        """

        if -1 < remainingSecs <= self.__lowTimeThr:
            currScreen = DFBaseServer.DFType3Screens.playingLowTime
            self._showScreen(currScreen)
        elif remainingSecs != -1:
            currScreen = DFBaseServer.DFType3Screens.playing
            self._showScreen(currScreen)
        
        if score != -1:
            score = round(score, 2) #numeros con coma limitados a 2 decimales
            self._updateParam('score',score)
        if remainingSecs != -1:
            self._updateParam('countdownTimer',remainingSecs)

    def showFinished(self, finalScore : any, recordScore : any = None):
        """
        Shows the game finished screen. The 'no new record' screen is shown if only 'finalScore' is provided, or if 'recordScore' is less than or equal to 'finalScore'. Otherwise, the 'new record' screen is shown.
        """
        if recordScore is None:
            recordScore = finalScore

        #numeros con coma limitados a 2 decimales
        finalScore = round(finalScore,2)
        recordScore = round(recordScore,2)

        if finalScore <= recordScore:
            currScreen = DFBaseServer.DFType3Screens.finishedNormal
        else:
            currScreen = DFBaseServer.DFType3Screens.finishedRecord
        
        self._showScreen(currScreen)
        self._updateParam('finalScore',f'{finalScore} {self._gameUnit}')
        self._updateParam('recordScore',f'récord: {recordScore} {self._gameUnit}')

class DFType4Server(DFBaseServer):
    """
    Template for the games that use a type 4 server. Must be inherited by the class visible to the game and should not used directly.
    """
    def __init__(self, gameName : str, gameUnit : str, playingTitle : str, host = '127.0.0.1', port = 5000):
        super().__init__(
            clientType = DFBaseServer.DFBaseServerType.type4,
            gameName = gameName,
            gameUnit = gameUnit,
            playingTitle = playingTitle,
            host = host,
            port = port
        )

    def showPlaying(self, score : int | float):
        """
        Shows the active game screen.
        """
        currScreen = DFBaseServer.DFType4Screens.playing
        self._showScreen(currScreen)
        score = round(score, 2) #numeros con coma limitados a 2 decimales
        self._updateParam('score',score)

    def showFinished(self, finalScore : int | float, recordScore : None | int | float = None):
        """
        Shows the game finished screen. The 'no new record' screen is shown if only 'finalScore' is provided, or if 'recordScore' is less than or equal to 'finalScore'. Otherwise, the 'new record' screen is shown.
        """
        if recordScore is None:
            recordScore = finalScore

        #numeros con coma limitados a 2 decimales
        finalScore = round(finalScore,2)
        recordScore = round(recordScore,2)

        if finalScore <= recordScore:
            currScreen = DFBaseServer.DFType4Screens.finishedNormal
        else:
            currScreen = DFBaseServer.DFType4Screens.finishedRecord
        
        self._showScreen(currScreen)
        self._updateParam('finalScore',f'{finalScore} {self._gameUnit}')
        self._updateParam('recordScore',f'récord: {recordScore} {self._gameUnit}')