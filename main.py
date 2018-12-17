'''
Main file of exicution
'''

from board import Board
from minimax import *
from os import system
from time import sleep


b = Board()

while b.running:
    system('clear')
    print b
    if b.turn % 2 == 0:
        # person
        piece = raw_input('what piece would you like to move?\n')
        to = raw_input('where would you like to move it?\n')
        options = [b.to_letter_number(item)
                   for item in b.list_possible_indexes(piece)]

        if to in options and b.index(*b.to_index(piece)) in b.o_pos:
            b.move(piece, to)
            b.turn += 1
        else:
            print "please make a valid move"

    else:
        # AI
        print "AI is making it's move"
        score, b.state = MiniMax(b, 2, True, b.state)
        b.turn += 1
        sleep(2)
