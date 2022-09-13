import copy
import random
import json
import pickle
import hashlib
from cardclass import GameTable, DeckOfCards, Card, Move
from dbwork import save_to_sql
from cardclass import GameTable


# начало программы
if __name__ == '__main__':

    sss = 'n'
    # sss = input('новую колоду? ->')
    if sss == 'y':
        k = DeckOfCards()
        k.rand()
        j = GameTable(k)
    else:
        with open("gametable.bin", "rb") as _file:
            j = GameTable()
            j = pickle.load(_file)

    with open("gametable.bin", "wb") as _file:
        pickle.dump(j, _file)

    while (len(j.active_move) > 0 or j.count_stack != 0) and len(j.move_history) <= 250:
        print(j)
        j.search_moves()
        j.do_move()
        j.check_table()

#  тестирование SQL

    save_to_sql()
