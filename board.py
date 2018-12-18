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
        self.running = True

        '''
        the game state is saved in a 1D list for mathematical reasons

        only storing the parts of the board that are actually used

        '''
        self.state = [
            ' ', ' ', ' ', ' ',
            ' ', 'o', 'o', ' ',
            ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ',
            ' ', 'x', 'x', ' ',
            ' ', ' ', ' ', ' '
        ]

        self.unjumpable = [0,1,2,3,4,11,12,19,20,27,28,29,30,31]

        self.x_pos = []
        self.o_pos = []

        for i in range(len(self.state)):
            if self.state[i].lower() == 'x':
                self.x_pos.append(i)
            elif self.state[i].lower() == 'o':
                self.o_pos.append(i)


        # self.player = {}

        # self.player['x'] = {
        #     'player': 'x',
        #     'opponent': 'o',
        #     'left': 4,
        #     'right': 5,
        #     'new left': lambda pos_i, row: pos_i + (3 + row % 2),
        #     'new right': lambda pos_i, row: pos_i + (4 + row % 2)
        # }

        # self.player['o'] = {
        #     'player': 'o',
        #     'opponent': 'x',
        #     'left': -4,
        #     'right': -3,
        #     'new left': lambda pos_i, row: pos_i - (5-row % 2),
        #     'new right': lambda pos_i, row: pos_i - (4-row % 2)
        # }


    def __repr__(self):
        # return string
        # system('clear')
        top = '\n    a   b   c   d   e   f   g   h\n'

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

        return "%s%d" % (letter, number)

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

    def move(self, loc, new_loc):
        '''
        the player picks a piece to move then the possible moves to make are
        given to them to pick from


        TODO:
            - [ ] jumps / taking pieces
            - [ ] Kinging
        '''


        index_choice = self.index(*self.to_index(new_loc))
        index_piece = self.index(*self.to_index(loc))
        self.state[index_piece], self.state[index_choice] = self.state[index_choice], self.state[index_piece]


        if self.state[index_choice].lower() == 'x':
            self.x_pos.remove(index_piece)
            self.x_pos.append(index_choice)

        elif self.state[index_choice].lower() == 'o':
            self.o_pos.remove(index_piece)
            self.o_pos.append(index_choice)


        # removing jumped
        diff = index_choice - index_piece
        letter, number = self.to_index(loc)
        if diff == 7:
            delete = index_piece+4 - (number % 2)
            self.o_pos.remove(delete)
            self.state[delete] = ' '
        elif diff == 9:
            delete = index_piece+5 - (number % 2)
            self.o_pos.remove(delete)
            self.state[delete] = ' '
        elif diff == -7:
            delete = index_piece-3 - (number % 2)
            self.x_pos.remove(delete)
            self.state[delete] = ' '
        elif diff == -9:
            self.state[index_piece-4 - (number % 2)] = ' '
            delete = index_piece-4 - (number % 2)
            self.x_pos.remove(delete)
            self.state[delete] = ' '

        # kinging
        number = int(new_loc[1])-1
        if self.state [index_choice] == "x" and number == 7:
            self.state[index_choice] = "X"
        elif self.state[index_choice] == "o" and number == 0:
            self.state[index_choice] = "O"


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

        if piece == 'x' or piece == "O" or piece == "X":
            if i+4 <= 31 and self.state[i+4] != piece:
                possible_indexes.append(i+4)

            # event row and not on left edge
            # right move
            if i+3 <= 31 and number % 2 == 1 and i % 4 != 0 and self.state[i+3] != piece:
                possible_indexes.append(i+3)
            # left move
            elif i+5 <= 31 and number % 2 == 0 and i % 4 != 3 and self.state[i+5] != piece:
                possible_indexes.append(i+5)

            # jumping pieces
            c = 0
            while c < len(possible_indexes):
                index = possible_indexes[c]
                if self.state[index].lower() == 'o' :
                    if possible_indexes[c] - i + number % 2 == 4:
                        new_i = possible_indexes[c] + (3 + number % 2)
                        if possible_indexes[c] not in self.unjumpable and self.state[new_i] == ' ':
                            possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c-=1

                    elif possible_indexes[c] - i + number % 2 == 5:
                        new_i = possible_indexes[c] + (4 + number % 2)
                        if possible_indexes[c] not in self.unjumpable and self.state[new_i] == ' ':
                            possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c-=1

                c += 1

        if piece == 'o' or piece == "O" or piece == "X":
            if i-4 >= 0 and self.state[i-4] != piece:
                possible_indexes.append(i-4)

            if i-3 >= 0 and number % 2 == 0 and i % 4 != 3 and self.state[i-3] != piece:
                possible_indexes.append(i-3)

            elif i-5 >= 0 and number % 2 == 1 and i % 4 != 0 and self.state[i-5] != piece:
                possible_indexes.append(i-5)

            # jumping pieces
            c = 0
            while c < len(possible_indexes):
                index = possible_indexes[c]
                if self.state[index].lower() == 'x':

                    if possible_indexes[c] - i + number % 2 == -4:
                        new_i = possible_indexes[c] - (5 - number % 2)
                        if possible_indexes[c] not in self.unjumpable and self.state[new_i] == ' ':
                            possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c-=1

                    elif possible_indexes[c] - i + number % 2 == -3:
                        new_i = possible_indexes[c] - (4 - number % 2)
                        if possible_indexes[c] not in self.unjumpable and self.state[new_i] == ' ':
                            possible_indexes[c] = new_i
                        else:
                            possible_indexes.pop(c)
                            c -= 1
                c += 1

        # elif piece == 'O' or piece == 'X':
        #     possible_indexes.extend([i+4,i-4])

        return possible_indexes



# b = Board()
# while True:
#     print b
#     piece = raw_input('what piece would you like to move?\n')
#     to = raw_input('where would you like to move it?\n')
#     options = [b.to_letter_number(item) for item in b.list_possible_indexes(piece)]

#     # print options

#     if to in options:
#         b.move(piece, to)
#         b.turn += 1
#     else:
#         print "please make a valid move"
