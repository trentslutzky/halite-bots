import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


myID, game_map = hlt.get_init()
hlt.send_init("Trent")

cardinals = [NORTH, EAST, SOUTH, WEST]

# -------------------------------------#

def random_direction():
    return random.randint(0,3)

# -------------------------------------#

def nearest_border(square):
    direction = STILL
    maxDistance = 30

    for dir in cardinals:
        distance = 0
        current = square
        target = game_map.get_target(current, dir)

        while (target.owner == myID and distance < maxDistance):
            distance = distance + 1
            current = game_map.get_target(current, dir)
            target = game_map.get_target(current, STILL)

        if (distance < maxDistance):
            direction = dir
            maxDistance = distance

    return direction

# -------------------------------------#

def nearest_enemy_border(square):
    direction = STILL
    maxDistance = 30

    for dir in cardinals:
        distance = 0
        current = square
        target = game_map.get_target(current, dir)
    
        while (target.owner == myID and distance < maxDistance):
            distance = distance + 1
            current = game_map.get_target(current, dir)
            target = game_map.get_target(current, STILL)
    
        if (distance < maxDistance):
            direction = dir
            maxDistance = distance

    return direction

# -------------------------------------#

def weakest_border(square):
    direction = STILL
    maxDistance = 30
    min_strength = 999

    for dir in cardinals:
        current = square
        distance = 0

        target = game_map.get_target(current, dir)
        while (target.owner == myID and distance < maxDistance):
            distance = distance + 1
            current = game_map.get_target(current, dir)
            target = game_map.get_target(current, STILL)

        if(target.strength < min_strength):
            min_strength = target.strength
            direction = dir

    return direction

# -------------------------------------#

def is_target_border(target):
    for dir in cardinals:
        n = game_map.get_target(target, dir)
        if n.owner != myID:
            return True
    return False

# -------------------------------------#

def weakest_neighbor(square, include_self=False):
    weakest_strength = 999
    weakest = square
    for dir in cardinals:
        n: Square = game_map.get_target(square, dir)
        if(include_self == False and n.owner == myID):
            continue
        if n.strength < weakest_strength:
            weakest_strength = n.strength
            weakest = n
    return weakest

# -------------------------------------#

def heuristic(square):
    return square.strength
    return square.production / square.strength if square.strength else square.production

def ideal_neighbor(square):
    best_rating = 999
    best = square
    for dir in cardinals:
        target = game_map.get_target(square, dir)
        if target.owner == myID:
            continue
        rating = heuristic(target)
        if rating < best_rating:
            best_rating = rating
            best = target
    return best

# -------------------------------------#

def direction_to_target(square: Square, target: Square):
    cart_x = target.x - square.x
    cart_y = target.y - square.y

    if cart_x == 0 and cart_y == 0:
        return STILL

    if cart_x == 0 and cart_y > 0:
        if abs(cart_y) > 1:
            return NORTH
        return SOUTH

    if cart_x == 0 and cart_y < 0:
        if abs(cart_y) > 1:
            return SOUTH
        return NORTH

    if cart_x > 0 and cart_y == 0:
        if abs(cart_x) > 1:
            return WEST
        return EAST

    if cart_x < 0 and cart_y == 0:
        if abs(cart_x) > 1:
            return EAST
        return WEST

# -------------------------------------#

def neighbor_smallest_neighbor_strength(target: Square) -> int:
    neighbors = [] 
    for dir in range(4):
        n = game_map.get_target(target, dir)
        if n.owner != myID:
            neighbors.append(n)
    if len(neighbors) > 0:
        neighbors.sort(key=lambda a: a.strength)
    else:
        return -1
    return neighbors[0].strength

# -------------------------------------#

def border_move(square):
    target = ideal_neighbor(square)
    if(target.strength < square.strength):
        return Move(square, direction_to_target(square, target))
    return Move(square, STILL)

# -------------------------------------#

def inside_move(square):
    if square.strength > square.production * 5:
        return Move(square, nearest_enemy_border(square))
    return Move(square, STILL)

# -------------------------------------#

def move(square):
    border = False
    for dir in range(4):
        n = game_map.get_target(square, dir)
        if n.owner != myID:
            border = True

    return border_move(square) if border else inside_move(square)
    
while True:
    game_map.get_frame()
    moves = [move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
