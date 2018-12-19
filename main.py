'''
Main file of execution
'''

from board import Board
from minimax import *
from os import system
from time import sleep


b = Board()
# b.random_board()

existLoser = False
turn = 0

while not existLoser:
    system('clear')
    print b
    if turn % 2 == 0:
        # person
        piece = raw_input('what piece would you like to move?\n')
        to = raw_input('where would you like to move it?\n')
        options = [b.to_letter_number(item)
                   for item in b.list_possible_indexes(piece)]

        if to in options and b.index(*b.to_index(piece)) in b.o_pos:
            b.move(piece, to)
            turn += 1
        else:
            print "please make a valid move"
            sleep(2)

        existLoser = b.check_lost("o")
    else:
        # AI
        print "AI is thinking..."
        score, b = MiniMax(b, 5, True)
        turn += 1
        existLoser = b.check_lost("x")
