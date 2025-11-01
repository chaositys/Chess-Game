import pygame as pyg
from pygame.locals import *



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
    if number>=0:
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
            
            #so this is quite experimental code, i think it should work however i don't know if this is how unicode arithmatic works.
            
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
        if self.ismoveValid(newSquare):
            
            
            oldSqare = self.square
            self.square = newSquare
            board[self.square][0] = Pawnpiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound)
            self.pieceCapture(oldSqare)#sets old square to "null"
            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)
            
    
        
    def ismoveValid(self,newSquare):
        squaresize = self.boardSize/8
        newSquareCordinate = self.squareToCordinates(newSquare)
        oldSquareCordinates = self.squareToCordinates()
       
        if newSquareCordinate[1] == (oldSquareCordinates[1] + squaresize*self.movemeantdirectionvalue):
            

            if newSquareCordinate[0] >= oldSquareCordinates[0]-squaresize and newSquareCordinate[0]<= oldSquareCordinates[0]+squaresize :

                if newSquareCordinate[0]== oldSquareCordinates[0]:

                    if board.get(newSquare)[0] != "null":
                        if board.get(newSquare)[0].getColour() == self.getColour():
                            print("invalid move, can't play a piece on your own piece, if this is a bug see is move valid fucntion within class") 
                            return False
                        else:
                            self.pieceCapture(newSquare)
                            print("will capture ",newSquare)
                            return True
                            
                    else:
                        print("invalid move, can't move directly ahead when there is not piece to capture")
                        return False
                    
                    
                else:
                    print("got here")
                    if board.get(newSquare)[0] == "null":
                        return True
                    else:
                        print("can't move there as there is a piece already there")
                        return False
                        
                        
             
    
            
    
class Dragonpiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound,canactlikecastle):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"dragon")
        self.canactlikecastle=canactlikecastle
    def movePiece(self,newSquare):
        if self.ismoveValid(newSquare):
            
            
            oldSqare = self.square
            self.square = newSquare
            if board[newSquare][0]!="null":
                if board[newSquare][0].getname()=="castle":
                    self.canactlikecastle = True
            board[self.square][0] = Dragonpiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound,self.canactlikecastle)
            self.pieceCapture(oldSqare)#sets old square to "null"
            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)
    def ismoveValid(self,newSquare):
        squaresize = self.boardSize/8
        newSquareCordinate = self.squareToCordinates(newSquare)
        oldSquareCordinates = self.squareToCordinates()
        squarescanmoveto = self.wherecanmove()
        validornot = False
        
        for item in squarescanmoveto:
            if item == newSquare:
                validornot=  True
        if self.canactlikecastle:
            validornot = self.ismovevalidcastlemove(newSquare)
            if validornot:
                self.canactlikecastle=False
        return validornot
    def ismovevalidcastlemove(self,newSquare):
        
        squaresize = self.boardSize/8
        oldsquarepos = self.squareToCordinates()
        newSquarepos = self.squareToCordinates(newSquare)
        vertical=0
        
        horizontal=0
        if newSquare == self.square:
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
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"bishop")
        
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
        newsquarepos= self.squareToCordinates(newSquare)
        possibleadditons = [(squaresize,squaresize),(squaresize,-squaresize),(-squaresize,squaresize),(-squaresize,-squaresize)]
        possiblepositions = []
        possiblepositionsfinal=[]
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
                        if board[self.cordinatesToSquare(testpos)][0]!="null":
                            return False
                    elif self.cordinatesToSquare(testpos)== newSquare:
                        return True
        
            
        
        
        return False
            
                
        
        
    """not DONE AND ITS MAKING ME CRYYYYYYYYYYYYYYYYYYYYYYYY"""
    """OMG OMGNDK NFDJASIOFJO ASDJIOF JIAOS ITS DOEEEEEEEEEEEEEEEEEEE DONE  YES YES YES FIXEDC DOEN AND ALLLLLLLLLLL!!!!!!!!!!!!!   fuckkkkkkkkkkkkkk stupid death link shit."""
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
        print(self.square)
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
            self.pieceCapture(oldSqare)#sets old square to "null"
            return True
        else:
            pyg.mixer.Sound.play(ErrorClickSound)
    def ismovevalid(self,newSquare):
        
        squaresize = self.boardSize/8
        oldsquarepos = self.squareToCordinates()
        newSquarepos = self.squareToCordinates(newSquare)
        vertical=0
        
        horizontal=0
        if newSquare == self.square:
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
                vertical+=ogvertical
                horizontal+=oghorizontal    
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
        
        vertical=0
        
        horizontal=0
        
        if self.distance<1:
            return False
        if newpos==oldpos:
            print(newSquare,self.square)
            print("invalid square can't move to the same square")
            return False
        
        
        
        
        
            
        if newpos[0]==oldpos[0] or newpos[1]==oldpos[1] :
            if newpos[1]>oldpos[1]:
                vertical+=squaresize
            elif newpos[1]<oldpos[1]:
                vertical-=squaresize
                
            if newpos[0]>oldpos[0]:
                horizontal+=squaresize
            elif newpos[0]<oldpos[0]:
                horizontal-=squaresize
        elif modulus(newpos[0]-oldpos[0])==modulus(newpos[1]-oldpos[1]):
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
                horizontal+=oghorizontal
                vertical+=ogvertical
            elif oldpos[0]+horizontal==newpos[0] and oldpos[1]+vertical==newpos[1]:
                return True
                
        print("ur max disance is ",self.distance)
        print("-"*30)
        print(f"oldpos = {oldpos}     newpos = {newpos}    horizontal = {horizontal}    vertical = {vertical}")
        return False
    
            
            
            
            
        
        
            
    def queenDegrade(self):
        if self.distance>0:
            self.distance-=1
        
    
class Kingpiece(piece):
    def __init__(self,square,colour,pieceImage,boardSize,incrementAmound):
        super().__init__(square,colour,pieceImage,boardSize,incrementAmound,"king")
        self.rookpostions = self.rookpositions()
    def rookpositions(self):
        
        castlepos= []
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
            board[self.square][0] = Kingpiece(self.square,self.colour,self.pieceImage,self.boardSize,self.incrementAmound)
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
        if not canslidecheck:
            if xdiff >squaresize or ydiff>squaresize:
                return False
            else:
                return True
        else:
            if canslidecheck[1] == "h":
                if ydiff!=0:
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
                if xdiff!=0:
                    return False
                if newpos[1]> oldpos[1]:
                    multiple = 1
                    addon = 1
                if newpos[1]<oldpos[1]:
                    multiple=-1
                    addon = -1
                while True:
                    if oldpos[1]+squaresize*multiple!= newpos[1]:
                        if board[self.cordinatesToSquare((oldpos[0],oldpos[1]+squaresize*multiple))][0]!="null":
                            return False
                    if oldpos[1]+squaresize*multiple== newpos[1]:
                        return True
                    multiple+=addon
print()
print()
print("*"*45)       
print("Welcome to my chess game i hope u enjoy!!!!!!")
print("*"*45)
print()
print()
input("Press Enter to play!")
pyg.init()
screendimention = 1000 
screen = pyg.display.set_mode((screendimention, screendimention))
pyg.display.set_caption("Five in a row")
font = pyg.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
running = True
clock = pyg.time.Clock()
BlackpawnImage = pyg.image.load("Blackpawn.png")
BlackrookImage = pyg.image.load("Blackrook.png")
BlackkniteImage= pyg.image.load("Blackknite.png")
BlackbishopImage= pyg.image.load("Blackbishop.png")
BlackqueenImage= pyg.image.load("Blackqueen.png")
BlackkingImage= pyg.image.load("Blackking.png")
WhitepawnImage = pyg.image.load("Whitepawn.png")
WhiterookImage = pyg.image.load("Whiterook.png")
WhitekniteImage = pyg.image.load("Whiteknite.png")
WhitebishopImage= pyg.image.load("Whitebishop.png")
WhitequeenImage= pyg.image.load("Whitequeen.png")
WhitekingImage= pyg.image.load("Whiteking.png")
StartupSound = pyg.mixer.Sound("StartupSound.mp3")
ErrorClickSound = pyg.mixer.Sound("ErrorClickSound.wav")
ClickSound = pyg.mixer.Sound("MouseClick.mp3")
keys = []
key_colour=""
selected =""
clicked = False

board = {}
selecties = []


def makeboardstruct():
    x,y = 0,0
    board_width = 1000
    letter = "a"
    number = 1
    colour1 =(80,80,80)
    colour2 = (160,160,160)
    current_colour = colour1
    square_width = board_width/8
    for lettercount in range (0,8):
        for numbercount in range(0,8):
            board[str(number)+letter] = ["null",(x,y),current_colour,False,False]
            keys.append(str(number)+letter)
            x+=square_width
            
            number+=1
            if current_colour == colour1:
                current_colour = colour2
            else:
                current_colour=colour1
        if current_colour ==colour1:
            current_colour = colour2
        else:
            current_colour=colour1
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
    
def drawBoard(selecties,colourturn):
    handle_hovering_square()
    square_size = 1000/8
    
    for key in keys:
        item = board[key][0]
        pos = board[key][1]
        x = pos[0]
        y = pos[1]
        if board[key][0]!="null":
            if board[key][0].getname()=="king":
                kingsAlive.append((key,board[key][0].getColour()))
        #ik this code is pretty bad as it is static, however i could not be asked to make it dynamic for this game as there is not really any point
        if board[key][4]:
            old_colour = board[key][2]
            if old_colour == (80,80,80):
                new_colour = (120,120,40)
                board[key][2] = new_colour
            elif old_colour == (160,160,160):
                new_colour = (200,200,120)
                board[key][2] = new_colour
        else:
            if board[key][2] == (120,120,40) or board[key][2] == (200,200,120):
                if board[key][2] == (120,120,40):
                    board[key][2] = (80,80,80)
                else:
                    board[key][2] = (160,160,160)
        if board[key][3]:
            board[key][3]=False
            
            selecties.append(key)
            
            if board[selecties[0]][0]!="null":
                
                print(selecties)
                
                
                
            if board[selecties[0]][0]=="null":
                selecties=[]
                
                pyg.mixer.Sound.play(ErrorClickSound)
                
            elif len(selecties)==2:
                if board[selecties[0]][0].getColour() != colourturn:
                    selecties=[]
                    
                    pyg.mixer.Sound.play(ErrorClickSound)
                elif board[selecties[1]][0]!="null":
                    if board[selecties[0]][0].getColour() != board[selecties[1]][0].getColour():
                        if board[selecties[0]][0].movePiece(selecties[1]):
                            if colourturn== "white":
                                colourturn="black"
                            else:
                                colourturn="white"
                                
                    else:
                        pyg.mixer.Sound.play(ErrorClickSound)
                else:
                    if board[selecties[0]][0].movePiece(selecties[1]):
                            if colourturn== "white":
                                colourturn="black"
                            else:
                                colourturn="white"  
                selecties=[]            
                

            
        pyg.draw.rect(screen, board[key][2],(x,y,square_size,square_size))
        if item!="null":
            
            itemdisplay=board[key][0].displayPiece()
            if itemdisplay!=0:
                screen.blit(itemdisplay[0],itemdisplay[1])
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
"""
def whichsquarehover():
    square_size = 1000/8
    posx = square_size
    posy = square_size
    number = 1
    letter = "a"
    mouse_pos = pyg.mouse.get_pos()
    while mouse_pos[0]> posx:
        
        posx+=square_size
        number+=1
    while mouse_pos[1]> posy:
        posy+=square_size
        letter = chr(ord(letter)+1)
    return (str(number)+letter)
        
    
  
  
def change_to_hover_colour(hovering_square):
    
    
    current_colour = board[hovering_square][2] 
    new_colour = (current_colour[0]+40,current_colour[1]+40,current_colour[2]-40) 
    board[hovering_square][2] = new_colour
  
def change_to_normal_colour(hovering_square):
    current_colour = board[hovering_square][2] 
    new_colour = (current_colour[0]-40,current_colour[1]-40,current_colour[2]+40) 
    board[hovering_square][2] = new_colour
    
def handle_hovering_square():
    hovering_square = whichsquarehover()
    for key in keys:
        board[key][4] = False
    board[hovering_square][4] = True
    


screen.fill((0,0,0))
makeboardstruct()
Turn = "white"



pyg.mixer.Sound.play(StartupSound)


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
            if event.button==1:
                pyg.mixer.Sound.play(ClickSound)
            
    
    
    
    
        
    
    
    if Turn == "white":
        selecties,Turn = drawBoard(selecties,Turn)
    elif Turn == "black":
        selecties,Turn = drawBoard(selecties,Turn)
    
    if len(kingsAlive)!=2:
        running = False
    elif len(kingsAlive)== 2:
        running = True
        kingsAlive=[]
        
            
           
    pyg.display.flip()
    clock.tick(60)

pyg.quit()
print(f"-"*31)
print(f"-"*31)
print(f"---CONGRATUATIONS {kingsAlive[0][1].upper()} WINS---")
print(f"-"*31)
print(f"-"*31)
