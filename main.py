import pygame
import sys
import time
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
caminho = []
distancia = []
id_cont = 0

'''CORES'''
BLACK = (0, 0, 0)
BLUE = (20, 20, 255)
RED = (204, 20, 20)
GREEN = (20, 255, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
CIAN = (52, 78, 91)
PINK = (224, 20, 227)

def random_color():
  return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)

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
        if event.key == pygame.K_SPACE:
          dijkstra(vertices[4][4], vertices[10][10])
        if event.key == pygame.K_r:
          reset('all')
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
          vertices[row][col].is_vortex = False
          vertices[row][col].color = BLACK
          vertices[row][col].draw_vortex()
        if pygame.mouse.get_pressed()[2]:
          vertices[row][col].is_vortex = True
          vertices[row][col].color = CIAN
          vertices[row][col].draw_vortex()
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
  def __init__(self, row, col, width, display, id) -> None:
    self.row = row * width
    self.col = col * width
    self.id = id
    self.x = row
    self.y = col
    self.color = BLACK
    self.size = width
    self.display = display
    self.neighbours = []
    self.is_vortex = True
    self.visited = False
    self.previous = None
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
        self.neighbours.append(field[self.x + 1][self.y])     # vizinho da direita
      if field[self.x - 1][self.y].is_vortex:
        self.neighbours.append(field[self.x - 1][self.y])     # vizinho da esquerda
      if field[self.x][self.y + 1].is_vortex:
        self.neighbours.append(field[self.x][self.y + 1])     # vizinho de baixo
      if field[self.x][self.y - 1].is_vortex:
        self.neighbours.append(field[self.x][self.y - 1])     # vizinho de cima
  
  def draw_vortex(self):
    pygame.draw.rect(self.display, self.color, (self.row, self.col, self.size, self.size))
    pygame.display.update()

def dijkstra(node, end):
  distancia = [float('inf') for _ in range(len(vertices))]
  distancia[node.id] = 0

  queue = PriorityQueue()
  queue.put((0, node))
  node.visited = True


  while queue:
    dist, s = queue.get()
    if s == end:
      aux = s
      while aux.previous:
        # print(aux.previous.x, aux.previous.x)
        caminho.append(aux.previous)
        aux = aux.previous
    for i in s.neighbours:
      if not i.visited and i.is_vortex:
        i.visited = True
        i.previous = s
        queue.put((0, i))
        i.color = BLACK
        i.draw_vortex()
        # time.sleep(0.001)
    
  # print(caminho)
  reset('path')
  


def make_field():
  global vertices, id_cont

  for i in range(ROWS):
    cols = []
    for j in range(COLUMNS):
      cols.append(Vortex(i, j, WIDTH // ROWS, display, id_cont // BLOCK_SIZE))
      id_cont += 1
    vertices.append(cols)

  for i in range(ROWS):
    for j in range(COLUMNS):
      vertices[i][j].see_neighbours(vertices)

def reset(mode):
  global caminho
  caminho = [] if mode == 'all' else caminho
  for i in range(ROWS):
    for j in range(COLUMNS):
      if vertices[i][j].is_vortex:
        if mode == 'all':
          vertices[i][j].visited = False
          vertices[i][j].color = CIAN
          vertices[i][j].draw_vortex()
        elif mode == 'path':
          if vertices[i][j] not in caminho:
            vertices[i][j].visited = False
            vertices[i][j].color = CIAN
            vertices[i][j].draw_vortex()
      



if __name__ == '__main__':
  make_field()
  draw_main_menu()
