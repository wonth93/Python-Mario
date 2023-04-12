import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

# setting the caption at the top of the window
pygame.display.set_caption("Martin Mario")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 600
# frame per second
FPS = 60
# player velocity moving around the screen
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
  image = pygame.image.load(join("assets", "Background", name))
  _, _, width, height = image.get_rect()
  tiles = []

  for i in range(WIDTH // width + 1):
    for j in range(HEIGHT // height + 1):
      pos = (i * width, j * height)
      tiles.append(pos)
  
  return tiles, image

def draw(window, background, bg_image):
  for tile in background:
    window.blit(bg_image, tuple(tile))

  pygame.display.update()

def main(window):
  clock = pygame.time.Clock()
  background, bg_image = get_background("Gray.png")

  # regulate the frame rate across different devices
  run = True
  while run:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break

  pygame.quit()
  quit()

if __name__ == "__main__":
  main(window)
