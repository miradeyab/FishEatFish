from cmath import inf
import pygame
import random
from enum import Enum

#initiaization logic
pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("Fish Eat Fish")

SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT = font = pygame.font.Font(pygame.font.get_default_font(), 12)

FPS = 60

SPAWN_PLAYER_SIZE = 10
VELOCITY = 1

class Player:
    def __init__(self, name, color, x, y, value, nextMove) -> None:
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.value = value
        self.nextMove = nextMove

class Fruit:
    def __init__(self, x, y, value) -> None:
        self.x = x
        self.y = y
        self.value = value

def draw_window(players, fruits):
    pygame.draw.rect(WIN, WHITE, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    for player in players:
        pygame.draw.circle(WIN, player.color, (player.x, player.y), player.value)
        playerSurface = pygame.font.Font.render(FONT, player.name, True, player.color)
        WIN.blit(playerSurface, (player.x + player.value, player.y + player.value))

    for fruit in fruits:
        pygame.draw.rect(WIN, BLACK, (fruit.x - fruit.value / 2, fruit.y - fruit.value / 2, fruit.value, fruit.value))

    pygame.display.update()

def movePlayers(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT) :
    for player in players :
        (up, down, left, right) = player.nextMove(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)

        if(up) :
            player.y -= VELOCITY

        if(down) :
            player.y += VELOCITY

        if(left) :
            player.x -= VELOCITY

        if(right) :
            player.x += VELOCITY

        player.x = min(SCREEN_WIDTH - player.value, max(player.value, player.x))
        player.y = min(SCREEN_HEIGHT - player.value, max(player.value, player.y))

def main():
    players = []
    fruits = []

    # generate random players for testing
    for i in range(1, 10):
        players.append(
            Player("player " + str(i),  
            pygame.Color(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)),
            random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), SPAWN_PLAYER_SIZE,
            lambda players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT : (bool(random.getrandbits(1)), False, False, bool(random.getrandbits(1)))
            )
        )

    for i in range(1, 15):
        fruits.append(
            Fruit(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(5, 10))
        )

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(players, fruits)
        
        movePlayers(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)

        '''
        calcuateFruitEats(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)
        calculatePlayersEats(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)
        '''

    pygame.quit()

if __name__ == "__main__":
    main()
