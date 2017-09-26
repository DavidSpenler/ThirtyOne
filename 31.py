import pyglet
from pyglet.window import mouse
import random
import sys
import math
import time

window = pyglet.window.Window(700,500,caption='Thirty One')

batch = pyglet.graphics.Batch()

board = pyglet.graphics.OrderedGroup(0)
bottom = pyglet.graphics.OrderedGroup(1)
back = pyglet.graphics.OrderedGroup(2)
front = pyglet.graphics.OrderedGroup(3)

class table():

    def __init__(self):
        self.image = pyglet.resource.image('table.png')
        self.image.width = window.width
        self.image.height = window.height
        self.sprite = pyglet.sprite.Sprite(self.image,batch=batch, group=board)

        
class card():

    def __init__(self,x,y,r,gx,gy,gr,gt,type,lastcard,faceup):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('fd.png'),batch=batch, group=back)
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
        dobjects.append(self)
        #print(type)

    def move(self):
        if (self.sprite.x != self.goal[0] or self.sprite.y != self.goal[1]) and (self.lastcard == None):
            if self.moving == False:
                self.moving = True
                self.sprite.group = front
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
            self.sprite.group = back
            self.flip()
            for object in dobjects:
                if object.lastcard == self:
                    object.lastcard = None

    def flip(self):
        if self in Game.players[0].cards:
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
        if Game.turn == 'p0':
            if Game.top == self:
                pass
            elif game.bottom == self:
                pass
            elif self in Game.players[0].cards:
                pass

class player():

    def __init__(self,c1x,c1y,c1r,c2x,c2y,c2r,c3x,c3y,c3r,c4x,c4y,c4r):

        self.cards = [None,None,None]
        
        self.cardp = [
                (c1x,c1y,c1r),
                (c2x,c2y,c2r),
                (c3x,c3y,c3r),
                (c4x,c4y,c4r)
            ]
        

class knock():

    def __init__(self,x,y):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('knock.png'),batch=batch,group=board)
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

class winmsg():

    def __init__(self,x,y):
        print('called')
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('p1.png'),batch=batch,group=front)
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
            self.sprite = pyglet.sprite.Sprite(pyglet.resource.image('p'+str(self.winner+1)+'.png'),batch=batch,group=front)
            self.sprite.image.anchor_x = self.sprite.image.width/2
            self.sprite.image.anchor_y = self.sprite.image.height/2
            self.sprite.x = self.x
            self.sprite.y = self.y
        else:
            self.count+=1
            
    

class fakecard():
    
    def  __init__(self,type):
        self.type = type

class computer():

    def __init__(self,c1x,c1y,c1r,c2x,c2y,c2r,c3x,c3y,c3r,c4x,c4y,c4r):

        self.cards = [None,None,None]
        
        self.cardp = [
                (c1x,c1y,c1r),
                (c2x,c2y,c2r),
                (c3x,c3y,c3r),
                (c4x,c4y,c4r)
            ]

        self.wait = 0
        self.waittime = 30

        self.opponents = [
                [None,None,None],
                [None,None,None],
                [None,None,None]
            ]

        self.top = None
        self.bottom = None
        self.deck = ['ac','as','ah','ad',
                     '2c','2s','2h','2d',
                     '3c','3s','3h','3d',
                     '4c','4s','4h','4d',
                     '5c','5s','5h','5d',
                     '6c','6s','6h','6d',
                     '7c','7s','7h','7d',
                     '8c','8s','8h','8d',
                     '9c','9s','9h','9d',
                     '10c','10s','10h','10d',
                     'jc','js','jh','jd',
                     'qc','qs','qh','qd',
                     'kc','ks','kh','kd',]
        
    def think(self):

        if self.wait == self.waittime:
   
            if Game.turn == Game.players.index(self) and Game.turn == Game.newturn:
                self.value = Game.getsum(self.cards)[0]
                self.average = []
                for opponent in self.opponents:
                    self.unknown = 3
                    for card in opponent:
                        if card != None:
                            self.unknown-=1
                    self.matches = []
                    self.average.append(Game.getsum([x for x in opponent if x != None])[0]+Game.const*(len(opponent)-len([x for x in opponent if x != None])))
                self.rank = 0
                
                for average in self.average:
                    self.rank+=(average-self.value)
                print(self.rank)
                print([x.type for x in self.cards])
                if Game.knocked == False:
                    if self.rank < -30:
                        self.strategy = 'knock' 
                    else:
                        self.strategy = 'shortterm'
                else:
                    self.strategy = 'shortterm'

                if self.strategy == 'knock' and Game.knocked == False:
                    print(Game.turn,Game.players.index(self))
                    Game.knock(Game.players.index(self))
                elif self.strategy == 'shortterm':
                    self.sumb = 0
                    self.sumts = []
                    self.sumt = 0
                    self.discardb = []
                    self.discardts = []
                    self.discardt = None
                    for card in self.cards:
                        if Game.getsum([x for x in self.cards if x != card]+[Game.bottom])[0] > self.sumb:
                            self.sumb = Game.getsum([x for x in self.cards if x != card]+[Game.bottom])[0]
                            self.discardb = card
                    for card1 in self.deck:
                        self.sumts.append(0)
                        for card2 in self.cards:
                            if Game.getsum([x for x in self.cards if x != card2]+[fakecard(card1)])[0] > self.sumts[self.deck.index(card1)]:
                                self.sumts[self.deck.index(card1)] = Game.getsum([x for x in self.cards if x != card2]+[fakecard(card1)])[0]
                    for match in self.sumts:
                        self.sumt+=match
                    self.averaget = self.sumt/len(self.sumts)
                    if self.averaget > self.sumb:
                        Game.choose(Game.top)
                    else:
                        Game.choose(Game.bottom)
                self.wait = 0
            elif Game.turn == 'r'+str(Game.players.index(self)) and Game.turn == Game.newturn:
                self.gsum = 0
                self.gsum2 = 0
                self.discard = None
                #print(self.cards[:3])
                for card in self.cards[:3]:
                    #print(Game.getsum(self.cards))
                    if Game.getsum([x for x in self.cards if x != card])[0] > self.gsum:
                        self.gsum = Game.getsum([x for x in self.cards if x != card])[0]
                        self.gsum2 = Game.getsum([x for x in self.cards if x != card])[1]
                        self.discard = card
                    elif Game.getsum([x for x in self.cards if x != card])[0] == self.gsum and Game.getsum([x for x in self.cards if x != card])[1] > self.gsum2:
                        self.gsum = Game.getsum([x for x in self.cards if x != card])[0]
                        self.gsum2 = Game.getsum([x for x in self.cards if x != card])[1]
                        self.discard = card
                Game.choose(self.discard)
                #print('chosen')
                self.rank = 0
                for average in self.average:
                    self.rank+=(average-Game.getsum(self.cards)[0])
                print(self.rank)
                if self.rank < -30 and Game.knocked == False:
                    Game.knock(Game.players.index(self))
                    
                self.wait = 0
        elif (Game.turn == Game.players.index(self) or Game.turn == 'r'+str(Game.players.index(self))) and Game.turn == Game.newturn:
            self.wait+=1

    def observedr(self,player,card):
        self.list = []
        for x in range(0,len(Game.players)):
            self.list.append(x)
        self.list.remove(Game.players.index(self))
        self.opponents[self.list.index(player)].append(card.type)

    def observedi(self,player,card):
        if card.type in self.deck:
            self.deck.remove(card.type)
        self.list = []
        for x in range(0,len(Game.players)):
            self.list.append(x)
        self.list.remove(Game.players.index(self))
        if card in self.opponents[self.list.index(player)]:
            self.opponents[self.list.index(player)][self.opponents[self.list.index(player)].index(card)] = None
        
class game():

    def __init__(self,players):
        self.players = []
        self.players.append(player(400,40,0,350,40,0,300,40,0,350,120,0))
        if players == 2:
            self.players.append(computer(300,460,180,350,460,180,400,460,180,350,380,180))
        elif players == 3:
            self.players.append(computer(40,200,90,40,250,90,40,300,90,120,250,90,120,250,90))
            self.players.append(computer(660,200,270,660,250,270,660,300,270,580,250,270))
        elif players == 4:
            self.players.append(computer(40,200,90,40,250,90,40,300,90,120,250,90))
            self.players.append(computer(300,460,180,350,460,180,400,460,180,350,380,180))
            self.players.append(computer(660,300,270,660,250,270,660,200,270,580,250,270))

        self.top = None
        self.bottom  = None
        self.behind = None
                
        self.deck = ['ac','as','ah','ad',
                     '2c','2s','2h','2d',
                     '3c','3s','3h','3d',
                     '4c','4s','4h','4d',
                     '5c','5s','5h','5d',
                     '6c','6s','6h','6d',
                     '7c','7s','7h','7d',
                     '8c','8s','8h','8d',
                     '9c','9s','9h','9d',
                     '10c','10s','10h','10d',
                     'jc','js','jh','jd',
                     'qc','qs','qh','qd',
                     'kc','ks','kh','kd',]
        
        self.turn = -1
        self.newturn = -1
        self.lastturn = None
        self.knocked = False
        self.const = 3.25

        self.deal()
        
    def deal(self):
        #print('dealing')
        type = random.choice(self.deck)
        self.deck.remove(type)
        self.top = card(375,250,0,375,250,0,0,type,None,False)
        for p in self.players:
            for c in range(0,3):
                type = random.choice(self.deck)
                self.deck.remove(type)
                self.lastcard = None
                if c == 0:
                    self.lastcard = self.players[self.players.index(p)-1].cards[2]
                else:
                    self.lastcard = p.cards[c-1]
                    
                p.cards[c] = card(375,250,0,p.cardp[c][0],p.cardp[c][1],p.cardp[c][2],10.5,type,self.lastcard,False)
        #print('flipping')
        type = random.choice(self.deck)
        self.deck.remove(type)
        self.bottom = card(375,250,0,325,250,0,10.5,type,self.players[len(self.players)-1].cards[2],True)
        self.newturn = 0

    def choose(self,cardt):
        if str(self.turn)[0] != 'r' and self.turn == self.newturn:
            if cardt == self.top:
                #print('top card')
                self.top.goal = (self.players[self.turn].cardp[3][0],self.players[self.turn].cardp[3][1],self.players[self.turn].cardp[3][2],10.5)
                self.players[self.turn].cards.append(self.top)
                type = random.choice(self.deck)
                self.deck.remove(type)
                self.top = card(375,250,0,375,250,0,0,type,None,False)
                self.newturn = 'r'+str(self.turn)
            elif cardt == self.bottom:
                for player in self.players:
                    if 'observedr' in dir(player) and int(self.turn) != Game.players.index(player):
                        player.observedr(int(self.turn),cardt)
                #print('bottom card')
                self.bottom.goal = (self.players[self.turn].cardp[3][0],self.players[self.turn].cardp[3][1],self.players[self.turn].cardp[3][2],10.5)
                self.players[self.turn].cards.append(self.bottom)
                self.newturn = 'r'+str(self.turn)
                self.bottom = None
        elif str(self.turn)[0] == 'r' and self.turn == self.newturn and cardt in self.players[int(str(self.turn)[1])].cards[:3]:
            for player in self.players:
                if 'observedi' in dir(player) and int(self.turn[1]) != Game.players.index(player):
                    player.observedi(int(self.turn[1]),cardt)
            self.players[int(self.turn[-1:])].cards[3].goal = cardt.goal
            self.players[int(self.turn[-1:])].cards[3].faceup = False
            self.players[int(self.turn[-1:])].cards[3].lastcard = cardt
            self.players[int(self.turn[-1:])].cards.remove(cardt)
            cardt.goal = (325,250,0,10.5)
            cardt.faceup = True
            cardt.flip()
            if self.bottom != None:
                if self.behind != None:
                    self.behind.sprite.batch = None
                self.behind = self.bottom
                self.behind.sprite.group = bottom
            self.bottom = cardt
            if self.bottom != None:
                pass
                #print('bottom: ',self.bottom.type,self.bottom.sprite.group)
            if self.behind != None:
                pass
                #print('behind: ',self.behind.type,self.behind.sprite.group)
            self.newturn = (int(self.turn[1])+1)%4
            

    def moving(self):
        for object in dobjects:
            if object.moving or object.lastcard != None:
                return True
        return False

    def knock(self,player):
        #print('knocked')
        self.lastturn = player
        #print(self.turn,player)
        if self.turn == player:
            self.turn=(self.turn+1)%4
            self.newturn = self.turn
        #print(self.turn)
        self.knocked = True
        Knock.hide()
        self.hand = self.players[player].cards
        self.sum = 0
        for card in self.hand:
            if card.type[:-1] == 'a':
                self.sum+=11
            elif card.type[:-1] == 'k' or card.type[:-1] == 'q' or card.type[:-1] == 'j' or card.type[:-1] == '10':
                self.sum+=10
        if self.hand[0].type[-1] == self.hand[1].type[-1] and self.hand[1].type[-1] == self.hand[2].type[-1] and self.sum == 31:
            self.win()
        
    def getsum(self,cards):
        self.suit = ['c','d','h','s']
        self.face = ['j','q','k']
        self.gsum = [0,0,0,0]
        self.psum = 0
        for suit in self.suit:
            for card in cards:
                if type(card) != str:
                    cardh = card.type
                else:
                    cardh = card
                if cardh[-1] == suit:
                    if cardh[:-1] in self.face:
                        self.gsum[self.suit.index(suit)]+=10
                    elif cardh[:-1] == 'a':
                        self.gsum[self.suit.index(suit)]+=11
                    else:
                        self.gsum[self.suit.index(suit)]+=float(cardh[:-1])
        self.finalsum = []
        while len(self.gsum) != 0:
            grt = None
            for item in self.gsum:
                if grt == None or item > grt:
                    grt = item
            self.gsum.remove(grt)
            self.finalsum.append(grt)
        self.gsum = self.finalsum
        ##print(self.gsum)
        if len(cards) == 3:
            if type(cards[0]) != str:
                if cards[0].type[:-1] == cards[1].type[:-1] and cards[1].type[:-1] == cards[2].type[:-1] and self.gsum[0] < 31:
                    self.gsum = [30,0,0,0]
            else:
                if cards[0][:-1] == cards[1][:-1] and cards[1][:-1] == cards[2][:-1] and self.gsum[0] < 31:
                    self.gsum = [30,0,0,0]
        return self.gsum
            
    def win(self):
        #print('choose winner')

        self.wsum = 0
        self.winner = None
        for player in self.players:
            self.sum = self.getsum(player.cards)
            print(self.sum[0])
            for card in player.cards:
                card.faceup = True
                card.flip()
            if self.sum[0] > self.wsum:
                self.wsum = self.sum[0]
                self.winner = self.players.index(player)
                batch.draw()
        WinMSG.winner = self.winner
        print('Player ',self.winner+1,' wins!')
        self.turn = 'en'
        self.newturn = 'en'

    def update(self,dt):
        ##print(self.turn)
        window.clear()
        for object in dobjects:
            object.move()
        if self.turn == self.lastturn and self.knocked == True and self.moving() == False:
            self.win()
        if self.turn != self.newturn and self.moving() == False:
            self.turn = self.newturn
            if self.turn == 0 and self.const < 5:
                self.const+=0.3
        if WinMSG.winner != None:
            WinMSG.show()
        for p in range(1,len(self.players)):
            self.players[p].think()
                
        
            

dobjects = []

Table = table()
WinMSG = winmsg(-100,0)
Knock = knock(200,40)
Game = game(4)

@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT and Game.turn != 'en':
        for object in dobjects:
            hitbox = [
                object.sprite.x + object.sprite.image.width/2,
                object.sprite.x - object.sprite.image.width/2,
                object.sprite.y + object.sprite.image.height/2,
                object.sprite.y - object.sprite.image.height/2
                ]
            if x > hitbox[1] and x < hitbox[0] and y > hitbox[3] and y < hitbox[2]:
                Game.choose(object)
        if x > Knock.hitbox[1] and x < Knock.hitbox[0] and y > Knock.hitbox[3] and y < Knock.hitbox[2] and (Game.newturn == 1 or Game.newturn == 0) and Game.turn != -1 and Game.knocked == False:
            Game.knock(0)
    
@window.event
def on_draw():
    batch.draw()
        

if __name__ == '__main__':
    pyglet.clock.schedule_interval(Game.update, 1/60)
    pyglet.app.run()
