import pygame
import random
from os import path

# Creo los directorios para
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'Sound')

WIDTH = 480
HEIGHT = 600
FPS = 60
powerup_time = 5000

# Defino colores por comodidad
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

# Inicializo pygame y creo ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


#Defino mi fuente para el SCORE
font_name = pygame.font.match_font('Arial')
def draw_text (surf,text,size,x,y):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit  (text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar (surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LARGO = 100
    BAR_ALTO = 10
    fill = (pct / 100.0) * BAR_LARGO
    outline_rect = pygame.Rect( x, y, BAR_LARGO, BAR_ALTO)
    fill_rect = pygame.Rect(x,y,fill, BAR_ALTO)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect (surf,WHITE, outline_rect, 2)

def draw_lives (surf, x,y,lives,img):
    for i in range(lives):
        img_rect =  img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit (img, img_rect)

class Player(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(player_img,(50,38))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.radius = 20
                #pygame.draw.circle(self.image,RED,self.rect.center, self.radius)
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
                self.speedx = 0
                self.shield = 100
                self.shoot_delay = 250
                self.last_shot = pygame.time.get_ticks()
                self.lives = 3
                self.hidden = False
                self.hide_timer = pygame.time.get_ticks()
                self.power = 1
                self.power_time = pygame.time.get_ticks()

        def update(self):
                # Duracion powerup
                if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
                    self.power = 1
                    self.power_time = pygame.time.get_ticks()
                # Escondo la nave si muere
                if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
                    self.hidden = False
                    self.rect.centerx = WIDTH / 2
                    self.rect.bottom = HEIGHT - 10
                self.speedx = 0
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_LEFT]:
                        self.speedx = -5
                if keystate[pygame.K_RIGHT]:
                        self.speedx = 5
                self.rect.x += self.speedx
                if self.rect.right > WIDTH:
                        self.rect.right = WIDTH
                if self.rect.left < 0:
                        self.rect.left = 0
                if keystate[pygame.K_SPACE]:
                    self.shoot()

        def powerup(self):
            if self.power == 1:
                self.power +=1
                self.power_time = pygame.time.get_ticks()
            else:
                self.power_time = pygame.time.get_ticks() + 5000
            



        def shoot(self):
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    if self.power == 1:
                        bullet = Bullet(self.rect.centerx, self.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        shoot_sound.play()
                    if self.power == 2:
                        bullet1 = Bullet(self.rect.left, self.rect.centery)
                        bullet2 = Bullet(self.rect.right, self.rect.centery)
                        all_sprites.add(bullet1)
                        all_sprites.add(bullet2)
                        bullets.add(bullet1)
                        bullets.add(bullet2)
                        shoot_sound.play()

        def hide(self):
            # Escondo la imagen del jugador mientras explota al perder una vida
            self.hidden = True
            self.hide_timer = pygame.time.get_ticks()
            self.rect.center = (WIDTH / 2, HEIGHT + 100)    

class Mob (pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image_orig = random.choice(meteor_images)
                self.image_orig.set_colorkey(BLACK)
                self.image = self.image_orig.copy()
                self.rect = self.image.get_rect()
                self.radius = int (self.rect.width *0.4)
                self.rect.x = random.randrange (WIDTH - self.rect.width)
                self.rect.y = random.randrange (-150, -100)
                self.speedy = random.randrange (1,8)
                self.speedx = random.randrange (-3,3)
                self.rot = 0
                self.rot_speed = random.randrange(-8, 8)
                self.last_update = pygame.time.get_ticks()

        def rotate(self):
                now = pygame.time.get_ticks()
                if now - self.last_update >50:
                        self.last_update = now
                        self.rot = (self.rot + self.rot_speed) % 360
                        new_image = pygame.transform.rotate(self.image_orig,self.rot)
                        old_center = self.rect.center
                        self.image = new_image
                        self.rect = self.image.get_rect()
                        self.rect.center = old_center

        def update(self):
                self.rotate()
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.top > HEIGHT + 10 or self.rect.left <-15 or self.rect.right > WIDTH +20:
                        self.rect.x = random.randrange (WIDTH - self.rect.width)
                        self.rect.y = random.randrange (-100, -40)
                        self.speedy = random.randrange (1,8)


class Bullet (pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_img
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -10

        def update(self):
                self.rect.y += self.speedy
                # kill it if it moves off the top of the screen
                if self.rect.bottom<0:
                        self.kill()

class Pow (pygame.sprite.Sprite):
        def __init__(self, center):
                pygame.sprite.Sprite.__init__(self)
                self.type = random.choice(['shield', 'gun'])
                self.image = powerup_images[self.type]
                if self.type == 'gun':
                    self.image.set_colorkey(BLACK)
                else:
                    self.image.set_colorkey(WHITE)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.speedy = 3

        def update(self):
                self.rect.y += self.speedy
                # kill it if it moves off the top of the screen
                if self.rect.top > HEIGHT:
                        self.kill()


class Explosion (pygame.sprite.Sprite):
    def __init__ (self,center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75


    def update (self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim [self.size][self.frame]
                self.rectr = self.image.get_rect()
                self.rect.center = center


# Cargo los graficos del juego
background = pygame.image.load(path.join(img_dir,"purple.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
vida_img = pygame.image.load (path.join (img_dir, "Vida.png")).convert()
vida_img_mini = pygame.transform.scale (vida_img, (25,19))
vida_img_mini.set_colorkey(WHITE)
corona_img = pygame.image.load(path.join(img_dir, 'PowerUp2.png')).convert()
meteor_images = []
meteor_list =['meteorBrown_med1.png','Meteo2.png','Meteo3.png','Meteo4.png']
for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75 , 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load (path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)

    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.transform.scale (corona_img, (40,60))
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'PowerUp1.png')).convert()

# Cargo los sonidos del juego
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Disparo_copado.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion_copada.wav'))
muerte_sound = pygame.mixer.Sound(path.join(snd_dir, 'Muerte.wav'))
shield_sound = pygame.mixer.Sound (path.join(snd_dir, 'Power1.wav'))
power_sound = pygame.mixer.Sound (path.join(snd_dir, 'Power2.wav'))
pygame.mixer.music.load (path.join(snd_dir,'Musica.mp3'))
pygame.mixer.music.set_volume(0.4)



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range (8):
        newmob()
score = 0

pygame.mixer.music.play(-1)
contador_muertes = 0
# Loop de juego
running = True
while running:
    # Mantengo el juego a una velocidad
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
      
    # Update
    all_sprites.update()
    # Ver si la bala rompe el meteorito
    hits = pygame.sprite.groupcollide(mobs,bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() >0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # Veo si la nave agarra un powerup
    hits = pygame.sprite.spritecollide (player,powerups,True)
    for hit in hits: 
        if hit.type == 'shield':
            player.shield += random.randrange(10,25)
            shield_sound.play()
            if player.shield >=100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()

    # Veo si el meteorito golpea la nave
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius
        newmob()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            muerte_sound.play()
            if player.lives != 0:
                player.shield = 100
            

    if player.lives == 0 and not death_explosion.alive() :
        running =  False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text (screen, str(score), 18, WIDTH /2, 10)
    draw_shield_bar (screen, 5,5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, vida_img_mini)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()