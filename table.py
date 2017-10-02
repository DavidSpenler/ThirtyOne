import pyglet

import global_vars

class table():

    def __init__(self):
        self.image = pyglet.resource.image('table.png')
        self.image.width = global_vars.window.width
        self.image.height = global_vars.window.height
        self.sprite = pyglet.sprite.Sprite(self.image,batch=global_vars.batch, group=global_vars.board)
