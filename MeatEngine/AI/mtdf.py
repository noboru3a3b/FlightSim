
"""MTD(f)

from http://www.cs.vu.nl/~aske/mtdf.html

The name of the algorithm is short for MTD(n, f), which stands for
something like Memory-enhanced Test Driver with node n and value f.
"""

import boardRep



POSINFINITY=99999
NEGINFINITY=-99999

AIPLAYER=1

class TranspositionTableEntry:
    def __init__(self):
        self.lowerBound = NEGINFINITY
        self.upperBound = POSINFINITY
        self.bestMove = None
        self.furthestDepthSearched = -1
        self.isTerminal = False

class TranspositionTable:
    def __init__(self):
        self.cache={}
        
    def lookup(self, node, depth):
        ttn=self.cache.get(node,None)
        if ttn is None:
            return ttn
        if depth<=ttn.furthestDepthSearched:
            return ttn
        if ttn.isTerminal:
            return ttn
        del self.cache[node]
        return None

    def storeLowerBound(self, node, value):
        t=self.cache.get(node, TranspositionTableEntry())
        t.lowerBound=max(value,t.lowerBound)
        self.cache[node]=t

    def storeUpperBound(self, node, value):
        t=self.cache.get(node, TranspositionTableEntry())
        t.upperBound=min(value,t.upperBound)
        self.cache[node]=t

    def storeDepth(self, node, value):
        t=self.cache.get(node, TranspositionTableEntry())
        t.furthestDepthSearched = value
        self.cache[node]=t

    def storeBestMove(self, node, value):
        t=self.cache.get(node, TranspositionTableEntry())
        t.bestMove = value
        self.cache[node]=t

    def setTerminal(self, node, value):
        t=self.cache.get(node, TranspositionTableEntry())
        t.isTerminal = value
        self.cache[node]=t

        

    

transTable=TranspositionTable()


def mtdf(node, f, depth):
    #print "in MTD(f) with node %d, firstGuess %d, depth %d"%(node, f, depth)
    g=f
    upperBound=POSINFINITY
    lowerBound=NEGINFINITY
    while lowerBound<upperBound:
        if g==lowerBound:
            beta = g+1
        else:
            beta = g
        g = alphaBetaWithMemory(node, beta-1, beta, depth, depth)
        if g< beta:
            upperBound=g
        else:
            lowerBound=g
    return g


def alphaBetaWithMemory(node, alpha, beta, depth, printDepth):
    indent=printDepth-depth
    indentString="    "*indent
    #print indentString,"in ABwM(node=%d, alpha=%d, beta=%d, depth=%d)"%(node,alpha,beta,depth)
    transTableInfo=transTable.lookup(node, depth)

    if transTableInfo:
        #print indentString,"got transTableInfo: [%d, %d] depth: %d"%(transTableInfo.lowerBound,
        #                                                             transTableInfo.upperBound,
        #                                                             transTableInfo.furthestDepthSearched)
        if transTableInfo.lowerBound >= beta:
            return transTableInfo.lowerBound
        if transTableInfo.upperBound <= alpha:
            return transTableInfo.upperBound
        alpha = max(alpha, transTableInfo.lowerBound)
        beta = min(beta, transTableInfo.upperBound)

    terminal=isTerminal(node)
    if depth==0 or terminal:
        g=evaluate(node, AIPLAYER)
        #print indentString,"evaluating [%d] got %d"%(node,g)
    elif isMaximizing(node):
        g = NEGINFINITY
        a = alpha
        for c in getChildren(node):
            if g >= beta:
                break
            g=max(g,alphaBetaWithMemory(c, a, beta, depth-1, printDepth))
            a=max(a,g)
    else:
        g = POSINFINITY
        b = beta
        for c in getChildren(node):
            if g <= alpha:
                break
            g = min(g,alphaBetaWithMemory(c, alpha, b, depth-1, printDepth))
            b = min(b,g)

    if g <= alpha:
        transTable.storeUpperBound(node,g)
    elif g > alpha and g < beta:
        transTable.storeLowerBound(node,g)
        transTable.storeUpperBound(node,g)
        raise "never happens"
    else:
        transTable.storeLowerBound(node,g)
    transTable.storeDepth(node, depth)
    transTable.setTerminal(node, terminal)
    return g

                  
def iterativeDeepening(node):
    #print "in iterative deepening of node", node
    firstGuess=0
    for d in range(1,12):
        firstGuess=mtdf(node, firstGuess,d)
        #print "first guess after depth %d is %d"%(d,firstGuess)
        #print "I would check the time here"
    return firstGuess

def isMaximizing(node):
    board=boardRep.TicTacToeBoard(node)
    return board.whoseTurn()==AIPLAYER
    
def isTerminal(node):
    board=boardRep.TicTacToeBoard(node)
    return board.isOver()

def getChildren(node):
    board=boardRep.TicTacToeBoard(node)
    sm=board.successorMap()
    return sm.values()

def evaluate(node, player, verbose=0):
    board=boardRep.TicTacToeBoard(node)
    return board.evaluate(player, verbose)
    
def getBestMoves(node, depth, guess=0):
    board=boardRep.TicTacToeBoard(node)
    bestMoves=set()
    if board.isOver():
        return bestMoves
    sm=board.successorMap()
    nodeValue=mtdf(node, guess, depth)
    for move in sm.keys():
        child=sm[move]
        childValue=iterativeDeepening(child)
        if childValue == nodeValue:
            bestMoves.add(move)
    return bestMoves

if __name__=="__main__":
    f=file("boardDescs.txt")
    fLines=f.readlines()
    f.close()

    for boardIndex in range(len(fLines)):
        splitLine=fLines[boardIndex].split(',')
        boardHash=int(splitLine[0])

        v=iterativeDeepening(boardHash)

        print boardHash,v,getBestMoves(boardHash, 10, v)
    
