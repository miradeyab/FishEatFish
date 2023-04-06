from cmath import inf
import pygame
import os
import time

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55
BULLET_WIDTH, BULLET_HEIGHT = 6, 6

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60

BORDER = pygame.Rect(int(SCREEN_WIDTH / 2)  - 5, 0, 10, SCREEN_HEIGHT)

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))

SPACE = pygame.transform.scale(SPACE_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)),
    90
)

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)),
    -90
)

VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BULLET_DELAY = 0.25

def draw_window(yellow_pos, red_pos, yellow_bullets, red_bullets):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, yellow_pos) 
    WIN.blit(RED_SPACESHIP, red_pos) 

    for rect in yellow_bullets:
        pygame.draw.rect(WIN, RED, rect)
    
    for rect in red_bullets:
        pygame.draw.rect(WIN, RED, rect)

    pygame.display.update()

def red_handle_movement(key_pressed, red) :
    if key_pressed[pygame.K_UP] :
        red.top -= VEL

    if key_pressed[pygame.K_DOWN]:
        red.top += VEL

    if key_pressed[pygame.K_LEFT]:
        red.left -= VEL

    if key_pressed[pygame.K_RIGHT]:
        red.left += VEL

def yellow_handle_movement(key_pressed, yellow) :
    if key_pressed[pygame.K_w]: #UP
        yellow.top -= VEL

    if key_pressed[pygame.K_s]: #DOWN
        yellow.top += VEL

    if key_pressed[pygame.K_a]: #LEFT
        yellow.left -= VEL

    if key_pressed[pygame.K_d]: #RIGHT
        yellow.left += VEL

def bounce(yellow, red):
    if yellow.left < 0:
        yellow.left = 0

    if yellow.top < 0:
        yellow.top = 0

    if yellow.top + SPACESHIP_HEIGHT  > SCREEN_HEIGHT:
        yellow.top = SCREEN_HEIGHT - SPACESHIP_HEIGHT

    if yellow.left + SPACESHIP_WIDTH > BORDER.left:
        yellow.left = BORDER.left - SPACESHIP_WIDTH


    if red.left < BORDER.left + BORDER.width:
        red.left = BORDER.left + BORDER.width

    if red.top < 0:
        red.top = 0

    if red.top + SPACESHIP_HEIGHT  > SCREEN_HEIGHT:
        red.top = SCREEN_HEIGHT - SPACESHIP_HEIGHT

    if red.left + SPACESHIP_WIDTH > SCREEN_WIDTH:
        red.left = SCREEN_WIDTH - SPACESHIP_WIDTH

def bullets_physics(yellow_bullets, red_bullets, yellow, red) :
    for bullet in yellow_bullets:
        bullet.left += BULLET_VEL
 
        if bullet.left > SCREEN_WIDTH:
            yellow_bullets.remove(bullet)
            continue

        if bullet.colliderect(red) :
            yellow_bullets.remove(bullet)
            continue

    for bullet in red_bullets:
        bullet.left -= BULLET_VEL

        if bullet.left + bullet.width < 0:
            red_bullets.remove(bullet)
            continue

        if bullet.colliderect(yellow):
            red_bullets.remove(bullet)
            continue

def delay_bullets(key_pressed, yellow, red, yellow_bullets, red_bullets, last_yellow_bullet_time, last_red_bullet_time):
    if key_pressed[pygame.K_RCTRL]:
        if time.time() - last_red_bullet_time > BULLET_DELAY : 
            red_bullets.append(pygame.Rect(red.left, red.top + int(SPACESHIP_HEIGHT / 2) - int(BULLET_HEIGHT / 2), BULLET_WIDTH, BULLET_HEIGHT))
            last_red_bullet_time = time.time()

    if key_pressed[pygame.K_f]:
        if time.time() - last_yellow_bullet_time > BULLET_DELAY :
            yellow_bullets.append(pygame.Rect(yellow.left + SPACESHIP_WIDTH, yellow.top + int(SPACESHIP_HEIGHT / 2) - int(BULLET_HEIGHT / 2), BULLET_WIDTH, BULLET_HEIGHT))
            last_yellow_bullet_time = time.time()
        
    return last_yellow_bullet_time, last_red_bullet_time

def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    last_yellow_bullet_time = -inf
    last_red_bullet_time = -inf

    clock = pygame.time.Clock()
    run = True
    
    pygame.display.set_caption("Space Shoot")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            #print(event)

            if event.type == pygame.QUIT:
                run = False

            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len (red_bullets) < MAX_BULLETS:
                    red_bullets.append(pygame.Rect(red.left, red.top + int(SPACESHIP_HEIGHT / 2) - int(BULLET_HEIGHT / 2), BULLET_WIDTH, BULLET_HEIGHT))
                
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    yellow_bullets.append(pygame.Rect(yellow.left + SPACESHIP_WIDTH, yellow.top + int(SPACESHIP_HEIGHT / 2) - int(BULLET_HEIGHT / 2), BULLET_WIDTH, BULLET_HEIGHT))
            '''
        key_pressed = pygame.key.get_pressed()

        red_handle_movement(key_pressed, red)
        yellow_handle_movement(key_pressed, yellow)
        bounce(yellow, red)

        last_yellow_bullet_time, last_red_bullet_time = delay_bullets(key_pressed, yellow, red, yellow_bullets, red_bullets, last_yellow_bullet_time, last_red_bullet_time)
        bullets_physics(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(yellow, red, yellow_bullets, red_bullets)

    pygame.quit()

if __name__ == "__main__":
    main()
