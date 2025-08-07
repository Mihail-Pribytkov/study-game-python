from helicopter import Helicopter as Helico
from pynput import keyboard
from map import Map
import time
import os

TICK_SLEEP = 0.11
TREE_UPDATE = 5
FIRE_UPDATE = 10
MAP_W, MAP_H = 20,10

tmp = Map(MAP_W, MAP_H)

helico = Helico(MAP_W, MAP_H)

MOVES = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
def process_key(key):
    global helico
    try:
        c = key.char.lower()
        if c in MOVES:
            dx, dy = MOVES[c][0], MOVES[c][1]
            helico.move(dx, dy)
    except AttributeError:
        pass
    # if key == keyboard.Key.esc:
    #     return False

listener = keyboard.Listener(
    on_press=process_key)
listener.start()

tick = 1
while True:
    os.system("cls")
    print("TICK", tick)
    helico.print_stats()
    tmp.process_helicopter(helico)
    tmp.print_map(helico)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        tmp.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        tmp.update_fires()