'''

Исследование сходимости пасьянса косынка

'''
GL_CARD_DECK = []
GLOBAL_TRACE = False

# from cardclass import GameTable, DeckOfCards, Card, Move
import time, sys
from cardclass import GameTable  # , set_global_var
from cardclass import Card
from cardclass import DeckOfCards
from dbwork import log_deck, log_attemp, open_db, close_db

GL_CARD_DECK.extend(Card(_I) for _I in range(0, 52))


# глобальная константа - карты по порядку
# def set_global_var():
#     global GL_CARD_DECK
#     GL_CARD_DECK = []
#     _I = 0
#     GL_CARD_DECK.extend(Card(_I) for _I in range(0, 52))
#     print(GL_CARD_DECK)
#     return


#  проведение эксперимента с указанием количества попыток
def steps(_all_steps=0, _log_connection=None):

    if _all_steps:
        _cursor, _k = 0, 0
        # _time_only_decision = 0
        step_start = time.time()
        for _tempI in range(1, _all_steps + 1):
            if do_one_table(_log_connection):
                _k = _k + 1
        _j = round(time.time() - step_start, 3)
        log_attemp(_log_connection, _j, _all_steps, _k, round(_k/_all_steps * 100, 2))
    return


#  решение одной раздачи c генерацией
def do_one_table(_log_connection=None):
    global GL_CARD_DECK
    k = DeckOfCards()
    k.rand()
    _table = GameTable(k)
    _table.solve_table()
    log_deck(_table, _log_connection)
    return _table.win


# начало программы
if __name__ == '__main__':

    # не сильно заморачиваемся с обработкой параметров
    _param = sys.argv
    _i = 1 if len(_param) == 1 else 10 ** (len(_param[1])-1)

    _conn = None
    # _conn = open_db()
    steps(_i, _conn)
    # close_db(_conn)

    print('THE END.')



# тестируем операции
#     odin = DeckOfCards()
#     dva = DeckOfCards(0)
#     _k = 1000
#
#     print('Тест методов объекта:')
#     time1 = time.time()
#     for _j in range(0, _k):
#         for _i in range(0, 52):
#             dva.app_first_card(odin.get_first_card())
#         odin, dva = dva, odin
#     time1 = time.time() - time1
#     print('Количество проходов: ' + str(_k) + '; Время: ' + str(round(time1, 4)))
#
#     odin = DeckOfCards()
#     dva = DeckOfCards(0)
#     print('Тест прямых операций:')
#     time2 = time.time()
#     for _j in range(0, _k):
#         for _i in range(0, 52):
#             dva.app_first(odin.get_first())
#         dva.list_of_cards.reverse()
#         odin, dva = dva, odin
#     time2 = time.time() - time2
#     print('Количество проходов: ' + str(_k) + '; Время: ' + str(round(time2, 4)))
#
#     print('!!! В : ' + str(round(time1/time2, 0)) + ' раз быстрее !!!')

