import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


myID, game_map = hlt.get_init()
hlt.send_init("Trent")

cardinals = [NORTH, EAST, SOUTH, WEST]

def random_direction():
    return random.randint(0,3)

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

def is_target_border(target):
    for dir in cardinals:
        n = game_map.get_target(target, dir)
        if n.owner != myID:
            return True
    return False

def direction_to_target(square: Square, target: Square):
    cart_x = target.x - square.x
    cart_y = target.y - square.y

    if cart_x == 0 and cart_y == 0:
        return STILL

    if cart_x == 0 and cart_y > 0:
        return SOUTH

    if cart_x == 0 and cart_y < 0:
        return NORTH

    if cart_x > 0 and cart_y == 0:
        return EAST

    if cart_x < 0 and cart_y == 0:
        return WEST

    # TODO: add case for when the square is at the edge

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

def move(square):
    # neighbors_smallest_neighbor_strength = []
    neighbors = [] 
    target = []

    for dir in range(4):
        n = game_map.get_target(square, dir)
        if n.owner != myID:
            neighbors.append(n)

    if len(neighbors) > 0:
        smallest = 999
        neighbor_with_smallest_neighbor_strength: Square = square
        for n in neighbors:
            small_neighbor = neighbor_smallest_neighbor_strength(n)
            if small_neighbor < smallest :
                smallest = small_neighbor
                neighbor_with_smallest_neighbor_strength = n

        # # neighbors.sort(key=lambda a: a.production, reverse=True)
        #
        # sort neighbors by their strength ascending and select first
        # neighbors.sort(key=lambda a: a.strength)
        # target = neighbors[0]

        target = neighbor_with_smallest_neighbor_strength
        
        # take neighbor if we have the strength
        if target.strength < square.strength:
            return Move(square, direction_to_target(square, target))
    else:
        if square.strength > square.production * 5:
            return Move(square, weakest_border(square))

    return Move(square, STILL)
    
while True:
    game_map.get_frame()
    moves = [move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
