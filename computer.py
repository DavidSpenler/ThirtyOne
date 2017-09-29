import pyglet
import random
import globvar

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
                (None,None,None),
                (None,None,None),
                (None,None,None),
                (None,None,None)
            ]
        
    def think(self):
        if self.wait == self.waittime:
            if globvar.Game.turn == globvar.Game.players.index(self) and globvar.Game.turn == globvar.Game.newturn:
                choice = random.randint(1,2)
                if choice == 1:
                    globvar.Game.choose(globvar.Game.top)
                else:
                    globvar.Game.choose(globvar.Game.bottom)
                self.wait = 0
            elif globvar.Game.turn == 'r'+str(globvar.Game.players.index(self)) and globvar.Game.turn == globvar.Game.newturn:
                globvar.Game.choose(self.cards[random.randint(0,2)])
                if random.randint(1,8) == 1 and globvar.Game.knocked == False:
                    globvar.Game.knock(globvar.Game.players.index(self))
                self.wait = 0
        elif (globvar.Game.turn == globvar.Game.players.index(self) or globvar.Game.turn == 'r'+str(globvar.Game.players.index(self))) and globvar.Game.turn == globvar.Game.newturn:
            self.wait+=1

    def observe(self,card,player):
        pass
