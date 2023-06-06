from time import sleep
import pygame 

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.init() 

 
bg = pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)


s = pygame.mixer.Sound("catch.wav")
s_win = pygame.mixer.Sound("sound_win.wav")
s_game_over = pygame.mixer.Sound("sound_game_over.wav")

back = (0, 0, 0) 
mw = pygame.display.set_mode((900, 700)) 
clock = pygame.time.Clock() 
dx = 3 
dy = 3 
score = 0
 
platform_x = 200 
platform_y = 550 
move_right = False 
move_left = False 
move_up = False
move_down = False
game_over = False 
 
 
class Area(): 
  def __init__(self, x=0, y=0, width=10, height=10, color=None): 
      self.rect = pygame.Rect(x, y, width, height) 
      self.fill_color = back 
      if color: 
          self.fill_color = color 
  def color(self, new_color): 
      self.fill_color = new_color 
  def fill(self): 
      pygame.draw.rect(mw, self.fill_color, self.rect) 
  def collidepoint(self, x, y): 
      return self.rect.collidepoint(x, y)       
  def colliderect(self, rect): 
      return self.rect.colliderect(rect)
   
 
 
class Label(Area): 
  def set_text(self, text, fsize=12, text_color=(0, 0, 0)): 
      self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color) 
  def draw(self, shift_x=0, shift_y=0): 
      self.fill() 
      mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y)) 
 
 
class Picture(Area): 
  def __init__(self, filename, x=0, y=0, width=10, height=10): 
      Area.__init__(self, x=x, y=y, width=width, height=height, color=None) 
      self.image = pygame.image.load(filename) 
     
  def draw(self): 
      mw.blit(self.image, (self.rect.x, self.rect.y)) 

ball = Picture('ball-removebg-preview (1).png', 160, 350, 5, 5) 
platform = Picture('platform-removebg-preview (1).png', platform_x, platform_y, 240, 160) 
start_x = 30 
start_y = 50 
count = 9 
image = pygame.image.load('bg5.jpg')
 
monsters = [] 
for j in range(3): 
  y = start_y + (100 * j) 
  x = start_x 
  for i in range (count): 
      d = Picture('enemy-removebg-preview.png',x, y, 100, 100) 
      monsters.append(d) 
      x = x + 95 
 
 
while not game_over: 
  ball.fill()
  platform.fill()
  mw.blit(image, (0,0))
     
  for event in pygame.event.get(): 
      if event.type == pygame.QUIT: 
          game_over = True 
      if event.type == pygame.KEYDOWN: 
          if event.key == pygame.K_RIGHT: 
              move_right = True 
          if event.key == pygame.K_LEFT: 
              move_left = True
          if event.key == pygame.K_UP:
              move_up = True
          if event.key == pygame.K_DOWN:
              move_down = True
      elif event.type == pygame.KEYUP: 
          if event.key == pygame.K_RIGHT: 
              move_right = False 
          if event.key == pygame.K_LEFT: 
              move_left = False
          if event.key == pygame.K_UP:
              move_up = False
          if event.key == pygame.K_DOWN:
              move_down = False 
  

  time_text = Label(0,0,0,0,back) 
  time_text.set_text(f'SCORE:{score}/27',40, (200,100,0)) 
  time_text.draw(10, 10)

  if move_right: 
      platform.rect.x +=10 
  if move_left: 
      platform.rect.x -=10
  if move_up:
      platform.rect.y -= 3
  if move_down:
      platform.rect.y +=3 
  ball.rect.x += dx 
  ball.rect.y += dy 
  if  ball.rect.y < 0:
      s.play() 
      dy *= -1 
  if ball.rect.x > 850 or ball.rect.x < 0:
      s.play() 
      dx *= -1 
  if ball.rect.y > 650: 
      pygame.mixer.music.stop()
      s_game_over.play(0)
      time_text = Label(200,360,0,0,back) 
      time_text.set_text('YOU LOSE',100, (255,0,0)) 
      time_text.draw(10, 10)

   
  if len(monsters) == 0:
      dy = 0
      dx = 0     
      s_win.play()
      pygame.mixer.music.stop()
      time_text = Label(200,360,0,0,back) 
      time_text.set_text('YOU WIN',100, (0,200,0)) 
      time_text.draw(10, 10)
   
  if ball.rect.colliderect(platform.rect): 
      s.play()
      dy *= -1 
  for m in monsters: 
      m.draw() 
      #если монстра коснулся мяч, удаляем монстра из списка и меняем направления движения мяча 
      if m.rect.colliderect(ball.rect):
          score += 1 
          s.play() 
          monsters.remove(m) 
          m.fill() 
          dy *= -1.1
  platform.draw() 
  ball.draw() 

  pygame.display.update() 
  clock.tick(999999999)


