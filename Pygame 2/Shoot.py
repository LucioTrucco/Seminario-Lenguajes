import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'Sound')

WIDTH = 480
HEIGHT = 600
FPS = 60

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

font_name = pygame.font.match_font('Arial')
def draw_text (surf,text,size,x,y):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit  (text_surface, text_rect)



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

        def update(self):
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

        def shoot(self):
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

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
                if self.rect.top > HEIGHT + 10 or self.rect.left <25 or self.rect.right > WIDTH +20:
                        self.rect.x = random.randrange (WIDTH - self.rect.width)
                        self.rect.y = random.randrange (-100, -40)
                        self.speedy = random.randrange (1,8)


class Bullet (pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(bullet_img,(8,15))
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

# Cargo los graficos del juego
background = pygame.image.load(path.join(img_dir,"purple.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list =['meteorBrown_med1.png','Meteo2.png','Meteo3.png','Meteo4.png']
for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

# Cargo los sonidos del juego
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Disparo_copado.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion_copada.wav'))
pygame.mixer.music.load (path.join(snd_dir,'Musica.mp3'))
pygame.mixer.music.set_volume(0.4)



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range (8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
score = 0

pygame.mixer.music.play(-1)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                        player.shoot()
    # Update
    all_sprites.update()
    # check to see if bullet hit mob
    hits = pygame.sprite.groupcollide(mobs,bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        explosion_sound.play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)


    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text (screen, str(score), 18, WIDTH /2, 10)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()