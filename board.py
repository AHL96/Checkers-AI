# from os import system


class Board(object):
    '''
    this class will hold all the data and functionality of the checker board

    Instead of white and black, i will use x's and o's for the game pieces and
    spaces, ' ', to represent and empty spot on the board

    When pieces get kinged they will turn into their uppercase version.
    '''

    def __init__(self):
        # who's turn is it? Mod turn to find out
        self.turn = 0

        '''
        the game state is saved in a 1D list for mathematical reasons

        only storing the parts of the board that are actually used

        '''
        self.state = [
            'x', 'x', 'x', 'x',
            'x', 'x', 'x', 'x',
            'x', ' ', ' ', ' ',
            'o', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ',
            'x', ' ', ' ', ' ',
            'o', 'o', 'o', 'o',
            'o', 'o', 'o', 'o'
        ]

        self.unjumpable = [0,1,2,3,4,11,12,19,20,27,28,29,30,31]

        self.player = {}

        self.player['x'] = {
            'player': 'x',
            'opponent': 'o',
            'left': 4,
            'right': 5,
            'new left': lambda pos_i, row: pos_i + (3 + row % 2),
            'new right': lambda pos_i, row: pos_i + (4 + row % 2)
        }

        self.player['o'] = {
            'player': 'o',
            'opponent': 'x',
            'left': -4,
            'right': -3,
            'new left': lambda pos_i, row: pos_i - (5-row % 2),
            'new right': lambda pos_i, row: pos_i - (4-row % 2)
        }


    def __repr__(self):
        # return string
        # system('clear')
        top = '    a   b   c   d   e   f   g   h\n'

        for i in range(8):
            top += '  ' + '-'*33 + '\n%s ' % (i+1)
            for spot in self.state[i*4:i*4+4]:
                if i % 2 == 0:
                    top += '|   | %s ' % spot
                else:
                    top += '| %s |   ' % spot
            top += '|\n'
        top += '  ' + '-'*33 + '\n'

        return top

    def to_letter_number(self, index):
        number = (index // 4) + 1
        # letter = chr(2*number + ((number+1) % 2) + 96)
        letters = ['b', 'd', 'f', 'h', 'a', 'c', 'e', 'g']
        letter = letters[index % 8]

        return "%s%s" % (letter, number)

    def to_index(self, letter_number):
        letter = ord(letter_number[0].lower()) % 97
        number = int(letter_number[1]) - 1

        return letter, number

    def index(self, i, j):
        '''
        use this function to treat the 1D list as a 2D list
        width of self.state is 4
        '''
        return 4*j + i//2

    def move(self, piece):
        '''
        the player picks a piece to move then the possible moves to make are
        given to them to pick from


        TODO:
            - [ ] Proper Turns
            - [ ] jumps / taking pieces
            - [ ] Kinging
        '''


        options = [self.to_letter_number(item)
                   for item in self.list_possible_indexes(piece)]
        choice = raw_input("your options are %s\n" % options)

        '''
        o = old move
        n = new move

        o,n = n,o
        '''
        if choice in options:
            index_choice = self.index(*self.to_index(choice))
            index_piece = self.index(*self.to_index(piece))
            self.state[index_piece], self.state[index_choice] = self.state[index_choice], self.state[index_piece]

            '''
            TODO:
                - [x] jumping to the left
                - [x] taking piece for odd rows
                - [x] all jumping with the o's
            '''
            diff = index_choice - index_piece
            # if self.state[index_piece] == 'x':
            letter, number = self.to_index(piece)
            # if number % 2 == 0: # odd rows
            if diff == 7:
                self.state[index_piece+4 - (number % 2)] = ' '
            elif diff == 9:
                self.state[index_piece+5 - (number % 2)] = ' '
            # elif self.state[index_piece] == 'o':
            elif diff == -7:
                self.state[index_piece-3 - (number % 2)] = ' '
            elif diff == -9:
                self.state[index_piece-4 - (number % 2)] = ' '

        self.turn += 1

    def list_possible_indexes(self, tile):
        letter, number = self.to_index(tile)

        i = self.index(letter, number)

        # if piece is o, subtract
        # if piece is x, add
        # if piece is uppercase, move in any direction
        piece = self.state[i]
        possible_indexes = []

        '''
        controls = self.player[piece]
        '''

        if piece == 'x' and self.turn % 2 == 0:
            if self.state[i+4] != piece:
                possible_indexes.append(i+4)

            # event row and not on left edge
            # right move
            if number % 2 == 1 and i % 4 != 0 and self.state[i+3] != piece:
                possible_indexes.append(i+3)
            # left move
            elif number % 2 == 0 and i % 4 != 3 and self.state[i+5] != piece:
                possible_indexes.append(i+5)

            # jumping pieces
            c = 0
            while c < len(possible_indexes):
                index = possible_indexes[c]
                if self.state[index] == 'o':
                    if possible_indexes[c] - i + number % 2 == 4:
                        if possible_indexes[c] not in self.unjumpable:
                            new_i = possible_indexes[c] + (3 + number % 2)
                            if self.state[new_i] == ' ' :
                                possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c-=1

                    elif possible_indexes[c] - i + number % 2 == 5:
                        if possible_indexes[c] not in self.unjumpable:
                            new_i = possible_indexes[c] + (4 + number % 2)
                            if self.state[new_i] == ' ':
                                possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c-=1

                c += 1

        elif piece == 'o' and self.turn % 2 == 1:
            if self.state[i-4] != piece:
                possible_indexes.append(i-4)

            if number % 2 == 0 and i % 4 != 3 and self.state[i-3] != piece:
                possible_indexes.append(i-3)

            elif number % 2 == 1 and i % 4 != 0 and self.state[i-5] != piece:
                possible_indexes.append(i-5)

            # jumping pieces
            c = 0
            while c < len(possible_indexes):
                index = possible_indexes[c]
                if self.state[index] == 'x':

                    if possible_indexes[c] - i + number % 2 == -4:
                        if possible_indexes[c] not in self.unjumpable:
                            new_i = possible_indexes[c] - (5 - number % 2)
                            if self.state[new_i] == ' ':
                                possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c-=1

                    elif possible_indexes[c] - i + number % 2 == -3:
                        if possible_indexes[c] not in self.unjumpable:
                            new_i = possible_indexes[c] - (4 - number % 2)
                            if self.state(new_i) == ' ':
                                possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c -= 1


                c += 1
        elif piece == 'O' or piece == 'X':
            # finish this part of the function for kinging
            possible_indexes.append()

        return possible_indexes

    def check_winner(self, xo):
        for row in self.state:
            for spot in row:
                if xo == spot.lower():
                    return False  # no winner yet

        return True  # someone has won


b = Board()
while True:
    print b
    piece = raw_input('what piece would you like to move?\n')
    b.move(piece)
