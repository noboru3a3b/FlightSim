

import libraryPyGame
import player

import pygame
from pygame.locals import *

if __name__ == '__main__':
    lib=libraryPyGame.LibraryPyGame()
    
    playerObj=player.Player(lib)
    
    pygame.init()
    
    playerObj.addState("intro")
    playerObj.addState("happy")
    playerObj.addState("medium")
    playerObj.addState("tense")
    
    playerObj.addMusicDirectoryToState("intro","Music/Ogg/Intro")
    playerObj.addMusicDirectoryToState("happy","Music/Ogg/Happy")
    playerObj.addMusicDirectoryToState("medium","Music/Ogg/Medium")
    playerObj.addMusicDirectoryToState("tense","Music/Ogg/Tense")
    
    playerObj.addTransition("happy","medium")
    playerObj.addTransition("medium","tense")
    playerObj.addTransition("tense","medium")
    playerObj.addTransition("medium","happy")
    
    playerObj.addMusicDirectoryToTransition("happy","medium","Music/Ogg/Transitions/Happy-Medium")
    playerObj.addMusicDirectoryToTransition("medium","tense","Music/Ogg/Transitions/Medium-Tense")
    playerObj.addMusicDirectoryToTransition("tense","medium","Music/Ogg/Transitions/Tense-Medium")
    playerObj.addMusicDirectoryToTransition("medium","happy","Music/Ogg/Transitions/Medium-Happy")
    
    
    playerObj.setState("intro")
    
    surf=pygame.display.set_mode((200,200))
    
    keyLabelText=["[1]: Intro",
                  "[2]: Happy",
                  "[3]: Medium",
                  "[4]: Tense",
                  "[R]: (rapid)",
                  "[ESC]: (quit)"]
    
    defName=pygame.font.get_default_font()
    print "default font name:", defName
    defFont=pygame.font.Font(defName, 16)
    labelsurfs=[defFont.render(x, 1, (190, 190, 0)) for x in keyLabelText]
    
                  
    
    gameOver=False
    myClock=pygame.time.Clock()
    
    while not gameOver:
        surf.fill((255,255,255))
        for i in range(6):
            surf.blit(labelsurfs[i], (0,20*i))
    
        curState=playerObj.getState()
        if curState:
            cursurf=defFont.render("mood: "+curState, 1, (80, 80, 200))
            surf.blit(cursurf, (0,130))
    
        if playerObj.musicLibrary.rapid:
            rapidsurf=defFont.render("RAPID ON", 1, (0, 200, 0))
        else:
            rapidsurf=defFont.render("RAPID OFF", 1, (200, 0, 0))
        surf.blit(rapidsurf, (0,160))
    
    
        
        
            
        myClock.tick(5)
        for e in pygame.event.get():
            if e.type==QUIT:
                gameOver=True
                break
            if e.type==KEYDOWN:
                if e.key==K_1:
                    playerObj.pushState("intro")
                elif e.key==K_2:
                    playerObj.pushState("happy")
                elif e.key==K_3:
                    playerObj.pushState("medium")
                elif e.key==K_4:
                    playerObj.pushState("tense")
                elif e.key==K_q:
                    gameOver=True
                elif e.key==K_ESCAPE:
                    gameOver=True
                elif e.key==K_r:
                    lib.rapid= not lib.rapid
        playerObj.tick()
        pygame.display.flip()
        
    
