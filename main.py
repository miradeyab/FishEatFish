import math
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

def calcuateFruitEats(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT):
    for fruit in fruits :
        for player in players :
            if(isPlayerTouchingFruit((fruit.x - fruit.value / 2, fruit.y - fruit.value / 2), (fruit.value, fruit.value), (player.x, player.y), player.value)) : 
                player.value =  math.sqrt(player.value ** 2 + fruit.value ** 2 / math.pi)
                fruits.remove(fruit)
                break


def isPlayerTouchingFruit(rect_tl, rect_size, circle_cpt, circle_rad):
    rect = pygame.Rect(*rect_tl, *rect_size)
    if rect.collidepoint(*circle_cpt):
        return True

    centerPt = pygame.math.Vector2(*circle_cpt)
    cornerPts = [rect.bottomleft, rect.bottomright, rect.topleft, rect.topright]
    if [p for p in cornerPts if pygame.math.Vector2(*p).distance_to(centerPt) <= circle_rad]:
        return True

    return False

def isPlayerTouchingPlayer(p1, p2) :
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2).real <= (p1.value + p2.value)

def calculatePlayersEats(players) :
    for p1 in players :
        for p2 in players :
            if p1 != p2 :
                if isPlayerTouchingPlayer(p1, p2) :
                    if(
                        p1.value > p2.value 
                        or
                        (p1.value == p2.value and bool(random.getrandbits(1)))
                    ) :
                        p1.value = math.sqrt(p1.value ** 2 + p2.value ** 2)
                        players.remove(p2)
                        continue

def main():
    players = []
    fruits = []

    # generate random players for testing
    for i in range(1, 10):
        players.append(
            Player("player " + str(i),  
            pygame.Color(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)),
            random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 
            #SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
            random.randint(5, 15), #SPAWN_PLAYER_SIZE,
            lambda players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT : (False, bool(random.getrandbits(1)), False, bool(random.getrandbits(1)))
            )
        )

    for i in range(1, 30):
        fruits.append(
            Fruit(
                random.randint(SCREEN_WIDTH / 2, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT / 2, SCREEN_HEIGHT), 
                random.randint(5, 10)
            )
        )

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
       
        movePlayers(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)
        calculatePlayersEats(players)
        calcuateFruitEats(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)

        draw_window(players, fruits)

    pygame.quit()

if __name__ == "__main__":
    main()
