import random
import pprint
import sys
import copy

from group import Group, GroupElement

V4 = Group("V4", {"e", "a", "b", "c"}, {
    "e": {"a": "a", "b": "b", "c": "c", "e": "e"},
    "a": {"a": "e", "b": "c", "c": "b", "e": "a"},
    "b": {"b": "e", "a": "c", "c": "a", "e": "b"},
    "c": {"c": "e", "b": "a", "a": "b", "e": "c"}
})

Z4 = Group("Z4", {"e", "a", "b", "c"}, {
    "e": {"a": "a", "b": "b", "c": "c", "e": "e"},
    "a": {"a": "b", "b": "c", "c": "e", "e": "a"},
    "b": {"a": "c", "b": "e", "c": "a", "e": "b"},
    "c": {"a": "e", "b": "a", "c": "b", "e": "c"}
})

Z2 = Group("Z2", {"e", "a"}, {
    "e": {"a": "a", "e": "e"},
    "a": {"a": "e", "e": "a"}
})


D3 = Group("D3", {"e", "a", "b", "c", "d", "f"}, {
    "e": {"e": "e", "a": "a", "b": "b", "c": "c", "d": "d", "f": "f"},
    "a": {"e": "a", "a": "b", "b": "e", "c": "f", "d": "c", "f": "d"},
    "b": {"e": "b", "a": "e", "b": "a", "c": "d", "d": "f", "f": "c"},
    "c": {"e": "c", "a": "d", "b": "f", "c": "e", "d": "a", "f": "b"},
    "d": {"e": "d", "a": "f", "b": "c", "c": "b", "d": "e", "f": "a"},
    "f": {"e": "f", "a": "c", "b": "d", "c": "a", "d": "b", "f": "e"},
})

class GameError(Exception):
    pass

class Game(object):
    def __init__(self, group, size=5, seed=None):
        self.group = group
        self.board = []
        self.size = size

        random.seed(seed)

        for row in range(size):
            self.board.append([])
            for col in range(size):
                self.board[-1].append(group[random.choice(list(group.S))])

        self.last_board = self.board
        self.last_move = []

    def victory(self):
        non_ident = 0
        for row in self.board:
            for col in row:
                if col.elem != self.group.ident:
                    non_ident += 1

        return non_ident <= 1

    def repeat(self):
        if len(self.last_move):
            self.move(*self.last_move[0], *self.last_move[1])

    def move(self, x1, y1, x2, y2):
        try:
            left = self.board[x1][y1]
            right = self.board[x2][y2]
        except IndexError:
            raise ValueError("Invalid coordinates: need integers between 0 and {}".format(self.size))
        if ((x1 == x2) and (abs(y1 - y2) != 1)) or \
           ((y1 == y2) and (abs(x1 - x2) != 1)) or \
           ((y1 != y2) and (x1 != x2)):
               raise GameError("Moves must be on adjacent squares")

        self.last_board = copy.deepcopy(self.board)
        self.last_move = [(x1, y1), (x2, y2)]

        # new_right = left * right
        new_left = right * left
        new_right = left * right
        self.board[x1][y1] = new_left
        self.board[x2][y2] = new_right

    def undo(self):
        self.board = self.last_board
        self.last_move = []

    def print_board(self):
        header_format = "\n\t\t" + "{}\t" * self.size + "\n\n"
        row_format = "{}\t\t" + "{}\t" * self.size + "\n\n"

        board_to_print = header_format.format(*range(self.size))
        for i in range(self.size):
            row = self.board[i]
            row_to_print = []
            for j in range(self.size):
                if row[j].elem == self.group.ident:
                    row_to_print.append('.')
                else:
                    row_to_print.append(row[j].elem)

                if (i, j) in self.last_move:
                    row_to_print[-1] += '*'

            board_to_print += row_format.format(i, *row_to_print)

        print(board_to_print)

    def __repr__(self):
        return "<Game:\n{}\n>".format(pprint.pformat(self.board))

game = Game(D3, size=5)

print("Loading game with group {}".format(game.group.name))

while True:
    game.print_board()

    move = input("Your move (x1 y1 x2 y2), (r)epeat last move, (u)ndo or (q)uit: ")
    if move.lower() in ['q', 'quit', 'exit']:
        sys.exit(0)

    if move.lower() in ['u', 'undo']:
        game.undo()
    elif move.lower() in ['r', 'repeat']:
        game.repeat()
    else:
        try:
            game.move(*[int(part.strip()) for part in move.split()])
        except (ValueError, TypeError):
            print("Move needs to be in the format: 'x1 y1 x2 y2'. For example: 0 0 0 1.")
            continue
        except GameError as e:
            print(e)
            continue

    if game.victory():
        print("You win!")
        break
