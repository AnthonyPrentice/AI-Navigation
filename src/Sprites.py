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
    sprite_color = black
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = self.rect.centerx
        self.y = self.rect.centery
    def rotate(self, ang):
        self.image = pygame.transform.rotate(self.image, ang)
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_color = black
        self.width = 100
        self.height = 10
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.sprite_color)
        self.rect = self.image.get_rect()
        self.rect.center = (70, 20)
        self.finish = False
#-------------------------------------------------------------------------------
class Car(pygame.sprite.Sprite, Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.angle = 1.57#90 degrees in rads 
        self.sprite_color = blue
        self.width = 35
        self.height = 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.sprite_color)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.sensors = list() 
        self.initSensors()
    def initSensors(self):
        for x in range(0, 4):
            self.sensors.append(Sensor())
            if x == 0:
                self.sensors[x].name = "left"
            elif x == 1:
                self.sensors[x].name = "bottom"
                self.sensors[x].resize(1, 50)
            elif x == 2:
                self.sensors[x].name = "right"
            elif x == 3:
                self.sensors[x].name = "top"
                self.sensors[x].resize(1, 50)
            else:
                pass
    def drive(self, steeringAngle, walls): #angle is in radians
        #--------------------moving-----------------------
        self.angle += steeringAngle
        self.x = self.x + (self.speed*math.cos(self.angle))
        self.y = self.y + (self.speed*math.sin(self.angle))
        self.rect.centerx = self.x
        self.rect.centery = self.y
        for sensor in self.sensors:
            sensor.calibrate(self)
            sensor.see(self, walls)
        #--------------------rotating---------------------
        if steeringAngle != 0:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(self.sprite_color)
            self.image = pygame.transform.rotate(self.image, math.degrees(self.angle * -1))
            self.rect = self.image.get_rect(center=self.rect.center)
    def getPos(self):
        position = [self.rect.centerx, self.rect.centery]
        return position
#-------------------------------------------------------------------------------
class Sensor(pygame.sprite.Sprite, Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 1), pygame.SRCALPHA)
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (70, 20)
        self.name = None
    def calibrate(self, car):
        if self.name == "left":
            self.rect.left = car.rect.right
            self.rect.centery = car.rect.centery
        elif self.name == "bottom":
            self.rect.bottom = car.rect.top
            self.rect.centerx = car.rect.centerx
        elif self.name == "right":
            self.rect.right = car.rect.left
            self.rect.centery = car.rect.centery
        elif self.name == "top":
            self.rect.top = car.rect.bottom
            self.rect.centerx = car.rect.centerx
        else:
            pass
    def see(self, car, wall_sprites):
        col = pygame.sprite.spritecollideany(self, wall_sprites)
        if col:
            if self.name == "left":
                self.resize(self.rect.width-2, self.rect.height)
            elif self.name == "bottom":
                self.resize(self.rect.width, self.rect.height-2)
            elif self.name == "right":
                self.resize(self.rect.width-2, self.rect.height)
            elif self.name == "top":
                self.resize(self.rect.width, self.rect.height-2)
            else:
                pass
        else:
            if self.name == "left":
                if self.rect.width < 50:
                    self.resize(self.rect.width+2, self.rect.height)
            elif self.name == "bottom":
                if self.rect.height < 50:
                    self.resize(self.rect.width, self.rect.height+2)
            elif self.name == "right":
                if self.rect.width < 50:
                    self.resize(self.rect.width+2, self.rect.height)
            elif self.name == "top":
                if self.rect.height < 50:
                    self.resize(self.rect.width, self.rect.height+2)
            else:
                pass
        self.calibrate(car)
#-------------------------------------------------------------------------------
