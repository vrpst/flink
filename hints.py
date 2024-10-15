import oldother.wikilink_func2 as wikilink_func2
import random

class Hints():
    def __init__(self):
        self.__real_links = []
        self.__display_links = []
        self.__first_sentences = []
        self.__real_link_dupe = []  # to display the progression at the end
        self.__game = False
        self.__length_hints = []
        self.__placeholders = []
        self.__placeholders_real = []

    def startGame(self):
        self.__lists = wikilink_func2.run()
        self.__real_links = self.__lists[0]  # create the list of actual article titles (will get trimmed as game goes on)
        self.__real_link_dupe = self.__lists[0]   # create the list of article titles unmodified (for progression)
        self.__display_links = self.__lists[1]  # create list of displayed links
        self.__prog_length = len(self.__lists[0])  # TO BE IMPLEMENTED; DO SOMETHING
        self.__prog_progress = 1
        self.__game = True
        self.__placeholders = self.__makePlaceholders(self.__display_links)  # make placeholder first
        self.__placeholders_real = self.__makePlaceholders(self.__real_link_dupe)  # make placeholders with real links for prog
        self.__first_sentences = self.__removeLinkFromSentence(self.__lists[2])  # replace links in firstsen with placeholders

    def getLinks(self):
        return (self.__lists[0], self.__lists[1])
                
    def checkGuess(self, guess):
        if guess.lower() == self.__display_links[0].lower() or guess.lower() == self.__real_links[1].lower():  # guess
            if len(self.__real_links) != 1:  # if it wasn't the final guess
                self.__moveToNextLink()
            else:  # GAME IS OVER
                self.__game = False
            return True
                # DO SOMETHING TO END THE GAME
        else:
            # DEAL WITH INCORRECT GUESS
            return False
        
    def findLongestLink(self):  # find the longest link possible so the box is never too small, get rid of testing with link
        self.__longest = [0, ""]
        for i in self.__real_links:
            if len(i) > self.__longest[0]:
                self.__longest[0] = len(i)
                self.__longest[1] = i
        for i in self.__display_links:
            if len(i) > self.__longest[0]:
                self.__longest[0] = len(i)
                self.__longest[1] = i
        return self.__longest[0]
    
    def returnPageTitle(self):
        return self.__real_links[0]

    def revealLength(self):  ## WORKS ## # REVEALS THE LENGTH OF THE LINK IN HANGMAN FORMAT
        self.__split_link = self.__display_links[0].split(" ")
        for i in range(len(self.__split_link)):
            self.__split_link[i] = len(self.__split_link[i])
        print(self.__length_hints[0])
        
    def revealFirstSentence(self):  ## WORKS ## REVEALS THE FIRST SENTENCE
        return self.__first_sentences[0]

    def revealsVowels(self):  ## WORKS ##
        self.__vowels = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")
        self.__new_placeholder = ""
        for i in range(len(self.__display_links[0])):
            if self.__display_links[0][i] in self.__vowels:
                self.__new_placeholder += self.__display_links[0][i]   # i+1 to account for `
            else:
                self.__new_placeholder += self.__placeholders[0][i+1]
        self.__placeholders[0] = self.__new_placeholder
        self.__updateSentence()
        return self.__verifyAndSendHint()

    def revealRandom(self):  ## WORKS ##
        self.__rand_index = random.randint(0, len(self.__display_links[0])-1)  # -1 because len is one larger than max index
        while 65 <= ord(self.__placeholders[0].upper()[self.__rand_index]) <=90 or ord(self.__placeholders[0][self.__rand_index]) == 32:  # if already revealed or a space, roll again
            self.__rand_index = random.randint(0, len(self.__display_links[0])-1)
        self.__placeholders[0] = self.__placeholders[0][:self.__rand_index] + self.__display_links[0][self.__rand_index] + self.__placeholders[0][self.__rand_index+1:]
        self.__updateSentence()
        return self.__verifyAndSendHint()

    def startsWith(self):  ## NEED TO TEST
        self.__placeholders[0] = "`" + self.__display_links[0][0] + self.__placeholders[0][2:]
        for i in range(len(self.__display_links[0])):
            if self.__display_links[0][i] == " ":
                self.__placeholders[0] = self.__placeholders[0][:i+2] + self.__display_links[0][i+1] + self.__placeholders[0][i+3:]  # this shouldn't be a problem with adding because no link ends in a space
        self.__updateSentence()
        return self.__verifyAndSendHint()            
        
        # no else so everything not a command attempt is ignored

    def __removeLinkFromSentence(self, sen):  ## WORKS ## to avoid prefixes (subregion vs region)
        for s in range(len(sen)):
            self.__word = " " + self.__display_links[s]
            self.__length_hints.append(self.__placeholders[s])
            sen[s] = sen[s][:sen[s].index(self.__word)+1] + self.__placeholders[s] + sen[s][len(self.__word)+sen[s].index(self.__word):]  # worst line of python ever (put the placeholder in the sentence)
        return sen

    def __makePlaceholders(self, words_to_replace):  ## WORKS  ##
        self.__ph = []
        for i in range(len(words_to_replace)):
            self.__wordlen = words_to_replace[i].split(" ")
            for w in range(len(self.__wordlen)):
                self.__wordlen[w] = len(self.__wordlen[w])
            placeholder = ""
            for j in self.__wordlen:  # build the placeholder
                placeholder += j*"_"
                placeholder += " "
            placeholder = placeholder[:-1]
            self.__ph.append(placeholder)
        return self.__ph

    def __updateSentence(self):  ## WORKS ## # update the sentence the word is used in with the hints that have been used
        self.__mono = self.__first_sentences[0].index("_")
        self.__first_sentences[0] = self.__first_sentences[0][:self.__mono] + self.__placeholders[0] + self.__first_sentences[0][self.__mono+len(self.__placeholders[0]):]

    def __verifyAndSendHint(self):  # used to verify the link hasn't been revealed by all the hints
        if self.__placeholders[0] == self.__display_links[0]:
            self.__moveToNextLink()
            if len(self.__real_links) == 1:
                # LINK WAS FULLY REVEALED; DO SOMETHING TO ACKNOWLEDGE
                pass
        else:
            return self.__placeholders[0]

    def __moveToNextLink(self):  ## WORKS I THINK ##
        self.__real_links = self.__real_links[1:]
        self.__display_links = self.__display_links[1:]  # sort out final link
        self.__first_sentences = self.__first_sentences[1:]
        self.__length_hints = self.__length_hints[1:]
        self.__placeholders = self.__placeholders[1:]
        self.__placeholders_real = self.__placeholders_real[1:]
        self.__prog_progress += 1

    def makeProgression(self, prog_progress, prog_length):  ## WORKS ## # if prog = progtotal then the end is reached and it uses the links 
        self.__progression = []
        if prog_progress == prog_length:
            self.__progression = self.__real_link_dupe
        else:
            for i in range(prog_progress):
                self.__progression.append(self.__real_link_dupe[i])
            for j in range(prog_progress, prog_length):
                self.__progression.append(self.__placeholders_real[j])
        return self.__progression
    
    def gameFinished(self):
        return self.__game

#h = Hints()
#h.startGame()
# CONVERT ALL MESSAGES TO EMBEDS (rm weird embed funct with reacts....)

# ERROR HANDLING

# RANDOMIZE ARTICLES

# CONVERT responses2 TO OOP