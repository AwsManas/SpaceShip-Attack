#lesson 1 - skeleton
import pygame
import random
import os
WIDTH = 400
HEIGHT = 600
FPS = 60
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
""" Initialise pygame and create window"""
pygame.init()
pygame.mixer.init() # initialise sound
screen= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shoot-em-up")
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"art(stolen)")
all_sprites= pygame.sprite.Group()
class battleship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load(os.path.join(img_folder,"battleship.jpg")).convert()
        self.image = pygame.Surface((30,40))
        #self.image.set_colorkey(white)
        self.image.fill(red)
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0
        self.speedy = 0 
    def update(self):    
        self.speedx = 0
        self.speedy = 0
        keyspressed = pygame.key.get_pressed()
        if keyspressed[pygame.K_LEFT]:
            self.speedx = -4
        if keyspressed[pygame.K_RIGHT]:
            self.speedx = 4
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1 
        if self.rect.left < 0:
            self.rect.left = 0    
        self.rect.x+=self.speedx
    def shoot(self):
        bullet = bullets(self.rect.centerx,self.rect.top)    
        all_sprites.add(bullet)
        Bull.add(bullet)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface((20,20))
       self.image.fill(black)
       self.rect = self.image.get_rect()
       self.rect.x = random.randrange(0,WIDTH-self.rect.width)
       self.rect.y = random.randrange(-140,-40)
       self.speedy = random.randrange(1,6)
       self.speedx = -2 + random.randrange(0,4)
    def update(self):
        self.rect.y+=self.speedy       
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +20 or self.rect.left < -20 or self.rect.right > WIDTH+20 :
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-140,-40)
            self.speedy = random.randrange(1,7)
mobs = pygame.sprite.Group()
Bull = pygame.sprite.Group()

class bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,8))
        self.image.fill((0,100,0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom<0:
            self.kill()            
ship = battleship()
for i in range(7):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)

#Game loop
all_sprites.add(ship)
running = True
while running:
    clock.tick(FPS)
    #Events

    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            running=False
        elif i.type==pygame.KEYDOWN:
            if i.key==pygame.K_SPACE:
                ship.shoot()

    all_sprites.update()
    # check  collision 
    hits = pygame.sprite.groupcollide(mobs,Bull,True,True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(ship,mobs, False)
    if hits : 
        running = False
    screen.fill(white)
    all_sprites.draw(screen)#Draw where?
    pygame.display.flip()
pygame.quit()