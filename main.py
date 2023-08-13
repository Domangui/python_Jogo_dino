import pygame
from pygame.locals import *
from sys import exit
from random import randrange, choice
import os

pygame.init()

LARGURA = 640
ALTURA = 480

TELA = pygame.display.set_mode((LARGURA, ALTURA))

diretorio_principal = os.path.dirname(__file__)
diretorio_imagem = os.path.join(diretorio_principal, 'Sprite')
diretorio_som = os.path.join(diretorio_principal, 'Som')

sprite_all = pygame.image.load(os.path.join(diretorio_imagem, 'DinoSprites.png'))
all_sprites = pygame.sprite.Group()

escolha_obstaculo = choice([0,1])
velocidade = 10
contador = 0
def definir_texto(msg,tamanho, cor,x,y):
    
    fonte = pygame.font.Font(None,tamanho)
    texto = fonte.render(str(msg),True, cor)
    texto_rect = texto.get_rect()
    texto_rect.midtop = (x,y)

    TELA.blit(texto, texto_rect)

def reiniciar(self):
    global velocidade, contador, escolha_obstaculo
        
    velocidade = 10
    contador = 0
    escolha_obstaculo = choice([0,1])
    cacto.rect.x = LARGURA
    dinoVoador.rect.x = LARGURA

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dino = []
        for i in range(3):
            img = sprite_all.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.dino.append(img)

        self.atual = 0
        self.image = self.dino[self.atual]
        self.rect = self.image.get_rect()
        self.mascara = pygame.mask.from_surface(self.image)
        self.pos_inicial_y = ALTURA - 64 - 96//2
        self.rect.center = (100,ALTURA - 64)

        self.pular = False



    def pulo(self):
        self.pular = True

    def Mov_dino(self):      
        self.atual += 0.5
        if self.atual >= len(self.dino):
            self.atual = 0  
        self.image = self.dino[int(self.atual)]

    def update(self):

        self.Mov_dino()        

        if self.pular == True:
            self.rect.y -= 14
            if self.rect.y <= 230:
                self.pular = False
        else:
            self.rect.y += 14
            if self.rect.y > self.pos_inicial_y:
                self.rect.y = self.pos_inicial_y

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_all.subsurface((5*32,0,32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.mascara = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA ,ALTURA - 64)
        self.rect.x = LARGURA
    
    def update(self):

        if self.escolha == 0:
            self.rect.x -= velocidade
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagem_dinossauro = []
        for i in range(3,5):
            img = sprite_all.subsurface((i*32,0,32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.imagem_dinossauro.append(img)
        self.atual = 0 
        self.image = self.imagem_dinossauro[self.atual]
        mascara = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, ALTURA - 220)
        self.rect.x = LARGURA

    
    def update(self):

        if self.escolha == 1:
            self.atual +=0.11 
            if self.atual >= len(self.imagem_dinossauro):
                self.atual = 0 
            self.image = self.imagem_dinossauro[int(self.atual)]

            self.rect.x -= velocidade
            if self.rect.topright[0] <= 0:
                self.rect.x = LARGURA

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_all.subsurface((32*6,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))

        self.rect = self.image.get_rect()
        self.rect.y = (ALTURA - 64)
        self.rect.x = (pos_x * 64)
    def update(self):
        if self.rect.topright[0] <= 0:
            self.rect.x = LARGURA
        self.rect.x -= 10

class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_all.subsurface((7*32,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32*3,32*3))

        self.rect = self.image.get_rect()
        self.rect.x = randrange(30,300,90)
        self.rect.y = randrange(50,200,50)
    def update(self):
        
        if self.rect.topright[0] <= 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50,200,50)
        self.rect.x -= velocidade


for i in range(3):
    nuvem = Nuvem()
    all_sprites.add(nuvem)

for i in range(LARGURA*3//64):
    chao = Chao(i)
    all_sprites.add(chao)

dino = Dino()
all_sprites.add(dino)

cacto = Cacto()
all_sprites.add(cacto)

dinoVoador = DinoVoador()
all_sprites.add(dinoVoador)

grupo_colisao = pygame.sprite.Group()
grupo_colisao.add(cacto)
grupo_colisao.add(dinoVoador)
while True:
    pygame.time.Clock().tick(30)
    TELA.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_inicial_y:
                    pass
                else:
                    dino.pulo()
            if event.key == K_r:
                reiniciar()

    colidiu = pygame.sprite.spritecollide(dino,grupo_colisao,False, pygame.sprite.collide_mask)


    if cacto.rect.x <= 0 or dinoVoador.rect.x < 0:
        escolha_obstaculo = choice([0,1])
        cacto.rect.x = LARGURA
        dinoVoador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dinoVoador.escolha = escolha_obstaculo    
        
    if colidiu:
        definir_texto('GAME OVER',40,(0,0,0), LARGURA //2, ALTURA//2)
        definir_texto('pressione r para reiniciar', 30,(0,0,0), LARGURA //2, ALTURA //2 + 30)
    else:
        all_sprites.update()
        contador += 1 
        if contador % 100 == 0:
            if velocidade >= 20:
                velocidade = 20
            velocidade += 10

        definir_texto(contador,50,(0,0,0),LARGURA - 50, 20)
        

    

    all_sprites.draw(TELA)
    
    pygame.display.flip()