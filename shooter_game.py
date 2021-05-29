from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self,image_player,x_player, y_player,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(image_player),(65,65))
        self.speed = player_speed
        self.rect  = self.image.get_rect()
        self.rect.x= x_player 
        self.rect.y= y_player

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, -2)
        bullets.add(bullet)

global lost
lost = 0

class Enemy(GameSprite):
    def update (self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 100)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        
win_width = 700
win_height = 500
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 100)

player = Player("rocket.png", 350, 430, 5)

UFOS = sprite.Group()
for i in range(1,6):
    UFO = Enemy("ufo.png", randint(50,win_width - 50), 0, 1)
    UFOS.add(UFO)

asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Enemy("asteroid.jpg", randint(50,win_width - 50), 0, 1)
    asteroids.add(asteroid)

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (700,500))

mixer.init()
mixer.music.load("Jasmin.mp3")
mixer.music.play()
bullet_sound = mixer.Sound("fire.ogg") 

clock = time.Clock()
FPS = 60
clock.tick(FPS)

game = True
finished = False
hits = 0
while game:

    for e in event.get():
        keys_pressed = key.get_pressed()
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet_sound.play()
                player.fire()


    if finished != True:
        window.blit(background, (0,0))

        player.update()
        UFOS.update()
        bullets.update()
        asteroids.update()

        bullets.draw(window)
        player.reset()
        UFOS.draw(window)
        asteroids.draw(window)

        sprites_list1 = sprite.groupcollide(UFOS, bullets, True, True)
        sprite_list2 = sprite.spritecollide(player, UFOS, False)
        sprite_list3 = sprite.spritecollide(player, asteroids, False)
        sprites_list4 = sprite.groupcollide(asteroids, bullets, True, True)
        
        for spr in sprites_list1:
            hits = hits + 1
            UFO = Enemy("ufo.png", randint(50,win_width - 50), 0, 1)
            UFOS.add(UFO)

        for spr in sprites_list4:
            asteroid = Enemy("asteroid.jpg", randint(50,win_width - 50), 0, 1)
            asteroids.add(asteroid)

        text_missed = font1.render("Missed: " + str(lost) ,1,(255,255,255))
        text_win = font2.render("YOU WIN!", 1 ,(0,177,0))
        text_lose = font2.render("YOU LOSE!", 1, (255,0,0))
        text_score = font1.render("Score: " + str(hits), 1,(255,255,255))
        
        window.blit(text_score, (50,100))
        window.blit(text_missed, (50,50))
        
        if hits >= 20:
            window.blit(text_win, (250,100))
            finished = True
        if lost >= 20:
            window.blit(text_lose, (250, 100))
            finished = True
        
        if len(sprite_list2) > 0 or len(sprite_list3) > 0:
            window.blit(text_lose, (250, 100))
            finished = True

        
            

    display.update()
