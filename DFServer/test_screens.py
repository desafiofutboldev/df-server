from time import sleep
from DFServer import ReaccionServer

#python -m DFServer.test_screens

server = ReaccionServer()
server.start()

sleep(1)

while (1):

    server.showDemoIdle()
    sleep(2)
    server.showGameInoperative()
    sleep(2)


