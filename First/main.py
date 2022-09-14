'''

Исследование сходимости пасьянса косынка

'''

# from cardclass import GameTable, DeckOfCards, Card, Move
from cardclass import DeckOfCards
from dbwork import log_deck, log_attemp, open_db, close_db
from cardclass import GameTable
import time, sys

global GLOBAL_TRACE

global _DECK_TUPLE
_DECK_TUPLE = [1]


#  проведение эксперимента с указанием количества попыток
def steps(_all_steps=0, _log_connection=None):

    if _all_steps and _log_connection:
        step_start = time.time()
        _cursor = 0
        _time_only_decision = 0
        _k = 0
        for _i in range(1, _all_steps + 1):
            d = time.time()
            if do_one_table(_log_connection):
                _k = _k + 1
            # print(_i, _k, round(_k/_i * 100, 1), '%', round(time.time() - d, 3))
            print(_i)

        _j = round(time.time() - step_start, 3)
        # print('Итого:', _i, _j)
        log_attemp(_log_connection, _j, _i, _k, round(_k/_i * 100, 2))
    return


#  решение одной раздачи c генерацией
def do_one_table(_log_connection=None):
    k = DeckOfCards()
    k.rand()
    _table = GameTable(k)
    _table.decision_table()
    log_deck(_table, _log_connection)
    return _table.win


# начало программы
if __name__ == '__main__':
    # не сильно заморачиваемся с обработкой параметров
    _param = sys.argv
    _i = 1 if len(_param) == 1 else 10 ** (len(_param[1])-1)

    _conn = open_db()
    steps(_i, _conn)
    close_db(_conn)

