import pygame as pyg
import os
import threading
from pygame.locals import *
from time import sleep
from Buttoncreation import Button

# Mods
NO_TURNS = True

"""
                
                >>>>>>>>>>>>>>Iggle<<<<<<<<<<<<<<
                
                
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 ^^^^^^^^ | ^^^^^^^^^ | ^^^^^^^^
                 ^^^^^^^^   ^^^^^^^^^   ^^^^^^^^
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 ^^^^^^^^^^<--------->^^^^^^^^^^
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
                         ---------------
                        @               @
                
                
                ^^^^^^^^^^^^^^Iggle^^^^^^^^^^^^^^
                
                """
def modulus(number):
    if number >= 0:
        return number
    else:
        return number*-1
    
class piece:
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound,name):
        self.square = square
        self.colour = colour
        self.pieceImage = pieceImage
        self.boardSize = boardSize
        self.incrementAmound = incrementAmound
        self.captured = False
        self.name = name

    def getColour(self):
        return self.colour
    
    def isCaptured(self):
        self.captured = True

    def squareToCordinates(self, newsquare = 0):
        if newsquare == 0: 
            squaresize = self.boardSize/8
            letter =  ord(self.square[1])-ord("a")
            number = int(self.square[0])-1
            pos = (number*squaresize,letter*squaresize)

            return pos
        else:
            squaresize = self.boardSize/8
            letter =  ord(newsquare[1])-ord("a")
            #so this is quite experimental code, i think it should work however i don't know if this is how unicode arithmatic works.
            number = int(newsquare[0])-1
            pos = (number*squaresize,letter*squaresize)
            return pos
        
    def cordinatesToSquare(self,pos):
        squaresize = self.boardSize/8
        num=1
        letter=0
        x=0
        y=0
        while True:
            if x!=pos[0]:
                num+=1
                x+=squaresize
            elif x == pos[0]:
                if y !=pos[1]:
                    letter+=1
                    y+=squaresize
                    
                elif y==pos[1]:
                    return str(num)+chr(letter+ord("a"))
                
    def getname(self):
        return self.name
    
    def pieceCapture(self,newSquare):
        piece = 0
        
        if board[newSquare][piece]!="null":
            board.get(newSquare)[piece].isCaptured()
            board[newSquare][piece] = "null"
        """this function will remove any piece that is on a square at one time. so if you do willpieceCapture("A1") then the piece on A1 will be set to captured."""
    
    def displayPiece(self):
        if not self.captured:
            pos = self.squareToCordinates()
            posx= pos[0]+40
            posy  = pos[1]+30
            return self.pieceImage,(posx,posy)
        else:
            print("Seb the piece is dead you will now need to make logic for this")
            
            self.pieceCapture(self.square)
            return 0

class Pawnpiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"pawn")
        self.movemeantdirectionvalue = self.movemeantDirection()
        
    def movemeantDirection(self):
        if self.colour.lower() == "black":
            return 1
        elif self.colour.lower() == "white":
            return  -1
        else:
            print(f"Error: could not assign directional value to pawn on {self.square}")
        return 0
    
    def movePiece(self,newSquare):
        if self.ismovevalid(newSquare):
            oldSqare = self.square
            self.square = newSquare
            board[self.square][0] = Pawnpiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound)
            self.pieceCapture(oldSqare) # sets old square to "null"

            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)
            
    def ismovevalid(self, newSquare):
        squaresize = self.boardSize/8
        newSquareCordinate = self.squareToCordinates(newSquare)
        oldSquareCordinates = self.squareToCordinates()
        
        if board.get(newSquare)[0] != "null" and board.get(newSquare)[0].getColour() == self.getColour():
            return False
        
        if newSquareCordinate[1] == (oldSquareCordinates[1] + squaresize * self.movemeantdirectionvalue):
            if newSquareCordinate[0] >= oldSquareCordinates[0]-squaresize and newSquareCordinate[0]<= oldSquareCordinates[0]+squaresize :
                if newSquareCordinate[0] == oldSquareCordinates[0]:
                    return board.get(newSquare)[0] != "null"
                
                else:
                    return board.get(newSquare)[0] == "null"   
        return False
                        
class Dragonpiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound,canactlikecastle):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"dragon")
        self.canactlikecastle = canactlikecastle

    def movePiece(self,newSquare):
        if self.ismovevalid(newSquare, True):
            oldSqare = self.square
            self.square = newSquare

            if board[newSquare][0] != "null":
                if board[newSquare][0].getname() == "castle":
                    self.canactlikecastle = True

            board[self.square][0] = Dragonpiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound,self.canactlikecastle)
            self.pieceCapture(oldSqare) #sets old square to "null"
            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)

    def ismovevalid(self, newSquare, istakingPiece=False):
        squaresize = self.boardSize/8  
        newSquareCordinate = self.squareToCordinates(newSquare)
        oldSquareCordinates = self.squareToCordinates()
        squarescanmoveto = self.wherecanmove()
        validornot = False
        
        if board.get(newSquare)[0] != "null" and board.get(newSquare)[0].getColour() == self.getColour():
            return False
    
        for item in squarescanmoveto:
            if item == newSquare:
                validornot = True

        if self.canactlikecastle:
            print("can act")
            validornot = self.ismovevalidcastlemove(newSquare)

            if validornot and istakingPiece:
                self.canactlikecastle = False
        return validornot
    
    def ismovevalidcastlemove(self, newSquare):
        squaresize = self.boardSize/8
        oldsquarepos = self.squareToCordinates()
        newSquarepos = self.squareToCordinates(newSquare)
        vertical = 0
        horizontal = 0

        if newSquare == self.square:
            return False
        
        if newSquarepos[0] != oldsquarepos[0]:
            if newSquarepos[1] == oldsquarepos[1]:
                if newSquarepos[0] < oldsquarepos[0]:
                    horizontal -= squaresize
                else:
                    horizontal += squaresize
            else:
                print("Invalid move, has to be straight...")
                return False
            
        elif newSquarepos[1] !=oldsquarepos[1]:
            if newSquarepos[0]== oldsquarepos[0]:
                if newSquarepos[1]<oldsquarepos[1]:
                    vertical-=squaresize
                else:
                    vertical+=squaresize

        ogvertical = vertical
        oghorizontal = horizontal

        while True:
            if oldsquarepos[0]+horizontal != newSquarepos[0] or oldsquarepos[1]+vertical!= newSquarepos[1]:
                if board[self.cordinatesToSquare((oldsquarepos[0]+horizontal,oldsquarepos[1]+vertical))][0]!="null":
                    print(self.cordinatesToSquare((oldsquarepos[0]+horizontal,oldsquarepos[1]+vertical)))
                    print(f"Invalid move there is a piece in the way || Vertical ={vertical} || Horizontal = {horizontal}")
                    return False
                
                vertical+=ogvertical
                horizontal+=oghorizontal

            elif oldsquarepos[0]+horizontal ==newSquarepos[0] and oldsquarepos[1]+vertical== newSquarepos[1]:
                return True
                
    def wherecanmove(self):
        newsquares = []
        
        number = int(self.square[0])
        letter = self.square[1]
        
        newletter1 = chr(ord(letter)-1)
        newletter2 = chr(ord(letter)+1)
        newnumber =str(number+2)
        newsquares.append(newnumber+newletter1)
        newsquares.append(newnumber+newletter2)
        
        #left
        newnumber =str(number-2)
        newsquares.append(newnumber+newletter1)
        newsquares.append(newnumber+newletter2)
        
        #up
        newnumber1 = str(number-1)
        newnumber2 = str(number+1)
        newletter = chr(ord(letter)-2)
        newsquares.append(newnumber1+newletter)
        newsquares.append(newnumber2+newletter)

        #down
        newletter = chr(ord(letter)+2)
        newsquares.append(newnumber1+newletter)
        newsquares.append(newnumber2+newletter)
        
        lngoflist = len(newsquares)
        
        finalsquares = []
        for i in range(0,lngoflist):
            if int(newsquares[i][0] != "-"):
                
                if int(newsquares[i][0]) <= 8 and int(newsquares[i][0])>=0 and ord(newsquares[i][1])<=ord("h") and ord(newsquares[i][1])>=ord("a"): 
                    finalsquares.append(newsquares[i])
                
        return finalsquares
    
class Bishopiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound, "bishop")
        
    def movePiece(self,newSquare):
        if self.ismovevalid(newSquare):
            oldSqare = self.square
            self.square = newSquare
            board[self.square][0] = Bishopiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound)
            self.pieceCapture(oldSqare)#sets old square to "null"

            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)

    def ismovevalid(self,newSquare):
        squaresize = self.boardSize/8
        currentsquarepos = self.squareToCordinates()
        newsquarepos = self.squareToCordinates(newSquare)
        possibleadditons = [(squaresize,squaresize),(squaresize,-squaresize),(-squaresize,squaresize),(-squaresize,-squaresize)]
        possiblepositions = []
        possiblepositionsfinal = []

        if board.get(newSquare)[0] != "null" and board.get(newSquare)[0].getColour() == self.getColour():
            return False
        
        for item in possibleadditons:
            for i in range(1,4):
                possiblepositions.append((item[0]*(i*2)+currentsquarepos[0],item[1]*(i*2)+currentsquarepos[1]))
        
        for newdiagonalpos in possiblepositions:
            if newdiagonalpos[0]<1000 and newdiagonalpos[1]<1000 and newdiagonalpos[0]>=0 and newdiagonalpos[1]>=0:
                possiblepositionsfinal.append(newdiagonalpos)
                
        for finalplace in possiblepositionsfinal:
            if finalplace[0] == newsquarepos[0] and finalplace[1]==newsquarepos[1]:
                diffenceInSquare = (newsquarepos[0]-currentsquarepos[0],newsquarepos[1]-currentsquarepos[1])
                
                horizontal = 0
                verticl = 0

                if diffenceInSquare[0]>0:
                    horizontal = 1
                else:
                    horizontal = -1

                if diffenceInSquare[1]>0:
                    verticl = 1
                else:
                    verticl = -1

                testposx = currentsquarepos[0]
                testposy = currentsquarepos[1]

                for i in range(0,4):
                    testposx+=squaresize*2*horizontal
                    if testposx>=1000:
                        testposx-=squaresize*2*horizontal
                    testposy+=squaresize*2*verticl
                    if testposy>=1000:
                        testposy-=squaresize*2*verticl
                    
                    testpos = testposx,testposy
                    
                    if self.cordinatesToSquare(testpos) != newSquare:
                        if board[self.cordinatesToSquare(testpos)][0] != "null":
                            return False
                        
                    elif self.cordinatesToSquare(testpos)== newSquare:
                        return True
        return False

    """not DONE AND ITS MAKING ME CRYYYYYYYYYYYYYYYYYYYYYYYY"""
    """OMG OMGNDK NFDJASIOFJO ASDJIOF JIAOS ITS DOEEEEEEEEEEEEEEEEEEE DONE  YES YES YES FIXEDC DOEN AND ALLLLLLLLLLL!!!!!!!!!!!!!   frickkkkkkkkkk stupid death link ."""

class Castlepiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound,selfdeathlinkpartner):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"castle")
        if selfdeathlinkpartner != "":
            self.deathlinkpartnerfinder = selfdeathlinkpartner
        elif selfdeathlinkpartner == "":
            self.selfdeathlinkpartner = self.deathlinkpartnerfinder()

    def setposdeathlinkpartner(self,newposforpartner):
        self.selfdeathlinkpartner = newposforpartner

    def getposdeathlinkpartner(self):
        return self.selfdeathlinkpartner
    
    def deathlinkpartnerfinder(self):
        if self.square == "1a":
            return "1h"
        if self.square == "1h":
            return "1a"
        if self.square == "8a":
            return "8h"
        if self.square == "8h":
            return "8a"
        
        #runs when u want to find the piece linked to it
    def movePiece(self,newSquare):
        if self.ismovevalid(newSquare):
            dead = False
            if board[self.selfdeathlinkpartner][0].getname() != "castle":
                print("deathlinkpartner is dead")
                dead = True
            else:
                board[self.selfdeathlinkpartner][0].setposdeathlinkpartner(newSquare)
                
            oldSqare = self.square
            self.square = newSquare
            
            board[self.square][0] = Castlepiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound,self.selfdeathlinkpartner)
            if not dead:
                board[newSquare][0].setposdeathlinkpartner(self.selfdeathlinkpartner)
            self.pieceCapture(oldSqare) # sets old square to "null"
            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)

    def ismovevalid(self,newSquare):
        squaresize = self.boardSize/8
        oldsquarepos = self.squareToCordinates()
        newSquarepos = self.squareToCordinates(newSquare)
        vertical = 0
        horizontal = 0

        if newSquare == self.square or board.get(newSquare)[0] != "null" and board.get(newSquare)[0].getColour() == self.getColour():
            return False
        
        if newSquarepos[0]!=oldsquarepos[0]:
            if newSquarepos[1]== oldsquarepos[1]:
                if newSquarepos[0]<oldsquarepos[0]:
                    horizontal-=squaresize
                else:
                    horizontal+=squaresize
            else:
                print("Invalid move has too be straight")
                return False
            
        elif newSquarepos[1] !=oldsquarepos[1]:
            if newSquarepos[0]== oldsquarepos[0]:
                if newSquarepos[1]<oldsquarepos[1]:
                    vertical-=squaresize
                else:
                    vertical+=squaresize

        ogvertical = vertical
        oghorizontal = horizontal

        while True:
            if oldsquarepos[0]+horizontal != newSquarepos[0] or oldsquarepos[1]+vertical!= newSquarepos[1]: 
                if board[self.cordinatesToSquare((oldsquarepos[0]+horizontal,oldsquarepos[1]+vertical))][0]!="null":    
                    print(self.cordinatesToSquare((oldsquarepos[0]+horizontal,oldsquarepos[1]+vertical)))
                    print(f"Invalid move there is a piece in the way || Vertical ={vertical} || Horizontal = {horizontal}")
                    return False
                
                vertical += ogvertical
                horizontal += oghorizontal

            elif oldsquarepos[0]+horizontal ==newSquarepos[0] and oldsquarepos[1]+vertical== newSquarepos[1]:
                return True
            
    def isCaptured(self):
        if not self.captured:
            self.captured = True

    def displayPiece(self):
        if board[self.selfdeathlinkpartner][0]!="null":
            if board[self.selfdeathlinkpartner][0].getname()=="castle":
                if not self.captured:
                    pos = self.squareToCordinates()
                    posx= pos[0]+40
                    posy  = pos[1]+30
                    return self.pieceImage,(posx,posy)
                
                else:
                    print("Seb the piece is dead you will now need to make logic for this")
                    self.pieceCapture(self.selfdeathlinkpartner)
                    self.pieceCapture(self.square)
                    return 0
            else:
                self.pieceCapture(self.square)
                return 0
        else:
            print("Seb the piece is dead you will now need to make logic for this")
            self.pieceCapture(self.selfdeathlinkpartner)
            self.pieceCapture(self.square)
            return 0
             
class Queenpiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound,distance):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"queen")
        self.distance = distance

    def movePiece(self,newSquare):
        if self.ismovevalid(newSquare):
            if board[newSquare][0]!="null":
                self.queenDegrade()
            print()
            oldSqare = self.square
            self.square = newSquare
            board[self.square][0] = Queenpiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound,self.distance)
            self.pieceCapture(oldSqare)#sets old square to "null"
            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)

    def ismovevalid(self,newSquare):
        squaresize = self.boardSize/8
        newpos = self.squareToCordinates(newSquare)
        oldpos = self.squareToCordinates()
        
        vertical = 0
        horizontal = 0
        
        if self.distance < 1 or board.get(newSquare)[0] != "null" and board.get(newSquare)[0].getColour() == self.getColour():
            return False
        
        if newpos==oldpos:
            print(newSquare,self.square)
            print("invalid square can't move to the same square")
            return False
        
        if newpos[0] == oldpos[0] or newpos[1] == oldpos[1] :
            if newpos[1] > oldpos[1]:
                vertical+=squaresize

            elif newpos[1] < oldpos[1]:
                vertical-=squaresize
                
            if newpos[0] > oldpos[0]:
                horizontal+=squaresize

            elif newpos[0] < oldpos[0]:
                horizontal-=squaresize

        elif modulus(newpos[0]-oldpos[0]) == modulus(newpos[1]-oldpos[1]):
            if newpos[1]>oldpos[1]:
                vertical+=squaresize
            elif newpos[1]<oldpos[1]:
                vertical-=squaresize
                
            if newpos[0]>oldpos[0]:
                horizontal+=squaresize
            elif newpos[0]<oldpos[0]:
                horizontal-=squaresize
        else:
            print(newSquare,self.square)
            
        ogvertical = vertical
        oghorizontal = horizontal
            
        while modulus(vertical)<=modulus(ogvertical*self.distance) and modulus(horizontal)<=modulus(oghorizontal*self.distance):
            if oldpos[0]+horizontal!= newpos[0] or oldpos[1]+vertical!=newpos[1]:
                if board[self.cordinatesToSquare((oldpos[0]+horizontal,oldpos[1]+vertical))][0]!="null":
                    print("Invalid input")
                    return False
                
                horizontal += oghorizontal
                vertical += ogvertical

            elif oldpos[0]+horizontal==newpos[0] and oldpos[1]+vertical==newpos[1]:
                return True
                
        print("ur max disance is ",self.distance)
        print("-"*30)
        print(f"oldpos = {oldpos}     newpos = {newpos}    horizontal = {horizontal}    vertical = {vertical}")
        return False
            
    def queenDegrade(self):
        if self.distance > 0:
            self.distance -= 1 
    
class Kingpiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"king")
        self.rookpostions = self.rookpositions()

    def rookpositions(self):
        castlepos = []
        for key in keys:
            if board[key][0]!="null":
                if board[key][0].getColour() == self.colour:
                    if board[key][0].getname()=="castle":
                          castlepos.append(key)

        return castlepos
    
    def canslide(self):
        castlepos = self.rookpositions()

        if len(castlepos)>1:
            firstcastle = self.squareToCordinates(castlepos[0])
            secondcastle = self.squareToCordinates(castlepos[1])
            castlepos = (firstcastle,secondcastle)
            squaresize = self.boardSize/8

            if len(castlepos)>1:
                if firstcastle[1]== secondcastle[1]== self.squareToCordinates(self.square)[1]:
                    if (firstcastle[0]+squaresize*2 == secondcastle[0] and firstcastle[0]+squaresize ==self.squareToCordinates(self.square)[0])or (secondcastle[0]+squaresize*2 == firstcastle[0] and secondcastle[0]+squaresize ==self.squareToCordinates(self.square[0])):
                        return True,"v"
                    else:
                        return False
                elif firstcastle[0]==secondcastle[0] == self.squareToCordinates(self.square)[0]:
                    if (firstcastle[1]+squaresize*2 == secondcastle[1] and firstcastle[1]+squaresize ==self.squareToCordinates(self.square)[1])or (secondcastle[1]+squaresize*2 == firstcastle[1] and secondcastle[1]+squaresize ==self.squareToCordinates(self.square[1])):
                        return True,"h"
                    else:
                        return False
                else:
                    return False
        else:
            return False
        #checks if the rooks are either beside them and then it returns true and "v" or if the rooks are above and below the king  then it returns "h", h = horizontal movemeant, v = vertical movemeant.
    def movePiece(self,newSquare):
        if self.ismovevalid(newSquare):
            oldSqare = self.square
            self.square = newSquare
            board[self.square][0] = Kingpiece(self.square, self.colour, self.pieceImage, self.boardSize, self.incrementAmound)
            self.pieceCapture(oldSqare)#sets old square to "null"

            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)

    def ismovevalid(self,newSquare):
        squaresize = self.boardSize/8
        newpos = self.squareToCordinates(newSquare)
        oldpos = self.squareToCordinates()
        xdiff = modulus(oldpos[0]-newpos[0])
        ydiff = modulus(oldpos[1]-newpos[1])
        canslidecheck = self.canslide()

        if board.get(newSquare)[0] != "null" and board.get(newSquare)[0].getColour() == self.getColour():
            return False
        
        if not canslidecheck:
            if xdiff >squaresize or ydiff>squaresize:
                return False
            else:
                return True
        else:
            if canslidecheck[1] == "h":
                if ydiff != 0:
                    return False
                
                if newpos[0]> oldpos[0]:
                    multiple = 1
                    addon = 1

                if newpos[0]<oldpos[0]:
                    multiple=-1
                    addon = -1

                while True:
                    if oldpos[0]+squaresize*multiple!= newpos[0]:
                        if board[self.cordinatesToSquare((oldpos[0]+squaresize*multiple,oldpos[1]))][0]!="null":
                            return False
                        
                    if oldpos[0]+squaresize*multiple== newpos[0]:
                        return True
                    multiple+=addon
                #need to check if there is anything in the way

            elif canslidecheck[1]== "v":
                if xdiff != 0:
                    return False
                
                if newpos[1] > oldpos[1]:
                    multiple = 1
                    addon = 1

                if newpos[1] < oldpos[1]:
                    multiple=-1
                    addon = -1

                while True:
                    if oldpos[1] + squaresize * multiple != newpos[1]:
                        if board[self.cordinatesToSquare((oldpos[0],oldpos[1]+squaresize*multiple))][0] != "null":
                            return False
                    if oldpos[1] + squaresize * multiple == newpos[1]:
                        return True
                    
                    multiple+=addon

PATHC = os.path.join
ASSET_PATH = PATHC("Spess", "Assets")
AUDIO_PATH = PATHC("Spess", "Audio")
DATA_PATH = PATHC("Spess", "Data")
PYIMAGE = pyg.image.load

def startscreen(PieceSet):
    PieceSet = PieceSet or "Default"
    print(PieceSet)
    running = True
    clicked = False
    
    clock = pyg.time.Clock()
    logo = PYIMAGE(PATHC(ASSET_PATH, "Logo", "spessLogo.ico"))
    pyg.display.set_icon(logo)
    pyg.display.set_caption("Spess")

    screenstage = "Start"
    pyg.mixer.Sound.play(StartupSound)
    screenX = 1000
    screenY = 800
    startScreen = pyg.display.set_mode((screenX,screenY))
    screenFillColour = (62, 0, 207)
    currentsets = ["Default","Gold","X"]
    imageicons = {}
    
    spesstitle = PYIMAGE(PATHC(ASSET_PATH, "Logo", "spessTitle.png"))

    xindex = 1
    yindex = 1
    padding = 0
    for pack in currentsets:
        imageicons[pack] = [
            PYIMAGE(PATHC(ASSET_PATH, pack + "Pieces", "PiecesSet.png")),
            PYIMAGE(PATHC(ASSET_PATH, pack + "Pieces", "PiecesSetHover.png")),
            pyg.Rect(xindex * screenX / 8, padding +( yindex * screenY / 8), 100, 101)
        ]

        if xindex >= 6:
            xindex = 0
            yindex +=1
            if yindex == 2:
                padding += 20
                
        xindex += 1
        
    coopPlayButton = Button(startScreen, screenX / 2, 2 * (screenY / 3), "Play: Offline", 30, 10)
    InventoryButton = Button(startScreen, (screenX / 2), 3 * (screenY / 4), "Inventory", 30, 10)
    returnButton = Button(startScreen, screenX / 20, screenY / 20, "X", 30, 10,"CRIMSON")

    def menuMusic():
        sleep(2)
        pyg.mixer.music.load(PATHC(AUDIO_PATH, "menuMusic.mp3"))

        pyg.mixer.music.play(1)
        pyg.mixer.music.set_pos(50)
        pyg.mixer.music.set_volume(0)

        for i in range(1,25):
            pyg.mixer.music.set_volume(i / 10)
            sleep(0.05)

    threading.Thread(target=menuMusic).start()
    
    angle = 100
    while running:
        startScreen.fill(screenFillColour)
        angle = (angle + 1) % 360
        spessTitleGood = pyg.transform.rotate(spesstitle, angle)
        startScreen.blit(spessTitleGood, (screenX/3, screenY/7))

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False
                
                with open(PATHC(DATA_PATH, "Currentpack.txt"), "w", encoding = "utf-8") as f:
                    f.write(PieceSet)
                raise SystemExit
            
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button==1:
                    pyg.mixer.Sound.play(ClickSound)

            elif event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    clicked = True
            
        mouse_pos = pyg.mouse.get_pos()
        if  screenstage == "Start":
            if coopPlayButton.makeButton(mouse_pos) and clicked:
                running = False

            if InventoryButton.makeButton(mouse_pos) and clicked:
                screenstage = "Inventory"
             
        elif screenstage == "Inventory":
            pyg.draw.rect(startScreen,(200,200,200),(screenX/10,screenY/10,8*screenX/10,6*screenY/8))
            pyg.draw.rect(startScreen,(0,0,0),(screenX/10,screenY/10,8*screenX/10,6*screenY/8),2)
        
            if returnButton.makeButton(mouse_pos) and clicked:
                screenstage = "Start"

            else:
                for k in currentsets:
                    setImage = imageicons[k][0]
                    setImageHover = imageicons[k][1]
                    SetRect = imageicons[k][2]
                    
                    screenXPlacment = SetRect[0]
                    screenYPlacment = SetRect[1]

                    if SetRect.collidepoint(mouse_pos):
                        startScreen.blit(setImageHover, (screenXPlacment, screenYPlacment))
                        
                        if SetRect.collidepoint(mouse_pos) and clicked:
                            if k != PieceSet:
                                PieceSet = k
                                print(f"{PieceSet} Selected!!!")
                            elif k== PieceSet:
                                print(f"Piece Set {PieceSet} is already selected!!!")
                    else: 
                        startScreen.blit(setImage, (screenXPlacment, screenYPlacment))

        clicked = False
        pyg.display.flip()
        clock.tick(60)
    pyg.quit()
    return PieceSet

# Loading main menu...
pyg.init()

StartupSound = pyg.mixer.Sound(PATHC(AUDIO_PATH, "StartupSound.mp3"))
StartupSound.set_volume(1)

ClickSound = pyg.mixer.Sound(PATHC(AUDIO_PATH, "MouseClick.mp3"))
ClickSound.set_volume(0.15)

# Auto equipping previously selected skins.
with open(PATHC(DATA_PATH, "currentpack.txt"), "r" , encoding="utf-8") as f:
    PieceSet = f.read()

PieceSet = startscreen(PieceSet)
with open(PATHC(DATA_PATH, "currentpack.txt"), "w", encoding="utf-8") as f:
    f.write(PieceSet)

# Loading main pygame scene.
pyg.init() 
screendimention = 1000 
screen = pyg.display.set_mode((screendimention, screendimention))

pyg.display.set_caption("Spess")
logo = PYIMAGE(PATHC(ASSET_PATH, "Logo", "spessLogo.ico"))
pyg.display.set_icon(logo)

font = pyg.font.Font(None, 36)
running = True
clock = pyg.time.Clock()

# Loading images
BLACK_PATH = PATHC(ASSET_PATH, PieceSet + "Pieces", "blackAssets")
WHITE_PATH = PATHC(ASSET_PATH, PieceSet + "Pieces", "whiteAssets")

BlackpawnImage      = PYIMAGE(PATHC(BLACK_PATH, "Blackpawn.png"))
BlackrookImage      = PYIMAGE(PATHC(BLACK_PATH, "Blackrook.png"))
BlackkniteImage     = PYIMAGE(PATHC(BLACK_PATH, "Blackknite.png"))
BlackbishopImage    = PYIMAGE(PATHC(BLACK_PATH, "Blackbishop.png"))
BlackqueenImage     = PYIMAGE(PATHC(BLACK_PATH, "Blackqueen.png"))
BlackkingImage      = PYIMAGE(PATHC(BLACK_PATH, "Blackking.png"))
WhitepawnImage      = PYIMAGE(PATHC(WHITE_PATH, "Whitepawn.png"))
WhiterookImage      = PYIMAGE(PATHC(WHITE_PATH, "Whiterook.png"))
WhitekniteImage     = PYIMAGE(PATHC(WHITE_PATH, "Whiteknite.png"))
WhitebishopImage    = PYIMAGE(PATHC(WHITE_PATH, "Whitebishop.png"))
WhitequeenImage     = PYIMAGE(PATHC(WHITE_PATH, "Whitequeen.png"))
WhitekingImage      = PYIMAGE(PATHC(WHITE_PATH, "Whiteking.png"))

ErrorClickSound = pyg.mixer.Sound(PATHC(AUDIO_PATH, "ErrorClickSound.wav"))
ErrorClickSound.set_volume(0.2)

TakeSound = pyg.mixer.Sound(PATHC(AUDIO_PATH, "takesound.mp3"))
TakeSound.set_volume(0.6)

BackgroundMusic = pyg.mixer.music.load(PATHC(AUDIO_PATH, "backgroundMusic.mp3"))

WinSound = pyg.mixer.Sound(PATHC(AUDIO_PATH, "WinSound.mp3"))
WinSound.set_volume(0.075)

keys = []
key_colour=""
selected =""
clicked = False

board = {}
selecties = []

# Themes
BOARD_LIGHT = (207, 181, 149)
BOARD_DARK = (81, 59, 40)
ACTIVE_PATH1 = (21, 148, 91)
ACTIVE_PATH2 = (15, 107, 66)
HOVER1 = (120,120,40)
HOVER2 = (200,200,120)

def makeboardstruct():
    x,y = 0,0
    board_width = 1000
    letter = "a"
    number = 1
    current_colour = BOARD_LIGHT
    square_width = board_width/8

    for lettercount in range (0,8):
        for numbercount in range(0,8):
            board[str(number)+letter] = ["null", (x,y), current_colour, False, False, current_colour, False]
            keys.append(str(number)+letter)
            x+=square_width
            
            number+=1
            if current_colour == BOARD_LIGHT:
                current_colour = BOARD_DARK
            else:
                current_colour = BOARD_LIGHT
        if current_colour == BOARD_LIGHT:
            current_colour = BOARD_DARK
        else:
            current_colour = BOARD_LIGHT

        letter = chr(ord(letter)+1)
        y+=square_width
        x=0
        number = 1
    
    #pawns
    for i in range(0,8):
        row = 8
        collum = 1
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Pawnpiece(keys[keynum],"black",BlackpawnImage,1000,10) 
        collum = 6
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Pawnpiece(keys[keynum],"white",WhitepawnImage,1000,10) 

    #Castles for the dragon to go tooooooooooooooo yaaaaaaaaas queen
    for i in range(0,8,7):
        collum=0
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Castlepiece(keys[keynum],"black",BlackrookImage,1000,10,"") 
        
        collum = 7
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Castlepiece(keys[keynum],"white",WhiterookImage,1000,10,"") 
    #dragons rawr
    for i in range(1,7,5):
        collum = 0
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Dragonpiece(keys[keynum],"black",BlackkniteImage,1000,10,False)   
        
        
        collum = 7
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Dragonpiece(keys[keynum],"white",WhitekniteImage,1000,10,False)   
        
    for i in range(2,6,3):
        collum = 0
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Bishopiece(keys[keynum],"black",BlackbishopImage,1000,10)   
        
        collum = 7
        keynum = (row*collum)+i
        board[keys[keynum]][0] = Bishopiece(keys[keynum],"white",WhitebishopImage,1000,10)   
    collum = 0
    keynum = (row*collum)+3
    board[keys[keynum]][0] = Queenpiece(keys[keynum],"black",BlackqueenImage,1000,10,7) 
    keynum = (row*collum)+4
    board[keys[keynum]][0] = Kingpiece(keys[keynum],"black",BlackkingImage,1000,10) 
    
    collum = 7
    keynum = (row*collum)+3
    board[keys[keynum]][0] = Queenpiece(keys[keynum],"white",WhitequeenImage,1000,10,7) 
    keynum = (row*collum)+4
    board[keys[keynum]][0] = Kingpiece(keys[keynum],"white",WhitekingImage,1000,10) 
    
kingsAlive = []
    
def checkforking():
    kings = []

    for key in keys:
        z = board[key][0]
        if z and z != "null" and z.getname() == "king":
            kings.append((key, z.getColour()))

    return kings

def drawBoard(selecties,colourturn):
    handle_hovering_square()
    square_size = 1000/8
    
    for key in keys:
        item = board[key][0]
        pos = board[key][1]
        x = pos[0]
        y = pos[1]

        # Win condition
        '''
            if board[key][0] != "null":
                if board[key][0].getname() == "king":
                    kingsAlive.append((key, board[key][0].getColour()))
        '''

        # Hovering code
        CALCULATED_COLOR = (board[key][5] == BOARD_DARK and ACTIVE_PATH2 or ACTIVE_PATH1)

        isSelected = len(selecties) > 0 and selecties[0] == key
        calculatedColour = (board[key][6] and CALCULATED_COLOR) or (isSelected and CALCULATED_COLOR) or (board[key][4] and (board[key][5] == BOARD_DARK and HOVER1 or HOVER2) or board[key][5]) or board[key][5]
        board[key][2] = calculatedColour

        if board[key][3]:
            board[key][3] = False
            
            selecties.append(key)
            
            if board[selecties[0]][0] != "null":
                for i in board:
                    board[i][6] = board[selecties[0]][0].ismovevalid(i)

            if board[selecties[0]][0] == "null":
                selecties = []
                pyg.mixer.Sound.play(ErrorClickSound)

                for i in board:
                    board[i][6] = False
                
            elif len(selecties) == 2:
                print(board[selecties[0]][0].ismovevalid(selecties[1]))

                if board[selecties[0]][0].getColour() != colourturn and not NO_TURNS:
                    pyg.mixer.Sound.play(ErrorClickSound)

                elif board[selecties[0]][0].movePiece(selecties[1]):
                    colourturn = colourturn == "white" and "black" or "white"

                    if board[selecties[1]][0] != "null":
                        pyg.mixer.Sound.play(TakeSound)
   
                selecties = []
                for i in board:
                    board[i][6] = False
                
        pyg.draw.rect(screen, board[key][2],(x,y,square_size,square_size))

        if item != "null":
            itemdisplay = board[key][0].displayPiece()

            if itemdisplay!=0:
                screen.blit(itemdisplay[0], itemdisplay[1])
            #print(f"displayed piece {item.getColour()} {item.getname()} at {item. squareToCordinates()}")
    return selecties,colourturn
    
"""
    what should the board contain
    a set of keys that are {A1, A2 ... H7, H8} 
    each key should link to data such as current piece, pos ect
    A1 ---> {Queen,pos,colour,selected,hover}
    Queen ---> just any piece could be pawn, bishop ...
    pos ---> this is the postition, it will be the top left of the square, 
    colour ---> (10,10,10) what ever the colour of the square is right now
    selected ---> a true of false value that says if the square is selected or not.
    hover ---> a true of false value that says if the mouse is hovering over this square or not.
    originalGrid --> the original grid background colour
    pathFound --> saves if the path was found or not for showing all valid paths.
"""

def whichsquarehover():
    square_size = 1000/8
    posx = square_size
    posy = square_size
    number = 1
    letter = "a"
    mouse_pos = pyg.mouse.get_pos()

    while mouse_pos[0] > posx:
        posx += square_size
        number += 1

    while mouse_pos[1] > posy:
        posy += square_size
        letter = chr(ord(letter)+1)

    return (str(number)+letter)
        
def change_to_hover_colour(hovering_square):
    current_colour = board[hovering_square][2] 
    new_colour = (current_colour[0] + 40, current_colour[1] + 40, current_colour[2] - 40) 
    board[hovering_square][2] = new_colour
    
def handle_hovering_square():
    hovering_square = whichsquarehover()

    for key in keys:
        board[key][4] = False

    board[hovering_square][4] = True
    
screen.fill((0,0,0))
makeboardstruct()
Turn = "white"

def aiturn():
    pass

pyg.mixer.music.play(-1)
pyg.mixer.music.set_volume(0.6)

while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
            raise SystemExit
        
        elif event.type == pyg.MOUSEBUTTONUP:
            if event.button== 1:
                """
                Seb this looks ugly but the for MOUSEBUTTONUP and MOUSEBUTTONDOWN they return 2 values one for button and one for pos, so in the future it might be worth passing in the value into whichsquarehover()
                ------.button------
                1 for left click,
                2 for mouse wheel button, 
                3 for right click,
                4 for when wheel scroll up,
                5 for when wheel scroll down.
                -------------------
                """
                
                square_to_click = whichsquarehover()
                board[square_to_click][3] = True

        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pyg.mixer.Sound.play(ClickSound)
            
    selecties,Turn = drawBoard(selecties,Turn)
    kingsAlive = checkforking()

    if len(kingsAlive) != 2:
        running = False

    elif len(kingsAlive) == 2:
        running = True
        kingsAlive = []

    pyg.display.flip()
    # print(clock.get_fps())
    clock.tick(60)

pyg.mixer.Sound.play(WinSound)

for i in range(1,5):
    if i == 3:
        print(f"---CONGRATUATIONS {kingsAlive[0][1].upper()} WINS---")
        pass

    print(f"-" * 31 )

print("Closing")
sleep(2)

pyg.quit()