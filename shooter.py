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
Yellow=(255,255,0)
green = (0,255,0)
""" Initialise pygame and create window"""
pygame.init()
pygame.mixer.init() # initialise sound
screen= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("HueHue:)")
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"shooter-graphics")
song_folder = os.path.join(game_folder,"sounds")
all_sprites= pygame.sprite.Group()
# Loading all game graphics 
background = pygame.image.load(os.path.join(img_folder,"back.png")).convert()
background_rect=background.get_rect()
ship_img = pygame.image.load(os.path.join(img_folder,"ship.png")).convert()
ship_tag = pygame.transform.scale(ship_img,(15,15))
ship_tag.set_colorkey(black)
laser_img = pygame.image.load(os.path.join(img_folder,"ebullet1.png")).convert()
#mob_img = pygame.image.load(os.path.join(img_folder,"ast1.png")).convert()
asteroid_images = []
asteroid_list = ["ast1.png","ast2.png","ast3.png","ast4.png"]
for img in asteroid_list:
    asteroid_images.append(pygame.image.load(os.path.join(img_folder,img)).convert())
#Loading sounds 
shoot_sound = pygame.mixer.Sound(os.path.join(song_folder,"bf.wav"))
explo_sound = pygame.mixer.Sound(os.path.join(song_folder,'explosion.wav'))
background_sound = pygame.mixer.music.load(os.path.join(song_folder,'bck.wav'))    
pygame.mixer.music.set_volume(0.3)
player_die_sound = pygame.mixer.Sound(os.path.join(song_folder,'shipdes.ogg'))
explosion_anim = {} 
explosion_anim['lar']=[]
explosion_anim['sml']=[]
explosion_anim['player']=[]

for i in range(9):
    filename = 'regularExplosion0'+str(i)+'.png'
    img = pygame.image.load(os.path.join(img_folder,filename)).convert()
    img.set_colorkey(black)
    img_lr = pygame.transform.scale(img,(60,60))
    img_sm = pygame.transform.scale(img,(30,30))
    explosion_anim['lar'].append(img_lr)
    explosion_anim['sml'].append(img_sm)
    filename = 'sonicExplosion0'+str(i)+'.png'
    img = pygame.image.load(os.path.join(img_folder,filename)).convert()
    img.set_colorkey(black)
    img_tr = pygame.transform.scale(img,(100,100))
    explosion_anim['player'].append(img_tr)
class battleship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load(os.path.join(img_folder,"battleship.jpg")).convert()
        self.image = pygame.transform.scale( ship_img ,(60,60)) #pygame.Surface((30,40))
        self.image.set_colorkey(black)
        #self.image.fill(red)
        self.rect = self.image.get_rect() 
        self.radius = 29
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0
        self.speedy = 0 
        self.health = 100
        self.lives = 2
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
    def update(self):    
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000 :
            self.hidden = False
            self.rect.centerx =WIDTH/2
            self.rect.bottom = HEIGHT -10
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
        shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image_orig = pygame.transform.scale( random.choice(asteroid_images) ,(30,30))#pygame.Surface((20,20))
       self.image_orig.set_colorkey(black)
       self.image = self.image_orig.copy()
       #self.image.fill(black)
       self.rect = self.image.get_rect()
       self.radius = 15
       #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
       self.rect.x = random.randrange(0,WIDTH-self.rect.width)
       self.rot = 0
       self.rotspeed = random.randrange(-10,10)
       self.rect.y = random.randrange(-140,-40)
       self.speedy = random.randrange(1,6)
       self.speedx = -2 + random.randrange(0,4)
       self.last_update=pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            self.rot = (self.rot + self.rotspeed) % 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center # rotating by center 
    def update(self):
        self.rotate()
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
        self.image = pygame.transform.scale( laser_img ,(5,10))#pygame.Surface((5,8))
        #self.image.fill((0,100,0))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom<0:
            self.kill()            
class explo(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame+=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else :
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


ship = battleship()
for i in range(7):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)
points = 10
font_name = pygame.font.match_font('comic')
def draw_text(surfacee,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,Yellow)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surfacee.blit(text_surface,text_rect)
def draw_health(surface,x,y,health):
    if health < 0:
        health = 0
    height = 5
    lenght = WIDTH 
    fill = (health/100)* lenght
    outerrect = pygame.Rect(x,y,lenght,height)
    innerrect = pygame.Rect(x,y,fill,height)
    pygame.draw.rect(surface,red,outerrect)
    pygame.draw.rect(surface,green,innerrect)
def draw_lives(surface,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 20*i
        img_rect.y = y
        surface.blit(img,img_rect)

#Game loop
all_sprites.add(ship)
pygame.mixer.music.play(loops=-1)
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
                points-=1
                if points<1:
                    running=False

    all_sprites.update()
    # check  collision 
    hits = pygame.sprite.groupcollide(mobs,Bull,True,True)
    for hit in hits:
        points+=int(hit.speedy)
        explo_sound.play()
        expl = explo(hit.rect.center,'lar')
        all_sprites.add(expl)
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(ship,mobs,True,pygame.sprite.collide_circle)
    for hit in hits : 
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        ship.health -= int(abs(hit.speedx) + int(hit.speedy))*2
        if not ship.health < 1: 
            explo_sound.play()
            expl = explo(hit.rect.center,'sml')
            all_sprites.add(expl)
        if ship.health < 1 :
            player_die_sound.play()
            death_explo = explo(ship.rect.center,'player')
            all_sprites.add(death_explo)
            ship.hide()
            ship.lives-=1
            ship.health=100

    if ship.lives==0 and not death_explo.alive():
        running = False      
    screen.fill(white)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(points),20,WIDTH/2,20)
    draw_health(screen,0,HEIGHT-7,ship.health)
    draw_lives(screen,WIDTH-50,5,ship.lives,ship_tag)
    #Draw where?
    pygame.display.flip()
pygame.quit()
