import math
import pygame
import random
from enum import Enum
import copy

#initiaization logic
pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("Fish Eat Fish")

SCREEN_WIDTH = 1280 #info.current_w
SCREEN_HEIGHT = 720 #info.current_h 

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT = font = pygame.font.Font(pygame.font.get_default_font(), 12)

FPS = 60

SPAWN_PLAYER_SIZE = 10
VELOCITY = 1

NUMBER_OF_FRUITS = 10
MIN_FRUIT_SIZE = 5
MAX_FRUIT_SIZE = 15

class Object :
    def distance(self, x, y) :
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


class Player(Object):
    def __init__(self, name, color, x, y, value, nextMove) -> None:
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.value = value
        self.nextMove = nextMove

class Fruit(Object):
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
        otherPlayers = players.copy()
        otherPlayers.remove(player)

        (up, down, left, right) = player.nextMove(copy.deepcopy(player), otherPlayers, copy.deepcopy(fruits), SCREEN_WIDTH, SCREEN_HEIGHT)

        player.y -= VELOCITY if up else 0   
        player.y += VELOCITY if down else 0
        player.x -= VELOCITY if left else 0 
        player.x += VELOCITY if right else 0

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

def miraStrategy(you, players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT) :
  
    DANGER_DISTANCE = SCREEN_WIDTH / 8

    x = you.x
    y = you.y
    r = you.value

    enemy = players[0]
    enemyX = players[0].x
    enemyY = players[0].y
    enemyR = players[0].value
    
    bestFruit = None
    minD = math.inf

    for fruit in fruits:
        d = fruit.distance(x, y)

        if d < minD:
            minD = d
            bestFruit = fruit

            pass

    if r <= enemyR:
        if enemy.distance(x, y) <= DANGER_DISTANCE:
            return awayFrom(x, y, enemyX, enemyY)
        else:
            return towards(x, y, bestFruit.x, bestFruit.y)
    else:
        return towards(x, y, enemyX, enemyY)

def defaulStrategy(you, players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT) :
    predators = []
    preys = []

    for player in players :
        if(player.value > you.value) :
            predators.append(player)
        else : 
            if (player.value < you.value) :
                preys.append(player)

    for fruit in fruits :
        preys.append(fruit)

    return strategy(you, predators, preys, SCREEN_WIDTH, SCREEN_HEIGHT)


def towards(x, y, distX, distY) :
    return (distY < y, distY > y, distX < x, distX > x)

def awayFrom(x, y, distX, distY) :
    (up, down, left, right) = towards(x, y, distX, distY)
    return (not up, not down, not left, not right)

def mohamedStrategy(me, players, fruits, W, H) :
    x = me.x
    y = me.y
    r = me.value

    enemey = players[0]
    X = players[0].x
    Y = players[0].y
    R = players[0].value

    GREAT_RADIUS = min(W, H) / 2

    bestFruitValue = - math.inf
    bestFruit = None 

    biggestFruitSize = - math.inf

    for f in fruits :
        if f.value > biggestFruitSize :
            biggestFruitSize = f.value

    for f in fruits :
        fruitValue = (1 -  (me.distance(f.x, f.y) / GREAT_RADIUS)) * (f.value / biggestFruitSize)
        
        if fruitValue > bestFruitValue :
            bestFruitValue = fruitValue
            bestFruit = f

    if r > R :
        # attack
        preyValue = (me.distance(X, Y) / GREAT_RADIUS) * (R / biggestFruitSize)

        if bestFruitValue > preyValue :
            return towards(x, y, bestFruit.x, bestFruit.y)
        else :
            return towards(x, y, bestFruit.x, bestFruit.y)
    else :
        danger = (me.distance(X, Y) / GREAT_RADIUS)

        if bestFruitValue > danger :
            return towards(x, y, bestFruit.x, bestFruit.y)
        else :
            return awayFrom(x, y, X, Y)


def strategy(you, predators, preys, W, H) :
    x = you.x
    y = you.y
    value = you.value

    min = math.inf
    closestPredator = None

    for predator in predators :
        if predator.distance(x, y) < min :
            min = predator.distance(x, y)
            closestPredator = predator
    
    if closestPredator == None :
        min = math.inf
        closestPrey = None

        for prey in preys :
            if(prey.distance(x, y) < min) :
                min = prey.distance(x, y)
                closestPrey = prey

        if(closestPrey == None) :
            return (False, False, False, False)

        return (closestPrey.y < y, closestPrey.y > y, closestPrey.x < x, closestPrey.x > x)
    else :
        max = - math.inf
        furthestPrey = None

        for prey in preys :
            Ax = closestPredator.x - x
            Ay = closestPredator.y - y
            Bx = prey.x - x
            By = prey.y - y


            theta = math.acos(((Ax * Bx) + (Ay * By)) / (math.sqrt(Ax ** 2 + Ay ** 2) * math.sqrt(Bx ** 2 + By ** 2)))

            if(theta > max) :
                max = theta
                furthestPrey = prey

        if(furthestPrey != None) :
            return (furthestPrey.y < y, furthestPrey.y > y, furthestPrey.x < x, furthestPrey.x > x)
        else :
            return (closestPredator.y > y, closestPredator.y < y, closestPredator.x > x, closestPredator.x < x)

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

    players.append(
        Player(
            "Mira",  
            pygame.Color(204, 0, 204),
            random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 
            SPAWN_PLAYER_SIZE,
            miraStrategy
        )
    )

    players.append(
        Player(
            "Mohamed",  
            pygame.Color(51, 51, 255),
            random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 
            SPAWN_PLAYER_SIZE,
            defaulStrategy
        )
    )

    for i in range(1, NUMBER_OF_FRUITS):
        fruits.append(
            Fruit(
                random.randint(0, SCREEN_WIDTH), 
                random.randint(0, SCREEN_HEIGHT), 
                random.randint(MIN_FRUIT_SIZE, MAX_FRUIT_SIZE)
            )
        )

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if(len(players) <= 1) :
            break;

        movePlayers(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)
        calculatePlayersEats(players)
        calcuateFruitEats(players, fruits, SCREEN_WIDTH, SCREEN_HEIGHT)

        while (len(fruits) < NUMBER_OF_FRUITS) :
            fruits.append(
                Fruit(
                    random.randint(0, SCREEN_WIDTH), 
                    random.randint(0, SCREEN_HEIGHT), 
                    random.randint(MIN_FRUIT_SIZE, MAX_FRUIT_SIZE)
                )
            )

        draw_window(players, fruits)

    pygame.quit()

if __name__ == "__main__":
    main()
