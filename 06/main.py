#!/usr/bin/env python3

import argparse
import icu
import os
import re
import socket
import sys


# We consider the following axis:
# y
# ^
# |
# |
# +--------> x
# Princess is at (1, 0)
# We start at (0, 0)


# A certain position on the map (or ∆positions)
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d %d)" % (self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Position):
            return TypeError
        return (self.x == other.x) and (self.y == other.y)

    def distance_to(self, pos):
        xdiff = abs(self.x - pos.x)
        ydiff = abs(self.y - pos.y)
        return max(xdiff, ydiff)


class Displacement(Position):
    def __init(self, x, y):
        super().__init__(x, y)


# A knight move
class Move:
    def __init__(self, displacement):
        self.displacement = displacement

    def __str__(self):
        return "%s" % (self.command())

    def apply(self, position):
        return Position(position.x + self.displacement.x, position.y + self.displacement.y)

    def getTile(self, tiles):
        return tiles[2 - self.displacement.y][2 + self.displacement.x]

    def command(self):
        command = ''
        command += str(abs(self.displacement.x))
        command += 'R' if self.displacement.x > 0 else 'L'
        command += str(abs(self.displacement.y))
        command += 'U' if self.displacement.y > 0 else 'D'
        return command

    def getReverseMove(self):
        return Move(Displacement(-self.displacement.x, -self.displacement.y))


# A "map" (the current context)
class Map:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.current_position = Position(0, 0)
        self.princess_position = Position(1, 0)
        self.tiles = None

    def __str__(self):
        result = '----- MAP -----\n'
        for i in range(0, 5):
            result += "%s\n" % self.tiles[i]
        result += 'Pos: %s\n' % (str(self.current_position))
        result += 'Available moves: %s\n' % ', '.join(str(x) for x in self.available_moves())
        result += 'Visited: %d\n' % len(self.visited)
        result += 'Path: %s\n' % ' '.join([str(x) for x in self.path])
        result += '---------------'
        return result

    def update_tiles(self):
        data = str(self.sock.recv(4096), encoding='utf-8').split('\n')
        print(*data, sep='\n')
        tiles = data[0:5]
        assert len(tiles) == 5
        for i in range(0, 5): assert len(tiles[i]) == 5
        self.tiles = tiles
        print(self)

    def available_moves(self):
        moves = []
        for move in KNIGHT_MOVES:
            if move.getTile(self.tiles) != '#': moves.append(move)
        moves.sort(key = lambda x: move.apply(self.current_position).distance_to(self.princess_position))
        return moves

    def apply_move(self, move):
        self.sock.send(move.command().encode())
        self.current_position = move.apply(self.current_position)
        if self.found_princess():
            print('yay!')
            data = str(self.sock.recv(4096), encoding='utf-8').split('\n')
            print(*data, sep='\n')
            sys.exit()
        self.update_tiles()
        print(self)

    def found_princess(self):
        return (self.current_position.x == self.princess_position.x) and \
               (self.current_position.y == self.princess_position.y)

    def search_princess(self):
        self.visited = []
        self.path = []
        map.update_tiles()
        while not self.found_princess():
            self.do_search_step()

    def do_search_step(self):
        if self.found_princess():
            print("FOUND IT!")
            sys.exit()
        self.visited.append(self.current_position)
        self.path.append(self.current_position)
        available_moves = self.available_moves()
        for move in available_moves:
            if move.apply(self.current_position) not in self.visited:
                self.apply_move(move)
                self.do_search_step()
                self.apply_move(move.getReverseMove())
        self.path.pop()


host = "52.49.91.111"
port = 2003

# compute valid moves by a knight
KNIGHT_MOVES = [
    Move(Displacement(-1, +2)),
    Move(Displacement(+1, +2)),
    Move(Displacement(-2, +1)),
    Move(Displacement(+2, +1)),
    Move(Displacement(-2, -1)),
    Move(Displacement(+2, -1)),
    Move(Displacement(-1, -2)),
    Move(Displacement(+1, -2)),
]

map = Map()
map.search_princess()