import pygame
import math

width, height = 1000, 700
white, blue , black, red, green = ((230, 230, 230), (0, 0, 255), (0, 0, 0),
                                 (255, 0, 0), (0, 128, 0))
#-------------------------------------------------------------------------------
class Sprite():
    x = 0.0 #to keep track of position as a double instead of int 
    y = 0.0 #since pygame only stores positions as ints, which causes data to be lost
            #when operations involving positions occur i.e. drive() for Car
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = self.rect.centerx
        self.y = self.rect.centery
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def move(self, x, y):
        self.rect.center = (x, y)
        self.x = self.rect.centerx
        self.y = self.rect.centery
    def resize(self, width, height):
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=self.rect.center)
    def color(self, color):
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.rect.center)
 #-------------------------------------------------------------------------------   
class Wall(pygame.sprite.Sprite, Sprite):
    image = pygame.Surface((100, 10))
    image.fill(black)
    rect = image.get_rect()
    rect.center = (70, 20)
    finish = False
#-------------------------------------------------------------------------------
class Car(pygame.sprite.Sprite, Sprite):
    image = pygame.Surface((20, 20), pygame.SRCALPHA)
    image.fill(blue)
    rect = image.get_rect()
    rect.center = (width/2, height/2)
    speed = 2
    angle = 1.57 
    sensors = list() 
    def initSensors(self):
        for x in range(0, 4):
            self.sensors.append(Sensor())
            if x == 0:
                self.sensors[x].name = "right"
            elif x == 1:
                self.sensors[x].name = "top"
                self.sensors[x].resize(1, 50)
            elif x == 2:
                self.sensors[x].name = "left"
            elif x == 3:
                self.sensors[x].name = "bottom"
                self.sensors[x].resize(1, 50)
            else:
                pass
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.initSensors()
    def drive(self): #angle is in radians
        self.x = self.x + (self.speed*math.cos(self.angle))
        self.y = self.y + (self.speed*math.sin(self.angle))
        self.rect.centerx = self.x
        self.rect.centery = self.y
    def getPos(self):
        position = [self.rect.centerx, self.rect.centery]
        return position
    def getDirection(self, sprite):
        x = (sprite.rect.centerx - self.rect.centerx)
        y = (sprite.rect.centery - self.rect.centery)
        theta = 0
        if x > 0:
            if y > 0:
                theta = math.atan2(y, x)
            elif y < 0:
                theta = math.atan2(y, x) + 6.28319
            elif y == 0:
                theta = 0
        elif x < 0:
            if y > 0:
                theta = math.atan2(y, x) + 3.14159
            elif y < 0:
                theta = math.atan2(y, x) + 3.14159
            elif y == 0:
                theta = 3.14159
        elif x == 0:
            if y > 0:
                theta = 1.5708
            elif y < 0:
                theta = 4.71239
            elif y == 0:
                theta = 0
        return theta
#-------------------------------------------------------------------------------
class Sensor(pygame.sprite.Sprite, Sprite):
    image = pygame.Surface((50, 1))
    image.fill(blue)
    rect = image.get_rect()
    rect.center = (70, 20)
    name = None
    def calibrate(self, car):
        if self.name == "right":
            self.rect.left = car.rect.right
            self.rect.centery = car.rect.centery
        elif self.name == "top":
            self.rect.bottom = car.rect.top
            self.rect.centerx = car.rect.centerx
        elif self.name == "left":
            self.rect.right = car.rect.left
            self.rect.centery = car.rect.centery
        elif self.name == "bottom":
            self.rect.top = car.rect.bottom
            self.rect.centerx = car.rect.centerx
        else:
            pass
    def see(self, car, wall_sprites):
        col = pygame.sprite.spritecollideany(self, wall_sprites)
        if col:
            if self.name == "right":
                self.resize(self.rect.width-2, self.rect.height)
            elif self.name == "top":
                self.resize(self.rect.width, self.rect.height-2)
            elif self.name == "left":
                self.resize(self.rect.width-2, self.rect.height)
            elif self.name == "bottom":
                self.resize(self.rect.width, self.rect.height-2)
            else:
                pass
        else:
            if self.name == "right":
                if self.rect.width < 50:
                    self.resize(self.rect.width+2, self.rect.height)
            elif self.name == "top":
                if self.rect.height < 50:
                    self.resize(self.rect.width, self.rect.height+2)
            elif self.name == "left":
                if self.rect.width < 50:
                    self.resize(self.rect.width+2, self.rect.height)
            elif self.name == "bottom":
                if self.rect.height < 50:
                    self.resize(self.rect.width, self.rect.height+2)
            else:
                pass
        self.calibrate(car)
#-------------------------------------------------------------------------------
