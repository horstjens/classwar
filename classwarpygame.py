# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: template to show how to move pygames Sprites, simple physic and
collision detection between sprite groups. Also Subclassing and super.
this example is tested using python 3.4 and pygame
"""
import pygame 
import math
import random
import os
from vectorclass2d import Vec2d






class Hitpointbar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Boss sprite
        Boss needs a unique number in FlyingObject.numbers,
        self.hitpoints and self.hitpointsfull"""
    
        def __init__(self, bossnumber, height=7, color = (0,255,0), ydistance=10):
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.bossnumber = bossnumber # lookup in Flyingobject.numbers
            self.boss = FlyingObject.numbers[self.bossnumber]
            self.height = height
            self.color = color
            self._layer = 1
            self.ydistance = ydistance
            self.image = pygame.Surface((self.boss.rect.width,self.height))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,self.boss.rect.width,self.height),1)
            self.rect = self.image.get_rect()
            self.oldpercent = 0
            
            
            
        def update(self, time):
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                    int(self.boss.rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - self.ydistance
            #check if boss is still alive
            if self.bossnumber not in FlyingObject.numbers:
                self.kill() # kill the hitbar


class FlyingObject(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }
    
    def __init__(self, radius = 50, color=None, x=320, y=240,
                 dx=None, dy=None, layer=4, hitpoints=100, mass=10,
                 damage=10, speed=100, target=None, miss=0,
                 text="", fontsize=10):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObject.number # unique number for each sprite
        FlyingObject.number += 1 
        FlyingObject.numbers[self.number] = self 
        self.radius = radius
        self.mass = mass
        self.text = text
        self.damage = damage
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.x = x
        self.y = y
        self.fontsize = fontsize
        if color is None: # create random color if no color is given
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else:
            self.color = color
        if dx is None:
            self.dx = random.random() * 100 - 50 # from -50 to 50
        else:
            self.dx = dx
        if dy is None:
            self.dy = random.random() * 100 - 50
        else:
            self.dy = dy
        self.hitpoints = hitpoints
        self.hitpointsfull = hitpoints
        self.create_image()
        self.rect= self.image.get_rect()
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        self.speed = speed
        self.target = target
        self.miss = miss
        self.init2()
        
    def kill(self):
        if self.number in self.numbers:
            del self.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
        
    def init2(self):
        pass # for subclasses
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        self.image.fill((self.color))
        self.image = self.image.convert()
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        if self.x - self.width //2 < 0:
            self.x = self.width // 2
            self.dx *= -1 
        if self.y - self.height // 2 < 0:
            self.y = self.height // 2
            self.dy *= -1
        if self.x + self.width //2 > PygView.width:
            self.x = PygView.width - self.width //2
            self.dx *= -1
        if self.y + self.height //2 > PygView.height:
            self.y = PygView.height - self.height //2
            self.dy *= -1
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # kill ?
        if self.hitpoints < 1:
            self.kill()

class Ball(FlyingObject):
    """it's a pygame Sprite!"""
        
                
    def init2(self):
        self.mass = 150
        checked = False
        Hitpointbar(self.number)
    
    def create_image(self):
        # create a rectangular surface for the ball 50x50
        self.image = pygame.Surface((self.width,self.height))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
        pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
        pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        # self.surface = self.surface.convert() # for faster blitting if no transparency is used. 
        # to avoid the black background, make black the transparent color:
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()


class Human(FlyingObject):
    """a red (left) or a blue (right) soldier"""
    
    redarmy = []
    bluearmy = []
    
    def init2(self):
        Hitpointbar(self.number)
        self.dx = 0
        self._layer = 0
        self.dy = 0
        self.courage = random.random() * 0.25 # 0 - 1  
        
        if self.color == (255,0,0):
            self.party = "red"
            self.couragex = 1
            Human.redarmy.append(self.number)
            self.x = PygView.width // 10
        elif self.color == (0,0,255):
            self.party = "blue"
            self.couragex = -1
            Human.bluearmy.append(self.number)
            self.x = PygView.width // 10 * 9
            

    def kill(self):
        #print(Human.redarmy, Human.bluearmy)
        if self.party == 'red':
            Human.redarmy.remove(self.number)
        if self.party == 'blue':
            Human.bluearmy.remove(self.number)
        del FlyingObject.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
        #print(Human.redarmy, Human.bluearmy)
        if len(self.redarmy) == 0 and len(self.bluearmy) > 0:
            print("Victory for the blue army")
            FlyingText(x=PygView.width//2, y=PygView.height//2, 
                       text="Victory for the blue side", color=(0,0,255), fontsize=32)
        if len(self.bluearmy) == 0 and len(self.redarmy) > 0:
            print("Victory for the red army")
            FlyingText(x=PygView.width//2, y=PygView.height//2, 
                       text="Victory for the red side", color=(255,0,0), fontsize=32)
    
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        pygame.draw.rect(self.image, self.color, (35,5, self.width-45, self.height-10))
        pygame.draw.circle(self.image, (0,255,0), (self.width//2, self.height//5),10)
        if self.color == (255,0,0):
            pygame.draw.rect(self.image, (207,156,27), (self.width//2, 25, self.width//2, 10))
        elif self.color == (0,0,255):
            pygame.draw.rect(self.image, (207,156,27), (0, 25, self.width//2, 10))
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
    
    def update(self, seconds):
        super(Human,self).update(seconds)  # ruft methode update vom FlyingObject auf
        if random.random() < self.courage:
            self.x += self.couragex
        if self.party == "red":
            if self.x > PygView.width * 0.4 :
                self.x = PygView.width * 0.4
            if self.x < PygView.width // 10:
                self.x = PygView.width // 10
        elif self.party == "blue":
            if self.x < PygView.width * 0.6:
                self.x = PygView.width * 0.6
            if self.x > PygView.width // 10 * 9:
                self.x = PygView.width // 10 * 9
            
        
            
            
            
   
class FlyingText(FlyingObject):
    """a moving text that disappears after a short time"""
    
    def init2(self):
        self.lifetime = 2.5 # seconds
        self.age = 0
        self.dy = -50
        self.dx = 0
        self.ddy = 0.95 # smaller 1: text flies and stop. Greater 1: text goes faster and faster
    
    def create_image(self):
        font = pygame.font.SysFont('mono', self.fontsize, bold=True)
        fw, fh = font.size(self.text)
        self.image = font.render(self.text, True, self.color)
        #self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x - fw//2, self.y - fh//2)
     
    def update(self, seconds):
        # FlyingObject(self,seconds):
        super(FlyingText,self).update(seconds)
        self.dy *= self.ddy
        #self.lifetime -= seconds # aging
        self.age += seconds 
        if self.age > self.lifetime:
            self.kill() 
        # change alpha
        #set_alpha: 255 = full opaque, 0=full transparent
        #agingfactor: 1 = newborn, 0 = dead
        #agefactor =  (self.lifetime - self.age) / self.lifetime
        #agefactor = max(0.5,agefactor) # no negative values
        #print(agefactor*255)
        #self.image.set_alpha(int(agefactor * 255))
        #self.image.convert_alpha()
        #mode = pygame.BLEND_RGBA_MULT
        #tmp = get_alpha_surface(self.image, 128, 255, 255, 255, mode) # get current alpha
        #self.image = tmp
        
        
        
    
        
class Bullet(FlyingObject):
    """a small Sprite"""

    def init2(self):
        self.mass = 5
        self.lifetime = 8.5 # seconds
        if self.target is not None:
            # calculate dx, dy with speed
            self.targetvector = Vec2d(self.target.x, self.target.y)
            if self.miss != 0:
                #vmiss = Vec2d(random.randint(0,self.miss),0)
                vmiss = Vec2d(self.miss,0)
                vmiss.rotate(random.randint(0,360))
                #move += vmiss
                self.targetvector += vmiss
            
            move = self.targetvector - Vec2d(self.x, self.y)
            #move.normalized
            #move *= self.speed
            self.dx = move.x / move.length * self.speed
            self.dy = move.y / move.length * self.speed
            #print(move, self.dx, self.dy)

    def update(self, seconds):
        # FlyingObject(self,seconds):
        super(Bullet,self).update(seconds)
        self.lifetime -= seconds # aging
        if self.lifetime < 0:
            self.kill() 
        if self.target is not None:
            if self.miss < 15:
                t="direct hit!"
                self.factor = 15
                #self.target.hitpoints -= 20
            elif self.miss < 30:
                t="minor hit"
                self.factor = 10
                #self.target.hitpoints -= 5
            elif self.miss < 45:
                t="near miss"
                self.factor = 5
            else:
                t="miss"
                self.factor = 1
            if (self.dx > 0 and self.x > self.target.x) or (
                self.dx < 0 and self.x < self.target.x):
                FlyingText(x=self.x, y=self.y, text=t, color=self.color)
                if self.miss < 30:
                    self.target.hitpoints -= 30 - self.miss
                self.target.x -= self.target.couragex * self.factor 
                self.kill()
          
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()

def draw_examples(background):
    """painting on the background surface"""
    #------- try out some pygame draw functions --------
    # pygame.draw.line(Surface, color, start, end, width) 
    pygame.draw.line(background, (0,255,0), (10,10), (50,100))
    # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
    pygame.draw.rect(background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
    # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    pygame.draw.circle(background, (0,200,0), (200,50), 35)
    # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
    pygame.draw.polygon(background, (0,180,0), ((250,100),(300,0),(350,50)))
    # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
    pygame.draw.arc(background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
    #return background # not necessary to return the surface, it's already in the memory


def get_alpha_surface( surf, alpha=128, red=128, green=128, blue=128, mode=pygame.BLEND_RGBA_MULT):
    """returns a copy of a surface object with user-defined 
       values for red, green, blue and alpha. 
       Values from 0-255. 
       thanks to Claudio Canepa <ccanepacc@gmail.com>
       for this function."""
  
    tmp = pygame.Surface( surf.get_size(), pygame.SRCALPHA, 32)
    tmp.fill( (red,green,blue,alpha) )
    tmp.blit(surf, (0,0), surf.get_rect(), mode)
    return tmp

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))
    
def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .x .y, .dx, dy
           by Leonard Michlmayr"""
        # here we do some physics: the elastic
        # collision
        #
        # first we get the direction of the push.
        # Let's assume that the sprites are disk
        # shaped, so the direction of the force is
        # the direction of the distance.
        dirx = sprite1.x - sprite2.x
        diry = sprite1.y - sprite2.y
        #
        # the velocity of the centre of mass
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        # if we sutract the velocity of the centre
        # of mass from the velocity of the sprite,
        # we get it's velocity relative to the
        # centre of mass. And relative to the
        # centre of mass, it looks just like the
        # sprite is hitting a mirror.
        #
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        # (dirx,diry) is perpendicular to the mirror
        # surface. We use the dot product to
        # project to that direction.
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            # no distance? this should not happen,
            # but just in case, we choose a random
            # direction
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        # We are done. (dirx * dp, diry * dp) is
        # the projection of the velocity
        # perpendicular to the virtual mirror
        # surface. Subtract it twice to get the
        # new direction.
        #
        # Only collide if the sprites are moving
        # towards each other: dp > 0
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp


class PygView(object):
    width = 0
    height = 0
  
    def __init__(self, width=640, height=400, fps=60):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        tmp = pygame.image.load(os.path.join("data","background01.jpg"))
        self.background = pygame.transform.scale(tmp, (self.width, self.height))
        self.background.convert()
        #self.background = pygame.Surface(self.screen.get_size()).convert()  
        #self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.paint() 
        
    def paint(self):
        """painting on the surface and create sprites"""
        # make an interesting background 
        draw_examples(self.background)
        # create (pygame) Sprites.
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.bulletgroup = pygame.sprite.Group()
        self.humangroup = pygame.sprite.Group()
        self.hitbargroup = pygame.sprite.Group()
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Bullet.groups = self.allgroup, self.bulletgroup
        Hitpointbar.groups = self.hitbargroup
        Human.groups = self.allgroup, self.humangroup
        FlyingText.groups = self.allgroup
        
        #self.ball1 = Ball(x=100, y=100) # creating a Ball Sprite
        #self.ball2 = Ball(x=200, y=100) # create another Ball Sprite
        
        for y in (100,200,300,400,500):
            Human(y=y, color=(255,0,0))
            Human(y=y, color=(0,0,255))
        #self.red1 = Human(y=100, color=(255,0,0))
        #self.blue1 =Human(y=366, color=(0,0,255))


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
                    if event.key == pygame.K_b:
                        Ball(x=random.randint(0,PygView.width-100)) # add big balls!
                    if event.key == pygame.K_c:
                        Bullet(radius=5, x=0,y=0, dx=200, dy=200)
                    if event.key == pygame.K_LSHIFT:
                        Bullet(radius=5, x=self.red1.x, y=self.red1.y,
                               target=self.blue1)
                    if event.key == pygame.K_RSHIFT:
                        Bullet(radius=5, x=self.blue1.x, y=self.blue1.y,
                               target=self.red1)
                    if event.key == pygame.K_LCTRL:
                        Bullet(radius=5, x=self.red1.x, y=self.red1.y, color=(250,0,0),
                               target=self.blue1, miss=random.randint(0,150))
                    if event.key == pygame.K_RCTRL:
                        Bullet(radius=5, x=self.blue1.x, y=self.blue1.y, color=(0,0,250),
                               target=self.red1, miss=random.randint(0,150))
                    if event.key == pygame.K_1:
                        self.red1.hitpoints-=1
                        print(self.red1.hitpoints, self.red1.hitpointsfull)
                    if event.key == pygame.K_2:
                        self.red1.hitpoints+=1
                    if event.key == pygame.K_SPACE:
                        redattacker  = FlyingObject.numbers[random.choice(Human.redarmy)]
                        redvictim    = FlyingObject.numbers[random.choice(Human.bluearmy)]
                        blueattacker = FlyingObject.numbers[random.choice(Human.bluearmy)]
                        bluevictim   = FlyingObject.numbers[random.choice(Human.redarmy)]
                        # red army is left, blue army is right
                        for _ in range(3):
                            Bullet(radius=5, x=redattacker.x, y=redattacker.y, color=(250,0,0),
                                   target=redvictim, miss=random.randint(0,PygView.width//2-redattacker.x))
                        for _ in range(3):
                            Bullet(radius=5, x=blueattacker.x, y=blueattacker.y, color=(0,0,250),
                                  target=bluevictim, miss=random.randint(0,blueattacker.x - PygView.width//2))
                            
                            
                            
                            
            # ----- pressed keys -------
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LCTRL]:
                Bullet(radius=5, x=self.red1.x, y=self.red1.y, color=(250,0,0),
                       target=self.blue1, miss=random.randint(0,150))
            if pressed[pygame.K_RCTRL]:
                Bullet(radius=5, x=self.blue1.x, y=self.blue1.y, color=(0,0,250),
                       target=self.red1, miss=random.randint(0,150))
                
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed
            # ---------- collision detection between ball and bullet sprites ---------
            for ball in self.ballgroup:
               crashgroup = pygame.sprite.spritecollide(ball, self.bulletgroup, False, pygame.sprite.collide_circle)
               for bullet in crashgroup:
                   elastic_collision(ball, bullet) # change dx and dy of both sprites
                   ball.hitpoints -= bullet.damage
            # --------- collision detection between ball and other balls
            for ball in self.ballgroup:
                crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
                for otherball in crashgroup:
                    if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
                        elastic_collision(ball, otherball) # change dx and dy of both sprites
            # ---------- collision detection between bullet and other bullets
            #for bullet in self.bulletgroup:
            #    crashgroup = pygame.sprite.spritecollide(bullet, self.bulletgroup, False, pygame.sprite.collide_circle)
            #    for otherbullet in crashgroup:
            #        if bullet.number > otherbullet.number:
            #             elastic_collision(bullet, otherball) # change dx and dy of both sprites
            # -------- remove dead -----
            #for sprite in self.ballgroup:
            #    if sprite.hitpoints < 1:
            #        sprite.kill()
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.hitbargroup.update(seconds)
            self.allgroup.draw(self.screen) 
            self.hitbargroup.draw(self.screen)          
            # write text over everything 
            #write(self.screen, "Press b to add another ball", x=self.width//2, y=250, center=True)
            #write(self.screen, "Press c to add another bullet", x=self.width//2, y=350, center=True)
            # next frame
            pygame.display.flip()
            #pygame.display.set_caption("hp red1: {} hp blue1: {}".format(self.red1.hitpoints, self.blue1.hitpoints))
        pygame.quit()

if __name__ == '__main__':
    PygView(960,600).run() # try PygView(800,600).run()
