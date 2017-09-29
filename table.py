import pyglet
import globvar

class table():

    def __init__(self):
        self.image = pyglet.resource.image('table.png')
        self.image.width = globvar.window.width
        self.image.height = globvar.window.height
        self.sprite = pyglet.sprite.Sprite(self.image,batch=globvar.batch, group=globvar.board)
