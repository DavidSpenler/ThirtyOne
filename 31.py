import pyglet
from pyglet.window import mouse

import random
import sys
import math
import time

from knock import knock
from table import table
from winmsg import winmsg
from player import player
from computer import computer
from card import card
from game import game
from fakecard import fakecard

import global_vars

global_vars.init()
global_vars.window = pyglet.window.Window(700,500,caption='Thirty One')
	
global_vars.batch = pyglet.graphics.Batch()

global_vars.board = pyglet.graphics.OrderedGroup(0)
global_vars.bottom = pyglet.graphics.OrderedGroup(1)
global_vars.back = pyglet.graphics.OrderedGroup(2)
global_vars.front = pyglet.graphics.OrderedGroup(3)

global_vars.dobjects = []

global_vars.Table = table()
global_vars.WinMSG = winmsg(-100,0)
global_vars.Knock = knock(200,40)
global_vars.Game = game(4)


                
@global_vars.window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT and global_vars.Game.turn != 'en':
        for object in global_vars.dobjects:
            hitbox = [
                object.sprite.x + object.sprite.image.width/2,
                object.sprite.x - object.sprite.image.width/2,
                object.sprite.y + object.sprite.image.height/2,
                object.sprite.y - object.sprite.image.height/2
                ]
            if x > hitbox[1] and x < hitbox[0] and y > hitbox[3] and y < hitbox[2]:
                global_vars.Game.choose(object)
        if x > global_vars.Knock.hitbox[1] and x < global_vars.Knock.hitbox[0] and y > global_vars.Knock.hitbox[3] and y < global_vars.Knock.hitbox[2] and (global_vars.Game.newturn == 1 or global_vars.Game.newturn == 0) and global_vars.Game.turn != -1 and global_vars.Game.knocked == False:
            global_vars.Game.knock(0)
    
@global_vars.window.event
def on_draw():
    global_vars.batch.draw()
        

if __name__ == '__main__':
    pyglet.clock.schedule_interval(global_vars.Game.update, 1/30)
    pyglet.app.run()
