from .DFBaseServer import DFBaseServer, DFType3Server, DFType4Server, Enum

# Type1

class TatetiServer(DFBaseServer):

    class TatetiPlayer(Enum):
        p1 = 'jugador 1'
        p2 = 'jugador 2'
        tie = 'empate'

    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            clientType = DFBaseServer.DFBaseServerType.type1,
            gameName = 'tateti',
            host = host,
            port = port)

    def showPlaying(self, player : TatetiPlayer):
        if not isinstance(player, TatetiServer.TatetiPlayer):
            raise ValueError("player must be of type 'TatetiServer.TatetiPlayer")

        if player == TatetiServer.TatetiPlayer.p1:
            currScreen = DFBaseServer.DFType1Screens.playingP1
        else:
            currScreen = DFBaseServer.DFType1Screens.playingP2
        
        self._showScreen(currScreen)

    def showWinner(self, player : TatetiPlayer):
        if not isinstance(player, TatetiServer.TatetiPlayer):
            raise ValueError("player must be of type 'TatetiServer.TatetiPlayer")
        
        if player == TatetiServer.TatetiPlayer.p1:
            currScreen = DFBaseServer.DFType1Screens.finishedP1
        elif player == TatetiServer.TatetiPlayer.p2:
            currScreen = DFBaseServer.DFType1Screens.finishedP2
        else:
            currScreen = DFBaseServer.DFType1Screens.finishedTie

        self._showScreen(currScreen)

# Type 3

class ArosServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'aros basket',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class ArqueroServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'arquero',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class AutopaseServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'autopase',
            gameUnit = 'pases',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class FuerzaServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'fuerza',
            gameUnit = 'kgf',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class OctogonoServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'octógono',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class PostesPasadasServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'postes pasadas',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class PunteriaServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'puntería',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class RampaServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'rampa',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

class ReaccionServer(DFType3Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'reacción',
            gameUnit = 'puntos',
            lowTimeThr = 15,
            host = host,
            port = port
        )

"""
* aros basket
* arquero
* autopase
* fuerza
* octógono
* postes pasadas
* puntería
* rampa
* reacción
"""

# Type 4

class PostesTiempoServer(DFType4Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'postes tiempo',
            gameUnit = '',
            playingTitle = 'midiendo el tiempo',
            host = host,
            port = port
        )

    def __seconds2Str(self, seconds : int | float):
        return f'{int(seconds / 60)}:{str(int(seconds % 60))[:2]}'

    # method overrides
    def showPlaying(self, elapsedSeconds : int):
        """
        Shows the active game screen.
        """
        currScreen = DFBaseServer.DFType4Screens.playing
        self._showScreen(currScreen)
        self._updateParam('score',self.__seconds2Str(elapsedSeconds))

    def showFinished(self, finalSeconds : int, recordSeconds : None | int = None):
        """
        Shows the game finished screen. The 'no new record' screen is shown if only 'finalScore' is provided, or if 'recordScore' is less than or equal to 'finalScore'. Otherwise, the 'new record' screen is shown.
        """
        if recordSeconds is None:
            recordSeconds = finalSeconds

        if finalSeconds <= recordSeconds:
            currScreen = DFBaseServer.DFType4Screens.finishedNormal
        else:
            currScreen = DFBaseServer.DFType4Screens.finishedRecord
        
        self._showScreen(currScreen)
        self._updateParam('finalScore',f'{self.__seconds2Str(finalSeconds)} {self._gameUnit}')
        self._updateParam('recordScore',f'récord: {self.__seconds2Str(recordSeconds)} {self._gameUnit}')

class PotenciaServer(DFType4Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'potencia',
            gameUnit = 'kgf',
            playingTitle = 'potencia',
            host = host,
            port = port
        )

class SaltoServer(DFType4Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'salto',
            gameUnit = 'cm',
            playingTitle = 'altura',
            host = host,
            port = port
        )

class VelocidadServer(DFType4Server):
    def __init__(self, host = '127.0.0.1', port = 5000):
        super().__init__(
            gameName = 'velocidad',
            gameUnit = 'km/h',
            playingTitle = 'velocidad',
            host = host,
            port = port
        )