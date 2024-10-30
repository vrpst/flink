import pygame
import os

class ScreenOperations():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.music.set_volume(0.5)
        self.screen = pygame.display.set_mode([1400, 900])
        self.__music_location = os.path.dirname(os.path.abspath(__file__)) + r"\resources\lobbymusic.mp3"
        self.setScreenColor((198, 207, 207))
        self.blankScreen()
        pygame.display.set_caption("Flink")        
        self.updateScreen()

    def blankScreen(self):
        self.screen.fill(self.__color)

    def setScreenColor(self, color):
        self.__color = color

    def getScreenColor(self):
        return self.__color

    def playMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.__music_location)
        pygame.mixer.music.play(loops=-1)  # loop

    def showText(self, text: str, font: str, size: int, color: tuple, location: tuple):
        self.__text_font = pygame.font.Font(font, size)
        self.__text = self.__text_font.render(text, True, color)
        self.screen.blit(self.__text, location)
        return self.__text.get_width()
    
    def centreTextHorizontally(self, text: str, font: str, size:int, color: tuple, location: int):
        self.__text_font = pygame.font.Font(font, size)
        self.__text = self.__text_font.render(text, True, color)
        self.screen.blit(self.__text, (700-(self.__text.get_width()/2), location))

    def createRectangle(self, color: str, dimensions: list, location: tuple, radius=0):
        return pygame.draw.rect(self.screen, color, pygame.Rect(location[0], location[1], dimensions[0], dimensions[1]), border_radius=radius)

    def createCircle(self, color: str, radius: float, location: tuple):
        return pygame.draw.circle(self.screen, color, location, radius)

    def stopMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def updateScreen(self):
        pygame.display.flip()