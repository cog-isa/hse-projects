import pygame
from time import sleep

DISPLAY = (320, 240)
pygame.init()
flags = pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(DISPLAY, flags)
background = pygame.Surface(DISPLAY)
background.fill(pygame.Color("#000000"))
for i in range(1, 63):
    try:
        path = 'raw/test'+str(i)+'.jpg'
        img = pygame.image.load(path)
    except pygame.error:
        try:
            path = 'raw/test'+str(i)+'.gif'
            img = pygame.image.load(path)
        except pygame.error:
            path = 'raw/test'+str(i)+'.png'
            img = pygame.image.load(path)
    screen.blit(img, [0, 0])
    pygame.display.update()
    save_as = 'people_big/test'+str(i)+'.bmp'
    pygame.image.save(screen, save_as)
    sleep(0.1)