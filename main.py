import pygame
import sys
import random

"""CONFIGURAÇÔES"""
WIDTH = 100                     # tamanho da tela(quanto maior, mais lento)
HEIGHT = 100
TESTE = True
#USE_RANDOM_COLOR = False
menu_x, menu_y = 720, 480
BLOCK_SIZE = 20                 # tamanho do block
ROWS = WIDTH // BLOCK_SIZE      # quantidade de linhas
COLUMNS = HEIGHT // BLOCK_SIZE
vertices = []

'''CORES'''
BLACK = (0, 0, 0)
BLUE = (20, 20, 255)
RED = (204, 20, 20)
GREEN = (20, 255, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
CIAN = (52, 78, 91)
PINK = (224, 20, 227)

pygame.init()
display = pygame.display.set_mode((menu_x, menu_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Draw to Find")
pygame.mixer.music.load('assets/RetroFunk.mp3')
pygame.mixer.music.play(-1)

initial_art = pygame.image.load('assets/img/8bit.jpg').convert_alpha()
initial_art = pygame.transform.scale(initial_art,(WIDTH, HEIGHT))

class Vortex:
  def __init__(self, row, col, width, weight) -> None:
    self.weight = weight
    self.row = row * width
    self.col = col * width
    self.x = row
    self.y = col
    self.color = PINK
    self.size = width
    self.neighbours = []
    self.is_vortex = True
    self.visited = False
    self.is_wall()

  def is_wall(self):
    w = display.get_width()
    h = display.get_height()
    y_cond = self.y == 0 or self.y >= h - 1
    x_cond = self.x == 0 or self.x >= w - 1

    if x_cond or y_cond:
      self.is_vortex = False
      self.color = BLACK
      self.neighbours = []

  def see_neighbours(self, field):
    if (self.x > 0 and self.x < ROWS - 2) and (self.y > 0 and self.y < COLUMNS - 2):
      if field[self.x + 1][self.y].is_vortex:
        self.neighbours.append([field[self.x + 1][self.y], self.weight])     # vizinho da direita
      if field[self.x - 1][self.y].is_vortex:
        self.neighbours.append([field[self.x - 1][self.y], self.weight])     # vizinho da esquerda
      if field[self.x][self.y + 1].is_vortex:
        self.neighbours.append([field[self.x][self.y + 1], self.weight])     # vizinho de baixo
      if field[self.x][self.y - 1].is_vortex:
        self.neighbours.append([field[self.x][self.y - 1], self.weight])     # vizinho de cima
  
  def draw_vortex(self, display):
    pygame.draw.rect(display, self.color, (self.row, self.col, self.width, self.width))
    pygame.display.update()

    
def make_field():
  global vertices

  for i in range(ROWS):
    cols = []
    for j in range(COLUMNS):
      cols.append(Vortex(i, j, WIDTH // ROWS, 1))
    vertices.append(cols)

  for i in range(ROWS):
    for j in range(COLUMNS):
      vertices[i][j].see_neighbours(vertices)

def reset():
  for i in range(ROWS):
    for j in range(COLUMNS):
      vertices[i][j].visited = False

make_field()

print(vertices[1][1].neighbours[0])


while TESTE:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      TESTE = False
  
  display.blit(initial_art, (0,0))        
  pygame.display.update()
