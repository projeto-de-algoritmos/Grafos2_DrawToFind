import pygame
import sys
import random
from queue import PriorityQueue

"""CONFIGURAÇÔES"""
WIDTH = 720                     # tamanho da tela(quanto maior, mais lento)
HEIGHT = 480
TESTE = True
ALG_RUN = False 
menu_x, menu_y = 720, 480
BLOCK_SIZE = 10                  # tamanho do block
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
# display = pygame.display.set_mode((menu_x, menu_y))
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Draw to Find")
pygame.mixer.music.load('assets/RetroFunk.mp3')
# pygame.mixer.music.play(-1)

initial_art = pygame.image.load('assets/img/8bit.PNG').convert_alpha()
initial_art = pygame.transform.scale(initial_art,(menu_x, menu_y))

options_art = pygame.image.load('assets/img/room.PNG').convert_alpha()
options_art = pygame.transform.scale(options_art,(menu_x, menu_y))



'''MENUS'''
def draw_text(text, font, color, scr, x, y):
  title = font.render(text, True, color)
  rect = title.get_rect(center=(x, y))
  scr.blit(title, rect)

def draw_main_menu():
  # display = pygame.display.set_mode((WIDTH, HEIGHT))
  display.fill(CIAN)
  pygame.display.update()
  while True:
    # display.blit(initial_art, (0,0))  
    # font70 = pygame.font.Font('assets/title-font.ttf', 70)
    # font30 = pygame.font.Font('assets/title-font.ttf', 40)
    
    # draw_text("Draw to Find", font70, BLACK, display, 360, 150)
    # draw_text("Clique na tela para iniciar", font30, BLACK, display, 360, 250)
    # draw_text("O - Opcoes", font30, BLACK, display, 360, 320)
    # draw_text("S - Sair", font30, BLACK, display, 360, 380)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        pass
        # if event.key == pygame.K_o:
        #   draw_options_menu()
        # if event.key == pygame.K_s:
        #   pygame.quit()
        #   sys.exit()
      if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row = (pos[0]) // BLOCK_SIZE
        col = (pos[1]) // BLOCK_SIZE   
        if pygame.mouse.get_pressed()[0]:
          print(row, col, len(vertices))
          vertices[row][col].is_vortex = False
          vertices[row][col].color = WHITE
          vertices[row][col].draw_vortex(display)
          pygame.display.update()
        if pygame.mouse.get_pressed()[2]:
          vertices[row][col].is_vortex = True
          vertices[row][col].color = CIAN
          vertices[row][col].draw_vortex(display)
          pygame.display.update()

          

    pygame.display.update()
    

def draw_options_menu():
  pygame.display.update()
  global BLOCK_SIZE, ALG_RUN, ROWS, COLUMNS
  b, d = "DIJKSTRA", "ESTRELA"
  FPS = 200
  while True:
    clock.tick(FPS)
    display.blit(options_art, (0,0))
    font40 = pygame.font.Font('assets/title-font.ttf', 50)
    font20 = pygame.font.Font('assets/title-font.ttf', 20)
    font24 = pygame.font.Font('assets/title-font.ttf', 24)
    font_obs = pygame.font.Font('assets/title-font.ttf', 17)
    draw_text("Opções:", font40, BLACK, display, 330, 55)
    draw_text("K/L Tamanho do pixel:", font24, BLACK, display, 330, 155)
    draw_text(f"{BLOCK_SIZE}", font24, BLUE, display, 510, 155)
    draw_text("(K = -   L = +)", font_obs, BLACK, display, 330, 185)
    draw_text("B/D Algoritmo usado: ", font24, BLACK, display, 330, 240)
    draw_text(f"{b if not ALG_RUN else d}", font24, BLUE, display, 575, 240)
    draw_text("V - Voltar", font20, BLACK, display, 100, 440)
    
     
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_v:
          draw_main_menu()
        #if event.key == pygame.K_r:
          #draw_resolution_menu()
        if event.key == pygame.K_l:
          BLOCK_SIZE += 1 if BLOCK_SIZE < 40 else 0
          pygame.display.update()
        if event.key == pygame.K_k:
          BLOCK_SIZE -= 1 if BLOCK_SIZE > 1 else 0
          pygame.display.update()
        if event.key == pygame.K_b:
          ALG_RUN = False
          pygame.display.update()
        if event.key == pygame.K_d:
          ALG_RUN = True
          pygame.display.update()
    
    ROWS = WIDTH // BLOCK_SIZE
    COLUMNS = HEIGHT // BLOCK_SIZE    
    pygame.display.update()

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
    pygame.draw.rect(display, self.color, (self.row, self.col, self.size, self.size))
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


if __name__ == '__main__':
  draw_main_menu()
