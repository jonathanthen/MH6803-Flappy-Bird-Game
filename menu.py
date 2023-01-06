import pygame
import pygame_menu
from pygame.locals import *
import sys
import os

# Initialize
pygame.init()
window = pygame.display.set_mode((696, 522))

# Make menu
def flying_penguin():
    os.system('python flyPenguinGame.py')

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    pygame.display.update()


def jump_penguin():
    os.system('python jumpPenguinGame.py')

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    pygame.display.update()


menu = pygame_menu.Menu('Welcome to the Penguin Game', 696, 522, theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Flying Penguin', flying_penguin)
menu.add.button('Jumping Penguin', jump_penguin)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Run menu
menu.mainloop(window)