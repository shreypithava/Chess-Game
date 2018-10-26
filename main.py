# import sys
# import pygame
import mainWindow
# import random

# import os

# print(os.system('ls'))
# for item in os.listdir('.'):
#     if 'png' in item:
#         print(item)

# import time

gui = mainWindow.Window()
for i in range(64):
    print('{}, {}{}, {}'.format(gui.blocks[i].label[1], chr(97 + (i % 8)), 8 - i // 8, i))
gui.run()

# pygame.init()
# print('Here')
# pygame.init()
#
# size = width, height = 480, 320
# speed = [2, 2]
# black = 0, 0, 0
#
# screen = pygame.display.set_mode(size)
#
# ball = pygame.image.load("imge.png")
# ballrect = ball.get_rect()
#
# while 1:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#
#     ballrect = ballrect.move(speed)
#     if ballrect.left < 0 or ballrect.right > width:
#         speed[0] = -speed[0]
#     if ballrect.top < 0 or ballrect.bottom > height:
#         speed[1] = -speed[1]
#
#     screen.fill(black)
#     screen.blit(ball, ballrect)
#     pygame.display.flip()
