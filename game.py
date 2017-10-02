import pyglet

import random

from player import player
from computer import computer
from card import card
import global_vars

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
                    if 'observedr' in dir(player) and int(self.turn) != global_vars.Game.players.index(player):
                        player.observedr(int(self.turn),cardt)
                #print('bottom card')
                self.bottom.goal = (self.players[self.turn].cardp[3][0],self.players[self.turn].cardp[3][1],self.players[self.turn].cardp[3][2],10.5)
                self.players[self.turn].cards.append(self.bottom)
                self.newturn = 'r'+str(self.turn)
                self.bottom = None
        elif str(self.turn)[0] == 'r' and self.turn == self.newturn and cardt in self.players[int(str(self.turn)[1])].cards[:3]:
            for player in self.players:
                if 'observedi' in dir(player) and int(self.turn[1]) != global_vars.Game.players.index(player):
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
                self.behind.sprite.group = global_vars.bottom
            self.bottom = cardt
            if self.bottom != None:
                pass
                #print('bottom: ',self.bottom.type,self.bottom.sprite.group)
            if self.behind != None:
                pass
                #print('behind: ',self.behind.type,self.behind.sprite.group)
            self.newturn = (int(self.turn[1])+1)%4
            

    def moving(self):
        for object in global_vars.dobjects:
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
        global_vars.Knock.hide()
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
                global_vars.batch.draw()
        global_vars.WinMSG.winner = self.winner
        print('Player ',self.winner+1,' wins!')
        self.turn = 'en'
        self.newturn = 'en'

    def update(self,dt):
        ##print(self.turn)
        global_vars.window.clear()
        for object in global_vars.dobjects:
            object.move()
        if self.turn == self.lastturn and self.knocked == True and self.moving() == False:
            self.win()
        if self.turn != self.newturn and self.moving() == False:
            self.turn = self.newturn
            if self.turn == 0 and self.const < 5:
                self.const+=0.3
        if global_vars.WinMSG.winner != None:
            global_vars.WinMSG.show()
        for p in range(1,len(self.players)):
            self.players[p].think()
