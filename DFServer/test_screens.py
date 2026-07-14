import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep
from DFServer import ReaccionServer

server = ReaccionServer()
server.start()

sleep(1)

while (1):

    server.showDemoIdle()
    sleep(2)
    server.showGameInoperative()
    sleep(2)


