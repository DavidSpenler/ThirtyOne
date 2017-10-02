import pyglet

import global_vars

class player():

    def __init__(self,c1x,c1y,c1r,c2x,c2y,c2r,c3x,c3y,c3r,c4x,c4y,c4r):

        self.cards = [None,None,None]
        
        self.cardp = [
                (c1x,c1y,c1r),
                (c2x,c2y,c2r),
                (c3x,c3y,c3r),
                (c4x,c4y,c4r)
            ]
