import random

class RandomTicTacToePlayer:
    def __init__(self, side):
        self.side=side

    def getMove(self, board):
        legalMoves=[]
        for x in range(3):
            for y in range(3):
                if board.isLegalMove(x,y,self.side):
                    legalMoves.append((x,y))
        x,y=random.choice(legalMoves)
        return 3*y+x+1
    
    
        
                
    
