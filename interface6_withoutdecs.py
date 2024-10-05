import pygame
import random
import math

class ScreenOperations():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1400, 900])
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
        pygame.mixer.music.load("lobbymusic.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)  # loop

    def showText(self, text: str, font: str, size:int, color: tuple, location: tuple):
        self.__text_font = pygame.font.Font(font, size)
        self.__text = self.__text_font.render(text, True, color)
        self.screen.blit(self.__text, location)
        return self.__text.get_width()

    def createRectangle(self, color: str, dimensions: list, location: tuple):
        return pygame.draw.rect(self.screen, color, pygame.Rect(location[0], location[1], dimensions[0], dimensions[1]))

    def createCircle(self, color: str, radius: float, location: tuple):
        return pygame.draw.circle(self.screen, color, location, radius)

    def stopMusic(self):
        pygame.mixer.music.stop()

    def updateScreen(self):
        pygame.display.flip()
        
class Buttons():
    def __init__(self):
        self.__hover = False
        self.__buttons_shape = {}
        self.__buttons_location = {}
        self.__buttons_color = {}
        self.__buttons_dimensions = {}
        self.__buttons = []
        self.__button_names = []

    def add(self, name: str, shape, dimensions, startingcolor: list, location: tuple, new: bool, usepreviouscolor: bool):  # size must be list
        if new:
            self.__buttons.append(self.__createButton(name, shape, dimensions, startingcolor, location, usepreviouscolor))
            self.__button_names.append(name)
        else:
            self.__createButton(name, shape, dimensions, startingcolor, location, usepreviouscolor)
    
    def checkButtonHover(self, mouse, click):  # check that the mouse doesn't cover a button
        for but in range(len(self.__buttons)):
            if click:
                self.__button_pressed = self.__mouseHover(mouse, self.__button_names[but], click)
                if self.__button_pressed != (False, ""):
                    return self.__button_pressed  # if clicked, return the button name that was clicked
            else:
                self.__mouseHover(mouse, self.__button_names[but], click)
        if click:  # if there was a click not on a button
            return (False, "")
        
    def __createButton(self, name: str, shape, dimensions, color: list, location: tuple, usepreviouscolor: bool):  # renders a text button
        self.__buttons_location.update({name: location})
        self.__buttons_shape.update({name: shape})
        self.__buttons_dimensions.update({name: dimensions})
        if not usepreviouscolor:  # if the user does not want to use the previously saved color, update the color before using it
            self.__buttons_color.update({name: color})
        if shape == "rect":
            self.__button = screen.createRectangle(self.__buttons_color.get(name), dimensions, location)
        elif shape == "circle":
            self.__button = screen.createCircle(self.__buttons_color.get(name), dimensions, location)
        return self.__button

    def __mouseHover(self, mousepos, name, click: bool):  # change color if needed
        self.__hover_location = self.__buttons_location.get(name)
        self.__hover_dimensions = self.__buttons_dimensions.get(name)
        self.__hover_shape = self.__buttons_shape.get(name)
        if isinstance(self.__hover_dimensions, float):  # IF IT'S A CIRCLE
            self.__hover_dimensions = [self.__hover_dimensions, self.__hover_dimensions]
            if (self.__hover_location[0] - self.__hover_dimensions[0] <= mousepos[0] <= self.__hover_location[0] + self.__hover_dimensions[0]):  # if within x bounds
                if (self.__hover_location[1] - self.__hover_dimensions[1] <= mousepos[1] <= self.__hover_location[1] + self.__hover_dimensions[1]):  # and within y
                    self.__hover = True
                else:
                    self.__hover = False  # if out of Y then False
            else:
                self.__hover = False  # if out of X then False

        else:  # FOR RECTANGLES
            if (self.__hover_location[0] <= mousepos[0] <= (self.__hover_location[0] + self.__hover_dimensions[0])):  # if within x bounds
                if (self.__hover_location[1] <= mousepos[1] <= (self.__hover_location[1] + self.__hover_dimensions[1])):  # and within y
                    self.__hover = True
                else:
                    self.__hover = False  # if out of X then False
            else:
                self.__hover = False  # if out of Y then False
                
        if self.__hover and self.__buttons_color.get(name) == [0, 0, 0]:  # if color should go blue
            screen.createRectangle("#c6cfcf", [self.__hover_dimensions[0], self.__hover_dimensions[1]], self.__hover_location)
            self.__createButton(name, self.__hover_shape, self.__buttons_dimensions.get(name), [0, 80, 89], self.__hover_location, usepreviouscolor=False)
        
        elif not self.__hover and self.__buttons_color.get(name) == [0, 80, 89]:
            screen.createRectangle("#c6cfcf", [self.__hover_dimensions[0], self.__hover_dimensions[1]], self.__hover_location)
            self.__createButton(name, self.__hover_shape, self.__buttons_dimensions.get(name), [0, 0, 0], self.__hover_location, usepreviouscolor=False)
        
        if self.__hover and click:  # if the button is clicked on
            return (True, name)

        elif not self.__hover and click:
            return (False, '')
    
class TextButtons():
    def __init__(self):
        self.__hover = False
        self.__buttons_text = {}
        self.__buttons_location = {}
        self.__buttons_color = {}
        self.__buttons = []
        self.__button_names = []

    def add(self, name: str, text: str, font: str, size: int, startingcolor: list, location: tuple, new: bool, usepreviouscolor: bool):
        if new:
            self.__buttons.append(self.__createButton(name, text, font, size, startingcolor, location, usepreviouscolor))
            self.__button_names.append(name)
        else:
            self.__createButton(name, text, font, size, startingcolor, location, usepreviouscolor)
    
    def checkButtonHover(self, mouse, click):  # check that the mouse doesn't cover a button
        for but in range(len(self.__buttons)):
            if click:
                self.__button_pressed = self.__mouseHover(self.__buttons[but], mouse, self.__button_names[but], click)
                if self.__button_pressed != (False, ""):
                    return self.__button_pressed  # if clicked, return the button name that was clicked
            else:
                self.__mouseHover(self.__buttons[but], mouse, self.__button_names[but], click)
        if click:
            return (False, "")
        
    def __createButton(self, name: str, text: str, font: str, size:int, color: list, location: tuple, usepreviouscolor: bool):  # renders a text button
        self.__text_font = pygame.font.Font(font, size)
        self.__buttons_text.update({name: text})
        self.__buttons_location.update({name: location})
        if not usepreviouscolor:  # if the user does not want to use the previously saved color
            self.__buttons_color.update({name: color})
        self.__text = self.__text_font.render(text, True, self.__buttons_color.get(name))  # render it with the dict color
        screen.screen.blit(self.__text, location)
        return self.__text

    def __mouseHover(self, obj: pygame.Surface, mousepos, name, click: bool):  # change color if needed
        self.__hover_location = self.__buttons_location.get(name)
        if (self.__hover_location[0] <= mousepos[0] <= (self.__hover_location[0] + obj.get_width())) and (self.__hover_location[1] <= mousepos[1] <= (self.__hover_location[1] + obj.get_height())):
            self.__hover = True
        else:
            self.__hover = False

        if self.__hover and self.__buttons_color.get(name) == [0, 0, 0]:  # if color should go blue
            screen.createRectangle("#c6cfcf", [obj.get_width(), obj.get_height()], self.__hover_location)
            self.startgame_button = self.__createButton(name, self.__buttons_text.get(name), "Helvetica.ttf", 30, [0, 80, 89], self.__hover_location, usepreviouscolor=False)
        
        elif not self.__hover and self.__buttons_color.get(name) == [0, 80, 89]:
            screen.createRectangle("#c6cfcf", [obj.get_width(), obj.get_height()], self.__hover_location)
            self.startgame_button = self.__createButton(name, self.__buttons_text.get(name), "Helvetica.ttf", 30, [0, 0, 0], self.__hover_location, usepreviouscolor=False)
        
        if self.__hover and click:  # if the button is clicked on
            return (True, name)
        elif not self.__hover and click:
            return (False, '')

class HomeScreen():
    def __init__(self):
        self.__text_buttons = TextButtons()
        self.__subtitles = ("the arts", "Earth", "humans", "human history", "life", "mathematics", "philosophy", "science", "society", "technology", "Wikipedia")
        self.__subtitles_colors = {
            "the arts": (110, 2, 22),  # scarlet
            "Earth": (12, 25, 120),  # muddy camo
            "humans": (77, 52, 32),  # brown
            "human history": (138, 123, 50),  # dark gold
            "life": (23, 71, 13),  # green
            "mathematics": (77, 86, 135), # dark blue
            "philosophy": (91, 73, 102), # purple
            "science": (148, 89, 1),  # yellow but ??
            "society": (102, 3, 102),  # dark pink
            "technology": (52, 92, 90),  # dark turquoise
            "Wikipedia": (0, 0, 0),
        }
        self.__no_article_shown = True
        self.__move_question = True
        self.__start_question = True
        self.__subtitle_to_show = ""

    def showScreen(self, prev):
        screen.showText("Flink", "Helvetica.ttf", 100, (0, 0, 0), (100, 100))
        screen.showText("How well do you know Wikipedia?", "Helvetica-Bold.ttf", 18, (0, 0, 0), (105, 200))
        self.__showEmojis()
        self.__manageSubtitle()
        self.__text_buttons.add("startgame", "[[start game]]", "Helvetica.ttf", 30, [0, 0, 0], (105, 300), new=True, usepreviouscolor=False)
        self.__text_buttons.add("howtoplay", "[[how to play]]", "Helvetica.ttf", 30, [0, 0, 0], (105, 380), new=True, usepreviouscolor=False)
        self.__text_buttons.add("about", "[[about]]", "Helvetica.ttf", 30, [0, 0, 0], (105, 460), new=True, usepreviouscolor=False)
        self.__prev = prev
        if self.__prev == "about":
            self.__color_transition = [207, 198, 207]
        elif self.__prev == "howtoplay":
            self.__color_transition = [207, 207, 198]
        else:
            self.__color_transition = [198, 207, 207]

    def checkTextButtons(self, mouse, click):
        if click:
            self.__clicked = self.__text_buttons.checkButtonHover(mouse, click)
            if self.__clicked[1] == "startgame":
                return "game"
            elif self.__clicked[1] == "howtoplay":
                return "howtoplay"
            elif self.__clicked[1] == "about":
                return "about"
        else:
            self.__text_buttons.checkButtonHover(mouse, click)
    
    def remakeScreen(self):
        screen.blankScreen()
        if self.__color_transition != [198, 207, 207]:
            if self.__prev == "about":
                self.__color_transition[0] -= 1
                self.__color_transition[1] += 1
            elif self.__prev == "howtoplay":
                self.__color_transition[0] -= 1
                self.__color_transition[2] += 1
            screen.setScreenColor(self.__color_transition)
        self.__manageSubtitle()
        screen.showText("Flink", "Helvetica-Bold.ttf", 100, (0, 0, 0), (100, 100))
        self.__base_sub_width = screen.showText("How well do you know ", "Helvetica.ttf", 18, (0, 0, 0), (105, 200))
        self.__article_sub_width = screen.showText(self.__subtitle_to_show, "Helvetica.ttf", 18, self.__subtitle_color, (105+self.__base_sub_width, 200))
        self.__manageQuestion()
        if self.__start_question:  # at the start make the final location the starting one
            self.__question_pos = self.__final_question_pos
            self.__start_question = False
        screen.showText("?", "Helvetica.ttf", 18, (0, 0, 0), (self.__question_pos, 200))
        self.__text_buttons.add("startgame", "[[start game]]", "Helvetica.ttf", 30, [0, 0, 0], (105, 300), new=False, usepreviouscolor=True)
        self.__text_buttons.add("howtoplay", "[[how to play]]", "Helvetica.ttf", 30, [0, 0, 0], (105, 380), new=False, usepreviouscolor=True)
        self.__text_buttons.add("about", "[[about]]", "Helvetica.ttf", 30, [0, 0, 0], (105, 460), new=False, usepreviouscolor=True)
        self.__showEmojis()

    def __manageSubtitle(self):
        if self.__no_article_shown:  # if there is no article shown
            self.__chooseArticle()
        self.__updateArticle()

    def __updateArticle(self):
        #print(self.__subtitle_color, self.__subtitle_final_color, self.__subtitle_to_show, self.__subtitle_scale)
        self.__check_subtitle_color = (round(self.__subtitle_color[0]), round(self.__subtitle_color[1]), round(self.__subtitle_color[2]))
        if self.__check_subtitle_color != self.__subtitle_final_color:  # if they're different colors
            if self.__hold:  # hold
                self.__hold_count += 1
                if self.__hold_count == 200:
                    self.__hold = False
            else:
                self.__subtitle_color[0] += self.__subtitle_scale[0]
                self.__subtitle_color[1] += self.__subtitle_scale[1]
                self.__subtitle_color[2] += self.__subtitle_scale[2]
        elif self.__subtitle_final_color != (198, 207, 207):  # if the subtitle color is its color and not bgrd (it has just finished fading in)
            self.__hold = True
            self.__hold_count = 0
            self.__subtitle_scale[0] = self.__subtitle_scale[0]*-1
            self.__subtitle_scale[1] = self.__subtitle_scale[1]*-1
            self.__subtitle_scale[2] = self.__subtitle_scale[2]*-1
            self.__subtitle_final_color = (198, 207, 207)
        elif self.__check_subtitle_color == self.__subtitle_final_color and self.__subtitle_final_color == (198, 207, 207):
            self.__no_article_shown = True

    def __chooseArticle(self):
        self.__hold = False
        self.__new_subtitle = random.choice(self.__subtitles)
        while self.__subtitle_to_show == self.__new_subtitle: # choose a random article
            print(self.__new_subtitle, self.__subtitle_to_show)
            self.__new_subtitle = random.choice(self.__subtitles)
        self.__subtitle_to_show = self.__new_subtitle
        self.__subtitle_color = [198, 207, 207]
        self.__subtitle_final_color = self.__subtitles_colors.get(self.__subtitle_to_show)  # get the final color
        self.__subtitle_scale = [
            (self.__subtitle_final_color[0] - self.__subtitle_color[0])/80,
            (self.__subtitle_final_color[1] - self.__subtitle_color[1])/80,
            (self.__subtitle_final_color[2] - self.__subtitle_color[2])/80
        ]
        self.__no_article_shown = False
        self.__move_question = True

    
    def __manageQuestion(self):
        if self.__move_question:
            self.__final_question_pos = 105+self.__base_sub_width+self.__article_sub_width
            self.__move_question = False
        elif self.__question_pos != self.__final_question_pos:
            if self.__question_pos < self.__final_question_pos:
                self.__question_pos += 1
            else:
                self.__question_pos -= 1

    def __showEmojis(self):
        self.__emojis_image = pygame.image.load("emojis_test.png").convert_alpha()
        screen.screen.blit(self.__emojis_image, (700, 290))

class HelpScreen():  # NOT DONE FINISH CODING
    def __init__(self):
        self.__color_transition = [198, 207, 207]
        self.__buttons = Buttons()
        self.__help_msg1 = [
            "On Wikipedia, articles are linked together, so you can click through. The primary objective in this game is to guess, "
            "for a given article, what the first article linked from it is.",
            "For instance, on the article 'London', the first word linked is 'capital', which directs the user to the article 'Capital city'. "
            "You will start at a random article, and you want to",
            "guess the first link of the article you are in. Once you are correct, "
            "you will then move on to the linked article you guessed, and you will want to guess what the first article",
            "linked from that article is, and so forth, forming a chain of links until you reach one of the two "
            "scenarios which ends the game. These are as follows:",
            "",
            "1) By reach one of the Vital Articles—these are ten articles designated the most important on the site, and what the ten "
            "emojis on the home screen represent. Reaching",
            "any of the ten will end the game. They are:",
            "","","","","","","","","","","","","","","",
            "2) By entering a loop—in some circumstances the first article linked in article A is article B, and the first article linked in article B "
            "is article A. Obviously it would not be",
            "possible to reach a Vital Article, and so your game would end once you reach the loop."
        ]

    def showScreen(self):
        screen.showText("How to play", "Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        self.__showHelp1()
        self.__buttons.add("back", "circle", 20.0, [0, 0, 0], (100, 800), new=True, usepreviouscolor=False)

    def __showHelp1(self):
        for i in range(len(self.__help_msg1)):
            screen.showText(self.__help_msg1[i], "Helvetica.ttf", 16, (0, 0, 0), (100, 220+(22*i)))
        self.__emojis_image = pygame.image.load("emojis_labelled.png").convert_alpha()
        screen.screen.blit(self.__emojis_image, (429, 405))

        
    def checkButtons(self, mouse, click):
        if click:
            self.__clicked = self.__buttons.checkButtonHover(mouse, click)
            if self.__clicked[1] == "back":
                return "back"
        else:
            self.__buttons.checkButtonHover(mouse, click)

    def remakeScreen(self):
        screen.blankScreen()
        if self.__color_transition != [207, 207, 198]:
            self.__color_transition[0] += 1
            self.__color_transition[2] -= 1
            screen.setScreenColor(self.__color_transition)
        screen.showText("How to play", "Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        self.__showHelp1()
        self.__buttons.add("back", "circle", 20.0, [0, 0, 0], (100, 800), new=False, usepreviouscolor=True)

class AboutScreen():
    def __init__(self):
        self.__bodytext_ls = ["Flink (short for 'first link') was originally concieved as a holiday boredom project. It ended up turning into a behemoth",
                            "of API requests, wikitext parsing & filtering (NEVER AGAIN), pygame fuckery, and general madness.",
                            "",
                            "The game was originally a Discord bot, but that was abandoned after I realized how ass writing code for Discord is.", 
                            "",
                            "Wikipedia is written by Wikipedians. They are an inconsistent, error-prone, argumentative group of people, and the",
                            "wikitext they write (which is parsed by the game) is code gibberish and requires extensive filtering. This filtering is",
                            "done by an algorithm using Python string matching techniques (lord knows why I didn't use regex). The algorithm",
                            "cannot possibly catch every edge case or scenario. The majority of links and sentences should be readable, but",
                            "occasionally you might get garbled ones, just like real life, but instead here you can report it and I will try to fix it.",
                            "",
                            "Lastly, some wise words past me foolishly ignored:"
                            "", "", "",
                            "Oh well. Enjoy."
        ]
        self.__color_transition = [198, 207, 207]
        self.__buttons = Buttons()

    def showScreen(self):
        screen.showText("About", "Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        for i in range(len(self.__bodytext_ls)):
            screen.showText(self.__bodytext_ls[i], "Helvetica.ttf", 18, (0, 0, 0), (100, 200+(30*i)))
        screen.showText("""<AntiComposite> the first rule of parsing wikitext is "don't parse wikitext" """, "LTYPE.ttf", 16, (0, 0, 0), (110, 570))
        self.__buttons.add("back", "circle", 50.0, [0, 0, 0], (100, 600), new=True, usepreviouscolor=False)
        
    def checkButtons(self, mouse, click):
        if click:
            self.__clicked = self.__buttons.checkButtonHover(mouse, click)
            if self.__clicked[1] == "back":
                return "back"
        else:
            self.__buttons.checkButtonHover(mouse, click)

    def remakeScreen(self):
        screen.blankScreen()
        if self.__color_transition != [207, 198, 207]:
            self.__color_transition[0] += 1
            self.__color_transition[1] -= 1
            screen.setScreenColor(self.__color_transition)
        screen.showText("About", "Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        for i in range(len(self.__bodytext_ls)):
            screen.showText(self.__bodytext_ls[i], "Helvetica.ttf", 18, (0, 0, 0), (100, 200+(30*i)))
        screen.showText("""<AntiComposite> the first rule of parsing wikitext is "don't parse wikitext" """, "LTYPE.ttf", 16, (0, 0, 0), (110, 570))
        self.__buttons.add("back", "circle", 20.0, [0, 0, 0], (100, 800), new=False, usepreviouscolor=True)
        
class Game():
    def __init__(self):
        self.__run = True
        self.__status = "home"
    
    def run(self):
        self.__homescreen = HomeScreen()
        self.__homescreen.showScreen("none")
        screen.playMusic()
        while self.__run == True:
            if self.__status == "home":
                self.__runHomeScreen()
            elif self.__status == "game":
                self.__runHelpScreen()
            elif self.__status == "howtoplay":  # create screens
                self.__runHelpScreen()
            elif self.__status == "about":
                self.__runAboutScreen()
            screen.updateScreen()

        pygame.quit()

    def __runHomeScreen(self):
        self.__homescreen.checkTextButtons(pygame.mouse.get_pos(), click=False)
        self.__homescreen.remakeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__homescreen_button = self.__homescreen.checkTextButtons(pygame.mouse.get_pos(), click=True)
                if self.__homescreen_button == "game":
                    screen.blankScreen()
                    screen.stopMusic()
                    self.__homescreen.remakeScreen()
                    self.__status = "game"

                elif self.__homescreen_button == "howtoplay":
                    screen.blankScreen()
                    self.__helpscreen = HelpScreen()
                    self.__status = "howtoplay"
                    self.__helpscreen.showScreen()

                elif self.__homescreen_button == "about":
                    screen.blankScreen()
                    self.__aboutscreen = AboutScreen()
                    self.__status = "about"
                    self.__aboutscreen.showScreen()


    def __runHelpScreen(self):
        self.__helpscreen.checkButtons(pygame.mouse.get_pos(), click=False)
        self.__helpscreen.remakeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__helpscreen_button = self.__helpscreen.checkButtons(pygame.mouse.get_pos(), click=True)
                if self.__helpscreen_button == "back":
                    screen.blankScreen()
                    self.__status = "home"
                    self.__homescreen = HomeScreen()
                    self.__homescreen.showScreen("howtoplay")
                
    def __runAboutScreen(self):
        self.__aboutscreen.checkButtons(pygame.mouse.get_pos(), click=False)
        self.__aboutscreen.remakeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__aboutscreen_button = self.__aboutscreen.checkButtons(pygame.mouse.get_pos(), click=True)
                if self.__aboutscreen_button == "back":
                    screen.blankScreen()
                    self.__status = "home"
                    self.__homescreen = HomeScreen()
                    self.__homescreen.showScreen("about")

screen = ScreenOperations()                
game = Game()
game.run()

# MAKE ICON FOR BACK BUTTON
# MAKE PROGRESS BAR
# MAKE LOADING SCREEN
# IMPLEMENT GAME