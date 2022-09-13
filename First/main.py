import copy
import random
import json
import pickle
import hashlib
from cardclass import GameTable, DeckOfCards, Card, Move
from dbwork import save_to_sql
from cardclass import GameTable
import time

global GLOBAL_TRACE, GLOBAL_SUCSESS

GLOBAL_SUCSESS = 0

def do_one_table():

    sss = 'y'  # работаем с новой колодой или сохраненной
    if sss == 'y':
        k = DeckOfCards()
        k.rand()
        _table = GameTable(k)
    else:
        with open("gametable.bin", "rb") as _file:
            _table = pickle.load(_file)

    with open("gametable.bin", "wb") as _file:
        pickle.dump(_table, _file)

    _table.decision_table()

    #  тестирование SQL пока только сохраняем
    save_to_sql(_table)

    return _table.win


# начало программы
if __name__ == '__main__':

    b = time.time()
    _k = 0
    for _i in range(1, 1000):
        if do_one_table():
            _k = _k + 1
        print(_i, _k, round(_k/_i * 100, 1), '%')

    print('Итого:', _i, time.time() - b, GLOBAL_SUCSESS)



