import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

# Initialize the pygame module
pygame.init()
pygame.font.init()

# setting the caption at the top of the window
pygame.display.set_caption("MW Ninja Frog")

# List of global variables
WIDTH, HEIGHT = 1000, 600
FPS = 60 # frame per second
PLAYER_VEL = 5 # player velocity moving around the screen
PLAYER_LIFE = pygame.font.SysFont('comicsans', 40)
ENDGAME = pygame.font.SysFont('comicsans', 40)
window = pygame.display.set_mode((WIDTH, HEIGHT))

# flip the png from facing right to left
def flip(sprites):
  return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
  path = join("assets", dir1, dir2)
  images = [f for f in listdir(path) if isfile(join(path, f))]

  all_sprites = {}

  for image in images:
    sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

    sprites = []
    for i in range(sprite_sheet.get_width() // width):
      surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
      rect = pygame.Rect(i * width, 0, width, height)
      surface.blit(sprite_sheet, (0, 0), rect)
      sprites.append(pygame.transform.scale2x(surface))
    
    if direction:
      all_sprites[image.replace(".png", "") + "_right"] = sprites
      all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
    else:
      all_sprites[image.replace(".png", "")] = sprites
  
  return all_sprites

def get_block(size):
  path = join("assets", "Terrain", "Terrain.png")
  image = pygame.image.load(path).convert_alpha()
  surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
  rect = pygame.Rect(96, 0, size, size)
  surface.blit(image, (0, 0), rect)
  return pygame.transform.scale2x(surface)

def get_orange_block(size):
  path = join("assets", "Terrain", "Terrain.png")
  image = pygame.image.load(path).convert_alpha()
  surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
  rect = pygame.Rect(96, 64, size, size)
  surface.blit(image, (0, 0), rect)
  return pygame.transform.scale2x(surface)

# Player info and movement
class Player(pygame.sprite.Sprite):
  COLOR = (255, 0, 0)
  GRAVITY = 1
  SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
  ANIMATION_DELAY = 5

  def __init__(self, x, y, width, height):
      super().__init__()
      self.rect = pygame.Rect(x, y, width, height)
      self.x_vel = 0
      self.y_vel = 0
      self.mask = None
      self.direction = "right"
      self.animation_count = 0
      self.fall_count = 0
      self.jump_count = 0
      self.hit = False
      self.hit_count = 0

  def jump(self):
    self.y_vel = -self.GRAVITY * 8
    self.animation_count = 0
    self.jump_count += 1
    if self.jump_count == 1:
      self.fall_count = 0

  def move(self, dx, dy):
    self.rect.x += dx
    self.rect.y += dy

  def make_hit(self):
    self.hit = True
    self.hit_count = 0

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
    if self.hit:
      self.hit_count += 1
    if self.hit_count > fps:
      self.hit = False
      self.hit_count = 0
    self.update_sprite()

  def landed(self):
    self.fall_count = 0
    self.y_vel = 0
    self.jump_count = 0

  def hit_head(self):
    self.count = 0
    self.y_vel *= -1

  def update_sprite(self):
    sprite_sheet = "idle"
    if self.hit:
      sprite_sheet = "hit"
    if self.x_vel != 0:
      sprite_sheet = "run"
    if self.y_vel < 0:
      if self.jump_count == 1:
        sprite_sheet = "jump"
      elif self.jump_count == 2:
        sprite_sheet = "double_jump"
    if self.y_vel > self.GRAVITY * 2:
      sprite_sheet = "fall"
    
    sprite_sheet_name = sprite_sheet + "_" + self.direction
    sprites = self.SPRITES[sprite_sheet_name]
    sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
    self.sprite = sprites[sprite_index]
    self.animation_count += 1
    self.update()

  def update(self):
    self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
    self.mask = pygame.mask.from_surface(self.sprite)

  def draw(self, win, offset_x):
    win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height, name=None):
    super().__init__()
    self.rect = pygame.Rect(x, y, width, height)
    self.image = pygame.Surface((width, height), pygame.SRCALPHA)
    self.width = width
    self.height = height
    self.name = name

  def draw(self, win, offset_x):
    win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
  def __init__(self, x, y, size):
    super().__init__(x, y, size, size)
    block = get_block(size)
    self.image.blit(block, (0, 0))
    self.mask = pygame.mask.from_surface(self.image)

class OrangeBlock(Object):
  def __init__(self, x, y, size):
    super().__init__(x, y, size, size)
    block = get_orange_block(size)
    self.image.blit(block, (0, 0))
    self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
  ANIMATION_DELAY = 3

  def __init__(self, x, y, width, height):
    super().__init__(x, y, width, height, "fire")
    self.fire = load_sprite_sheets("Traps", "Fire", width, height)
    self.image = self.fire["off"][0]
    self.mask = pygame.mask.from_surface(self.image)
    self.animation_count = 0
    self.animation_name = "off"
  
  def on(self):
    self.animation_name = "on"

  def off(self):
    self.animation_name = "off"

  def loop(self):
    sprites = self.fire[self.animation_name]
    sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
    self.image = sprites[sprite_index]
    self.animation_count += 1

    self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
    self.mask = pygame.mask.from_surface(self.image)

    if self.animation_count // self.ANIMATION_DELAY > len(sprites):
      self.animation_count = 0

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
def draw(window, background, bg_image, player, objects, offset_x, player_life):
  for tile in background:
    window.blit(bg_image, tuple(tile))

  for obj in objects:
    obj.draw(window, offset_x)

  player_life_text = PLAYER_LIFE.render("Your life: " + str(player_life), 1, (0, 0, 0))
  window.blit(player_life_text, (10, 10))
  player.draw(window, offset_x)
  pygame.display.update()

def draw_endgame(text):
  endgame_text = ENDGAME.render(str(text), 1, (255, 0, 0))
  window.blit(endgame_text, (WIDTH / 2 - endgame_text.get_width() / 2, HEIGHT / 2 - endgame_text.get_height() / 2))
  pygame.display.update()
  pygame.time.delay(2000)

def handle_vertical_collision(player, objects, dy):
  collided_objects = []
  for obj in objects:
    if pygame.sprite.collide_mask(player, obj):
      if dy > 0:
        player.rect.bottom = obj.rect.top
        player.landed()
      elif dy < 0:
        player.rect.top = obj.rect.bottom
        player.hit_head()
      collided_objects.append(obj)
  return collided_objects

def collide(player, objects, dx):
  player.move(dx, 0)
  player.update()
  collided_object = None
  for obj in objects:
    if pygame.sprite.collide_mask(player, obj):
      collided_object = obj
      break
  player.move(-dx, 0)
  player.update()
  return collided_object


# Function for player movement
def handle_move(player, objects):
  # check the keys are being pressed on keyboard
  keys = pygame.key.get_pressed()

  # Move only when holding down the keys
  player.x_vel = 0
  collide_left = collide(player, objects, -PLAYER_VEL * 2)
  collide_right =  collide(player, objects, PLAYER_VEL * 2)
  if keys[pygame.K_LEFT] and not collide_left:
    player.move_left(PLAYER_VEL)
  if keys[pygame.K_RIGHT] and not collide_right:
    player.move_right(PLAYER_VEL)
  
  

  vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
  to_check = [collide_left, collide_right, *vertical_collide]
  for obj in to_check:
    if obj and obj.name == "fire":
      player.make_hit()

# Main function - what we run to start the game
def main(window):
  clock = pygame.time.Clock()
  background, bg_image = get_background("Green.png")
  block_size = 96
  player = Player(100, 100, 50, 50)
  fire = Fire(block_size / 3, HEIGHT - block_size * 5 - 64, 16, 32)
  fire.on()
  fire_2 = Fire(block_size * 8 + block_size / 3, HEIGHT - block_size * 4 - 64, 16, 32)
  fire_2.on()
  floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-2, 13)]
  floor_2 = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(20, 30)]
  wall = [Block(0, HEIGHT - block_size * i, block_size) for i in range(2, 6)]
  wall_2 = [Block(block_size, HEIGHT - block_size * i, block_size) for i in range(2, 4)]
  wall_3 = [Block(block_size * 2, HEIGHT - block_size * i, block_size) for i in range(2, 4)]
  wall_4 = Block(block_size * 3, HEIGHT - block_size * 2, block_size)
  obs = [Block(block_size * i, HEIGHT - block_size * 2, block_size) for i in range (7, 10)]
  obs_2 = [Block(block_size * i + block_size / 2, HEIGHT - block_size * 3, block_size) for i in range (7, 9)]
  obs_3 = Block(block_size * 8, HEIGHT - block_size * 4, block_size)
  float = [OrangeBlock(block_size * i,  HEIGHT - block_size * 4, block_size) for i in range (4, 6)]
  float_2 = [OrangeBlock(block_size * i,  HEIGHT - block_size * 1.5, block_size) for i in range (14, 16)]
  float_3 = [OrangeBlock(block_size * i,  HEIGHT - block_size * 2.75, block_size) for i in range (16, 18)]
  float_4 = [OrangeBlock(block_size * i,  HEIGHT - block_size * 4.5, block_size) for i in range (18, 20)]
  objects =[*floor, *floor_2, fire, fire_2, *wall, *wall_2, *wall_3, wall_4, *obs, *obs_2, obs_3, *float, *float_2, *float_3, *float_4]
  offset_x = 0
  scroll_area_width = 200
  player_life = 50
  endgame_text = ""

  # regulate the frame rate across different devices
  run = True
  while run:
    clock.tick(FPS)

    for event in pygame.event.get():
      # allow player to quit the game
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and player.jump_count < 2:
          player.jump()
    
    player.loop(FPS)
    fire.loop()
    fire_2.loop()
    handle_move(player, objects)

    # restart the game after falling down
    if player.rect.bottom > HEIGHT + block_size:
      endgame_text = "You died!"
      draw_endgame(endgame_text)
      break
    
    if player.hit == True and player.hit_count == 0:
      player_life -= 1

    if player_life <= 0:
      endgame_text = "You died!"
      draw_endgame(endgame_text)
      break

    draw(window, background, bg_image, player, objects, offset_x, player_life)
    if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel >= 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
      offset_x += player.x_vel


  main(window)

if __name__ == "__main__":
  main(window)
