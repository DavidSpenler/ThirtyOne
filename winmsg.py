import pyglet

import global_vars

class winmsg():

    def __init__(self,x,y):
        print('called')
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('p1.png'),batch=global_vars.batch,group=global_vars.front)
        self.sprite.image.anchor_x = self.sprite.image.width/2
        self.sprite.image.anchor_y = self.sprite.image.height/2
        self.sprite.x = x
        self.sprite.y = y
        self.count = 0
        self.winner = None

    def show(self):
        if self.count >= 30:
            self.shown = True
            if self.winner == 0:
                self.x = 350
                self.y = 150
            elif self.winner == 1:
                self.x = 190
                self.y = 250
            elif self.winner == 2:
                self.x = 350
                self.y = 350
            elif self.winner == 3:
                self.x = 510
                self.y = 250
            self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('p'+str(self.winner+1)+'.png'),batch=global_vars.batch,group=global_vars.front)
            self.sprite.image.anchor_x = self.sprite.image.width/2
            self.sprite.image.anchor_y = self.sprite.image.height/2
            self.sprite.x = self.x
            self.sprite.y = self.y
        else:
            self.count+=1
