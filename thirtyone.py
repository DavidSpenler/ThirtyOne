import pyglet
from pyglet.window import mouse
import random
import sys
import math
import time

import globvar

globvar.init()

globvar.window = pyglet.window.Window(700,500,caption='Thirty One')

globvar.batch = pyglet.graphics.Batch()

globvar.board = pyglet.graphics.OrderedGroup(0)
globvar.bottom = pyglet.graphics.OrderedGroup(1)
globvar.back = pyglet.graphics.OrderedGroup(2)
globvar.front = pyglet.graphics.OrderedGroup(3)

globvar.dobjects = []

from table import table
from knock import knock
from player import player
from computer import computer
from card import card
from winmsg import winmsg
from game import game

Table = table()
globvar.WinMSG = winmsg(-100,0)
globvar.Knock = knock(200,40)
globvar.Game = game(4)

@globvar.window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT:
        for object in globvar.dobjects:
            hitbox = [
                object.sprite.x + object.sprite.image.width/2,
                object.sprite.x - object.sprite.image.width/2,
                object.sprite.y + object.sprite.image.height/2,
                object.sprite.y - object.sprite.image.height/2
                ]
            if x > hitbox[1] and x < hitbox[0] and y > hitbox[3] and y < hitbox[2]:
                globvar.Game.choose(object)
        if x > globvar.Knock.hitbox[1] and x < globvar.Knock.hitbox[0] and y > globvar.Knock.hitbox[3] and y < globvar.Knock.hitbox[2] and (globvar.Game.newturn == 1 or globvar.Game.newturn == 0) and globvar.Game.turn != -1 and globvar.Game.knocked == False:
            globvar.Game.knock(0)
    
@globvar.window.event
def on_draw():
    globvar.batch.draw()
        

if __name__ == '__main__':
    pyglet.clock.schedule_interval(globvar.Game.update, 1/30)
    pyglet.app.run()
