import pygame
import sys
import random

"""CONFIGURAÇÔES"""
WIDTH = 720                     # tamanho da tela(quanto maior, mais lento)
HEIGHT = 480
TESTE = True
#ALG_RUN = False                # True = DFS      False = FFS
#USE_RANDOM_COLOR = False
menu_x, menu_y = 720, 480
#BLOCK_SIZE = 20                 # tamanho do block
#ROWS = WIDTH // BLOCK_SIZE      # quantidade de linhas
#COLUMNS = HEIGHT // BLOCK_SIZE
#RANDOM_BFS = True              # muda o efeito de preenchimento da BFS
#RANDOM_DFS = True              # muda o efeito de preenchimento da DFS
#TAXA_COR = 2                  # muda a frequencia com que cada cor é alterada, quanto maior, mais cores aparecerão (melhor efeito entre 16 e 100)
vertices = []

'''CORES'''
#RANDOM_COLOR = (random.randrange(256),random.randrange(256),random.randrange(256))
#BLACK = (0, 0, 0)
#BLUE = (20, 20, 255)
#RED = (204, 20, 20)
#GREEN = (20, 255, 20)
#WHITE = (255, 255, 255)
#YELLOW = (255, 255, 102)
#CIAN = (52, 78, 91)

pygame.init()
display = pygame.display.set_mode((menu_x, menu_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Draw to Find")
pygame.mixer.music.load('assets/RetroFunk.mp3')
pygame.mixer.music.play(-1)

initial_art = pygame.image.load('assets/img/8bit.jpg').convert_alpha()
initial_art = pygame.transform.scale(initial_art,(WIDTH, HEIGHT))


while TESTE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            TESTE = False
    
    display.blit(initial_art, (0,0))        
    pygame.display.update()
