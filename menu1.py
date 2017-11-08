# -*- coding: utf-8 -*-
"""
menu system for pygame
"""


import pygame 
import template004_sprites_collision_detection
import textscroller_vertical
import random
import sys
import os.path


class Settings(object):
    gold = 100
    red_defenders = 0
    red_attackers = 0
    blue_defenders = 0
    blue_attackers = 0
    price_red = 10
    price_blue = 10
    menu = {"root":["Play!","Buy red army", "Buy blue army", "Difficulty", "Help", "Credits", "Options","Quit"],
            "Buy blue army":["Buy blue attacker", "Buy blue defender", "Sell blue attacker", "Sell blue defender"],
            "Buy red army":["Buy red attacker", "Buy red defender", "Sell red attacker", "Sell red defender"],
            "Options":["Turn music off","Turn sound off","Change screen resolution", "Turn off Wilhelm"],
            "Difficulty":["easy","medium","elite","hardcore"],
            "Change screen resolution":["640x400","800x640","1024x800"],
            "Credits":["bla1","bla2", "False"],
            "Help":["How to play", "How to win"]
            } 
        


class Menu(object):
    """ each menu item name must be unique"""
    def __init__(self, menu={"root":["Play","Help","Quit"]}):
        self.menudict = menu
        self.menuname="root"
        self.oldnames = []
        self.oldnumbers = []
        self.items=self.menudict[self.menuname]
        self.active_itemnumber=0
    
    def nextitem(self):
        if self.active_itemnumber==len(self.items)-1:
            self.active_itemnumber=0
        else:
            self.active_itemnumber+=1
        return self.active_itemnumber
            
    def previousitem(self):
        if self.active_itemnumber==0:
            self.active_itemnumber=len(self.items)-1
        else:
            self.active_itemnumber-=1
        return self.active_itemnumber 
        
    def get_text(self):
        """ change into submenu?"""
        try:
            text = self.items[self.active_itemnumber]
        except:
           print("exception!")
           text = "root"
        if text in self.menudict:
            self.oldnames.append(self.menuname)
            self.oldnumbers.append(self.active_itemnumber)
            self.menuname = text
            self.items = self.menudict[text]
            if self.menuname != "root":
                self.items.append("back")
            self.active_itemnumber = 0
            return None
        elif text == "back":
            self.menuname =  self.oldnames.pop(-1)
            self.active_itemnumber= self.oldnumbers.pop(-1)
            print("back ergibt:", self.menuname)
            self.items = self.menudict[self.menuname]
            return None
            
        return self.items[self.active_itemnumber] 
        
        
        
            

class PygView(object):
    width = 640
    height = 400
  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        
        pygame.mixer.pre_init(44100, -16, 2, 2048) 

        pygame.init()
        
        self.cash = pygame.mixer.Sound(os.path.join("data", "cash.wav"))
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width
        PygView.height = height
        self.set_resolution()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)

    def set_resolution(self):
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white

    def paint(self):
        """painting on the surface"""
        for i in  m.items:
            n=m.items.index(i)
            if n==m.active_itemnumber:
                self.draw_text("-->",50,  m.items.index(i)*30+10,(0,0,255))
                self.draw_text(i, 100, m.items.index(i)*30+10,(0,0,255))
            else:
                self.draw_text(i, 100, m.items.index(i)*30+10)
        y = self.height - 120
        self.draw_text("Gold: {}".format(Settings.gold), 10, y, (255, 255, 0))
        self.draw_text("Red: A:{} D:{}".format(Settings.red_attackers, Settings.red_defenders), 150, y, (255, 0, 0))
        self.draw_text("Blue: A:{} D:{}".format(Settings.blue_attackers, Settings.blue_defenders), 340, y, (0, 0, 255))

    def run(self):
        """The mainloop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key==pygame.K_DOWN or event.key == pygame.K_KP2:
                        m.nextitem()
                        print(m.active_itemnumber)
                    if event.key==pygame.K_UP or event.key == pygame.K_KP8:
                        m.previousitem()
                    if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        result = m.get_text()
                        print(result)
                        if result is None:
                            break 
                        elif "x" in result:
                            left = result.split("x")[0]
                            right = result.split("x")[1]
                            if str(int(left))==left and str(int(right))== right:
                                PygView.width = int(left)
                                PygView.height = int(right)
                                self.set_resolution()
                                                        
                        elif result=="Play":
                        
                            print("activating external program")
                            pygame.quit()
                            template004_sprites_collision_detection.PygView(900,900).run()
                            print("bye") 
                            self.__init__()
                        elif result == "Buy blue attacker":
                            self.cash.play
                            if Settings.gold >= Settings.price_blue:
                                Settings.gold -= Settings.price_blue
                                Settings.blue_attackers += 1
                            else:
                                print("Earn some money first!")
                                                  
                        elif result == "Buy blue defender":
                            self.cash.play
                            if Settings.gold >= Settings.price_blue:
                                Settings.gold -= Settings.price_blue
                                Settings.blue_defenders += 1
                            else:
                                print("Earn some money first!")
                                
                        elif result == "Buy red attacker":
                            self.cash.play
                            if Settings.gold >= Settings.price_red:
                                Settings.gold -= Settings.price_red
                                Settings.red_attackers += 1
                            else:
                                print("Earn some money first!")
                                
                        elif result == "Buy red defender":
                            self.cash.play
                            if Settings.gold >= Settings.price_red:
                                Settings.gold -= Settings.price_red
                                Settings.red_defenders += 1
                            else:
                                print("Earn some money first!")
                                
                        elif result == "Sell blue attacker":
                            self.cash.play
                            if Settings.blue_attackers > 0:
                                Settings.gold += Settings.price_blue //2
                                Settings.blue_attackers -= 1
                            else:
                                print("You have no blue attacker!")
                                                  
                        elif result == "Sell blue defender":
                            self.cash.play
                            if Settings.blue_defenders > 0:
                                Settings.gold += Settings.price_blue //2
                                Settings.blue_defenders -= 1
                            else:
                                print("You have no blue defenders!")
                                
                        elif result == "Sell red attacker":
                            self.cash.play
                            if Settings.red_attackers > 0:
                                Settings.gold += Settings.price_red //2
                                Settings.red_attackers -= 1
                            else:
                                print("You have no red attacker!")
                                
                        elif result == "Sell red defender":
                            self.cash.play
                            if Settings.red_defenders > 0:
                                Settings.gold += Settings.price_red //2
                                Settings.red_defenders -= 1
                            else:
                                print("You have no red defenders!")
                                
                        elif result == "how to play":
                            text="play this game\n as you like\n and win!"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "nix":
                            text="nix\n gar nix\n wirklich nix!"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "how to win":
                            text="to win the game:\n shoot down enemies\n avoid catching bullets"
                            textscroller_vertical.PygView(text, self.width, self.height, bg_filename=os.path.join("data", "800px-La_naissance_de_Venus.jpg")).run()
                        elif result == "False":
                            Settings.menu["Credits"][2] = "True" # toggle
                        elif result == "True":
                           Settings.menu["Credits"][2] = "False" # toggle
                        elif result=="Quit":
                            print("Bye")
                            pygame.quit()
                            sys.exit()
                                            

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0 
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime), color=(30, 120 ,18))
            pygame.draw.line(self.screen,(random.randint(0,255),random.randint(0,255), random.randint(0,255)),(50,self.height - 80),(self.width -50,self.height - 80) ,3)             
            self.paint()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()

    def draw_text(self, text ,x=50 , y=0,color=(27,135,177)):
        if y==0:
            y= self.height - 50
        
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))


if __name__ == '__main__':

    # call with width of window and fps
    m=Menu(Settings.menu)
    PygView().run()
