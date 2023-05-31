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
WIDTH, HEIGHT = 1000, 600
FPS = 60 # frame per second
PLAYER_VEL = 5 # player velocity moving around the screen
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Player info and movement
class Player(pygame.sprite.Sprite):
  COLOR = (255, 0, 0)
  GRAVITY = 1

  def __init__(self, x, y, width, height):
      self.rect = pygame.Rect(x, y, width, height)
      self.x_vel = 0
      self.y_vel = 0
      self.mask = None
      self.direction = "left"
      self.animation_count = 0
      self.fall_count = 0

  def move(self, dx, dy):
    self.rect.x += dx
    self.rect.y += dy

  def move_left(self, vel):
    self.x_vel = -vel
    if self.direction != "left":
      self.direction = "left"
      self.animation_count = 0
  
  def move_right(self, vel):
    self.x_vel = vel
    if self.direction != "right":
      self.direction = "right"
      self.animation_count = 0
  
  def loop(self, fps):
    self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY) # setting the gravity
    self.move(self.x_vel, self.y_vel)

    self.fall_count += 1

  def draw(self, win):
    pygame.draw.rect(win, self.COLOR, self.rect)

# Function to create the game background
def get_background(name):
  image = pygame.image.load(join("assets", "Background", name))
  _, _, width, height = image.get_rect()
  tiles = []

  for i in range(WIDTH // width + 1):
    for j in range(HEIGHT // height + 1):
      pos = (i * width, j * height)
      tiles.append(pos)
  
  return tiles, image

# Function to draw the background and player
def draw(window, background, bg_image, player):
  for tile in background:
    window.blit(bg_image, tuple(tile))

  player.draw(window)
  pygame.display.update()

# Function for player movement
def handle_move(player):
  # check the keys are being pressed on keyboard
  keys = pygame.key.get_pressed()

  # Move only when holding down the keys
  player.x_vel = 0
  if keys[pygame.K_LEFT]:
    player.move_left(PLAYER_VEL)
  if keys[pygame.K_RIGHT]:
    player.move_right(PLAYER_VEL)

# Main function - what we run to start the game
def main(window):
  clock = pygame.time.Clock()
  background, bg_image = get_background("Green.png")

  player = Player(100, 100, 50, 50)

  # regulate the frame rate across different devices
  run = True
  while run:
    clock.tick(FPS)

    for event in pygame.event.get():
      # allow player to quit the game
      if event.type == pygame.QUIT:
        run = False
        break
    
    player.loop(FPS)
    handle_move(player)
    draw(window, background, bg_image, player)

  pygame.quit()
  quit()

if __name__ == "__main__":
  main(window)
