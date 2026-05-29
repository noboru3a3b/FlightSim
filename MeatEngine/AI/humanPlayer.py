class HumanTicTacToePlayer:
    def __init__(self, side):
        """ side: 1=X, 2=O """
        self.side=side

    def getMove(self, board):
        """
        displays the board to the human, who returns a move number (or
        0 to quit)
        """

        r1=board.squares[:3]
        r2=board.squares[3:6]
        r3=board.squares[6:]

        print r1
        print r2
        print r3

        prompt="player %d enter move (1-9) or 0 to quit:"%self.side
        
        i=raw_input(prompt)

        return int(i)


if __name__=="__main__":
    
    import boardRep
    import randomPlayer

    p1=HumanTicTacToePlayer(1)
    #p2=HumanTicTacToePlayer(2)
    p2=randomPlayer.RandomTicTacToePlayer(2)


    b=boardRep.TicTacToeBoard()

    movingPlayer=0
    players=[p1,p2]
    
    while not b.isOver():
        m=players[movingPlayer].getMove(b)
        if m==0:
            break
        m=m-1

        x=m%3
        y=(m-x)/3
        if b.isLegalMove(x,y,movingPlayer+1):
            b.move(x,y,movingPlayer+1)
            movingPlayer += 1
            movingPlayer %= 2
        else:
            print "illegal move, try again",x,y

        print "canonical version of the board:"
        r,nb=b.getCanonicalCopy()
        print r,nb.hashVal()
        nb.display()

    w=b.getWinner()
    winString={-1:"Draw",
               0:"Ongoing",
               1:"Player 1 wins",
               2:"Player 2 wins"}[w]
    print winString


    
        
        
        
        
