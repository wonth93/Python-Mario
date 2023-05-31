import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

# Initialize the pygame module
pygame.init()

# setting the caption at the top of the window
pygame.display.set_caption("MW Mario")

# List of global variables
BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 600
FPS = 60 # frame per second
PLAYER_VEL = 5 # player velocity moving around the screen
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

# Main function - what we run to start the game
def main(window):
  clock = pygame.time.Clock()
  background, bg_image = get_background("Gray.png")

  # regulate the frame rate across different devices
  run = True
  while run:
    clock.tick(FPS)

    for event in pygame.event.get():
      # allow player to quit the game
      if event.type == pygame.QUIT:
        run = False
        break

  pygame.quit()
  quit()

if __name__ == "__main__":
  main(window)
