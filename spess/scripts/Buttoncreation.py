import pygame
class Button:
    def __init__(self,screen,x,y,text,width,height,colour_name = "LIGHT_GRAY"):
        self.screen = screen
        self.width = width
        self.x =x
        self.y = y
        self.height = height
        self.colour_name = colour_name
        self.font = pygame.font.SysFont("Tahoma", 36)
        self.colourSelection = {"LIGHT_GRAY":((238, 238, 238), (190, 190, 190), (0, 0, 0)),
                                "LIGHT_BLUE":((40, 180, 190),(10,140,160),(0, 0, 0)),
                                "CRIMSON":((220, 20, 60), (190, 16, 50), (255, 255, 255)), 
                                "GREEN":((39, 174, 96), (30, 140, 78), (255, 255, 255)), 
                                "PURPLE":((142, 68, 173), (115, 55, 140), (255, 255, 255)) }
        self.selection = 0
        self.text = text
        self.textDisplay = self.font.render(text, True, self.colourSelection[self.colour_name][2])
        
        self.colour = self.colourSelection[self.colour_name][0]
        self.textSize = self.font.size(self.text)
        
        
        self.width += self.textSize[0] 
        
        self.height+= self.textSize[1]
            
        self.x =x-(self.width/2)
        self.y = y-(self.height/3)
        self.button = pygame.Rect(self.x, self.y, self.width, self.height)
    def makeButton(self,mouse_pos):
        
        colourB = (0,0,0)
        #print(self.colour)
        self.isHover(mouse_pos)
        
        buttonF = pygame.draw.rect(self.screen, self.colour, self.button, 0, 10)
        buttonB = pygame.draw.rect(self.screen, colourB, self.button, 2, 10)
        self.screen.blit(self.textDisplay,(self.x+(self.width/2)-(self.textSize[0]/2),self.y+(self.height/2)-(self.textSize[1]/2)))
        if self.isClicked(mouse_pos):
            return True
        else:
            return False
    def isClicked(self, mousePos):
        
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mousePos)
        
    
    def changeColour(self,newColour):
        self.colour = newColour
    def isHover(self, mousePos):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mousePos):
            
            
            self.changeColour(self.colourSelection[self.colour_name][1])
           
        else:
           
            self.changeColour(self.colourSelection[self.colour_name][0])
    def tryNewColour(self):
        if self.selection == 5:
            self.selection =0
        else:
            self.selection+=1
        #print(self.colourSelection[self.selection][0])
        self.changeColour(self.colourSelection[self.colour_name][0])#this is chnaged code and will not work 
        self.newCorouredText()
        
    def newCorouredText(self):
        self.textDisplay = self.font.render(self.text, True,self.colourSelection[self.colour_name][1])