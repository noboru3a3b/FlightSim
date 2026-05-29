from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import boardRep
import mtdf

boardSize=0.8 * inch
boardSlotWidth=2*boardSize
boardLeftMargin=0.15*inch
boardBottomMargin=0.05*inch
boardRightMargin=boardLeftMargin+boardSize-2*boardBottomMargin
squareSize=(boardSize-2*boardBottomMargin)/3
pieceSize=squareSize*0.6
pieceMargin=(squareSize-pieceSize)/2

boardsAcross=4
boardsDown=12
boardsOnAPage=boardsAcross*boardsDown

contentWidth=boardSlotWidth*boardsAcross
contentDepth=boardSize*boardsDown
pageWidth,pageHeight=letter
leftMargin=(pageWidth-contentWidth)/2
bottomMargin=(pageHeight-contentDepth)/2

boardIndexList=[]

def drawBoard(c, xIndex, yIndex, hashVal, boardIndex):
    left=xIndex*boardSlotWidth+leftMargin
    bottom=pageHeight-((yIndex+1)*boardSize+bottomMargin)
    c.saveState()
    c.translate(left,bottom)

    c.saveState()
    FONTSIZE=8
    c.setFont("Helvetica",FONTSIZE)
    labelColor=(1.0,1.0,1.0)
    labelBackground=(0.5, 0.5, 0.5)
    
    c.setFillColor(labelBackground)
    c.rect(0,boardBottomMargin,boardLeftMargin,boardSize-2*boardBottomMargin,stroke=0,fill=1)
    c.rotate(90)
    #label="%d (%d)"%(boardIndex,hashVal)
    label=str(boardIndex)
    w=c.stringWidth(label, "Helvetica", FONTSIZE)
    
    c.setStrokeColor(labelColor)
    c.setFillColor(labelColor)
    c.drawString((boardSize-w)/2,-(boardLeftMargin+FONTSIZE)/2,label)
    c.restoreState()
    

    c.line(boardLeftMargin,boardBottomMargin+squareSize,boardRightMargin,boardBottomMargin+squareSize)
    c.line(boardLeftMargin,boardBottomMargin+2*squareSize,boardRightMargin,boardBottomMargin+2*squareSize)
    c.line(boardLeftMargin+squareSize,boardBottomMargin,boardLeftMargin+squareSize,boardSize-boardBottomMargin)
    c.line(boardLeftMargin+2*squareSize,boardBottomMargin,boardLeftMargin+2*squareSize,boardSize-boardBottomMargin)

    b=boardRep.TicTacToeBoard(hashVal)

    for x in range(3):
        for y in range(3):
            si=3*y+x
            sv=b.squares[si]
            c.saveState()
            c.translate(boardLeftMargin+pieceMargin+x*squareSize,
                        boardBottomMargin+pieceMargin+y*squareSize)
                        
            if sv==1:
                c.line(0,0,
                       pieceSize,pieceSize)
                c.line(0,pieceSize,
                       pieceSize,0)
            elif sv==2:
                c.ellipse(0,0,
                          pieceSize,pieceSize)
            c.restoreState()

    v=mtdf.mtdf(hashVal,0,12)
    valueStr={-1000:"O Wins",
              0:"Draw",
              1000:"X Wins"}[v]

    sm=b.successorMap()
    bestMoves=mtdf.getBestMoves(hashVal,12,v)
    bestMoveList=list(bestMoves)

    destList=[]
    if sm:
        destSet=set()
        for m in bestMoves:
            destSet.add(1+boardIndexList.index(sm[m]))
        destList=list(destSet)
        destList.sort()

    for m in bestMoves:
        x=m%3
        y=(m-x)/3
        c.saveState()
        c.setFont("Helvetica",pieceSize)
        c.translate(boardLeftMargin+pieceMargin+x*squareSize,
                    boardBottomMargin+pieceMargin+y*squareSize)
        c.drawCentredString(pieceSize/2.0,0,str(1+destList.index(1+boardIndexList.index(sm[m]))))
        c.restoreState()

    CAPTIONSIZE=5.6
    c.setFont("Helvetica",CAPTIONSIZE)

    if b.isOver():
        wtString="Game Over"
    else:
        wt=b.whoseTurn()
        wtString={1:"X to move",
                  2:"O to move"}[wt]
    
    c.drawString(boardRightMargin,boardSize-boardBottomMargin-CAPTIONSIZE,wtString)
    c.drawString(boardRightMargin,boardSize-boardBottomMargin-2*CAPTIONSIZE,valueStr)

    moveStr=""
    for destIndex in range(len(destList)):
        c.drawString(boardRightMargin,
                     boardSize-boardBottomMargin-(3+destIndex)*CAPTIONSIZE,
                     "%d : %d"%(destIndex+1,destList[destIndex]))
    

    
    
    c.restoreState()


if __name__=="__main__":
    c = canvas.Canvas("tictactoe.pdf", pagesize=letter)
    c.setAuthor("Dave LeCompte")
    c.setTitle("How to Play Perfect Tic Tac Toe")
    
    f=file("boardDescs.txt")
    fLines=f.readlines()
    f.close()
    
    
    for boardIndex in range(len(fLines)):
        splitLine=fLines[boardIndex].split(',')
        boardHash=int(splitLine[0])
        boardIndexList.append(boardHash)
    
    pageCount=1
    for boardIndex in range(len(boardIndexList)):
        boardHash=boardIndexList[boardIndex]
    
        pageIndex=boardIndex%boardsOnAPage
        x=pageIndex%boardsAcross
        y=(pageIndex-x)/boardsAcross
    
        drawBoard(c, x, y, boardHash, boardIndex+1)
    
        if (boardIndex+1)%boardsOnAPage==0:
            c.drawCentredString(pageWidth/2,inch/2,"Page: %d"%pageCount)
            pageCount += 1
            c.showPage()
            
    c.drawCentredString(pageWidth/2,inch/2,"Page: %d"%pageCount)
    c.showPage()
    c.save()
    
    
