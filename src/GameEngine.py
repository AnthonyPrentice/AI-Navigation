import pygame
import math
from  Sprites import *

#configurations
width, height = 1000, 700
white, blue , black, red, green = ((230, 230, 230), (0, 0, 255), (0, 0, 0),
                                 (255, 0, 0), (0, 128, 0))

pygame.init()
pygame.display.set_caption("AI Navigation Project")
screen = pygame.display.set_mode(size=(width, height))
clock = pygame.time.Clock()
fps = 60
pi = math.pi

#objects
wall_sprites = pygame.sprite.Group()
car_sprites = pygame.sprite.Group()
sensor_sprites =  pygame.sprite.Group()
#node_sprites = pygame.sprite.Group()
walls = list()
cars = list()
#nodes = list()

#init walls
for x in range(0,16):
    walls.append(Wall())
    wall_sprites.add(walls[x])

#placing walls
walls[0].move(200, 150), walls[0].resize(110, 10)
walls[1].move(150, 350), walls[1].resize(10, 400)
walls[2].move(250, 300), walls[2].resize(10, 300)
walls[3].move(305, 445), walls[3].resize(100, 10)
walls[4].move(305, 545), walls[4].resize(300, 10)
walls[5].move(350, 290), walls[5].resize(10, 300)
walls[6].move(450, 390), walls[6].resize(10, 300)
walls[7].move(505, 145), walls[7].resize(300, 10)
walls[8].move(505, 245), walls[8].resize(100, 10)
walls[9].move(650, 300), walls[9].resize(10, 300)
walls[10].move(550, 400), walls[10].resize(10, 300)
walls[11].move(705, 445), walls[11].resize(100, 10)
walls[12].move(705, 545), walls[12].resize(300, 10)
walls[13].move(750, 290), walls[13].resize(10, 300)
walls[14].move(850, 340), walls[14].resize(10, 400)
walls[15].move(800, 140), walls[15].resize(110, 10)
walls[15].color(red)
walls[15].finish = True

#cars
cars.append(Car())
car_sprites.add(cars[0])
cars[0].move(200,250)
#car sensors
for x in range(0, 4):
    sensor_sprites.add(cars[0].sensors[x])

'''ai nodes
for x in range(0, 7):
    nodes.append(Node())
    node_sprites.add(nodes[x])
nodes[0].move(200, 500), nodes[0].color(green)
nodes[1].move(400, 500), nodes[1].color(green)
nodes[2].move(400, 200), nodes[2].color(green)
nodes[3].move(600, 200), nodes[3].color(green)
nodes[4].move(600, 500), nodes[4].color(green)
nodes[5].move(800, 500), nodes[5].color(green)
nodes[6].move(800, 130), nodes[6].color(green)
'''

#program running
drive = True
run = True
#node = 0
while run:
    clock.tick(fps)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cars[0].angle -= .5
            if event.key == pygame.K_RIGHT:
                cars[0].angle += .5

    cars[0].drive()

    '''
    if node < 7:
        cars[0].angle = cars[0].getDirection(nodes[node])
        cars[0].drive()
        nodeCol = pygame.sprite.spritecollideany(cars[0], node_sprites)
        if nodeCol:
            nodes[node].move(-20, 1)
            node += 1
    '''

    #sensor detection
    for sensor in cars[0].sensors:
        sensor.calibrate(cars[0])
        sensor.see(cars[0], wall_sprites)

    #car collisions
    col = pygame.sprite.spritecollideany(cars[0], wall_sprites)
    if col:
        cars[0].speed = 0
        cars[0].image.fill(green)

    #Displaying to screen
    wall_sprites.update()
    car_sprites.update()
    sensor_sprites.update()
    #node_sprites.update()
    wall_sprites.draw(screen)
    car_sprites.draw(screen)
    sensor_sprites.draw(screen)
    #node_sprites.draw(screen)

    pygame.display.update()

pygame.quit()
