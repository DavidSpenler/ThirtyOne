import pyglet

import global_vars

class knock():

    def __init__(self,x,y):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('knock.png'),batch=global_vars.batch,group=global_vars.front)
        self.sprite.image.anchor_x = self.sprite.image.width/2
        self.sprite.image.anchor_y = self.sprite.image.height/2
        self.sprite.x = x
        self.sprite.y = y
        self.hitbox = [
                    self.sprite.x + self.sprite.image.width/2,
                    self.sprite.x - self.sprite.image.width/2,
                    self.sprite.y + self.sprite.image.height/2,
                    self.sprite.y - self.sprite.image.height/2
                    ]

    def hide(self):
        self.sprite.x = -100
