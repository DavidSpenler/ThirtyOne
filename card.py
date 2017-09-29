import pyglet
import math
import globvar

class card():

    def __init__(self,x,y,r,gx,gy,gr,gt,type,lastcard,faceup):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('fd.png'),batch=globvar.batch, group=globvar.back)
        self.sprite.image.anchor_x = self.sprite.image.width/2
        self.sprite.image.anchor_y = self.sprite.image.height/2
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.rotation = r
        self.moving = False
        self.goal = (gx,gy,gr,gt)
        self.faceup = faceup
        self.type = type
        self.lastcard = lastcard
        globvar.dobjects.append(self)
        print(type)

    def move(self):
        if (self.sprite.x != self.goal[0] or self.sprite.y != self.goal[1]) and (self.lastcard == None):
            if self.moving == False:
                self.moving = True
                self.sprite.group = globvar.front
                self.distx = self.goal[0]-self.sprite.x
                self.disty = self.goal[1]-self.sprite.y
                self.dist = math.sqrt(self.distx**2+self.disty**2)
                self.speed = self.dist/self.goal[3]
                if self.distx == 0:
                    self.speedx = 0
                    self.speedy = self.speed*(self.disty/abs(self.disty))
                elif self.disty == 0:
                    self.speedy = 0
                    self.speedx = self.speed*(self.distx/abs(self.distx))
                else:
                    self.theta = math.atan(self.disty/self.distx)
                    self.speedx = abs(math.cos(self.theta)*self.speed)*(self.distx/abs(self.distx))
                    self.speedy = abs(math.sin(self.theta)*self.speed)*(self.disty/abs(self.disty))
                    
                self.rot1 = (self.goal[2]-self.sprite.rotation)
                self.rot2 = -360+(self.goal[2]-self.sprite.rotation)
                if self.rot1 > 360 or self.rot1 < -360:
                    self.rot1-=360*((self.rot1-(self.rot1%360))/360)
                if self.rot2 > 360 or self.rot2 < -360:
                    self.rot2-=360*((self.rot2-(self.rot2%360))/360)
                if abs(self.rot1) < abs(self.rot2):
                    self.rot = self.rot1
                else:
                    self.rot = self.rot2
                    
            self.sprite.rotation+=(self.rot/(self.dist/self.speed))
                
            
            if abs(self.goal[0]-self.sprite.x) < abs(self.speedx):
                self.sprite.x = self.goal[0]
                self.sprite.rotation = self.goal[2]
            else:
                self.sprite.x+=self.speedx
            if abs(self.goal[1]-self.sprite.y) < abs(self.speedy):
                self.sprite.y = self.goal[1]
                self.sprite.rotation = self.goal[2]
            else:
                self.sprite.y+=self.speedy
        elif self.sprite.x == self.goal[0] and self.sprite.y == self.goal[1] and self.moving == True:
            self.moving = False
            self.sprite.group = globvar.back
            self.flip()
            for object in globvar.dobjects:
                if object.lastcard == self:
                    object.lastcard = None

    def flip(self):
        if self in globvar.Game.players[0].cards:
            self.faceup = True
        if self.faceup == True:
            self.sprite.image = pyglet.resource.image(self.type+'.png')
        else:
            self.sprite.image = pyglet.resource.image('fd.png')

        self.sprite.image.anchor_x = self.sprite.image.width/2
        self.sprite.image.anchor_y = self.sprite.image.height/2
        self.sprite.x = self.sprite.x
        self.sprite.y = self.sprite.y

    def choose(self):
        if globvar.Game.turn == 'p0':
            if globvar.Game.top == self:
                pass
				#used to be game.bottom
            elif globvar.Game.bottom == self:
                pass
            elif self in globvar.Game.players[0].cards:
                pass
