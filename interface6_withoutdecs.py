import pygame
import random
import hints
import screen_operations
import os
import requests.exceptions
import threading

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

class ImageButtons():
    def __init__(self):
        self.__hover = False
        self.__buttons_names = []
        self.__buttons = []
        self.__buttons_locations = {}
        self.__buttons_status = {}
        self.__buttons_disabled_allowed = {}
        self.__buttons_dimensions = {}

    def add(self, name, location, dimensions, new, disable):
        if new:
            self.__buttons_names.append(name)
            self.__buttons.append(self.__createButton(name, location, dimensions, hover=False, disabled=False))
            if disable:
                self.__buttons_disabled_allowed.update({name: True})
            else:
                self.__buttons_disabled_allowed.update({name: False})
        else:
            if self.__buttons_status[name] == "disabled":
                self.__createButton(name, location, dimensions, hover=False, disabled=True)
            elif self.__buttons_status[name] == "hover":
                self.__createButton(name, location, dimensions, hover=True, disabled=False)
            else:
                self.__createButton(name, location, dimensions, hover=False, disabled=False)

    def __createButton(self, name, location, dimensions, hover: bool, disabled: bool):
        if disabled:
            self.__button_image_loc = fr"{RESOURCES}\b_{name}_disabled.png"
            self.__buttons_status.update({name: "disabled"})
        elif hover:
            self.__button_image_loc = fr"{RESOURCES}\b_{name}_hover.png"
            self.__buttons_status.update({name: "hover"})
        else:
            self.__button_image_loc = fr"{RESOURCES}\b_{name}.png"
            self.__buttons_status.update({name: "active"})

        self.__button_image = pygame.image.load(self.__button_image_loc).convert_alpha()
        screen.screen.blit(self.__button_image, (location[0], location[1]))
        self.__buttons_locations.update({name: location})
        self.__buttons_dimensions.update({name: dimensions})

    def checkButtonHover(self, mouse, click):  # check that the mouse doesn't cover a button
        for but in range(len(self.__buttons)):
            if click:
                self.__button_pressed = self.__mouseHover(mouse, self.__buttons_names[but], click)
                if self.__button_pressed != (False, ""):
                    return self.__button_pressed  # if clicked, return the button name that was clicked
            else:
                self.__mouseHover(mouse, self.__buttons_names[but], click)
        if click:
            return (False, "")
    
    def resetDisabledButtons(self):
        for name in self.__buttons_names:
            self.__buttons_status[name] = "active"

    def __mouseHover(self, mousepos, name, click: bool):
        self.__hover_location = self.__buttons_locations.get(name)
        if (self.__hover_location[0] <= mousepos[0] <= (self.__hover_location[0] + self.__buttons_dimensions[name][0])) and (self.__hover_location[1] <= mousepos[1] <= (self.__hover_location[1] + self.__buttons_dimensions[name][1])):
            self.__hover = True
        else:
            self.__hover = False

        if self.__hover and click and self.__buttons_status[name] != "disabled":  # why is this here
            pygame.mixer.music.load(fr"{RESOURCES}\button.wav")
            pygame.mixer.music.play()
            if self.__buttons_disabled_allowed[name]:  # only disable the button if it's allowed to be
                self.__createButton(name, self.__hover_location, self.__buttons_dimensions[name], hover=False, disabled=True)
            else:
                self.__createButton(name, self.__hover_location, self.__buttons_dimensions[name], hover=False, disabled=False)
            return (True, name)
        else:
            if self.__buttons_status[name] == "disabled":
                self.__createButton(name, self.__hover_location, self.__buttons_dimensions[name], hover=False, disabled=True)
            elif self.__hover:
                self.__createButton(name, self.__hover_location, self.__buttons_dimensions[name], hover=True, disabled=False)
            else:
                self.__createButton(name, self.__hover_location, self.__buttons_dimensions[name], hover=False, disabled=False)
            return (False, "")            

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
            self.startgame_button = self.__createButton(name, self.__buttons_text.get(name), fr"{RESOURCES}\Helvetica.ttf", 30, [0, 80, 89], self.__hover_location, usepreviouscolor=False)
        
        elif not self.__hover and self.__buttons_color.get(name) == [0, 80, 89]:
            screen.createRectangle("#c6cfcf", [obj.get_width(), obj.get_height()], self.__hover_location)
            self.startgame_button = self.__createButton(name, self.__buttons_text.get(name), fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], self.__hover_location, usepreviouscolor=False)
        
        if self.__hover and click:  # if the button is clicked on
            pygame.mixer.music.load(fr"{RESOURCES}\button.wav")
            pygame.mixer.music.play()
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
        self.__question_fade = [2.475, 2.5875, 2.5875]  # start inverted because it will be multiplied by -1 at start
        self.__subtitle_to_show = ""
        self.__startgame_text = "[[start game]]"

    def showScreen(self, prev):
        screen.showText("Flink", fr"{RESOURCES}\Helvetica.ttf", 100, (0, 0, 0), (100, 100))
        screen.showText("How well do you know", fr"{RESOURCES}\Helvetica-Bold.ttf", 18, (0, 0, 0), (105, 200))
        self.__showEmojis()
        self.__text_buttons.add("startgame", self.__startgame_text, fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], (105, 300), new=True, usepreviouscolor=False)
        self.__text_buttons.add("howtoplay", "[[how to play]]", fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], (105, 380), new=True, usepreviouscolor=False)
        self.__text_buttons.add("about", "[[about]]", fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], (105, 460), new=True, usepreviouscolor=False)
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
        screen.blankScreen()  # blank the screen
        if self.__color_transition != [198, 207, 207]:  # if the screen color isn't the final color, transition
            if self.__prev == "about":
                self.__color_transition[0] -= 1
                self.__color_transition[1] += 1
            elif self.__prev == "howtoplay":
                self.__color_transition[0] -= 1
                self.__color_transition[2] += 1
            screen.setScreenColor(self.__color_transition)
        screen.showText("Flink", fr"{RESOURCES}\Helvetica-Bold.ttf", 100, (0, 0, 0), (100, 100))  # show the title
        if self.__no_article_shown:  # if there is no article shown
            self.__chooseArticle()  # pick and article
        self.__base_sub_width = screen.showText("How well do you know ", fr"{RESOURCES}\Helvetica.ttf", 18, (0, 0, 0), (105, 200))  # render the subtitle
        self.__article_sub_width = screen.showText(self.__subtitle_to_show, fr"{RESOURCES}\Helvetica.ttf", 18, self.__subtitle_color, (105+self.__base_sub_width, 200))
        self.__updateArticle()  # update them for the fading
        screen.showText("?", fr"{RESOURCES}\Helvetica.ttf", 18, self.__question_color, (105+self.__question_pos, 200))
        self.__text_buttons.add("startgame", self.__startgame_text, fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], (105, 300), new=False, usepreviouscolor=True)
        self.__text_buttons.add("howtoplay", "[[how to play]]", fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], (105, 380), new=False, usepreviouscolor=True)
        self.__text_buttons.add("about", "[[about]]", fr"{RESOURCES}\Helvetica.ttf", 30, [0, 0, 0], (105, 460), new=False, usepreviouscolor=True)
        self.__showEmojis()

    def __updateArticle(self):
        self.__question_pos = self.__article_sub_width + self.__base_sub_width
        self.__check_subtitle_color = (round(self.__subtitle_color[0]), round(self.__subtitle_color[1]), round(self.__subtitle_color[2]))
        if self.__check_subtitle_color != self.__subtitle_final_color:  # if they're different colors
            if self.__hold:  # hold
                self.__hold_count += 1
                if self.__hold_count == 200:
                    self.__hold = False
            else:  # if the transition should happen
                for i in range(3):
                    self.__subtitle_color[i] += self.__subtitle_scale[i]
                    self.__question_color[i] += self.__question_fade[i]
        elif self.__subtitle_final_color != (198, 207, 207):  # if the subtitle color is fully its color and not bgrd (it has just finished fading in)
            self.__hold = True
            self.__hold_count = 0
            for i in range(3): # flip the fades to fade out
                self.__subtitle_scale[i] = self.__subtitle_scale[i]*-1
                self.__question_fade[i] = self.__question_fade[i]*-1
            self.__subtitle_final_color = (198, 207, 207)  # make the target the background for fade out
        elif self.__check_subtitle_color == self.__subtitle_final_color and self.__subtitle_final_color == (198, 207, 207):
            self.__no_article_shown = True

    def __chooseArticle(self):
        self.__hold = False
        self.__new_subtitle = random.choice(self.__subtitles)
        while self.__subtitle_to_show == self.__new_subtitle: # choose a random article
            self.__new_subtitle = random.choice(self.__subtitles)
        self.__subtitle_to_show = self.__new_subtitle
        self.__subtitle_color = [198, 207, 207]
        self.__question_color = [198, 207, 207]
        self.__subtitle_final_color = self.__subtitles_colors.get(self.__subtitle_to_show)  # get the final color
        self.__subtitle_scale = [
            (self.__subtitle_final_color[0] - self.__subtitle_color[0])/80,
            (self.__subtitle_final_color[1] - self.__subtitle_color[1])/80,
            (self.__subtitle_final_color[2] - self.__subtitle_color[2])/80
        ]
        for i in range(3):
            self.__question_fade[i] = self.__question_fade[i]*-1
        self.__no_article_shown = False
        self.__move_question = True

    def __showEmojis(self):
        self.__emojis_image = pygame.image.load(fr"{RESOURCES}\emojis_test.png").convert_alpha()
        screen.screen.blit(self.__emojis_image, (700, 290))

    def setLoading(self):
        self.__startgame_text = "[[loading]]"

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
        screen.showText("How to play", fr"{RESOURCES}\Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        self.__showHelp1()
        self.__buttons.add("back", "circle", 20.0, [0, 0, 0], (100, 800), new=True, usepreviouscolor=False)

    def __showHelp1(self):
        for i in range(len(self.__help_msg1)):
            screen.showText(self.__help_msg1[i], fr"{RESOURCES}\Helvetica.ttf", 16, (0, 0, 0), (100, 220+(22*i)))
        self.__emojis_image = pygame.image.load(fr"{RESOURCES}\emojis_labelled.png").convert_alpha()
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
        screen.showText("How to play", fr"{RESOURCES}\Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        self.__showHelp1()
        self.__buttons.add("back", "circle", 20.0, [0, 0, 0], (100, 800), new=False, usepreviouscolor=True)

class AboutScreen():
    def __init__(self):
        self.__bodytext_ls = ["Flink (short for 'first link') was originally concieved as a holiday boredom project. It ended up turning into a behemoth",
                            "of API requests, wikitext parsing & filtering (NEVER AGAIN), pygame hell, and general madness.",
                            "",
                            "The game was originally a Discord bot, but that was abandoned after I realized how bad writing code for Discord is.", 
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
        screen.showText("About", fr"{RESOURCES}\Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        for i in range(len(self.__bodytext_ls)):
            screen.showText(self.__bodytext_ls[i], fr"{RESOURCES}\Helvetica.ttf", 18, (0, 0, 0), (100, 200+(30*i)))
        screen.showText("""<AntiComposite> the first rule of parsing wikitext is "don't parse wikitext" """, fr"{RESOURCES}\LTYPE.ttf", 16, (0, 0, 0), (110, 570))
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
        screen.showText("About", fr"{RESOURCES}\Helvetica-Bold.ttf", 80, (0, 0, 0), (100, 100))
        for i in range(len(self.__bodytext_ls)):
            screen.showText(self.__bodytext_ls[i], fr"{RESOURCES}\Helvetica.ttf", 18, (0, 0, 0), (100, 200+(30*i)))
        screen.showText("""<AntiComposite> the first rule of parsing wikitext is "don't parse wikitext" """, fr"{RESOURCES}\LTYPE.ttf", 16, (0, 0, 0), (110, 570))
        #screen.screen.blit(pygame.image.load("game_drawing2.png").convert_alpha(), (850, 190))
        self.__buttons.add("back", "circle", 20.0, [0, 0, 0], (100, 800), new=False, usepreviouscolor=True)

class GameScreen():
    def __init__(self):  # UNCOMMENT BACKEND WHEN IT'S DONE; COMMENTED FOR SPEED
        self.__connected = True
        self.__hints = intf.getHints()
        self.__finished_setup = False

    def setupGame(self):
        try:
            self.__hints.startGame()
        except requests.exceptions.ConnectionError:
            self.__connected = False
        self.__finished_setup = True

    def startGame(self):
        self.__page_title = self.__hints.returnPageTitle()
        self.__buttons = ImageButtons()
        self.__guess_box_length = self.__hints.findLongestLink()
        self.__inputted_text = ""
        self.__guess_box_color = [207, 207, 207]
        self.__animate_guess = False
        self.__progress_box = len(self.__hints.getLinks()[0]) - 1
        self.__progress_box_correct = -1
        self.__hints_used = []
        self.__first_sentence = self.__hints.revealFirstSentence()
        for i in range(self.__progress_box):
            self.__hints_used.append(0)

    def returnConnected(self):
        return self.__connected
    
    def returnFinishedSetup(self):
        return self.__finished_setup

    def addToInput(self, char, raw: bool):
        if len(self.__inputted_text) < self.__guess_box_length:
            if not raw:  # if it's the ord value and not the actual char
                self.__inputted_text += chr(char)
            else:
                self.__inputted_text += char

    def removeFromInput(self):
        if len(self.__inputted_text) > 0:
            self.__inputted_text = self.__inputted_text[:-1]

    def __drawProgressBoxes(self):
        for i in range(self.__progress_box):
            if i <= self.__progress_box_correct:
                screen.createRectangle("#9cacac", (50, 50), (100, 100+55*i), radius=5)
                if self.__hints_used[i] == 1:  # if hint used
                    screen.createRectangle((255, 242, 137), (46, 46), (102, 102+55*i), radius=5)
                elif self.__hints_used[i] == 0:  # if hint not used
                    screen.createRectangle((180, 217, 178), (46, 46), (102, 102+55*i), radius=5)
                elif self.__hints_used[i] == 2:  # if link was fully revealed by hints
                    screen.createRectangle((180, 0, 0), (46, 46), (102, 102+55*i), radius=5)
            else:
                screen.createRectangle("#9cacac", (50, 50), (100, 100+55*i), radius=5)
                screen.createRectangle((207, 207, 207), (46, 46), (102, 102+55*i), radius=5)

    def showScreen(self, new: bool, end=False):
        if not end:
            self.__drawHintsBox(new)
            self.__drawProgressBoxes()
            if self.__animate_guess:
                self.__guessAnimation(self.__color_to_animate_guess)  # flash green or red on guess box
            self.__drawGuessBox()
            self.__drawPageTitle()
            self.__drawFirstSentence()
            screen.centreTextHorizontally(self.__inputted_text, fr"{RESOURCES}\Helvetica.ttf", 32, (0, 0, 0), 200)
            if new:
                self.__buttons.add("sound_off", (700, 700), (50, 50), new=new, disable=False)
                self.__buttons.add("sound_on", (700, 700), (50, 50), new=new, disable=False)
            else:
                self.__buttons.add(intf.checkMute(), (700, 700), (50, 50), new=new, disable=False)
        else:
            if new:
                self.__endlinks = self.__hints.endScreenAllLinks()
            self.__drawProgressBoxes()
            self.__buttons.add('quit', (1000, 700), (50, 50), new=new, disable=False)
            for i in range(self.__progress_box):
                screen.showText(f"{self.__endlinks[i]}", fr"{RESOURCES}\Helvetica.ttf", 30, (0, 0, 0), (162, 108+55*i))


    def __drawPageTitle(self):
        screen.createRectangle("#9cacac", [22*self.__guess_box_length+4, 56], (700-(11*self.__guess_box_length)-2, 96))
        screen.createRectangle((184, 195, 195), [22*self.__guess_box_length, 52], (700-(11*self.__guess_box_length), 98))
        screen.centreTextHorizontally(self.__page_title, fr"{RESOURCES}\Helvetica-Bold.ttf", 40, (0, 0, 0), 107)

    def __drawFirstSentence(self):
        self.__sentence_box_dimensions = self.__calculateSentenceBox(self.__first_sentence)
        screen.createRectangle("#9cacac", [16*self.__sentence_box_dimensions[0]+4, 40*self.__sentence_box_dimensions[1]+4], (700-(8*self.__sentence_box_dimensions[0])-2, 396))
        screen.createRectangle((184, 195, 195), [16*self.__sentence_box_dimensions[0], 40*self.__sentence_box_dimensions[1]], (700-(8*self.__sentence_box_dimensions[0]), 398))
        for i in range(len(self.__sentence_box_dimensions[2])):
            screen.showText(self.__sentence_box_dimensions[2][i], fr"{RESOURCES}\Helvetica.ttf", 32, (0, 0, 0), (712-(8*self.__sentence_box_dimensions[0])-2, 404+(36*i)))

    def __calculateSentenceBox(self, fs: str):
        fsl = fs.split()
        fsl2 = []
        total = 0
        total_temp = 0
        for i in fsl:
            if total_temp > 45:
                fsl2.append(total)
                total_temp = 0
            total += len(i)+1  # +1 for the space
            total_temp += len(i)+1
        if total_temp != 0:
            fsl2.append(len(fs))
        for j in range(len(fsl2)-1, 0, -1):
            fsl2[j] = (fsl2[j-1], fsl2[j])
        fsl2[0] = (0, fsl2[0])
        for k in range(len(fsl2)):
            fsl2[k] = fs[fsl2[k][0]:fsl2[k][1]]  # add sentence to end
        for m in range(len(fsl2) - 1):
            fsl2[m] = fsl2[m][:-1]
        max_line_length = 0
        for n in fsl2:
            if len(n) > max_line_length:
                max_line_length = len(n)
        return (max_line_length, len(fsl2), fsl2)

    def __drawHintsBox(self, new):
        screen.createRectangle("#9cacac", (178, 232), (1190, 406))
        screen.createRectangle("#c6cfcf", (93, 42), (1232, 385))
        screen.createRectangle("#c6cfcf", (174, 228), (1192, 408))
        screen.showText("Hints", fr"{RESOURCES}\Helvetica.ttf", 32, (0, 0, 0), (1242, 390))
        self.__buttons.add('random', (1200, 430), (158, 59), new=new, disable=False)
        self.__buttons.add('vowel', (1200, 500), (158, 59), new=new, disable=True)
        self.__buttons.add('startswith', (1200, 570), (158, 59), new=new, disable=True)

    def __drawGuessBox(self):
        screen.createRectangle("#9cacac", [20*self.__guess_box_length+4, 52], ((700-10*self.__guess_box_length)-2, 190))
        screen.createRectangle(self.__guess_box_color, [20*self.__guess_box_length, 48], (700-10*self.__guess_box_length, 192))
    
    def __guessAnimationSetup(self):
        self.__hold = 0
        self.__to_color = True
        self.__animate_guess = True
    
    def __guessAnimation(self, color):
        if self.__to_color == True:
            if round(self.__guess_box_color[0]) != color[0] and round(self.__guess_box_color[1]) != color[1] and round(self.__guess_box_color[2]) != color[2]:
                self.__guess_box_color[0] += (color[0]-207)/10
                self.__guess_box_color[1] += (color[1]-207)/10
                self.__guess_box_color[2] += (color[2]-207)/10
            else:
                self.__hold += 1
                if self.__hold == 5:
                    self.__to_color = False
                    self.__hold = 0
        else:
            if round(self.__guess_box_color[0]) != 207 and round(self.__guess_box_color[1]) != 207 and round(self.__guess_box_color[2]) != 207:
                self.__guess_box_color[0] -= (color[0]-207)/10
                self.__guess_box_color[1] -= (color[1]-207)/10
                self.__guess_box_color[2] -= (color[2]-207)/10
            else:
                self.__hold += 1
                if self.__hold == 5:
                    self.__animate_guess = False

    def remakeScreen(self, end=False):
        screen.blankScreen()
        self.showScreen(False, end=end)

    def checkTextButtons(self, mouse, click):
        if click:
            self.__clicked = self.__buttons.checkButtonHover(mouse, click)
            if self.__clicked[1] == "vowel":
                self.__first_sentence = self.__hints.revealsVowels()
                self.__hints_used[self.__progress_box_correct+1] = 1
            elif self.__clicked[1] == "random":
                self.__first_sentence = self.__hints.revealRandom()
                if self.__first_sentence == False:
                    self.__hints_used[self.__progress_box_correct+1] = 2
                    self.checkGuess(override=True)
                else:
                    self.__hints_used[self.__progress_box_correct+1] = 1
            elif self.__clicked[1] == "startswith":
                self.__first_sentence = self.__hints.startsWith()
                self.__hints_used[self.__progress_box_correct+1] = 1
            elif self.__clicked[1] == "quit":
                return "quit"
            elif self.__clicked[1] == "sound_on" or self.__clicked[1] == "sound_off":
                intf.setMute()
            elif self.__clicked[1] == "quit":
                return True
        else:
            self.__buttons.checkButtonHover(mouse, click)

    def checkGuess(self, override=False):  # override used to move to next link when fully revealed
        if override:
                self.__color_to_animate_guess = (190, 227, 188)
                self.__page_title = self.__hints.returnPageTitle()
                self.__first_sentence = self.__hints.revealFirstSentence()
                self.__buttons.resetDisabledButtons()
                self.__progress_box_correct += 1
        else:
            if self.__inputted_text != "":
                if self.__hints.checkGuess(self.__inputted_text):  # get the text inputted and check if the guess is correct
                    self.__inputted_text = ""
                    pygame.mixer.music.load(fr"{RESOURCES}\correct.wav")
                    pygame.mixer.music.play()
                    self.__guessAnimationSetup()
                    self.__color_to_animate_guess = (190, 227, 188)
                    self.__page_title = self.__hints.returnPageTitle()
                    try:
                        self.__first_sentence = self.__hints.revealFirstSentence()
                    except IndexError:
                        self.__progress_box_correct += 1
                        return False
                    else:
                        self.__buttons.resetDisabledButtons()
                        self.__progress_box_correct += 1
                        return True
                else:
                    pygame.mixer.music.load(fr"{RESOURCES}\incorrect.wav")
                    pygame.mixer.music.play()
                    self.__guessAnimationSetup()
                    self.__color_to_animate_guess = (232, 116, 116)
                self.__inputted_text = ""
                return True

class EndGameScreen():
    def __init__(self):
        self.__buttons = ImageButtons()

    def showScreen(self, new=False):
        # add the progress
        # add the list of articles from the hints page
        # add a header
        self.__buttons.add(new=new)  # add a quit button

class Interface():
    def __init__(self):
        self.__run = True
        self.__valid_inputs = [32, 44, 46, 59, 39, 35, 45, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 61, 47] # space , . ; ' # - 1 2 3 4 5 6 7 8 9 0 = /
        self.__shift_inputs = {
            32: " ",  # this is just a space and nothing happens if you shift a space i just didn't want ANOTHER if statement
            44: "<",
            46: ">",
            59: ":",
            39: "@",
            35: "~",
            45: "_",
            49: "!",
            50: '"',
            51: "£",
            52: "$",
            53: "%",
            54: "^",
            55: "&",
            56: "*",
            57: "(",
            48: ")",
            61: "+",
            47: "?",
        }
        self.__status = "home"
        self.__shift = False
        self.__mute = False
        self.__hints: hints.Hints = hints.Hints()  # typeset so the methods come up
        self.__icon = pygame.image.load(fr"{RESOURCES}\icon.png").convert_alpha()  # MOVE ALL OF THIS TO SCREEN OPERATIONS
        pygame.display.set_icon(self.__icon)

    def run(self):
        self.__homescreen = HomeScreen()
        self.__homescreen.showScreen("none")
        #screen.playMusic()
        while self.__run == True:
            if self.__status == "home":
                self.__runHomeScreen()
            elif self.__status == "setupgame":
                self.__gamescreen = None
                self.__gamescreen = GameScreen()
                self.__sg_thread = threading.Thread(target=self.__startGame)
                self.__sg_thread.start()
                self.__status = "setupinprogress"
            elif self.__status == "setupinprogress":
                self.__runSetupGame()
            elif self.__status == "game":
                self.__runGameScreen()
            elif self.__status == "howtoplay":  # create screens
                self.__runHelpScreen()
            elif self.__status == "about":
                self.__runAboutScreen()
            elif self.__status == "disconnected":
                self.__runDisconnectedScreen()
            elif self.__status == "endgame":
                self.__runEndGame()
            screen.updateScreen()
        pygame.quit()

    def __runEndGame(self):
        self.__gamescreen.checkTextButtons(pygame.mouse.get_pos(), click=False)
        self.__gamescreen.remakeScreen(end=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__gamescreen_button = self.__gamescreen.checkTextButtons(pygame.mouse.get_pos(), click=True)
                if self.__gamescreen_button:
                    self.__homescreen = HomeScreen()
                    self.__homescreen.showScreen("none")
                    self.__status = "home"
        
    def __runSetupGame(self):
        self.__homescreen.setLoading()
        self.__homescreen.remakeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
        if self.__gamescreen.returnFinishedSetup():
            self.__sg_thread.join()
            if not self.__gamescreen.returnConnected():
                self.__status = "disconnected"
            else:
                self.__gamescreen.startGame()  # assign all the variables
                self.__gamescreen.showScreen(True)
                self.__status = "game"
                pygame.mixer.music.set_volume(0.1)

    def __startGame(self):            
        self.__gamescreen.setupGame()

    def getHints(self):
        return self.__hints
    
    def __runDisconnectedScreen(self):
        screen.blankScreen()
        screen.centreTextHorizontally("No connection", fr"{RESOURCES}\Helvetica-Bold.ttf", 80, (0, 0, 0), 100)
        screen.centreTextHorizontally("Please ensure you are connected to the internet, and restart the game.", fr"{RESOURCES}\Helvetica.ttf", 40, (0, 0, 0), 250)
        screen.centreTextHorizontally("There is a very small chance the Wikimedia servers are down. But it's probably you.", fr"{RESOURCES}\Helvetica.ttf", 14, (0, 0, 0), 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False

    def __runGameScreen(self):
        self.__gamescreen.checkTextButtons(pygame.mouse.get_pos(), click=False)
        self.__gamescreen.remakeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__gamescreen_button = self.__gamescreen.checkTextButtons(pygame.mouse.get_pos(), click=True)
                if self.__gamescreen_button == "quit":  # IMPLEMENT BUT MAKE ALL OTHERS IN THE PYGAME CLASS
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key != 13 and event.key != 8: #if not enter (13) or backspace (8)
                    if 97 <= event.key and event.key <= 122 or event.key in self.__valid_inputs: #if a valid input
                        if self.__shift == True:  # if the shift is true
                            self.__shift = False
                            if event.key in self.__valid_inputs:  # if it's not a letter, take the new symbol
                                self.__gamescreen.addToInput(self.__shift_inputs.get(event.key), raw=True)
                            else:  # if it is a letter, just make it capital
                                self.__gamescreen.addToInput(event.key-32, raw=False)
                        else:  # if it's not a shift just paste the character
                            self.__gamescreen.addToInput(event.key, raw=False)  # show it
                    elif event.key == 1073742053 or event.key == 1073742049:  # if shift
                        self.__shift = True
                elif event.key == 8:  # if it's a backspace, get rid of it
                    self.__gamescreen.removeFromInput()
                elif event.key == 13:  # enter
                    if not self.__gamescreen.checkGuess():
                        self.__gamescreen.showScreen(True, end=True)
                        self.__status = "endgame"

    def __runHomeScreen(self):
        self.__homescreen.checkTextButtons(pygame.mouse.get_pos(), click=False)
        self.__homescreen.remakeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__homescreen_button = self.__homescreen.checkTextButtons(pygame.mouse.get_pos(), click=True)
                if self.__homescreen_button == "game":
                    self.__status = "setupgame"

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

    def setMute(self):
        if self.__mute:
            pygame.mixer.music.set_volume(0.1)
        else:
            pygame.mixer.music.set_volume(0)
        self.__mute = not self.__mute

    def checkMute(self):
        if self.__mute:
            return "sound_off"
        else:
            return "sound_on" 

resources = os.path.dirname(os.path.abspath(__file__))
RESOURCES = resources + r"\resources"
screen = screen_operations.ScreenOperations()                
intf = Interface()
intf.run()

#TO DO
# add mute and back buttons
# fix game end
# fix showscreen etc
# mod to local variables