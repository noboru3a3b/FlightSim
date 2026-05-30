import pygame

RAPID_SPEED=15

class LibraryPyGame:
    def __init__(self):
        self.rapid=True

    def isPlaying(self):
        if not pygame.mixer.music.get_busy():
            return False
        if self.rapid and pygame.mixer.music.get_pos()> 1000*RAPID_SPEED:
            return False
        return True

    def play(self, trackName):
        pygame.mixer.music.load(trackName)
        pygame.mixer.music.play()
        
