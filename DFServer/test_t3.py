from time import sleep, perf_counter
from random import random
from DFServer import *

server = RampaServer()
server.start()

sleep(6)

for cd in range(3,0,-1):
    server.showCountdown(cd)
    sleep(1)

prev_pc = perf_counter()
next_pc = perf_counter() + random()
remaining_secs = 20
score = 0

server.showPlaying(score, remaining_secs)

while remaining_secs >= 0:
    curr_pc = perf_counter()

    if curr_pc - prev_pc >= 1:
        prev_pc = curr_pc
        remaining_secs -= 1
        server.showPlaying(remainingSecs = remaining_secs)
    
    if curr_pc >= next_pc:
        next_pc += random()
        score += 1
        server.showPlaying(score = score)

server.showFinished(score, 100)

sleep(1)