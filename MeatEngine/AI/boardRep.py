

class TicTacToeBoard:
    def __init__(self, hashVal=0):
        self.squares=[0]*9
        if hashVal!=0:
            for i in range(9):
                v=hashVal%3
                hashVal/=3
                self.squares[i]=v

    def countNum(self,num):
        c=0
        for i in range(9):
            if self.squares[i]==num:
                c+=1
        return c
        
    def countX(self):
        return self.countNum(1)
    
    def countO(self):
        return self.countNum(2)

    def countEmpty(self):
        return self.countNum(0)

    def hashVal(self):
        s=0
        for i in range(9):
            s += self.squares[i] * 3**i
        return s

    def getCanonicalHash(self):
        perm,boardCopy=self.getCanonicalCopy()
        return boardCopy.hashVal()

    def getCanonicalCopy(self):
        maps=[[0,1,2,
               3,4,5,
               6,7,8],
              [2,5,8,
               1,4,7,
               0,3,6],
              [8,7,6,
               5,4,3,
               2,1,0],
              [6,3,0,
               7,4,1,
               8,5,2],
              [2,1,0,
               5,4,3,
               8,7,6],
              [8,5,2,
               7,4,1,
               6,3,0],
              [6,7,8,
               3,4,5,
               0,1,2],
              [0,3,6,
               1,4,7,
               2,5,8]]

        bestVal=-1
        bestMap=-1
        for i in range(len(maps)):
            m=maps[i]
            thisVal=0
            for si in range(9):
                thisVal+=self.squares[m[si]] * 3**si
            if bestVal==-1 or bestVal>thisVal:
                bestVal=thisVal
                bestMap=i
        newBoard=TicTacToeBoard()
        bm=maps[bestMap]
        for i in range(9):
            newBoard.squares[i]=self.squares[bm[i]]

        return bestMap,newBoard

    def whoseTurn(self):
        nX=self.countX()
        nO=self.countO()
        if nX==nO:
            return 1
        if nX-1==nO:
            return 2
        raise "not a valid turn"
        return 0
    
    def successorMap(self):
        if self.isOver():
            return None
        if not self.anyMoves():
            return None
        m={}
        wt=self.whoseTurn()
        for x in range(3):
            for y in range(3):
                p=3*y+x
                perm,bc=self.getCanonicalCopy()
                if bc.isLegalMove(x,y,wt):
                    bc.move(x,y,wt)
                    v=bc.getCanonicalHash()
                    m[p]=v
        return m

    def display(self):
        for i in range(3):
            for j in range(3):
                p=3*i+j
                print self.squares[p]," ",
            print

    def move(self,x,y,p):
        pos=3*y+x
        self.squares[pos]=p

    def isLegalMove(self, x,y,p):
        pos=y*3+x
        return self.squares[pos]==0

    def anyMoves(self):
        return 0 in self.squares

    def getWinner(self):
        """
        returns 1 if p1 won, 2 if p2 won,
        -1 for a draw, 
        or 0 if game is still ongoing
        """

        #print "in getWinner"
        patterns=[[0,1,2],
                  [3,4,5],
                  [6,7,8],
                  [0,3,6],
                  [1,4,7],
                  [2,5,8],
                  [0,4,8],
                  [2,4,6]]

        for p in patterns:
            #print "testing pattern",p
            isPatGood=True
            for si in p:
                #print "testing square index",si
                isPatGood = (isPatGood and (self.squares[si] and self.squares[si]==self.squares[p[0]]))
                #print "isPatGood=",isPatGood
            if isPatGood:
                return self.squares[p[0]]

        if self.anyMoves():
            return 0
        return -1
    
        

    def isOver(self):
        w=self.getWinner()
        return w!=0

    def evaluate(self, player, verbose=0):
        if self.isOver():
            w=self.getWinner()
            if w==player:
                # I win
                return 1000
            if w==-1:
                # draw
                return 0
            else:
                # I lose
                return -1000
            
            
        patterns=[[0,1,2],
                  [3,4,5],
                  [6,7,8],
                  [0,3,6],
                  [1,4,7],
                  [2,5,8],
                  [0,4,8],
                  [2,4,6]]

        v=0

        if verbose:
            print "evaluating",self.squares
        for p in patterns:
            if verbose:
                print "pattern",p
            vals=[self.squares[x] for x in p]

            countMine=0
            countEmpty=0
            countEnemy=0
            for i in range(3):
                if vals[i]==player:
                    countMine += 1
                elif vals[i]==0:
                    countEmpty += 1
                else:
                    countEnemy += 1

            if verbose:
                print "countMine",countMine
                print "countEmpty",countEmpty
                print "countEnemy",countEnemy

            if countMine==3:
                v+=100
            if countMine==2 and countEmpty==1:
                v+=10
            if countMine==1 and countEmpty==2:
                v+=1
            if countEnemy==3:
                v-=100
            if countEnemy==2 and countEmpty==1:
                v-=10
            if countEnemy==1 and countEmpty==2:
                v-=1
        if verbose:
            print "returning",v
        return v
            


if __name__=="__main__":
    b=TicTacToeBoard()

    b.display()

    b.move(0,0,1)
    b.move(0,1,2)

    b.display()

    print b.isOver()        

    b.move(1,0,1)
    b.move(2,0,1)

    b.display()
    print b.isOver()

    totalBoards=3**9

    validBoards={}
    
    for i in xrange(totalBoards):
        b=TicTacToeBoard(i)
        numX=b.countX()
        numO=b.countO()
        if ((numO==numX or
             numO==numX-1)and
            b.getCanonicalHash()==i):
            numMoves=numX+numO
            vb=validBoards.get(numMoves,[])
            vb.append(i)
            validBoards[numMoves]=vb

    tot=0
    vbk=validBoards.keys()
    vbk.sort()

    f=file("tictactoeboards.txt","wt")
    for i in vbk:
        print i,len(validBoards[i])
        tot+=len(validBoards[i])

        boards=validBoards[i][:]
        boards.sort()
        for b in boards:
            f.write(`b`)
            f.write("\n")
    print "total:",tot

    openList=[0]
    closedList=[]

    stateDescs=[]

    while openList:
        hv=openList.pop()
        b=TicTacToeBoard(hv)
        succ=b.successorMap()
        if hv not in closedList:
            closedList.append(hv)
            stateDescs.append((9-b.countEmpty(), hv, succ))
        if not succ is None:
            for move in succ:
                nextState=succ[move]
                if ((nextState not in openList) and
                    (nextState not in closedList)):
                    openList.append(nextState)
    print "having generated only legal moves,"
    print "the number of legal moves are:",len(closedList)

    """
    stateDescs.sort()

    f=file("boardDescs.txt","wt")
    for sd in stateDescs:
        f.write("%6d, "%sd[1])
        if sd[2]:
            for move in sd[2]:
                succState=sd[2][move]
                f.write("%6d, "%succState)
        f.write("\n")
    f.close()
    """
                
    countPieces={}

    for sd in stateDescs:
        pieceCount=sd[0]
        oldCount=countPieces.get(pieceCount,0)
        countPieces[pieceCount]=oldCount+1

    keys=countPieces.keys()
    keys.sort()

    for k in keys:
        print k, countPieces[k]
        
        
        
            
    
            
