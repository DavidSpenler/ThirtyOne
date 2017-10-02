import pyglet

from fakecard import fakecard
import global_vars

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
   
            if global_vars.Game.turn == global_vars.Game.players.index(self) and global_vars.Game.turn == global_vars.Game.newturn:
                self.value = global_vars.Game.getsum(self.cards)[0]
                self.average = []
                for opponent in self.opponents:
                    self.unknown = 3
                    for card in opponent:
                        if card != None:
                            self.unknown-=1
                    self.matches = []
                    self.average.append(global_vars.Game.getsum([x for x in opponent if x != None])[0]+global_vars.Game.const*(len(opponent)-len([x for x in opponent if x != None])))
                self.rank = 0
                
                for average in self.average:
                    self.rank+=(average-self.value)
                print(self.rank)
                print([x.type for x in self.cards])
                if global_vars.Game.knocked == False:
                    if self.rank < -30:
                        self.strategy = 'knock' 
                    else:
                        self.strategy = 'shortterm'
                else:
                    self.strategy = 'shortterm'

                if self.strategy == 'knock' and global_vars.Game.knocked == False:
                    print(global_vars.Game.turn,global_vars.Game.players.index(self))
                    global_vars.Game.knock(global_vars.Game.players.index(self))
                elif self.strategy == 'shortterm':
                    self.sumb = 0
                    self.sumts = []
                    self.sumt = 0
                    self.discardb = []
                    self.discardts = []
                    self.discardt = None
                    for card in self.cards:
                        if global_vars.Game.getsum([x for x in self.cards if x != card]+[global_vars.Game.bottom])[0] > self.sumb:
                            self.sumb = global_vars.Game.getsum([x for x in self.cards if x != card]+[global_vars.Game.bottom])[0]
                            self.discardb = card
                    for card1 in self.deck:
                        self.sumts.append(0)
                        for card2 in self.cards:
                            if global_vars.Game.getsum([x for x in self.cards if x != card2]+[fakecard(card1)])[0] > self.sumts[self.deck.index(card1)]:
                                self.sumts[self.deck.index(card1)] = global_vars.Game.getsum([x for x in self.cards if x != card2]+[fakecard(card1)])[0]
                    for match in self.sumts:
                        self.sumt+=match
                    self.averaget = self.sumt/len(self.sumts)
                    if self.averaget > self.sumb:
                        global_vars.Game.choose(global_vars.Game.top)
                    else:
                        global_vars.Game.choose(global_vars.Game.bottom)
                self.wait = 0
            elif global_vars.Game.turn == 'r'+str(global_vars.Game.players.index(self)) and global_vars.Game.turn == global_vars.Game.newturn:
                self.gsum = 0
                self.gsum2 = 0
                self.discard = None
                #print(self.cards[:3])
                for card in self.cards[:3]:
                    #print(global_vars.Game.getsum(self.cards))
                    if global_vars.Game.getsum([x for x in self.cards if x != card])[0] > self.gsum:
                        self.gsum = global_vars.Game.getsum([x for x in self.cards if x != card])[0]
                        self.gsum2 = global_vars.Game.getsum([x for x in self.cards if x != card])[1]
                        self.discard = card
                    elif global_vars.Game.getsum([x for x in self.cards if x != card])[0] == self.gsum and global_vars.Game.getsum([x for x in self.cards if x != card])[1] > self.gsum2:
                        self.gsum = global_vars.Game.getsum([x for x in self.cards if x != card])[0]
                        self.gsum2 = global_vars.Game.getsum([x for x in self.cards if x != card])[1]
                        self.discard = card
                global_vars.Game.choose(self.discard)
                #print('chosen')
                self.rank = 0
                for average in self.average:
                    self.rank+=(average-global_vars.Game.getsum(self.cards)[0])
                print(self.rank)
                if self.rank < -30 and global_vars.Game.knocked == False:
                    global_vars.Game.knock(global_vars.Game.players.index(self))
                    
                self.wait = 0
        elif (global_vars.Game.turn == global_vars.Game.players.index(self) or global_vars.Game.turn == 'r'+str(global_vars.Game.players.index(self))) and global_vars.Game.turn == global_vars.Game.newturn:
            self.wait+=1

    def observedr(self,player,card):
        self.list = []
        for x in range(0,len(global_vars.Game.players)):
            self.list.append(x)
        self.list.remove(global_vars.Game.players.index(self))
        self.opponents[self.list.index(player)].append(card.type)

    def observedi(self,player,card):
        if card.type in self.deck:
            self.deck.remove(card.type)
        self.list = []
        for x in range(0,len(global_vars.Game.players)):
            self.list.append(x)
        self.list.remove(global_vars.Game.players.index(self))
        if card in self.opponents[self.list.index(player)]:
            self.opponents[self.list.index(player)][self.opponents[self.list.index(player)].index(card)] = None
