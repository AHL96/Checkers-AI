from board import Board


def evaluate(state):
    node = Node(state)
    score = 0
    x = len(node.x_pos)
    o = len(node.o_pos)
    if o == 0:  # winning
        score += 1000
    if x == 0:  # losing
        score -= 1000
    score += 10*(x - o)  # jumping
    for x in node.x_pos:  # how far down the board AI is
        letter, number = node.to_index(node.to_letter_number(x))
        score += 2*number
        if x in node.unjumpable:  # edge piece
            score += 5
    for o in node.o_pos:  # how far opponent is up the board
        letter, number = node.to_index(node.to_letter_number(o))
        score += 2 * (7 - number)
        if o in node.unjumpable:  # edge piece
            score -= 5
    return score


def MiniMax(game, depth, isMaximissingPlayer, bestBoard):
    if depth == 0:
        return evaluate(game.state), bestBoard

    possible_boards = list_possible_boards(game.state, isMaximissingPlayer)

    if isMaximissingPlayer:
        bestMove = -9999
        for i in range(len(possible_boards)):
            oldMove = bestMove
            bestMove = max([
                bestMove,
                MiniMax(Node(possible_boards[i]), depth-1, False, bestBoard)[0]
            ])
            if bestMove != oldMove:
                bestBoard = possible_boards[i]

    else:
        bestMove = 9999
        for i in range(len(possible_boards)):
            bestMove = min([bestMove, MiniMax(
                Node(possible_boards[i]), depth-1, True, bestBoard)[0]])

    return bestMove, bestBoard


class Node(Board):
    def __init__(self, state):
        self.state = state

        self.unjumpable = [0, 1, 2, 3, 4, 11, 12, 19, 20, 27, 28, 29, 30, 31]

        self.x_pos = []
        self.o_pos = []

        for i in range(len(self.state)):
            if self.state[i].lower() == 'x':
                self.x_pos.append(i)
            elif self.state[i].lower() == 'o':
                self.o_pos.append(i)


def print_board(b):
    top = '\n    a   b   c   d   e   f   g   h\n'

    for i in range(8):
        top += '  ' + '-'*33 + '\n%s ' % (i+1)
        for spot in b[i*4:i*4+4]:
            if i % 2 == 0:
                top += '|   | %s ' % spot
            else:
                top += '| %s |   ' % spot
        top += '|\n'
    top += '  ' + '-'*33 + '\n'

    print top


def list_possible_boards(state, isMaximissingPlayer):
    possible_boards = []
    game = Node(state[:])

    if isMaximissingPlayer:
        spots = game.x_pos
    else:
        spots = game.o_pos

    for spot in spots:
        for direction in game.list_possible_indexes(game.to_letter_number(spot)):
            possible = Node(game.state[:])
            loc = game.to_letter_number(spot)
            new_loc = game.to_letter_number(direction)
            possible.move(loc, new_loc)
            possible_boards.append(possible.state)

    # for b in possible_boards:
    #     print_board(b)
    return possible_boards


# b = Board()
# print b
# best = MiniMax(b, 3, True, b.state)
# print "best move ", best[0]

# print_board(best[1])
