'''

Исследование сходимости пасьянса косынка

'''
GL_CARD_DECK = []
GLOBAL_TRACE = False
GL_LOG_DECK = []

import time
import sys
from cardclass import GameTable, log_deck, log_trial
# from cardclass import Card
from cardclass import DeckOfCards

import asyncio


#  проведение эксперимента с указанием количества попыток
async def steps(_all_steps=0):

    if _all_steps:
        _cursor, _k = 0, 0
        step_start = time.time()
        for _tempI in range(1, _all_steps + 1):
            if await do_one_table():
                _k = _k + 1
        _j = round(time.time() - step_start, 3)
        await log_deck(0, True)
        await log_trial(_j, _all_steps, _k, round(_k / _all_steps * 100, 2))
    return


#  решение одной раздачи c генерацией
async def do_one_table():
    k = DeckOfCards()
    k.rand()
    _table = GameTable(k)
    _table.solve_table()
    await log_deck(_table)
    return _table.win


# начало программы
if __name__ == '__main__':

    # не сильно заморачиваемся с обработкой параметров
    _param = sys.argv
    _i = 1000 if len(_param) == 1 else 10 ** (len(_param[1])-1)

    asyncio.run(steps(_i))
    print('THE END.')

