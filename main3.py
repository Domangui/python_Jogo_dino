import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange
pygame.init()

LARGURA = 640
ALTURA = 480

TELA =  pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo do dino')

diretorio_principal = os.path.dirname(__file__)
diretorio_imagem = os.path.join(diretorio_principal, 'Sprite')
diretorio_som = os.path.join(diretorio_principal, 'Som')

Sprite_do_jogo = pygame.image.load(os.path.join(diretorio_imagem, 'DinoSprites.png'))
all_sprites = pygame.sprite.Group()

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dino = []
        for i in range(3):
            self.dino_imagem = Sprite_do_jogo.subsurface((i*32,0),(32,32))
            self.dino_imagem = pygame.transform.scale(self.dino_imagem, (32*3,32*3))
            self.dino.append(self.dino_imagem)
        self.atual = 0
        self.image = self.dino[self.atual]
        self.rect = self.image.get_rect()
        self.rect.center = (64, ALTURA-64)
    
    def update(self):
        self.atual += 0.5
        if self.atual >= len(self.dino):
            self.atual = 0
        self.image = self.dino[int(self.atual)]

class Chao(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = Sprite_do_jogo.subsurface((32*6,0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.rect.x = (LARGURA - 64 *loc)
        self.rect.y = (ALTURA - 64)
    def update(self):
        self.rect.x -= 5
        if self.rect.topright[0] <= 0:
            self.rect.x = LARGURA

class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Sprite_do_jogo.subsurface((32*7,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*3,32*3))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(30,350,90)
        self.rect.y = randrange(30,200,50)

    def update(self):
        self.rect.x -=6
        if self.rect.topright[0] <= 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50,200,50)
dino = Dino()
all_sprites.add(dino)
for i in range(LARGURA*3//64):
    chao = Chao(i)
    all_sprites.add(chao)

for i in range(4):
    nuvem = Nuvem()
    all_sprites.add(nuvem)



while True:
    pygame.time.Clock().tick(30)
    TELA.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            exit()
    all_sprites.draw(TELA)
    all_sprites.update()
    pygame.display.flip()
