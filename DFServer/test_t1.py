from time import sleep
from DFServer import TatetiServer

server = TatetiServer()
server.start()

sleep(3)

for cd in range(3,0,-1):
    server.showCountdown(cd)
    sleep(1)

player_turns = [TatetiServer.TatetiPlayer.p1, TatetiServer.TatetiPlayer.p2] * 3
for player in player_turns:
    server.showPlaying(player)
    sleep(1)

player_wins = [TatetiServer.TatetiPlayer.p1, TatetiServer.TatetiPlayer.p2, TatetiServer.TatetiPlayer.tie]
for player in player_wins:
    server.showWinner(player)
    sleep(1)

sleep(10000)