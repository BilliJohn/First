#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''

классы по работе с картами

'''
import copy
import random
import time
global GLOBAL_TRACE, _DECK_TUPLE
GLOBAL_TRACE = False


# определение класса - карта;
#  0000 - значение + 00 - масть. От 0 до 51
#  63 (111111) - признак пустой карты


# ------------------------------------------------------------------------------------------
class Card(object):
    def __init__(self, input_x=None):
        self.card_num = None  # номер карты

        if isinstance(input_x, int) and 0 <= input_x <= 51:
            self.card_num = input_x
        else:
            self.card_num = 63  # пустая карта 1111 11
        return

    def __eq__(self, other):
        return self.number() == other.number()

    def __ne__(self, other):
        return self.number() != other.number()

    def number(self):
        return self.card_num if isinstance(self.card_num, int) and 0 <= self.card_num <= 51 else 63

    def range(self):
        return self.card_num >> 2 if self.card_num != 63 else 63

    # масть 3 -> 000011
    def suit(self):
        return self.card_num & 3 #if self.card_num != 63 else 63

    # один цвет
    def same_color(self, _card):
        return self.suit() % 2 == _card.suit() % 2

    # следующая карта
    def next_card_for(self, _card: object) -> object:
        return (_card.range() - self.range() == 1) or (_card.range() == 0 and self.range() == 12)

    # расшифровка карты
    def __str__(self):
        _tempI = ''
        _x = 63
        if isinstance(self.card_num, int) and 0 <= self.card_num <= 51:
            _x = Card.suit(self)
            _y = Card.range(self)
            # масть
            if _x == 3:
                _tempI = f'\u2660'  # пики
            elif _x == 2:
                _tempI = f'\u2666'  # 'Б'
            elif _x == 1:
                _tempI = f'\u2663'  # 'Т'
            elif _x == 0:
                _tempI = f'\u2665'  # 'Ч'
            # ранг
            if _y == 12:
                _tempI = ' Т' + _tempI
            elif _y == 0:
                _tempI = ' 2' + _tempI
            elif _y == 1:
                _tempI = ' 3' + _tempI
            elif _y == 2:
                _tempI = ' 4' + _tempI
            elif _y == 3:
                _tempI = ' 5' + _tempI
            elif _y == 4:
                _tempI = ' 6' + _tempI
            elif _y == 5:
                _tempI = ' 7' + _tempI
            elif _y == 6:
                _tempI = ' 8' + _tempI
            elif _y == 7:
                _tempI = ' 9' + _tempI
            elif _y == 8:
                _tempI = '10' + _tempI
            elif _y == 9:
                _tempI = ' В' + _tempI
            elif _y == 10:
                _tempI = ' Д' + _tempI
            elif _y == 11:
                _tempI = ' К' + _tempI
        else:
            _tempI = f'  \u2298'

        # покрасим
        if _x == 0 or _x == 2:
            _tempI = PrintStyle.RED + PrintStyle.BLEK + _tempI + PrintStyle.END
        else:
            _tempI = PrintStyle.BLUE + _tempI + PrintStyle.END

        return _tempI


# ---------------------------------------------------------------------------------------------
class PrintStyle:
    UNDER = '\033[4m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    BLEK = '\033[2m'
    END = '\033[0m'


# определяем класс колода карт, если вход пустой, то формируем раздачу 52 карты
class DeckOfCards(object):

    def __init__(self, _input_list=[]):  # при инициации, или входной список или последовательный набор карт
        self.list_of_cards = []

        if isinstance(_input_list,
                      int) and _input_list != 0:  # если чиcло, то создаем список длинной _input_list с пустыми картами
            for _tempI in range(_input_list):
                self.list_of_cards.append(Card())
        elif isinstance(_input_list, int) and _input_list == 0:  # создаем пустой список
            self.list_of_cards = []
        else:  # ничего нет - даем 52 карты
            for _tempI in range(52):
                self.list_of_cards.append(Card(_tempI))

        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', _DECK_TUPLE)
        return

    def see_first_card(self):
        return self.list_of_cards[0] if len(self) else Card(63)

    def see_end_card(self):
        return self.list_of_cards[len(self) - 1] if len(self) >= 1 else Card(63)

    def get_first_card(self):
        _x = Card(63)
        if len(self) > 0:
            _x = self.list_of_cards.pop(0)
        return _x

    def get_end_card(self):
        _x = Card(63)
        if len(self) > 0:
            _x = self.list_of_cards.pop()
        return _x

    def app_first_card(self, _app_card):
        _x = [_app_card]
        _x.extend(self.list_of_cards)
        self.list_of_cards = copy.deepcopy(_x)
        # self.list_of_cards.append(_app_card)
        # self.list_of_cards.reverse()
        return

    def app_end_card(self, _app_card):
        self.list_of_cards.append(_app_card)
        return

    def __str__(self, _index=63):  # печатаем колоду строкой True - печать циферок для отладки
        _x = '['
        _y = 0
        for _tempI in self.list_of_cards:
            _x = _x + PrintStyle.UNDER if _y == _index else _x  # выделение элемента при печати
            _x = _x + _tempI.__str__()
            _x = _x + PrintStyle.END if _y == _index else _x
            _y = _y + 1
        return _x + ']'

    def rand(self):  # перемешивает раздачу в случайном порядке
        random.shuffle(self.list_of_cards)
        return

    def __len__(self):
        return len(self.list_of_cards)


# --------------------------------------------------------------------------------------------------

# определяем класс игровой стол (косынка)
class GameTable(object):

    def __init__(self, _input_deck=DeckOfCards(0)):

        self.start_deck = copy.deepcopy(_input_deck)
        self.start_hash = hash(tuple(self.start_deck.list_of_cards.__str__()))
        self.play_off = []
        for _tempI in range(4):
            self.play_off.append(DeckOfCards(0))
        self.play_stack = DeckOfCards(0)
        self.play_st_i = 0
        # если 100, значит это первый проход. N - количество проходов стека без сноса
        # 50 - были сносы
        # 25 - сносов не было
        self.count_stack = 100
        self.play_visible = []
        for _tempI in range(7):  self.play_visible.append(DeckOfCards(0))
        self.play_invisible = []
        for _tempI in range(7):  self.play_invisible.append(DeckOfCards(0))
        self.active_move = []
        self.move_history = []
        self.count_moves = 0
        self.desicion_time = 0.0
        self.win = False

        if len(_input_deck) == 52:  # раздаем карты
            _x = 0
            self.play_visible[0].app_first_card(_input_deck.get_first_card())
            for _x in range(1, 7):
                for _tempI in range(_x, 7):
                    self.play_invisible[_tempI].app_first_card(_input_deck.get_first_card())
                self.play_visible[_x].app_first_card(_input_deck.get_first_card())
            for _tempI in range(1, len(_input_deck.list_of_cards) + 1):
                self.play_stack.app_end_card(_input_deck.get_first_card())
        return

    #  решение игрового стола
    def decision_table(self):

        time_start = time.time()

        while (len(self.active_move) > 0 or self.count_stack != 0) and len(self.move_history) <= 250:
            self.search_moves()
            self.do_move()
            self.check_table()

        # проверяем сходимость
        _desi = True
        for i in range(0,3):
            _desi = _desi and len(self.play_off[i].list_of_cards) == 13
        if _desi:
            # print('***********')
            self.win = True

        self.desicion_time = round(time.time() - time_start, 5)

        return self.win

    # проверка игрового стола, ничего не пропало
    def check_table(self):

        _all_sum = 1326
        _message = '\nО!->'
        _all_card = 0
        _y = []
        # количественная проверка
        for _tempI in self.play_off:
            _y.extend(_tempI.list_of_cards)
        for _tempI in self.play_invisible:
            _y.extend(_tempI.list_of_cards)
        for _tempI in self.play_visible:
            _y.extend(_tempI.list_of_cards)
        _y.extend(self.play_stack.list_of_cards)

        _all_card = len(_y)
        for _tempI in _y:
            _all_sum = _all_sum - _tempI.number()
        # включаем трасировку, если потеряли карту
        GLOBAL_TRACE = (_all_card != 52 or _all_sum)

        #  логическое соответствие !!!!!!!!!!!!!!!


        if GLOBAL_TRACE:
            print('карт->', _all_card, 'сумма->', _all_sum)
            # print(_message)
        return

    # анализ текущего состояния и поиск возможных ходов
    def search_moves(self):  # ищем активные шаги
        # первый проход
        if self.count_stack == 100:
            self.count_stack = 50

        # очистим список
        self.active_move.clear()

        # анализируем visible - перебор
        for _deck_from in self.play_visible:

            # смотрим колоду с которой хотим переложить
            _card_from = _deck_from.see_first_card()
            _card_from_e = _deck_from.see_end_card()
            # проверим OFF
            _card_to = self.play_off[_card_from.suit()].see_first_card()

            if (_card_from.range() == 12 and _card_to == Card(63)) or _card_to.next_card_for(_card_from):
                self.active_move.append(Move('vis',
                                             self.play_visible.index(_deck_from),
                                             _deck_from.list_of_cards.index(_card_from), _card_from,
                                             'off', _card_from.suit(), 0, _card_to))
            # проходим по визиблу
            for _deck_to in self.play_visible:
                # это не тот же столбец
                if _deck_to != _deck_from:
                    # смотрим только первую карту в колоде, на которую хотим переложить
                    _card_to = _deck_to.see_first_card()
                    _card_to_e = _deck_to.see_end_card()
                    # закрытая стопка пуста
                    _empty_inv_from = (self.play_invisible[self.play_visible.index(_deck_from)].see_first_card() == Card(63))

                    # проверим, что лежит единственной в колоде, чтобы цикл предотвратить
                    if _card_from == _card_from_e:
                        # разный цвет и следующая
                        if ((not _card_from.same_color(_card_to)) and _card_from.next_card_for(_card_to) \
                                and _card_to.range() != 12 and _card_to.range() != 11):
                            self.add_move('vis', self.play_visible.index(_deck_from),
                                          _deck_from.list_of_cards.index(_card_from), _card_from,
                                          'vis', self.play_visible.index(_deck_to),
                                          _deck_to.list_of_cards.index(_card_to), _card_to)
                    # то же, но для последней карты....
                    if (not _card_from_e.same_color(_card_to)) and _card_from_e.next_card_for(_card_to) and \
                            _card_to.range() != 12:
                        self.add_move('vis', self.play_visible.index(_deck_from),
                                      _deck_from.list_of_cards.index(_card_from_e), _card_from_e,
                                      'vis', self.play_visible.index(_deck_to), 0, _card_to)
                    #     переносим короля на пустой столбец, если под ним что-то есть
                    elif _card_from_e.range() == 11 and _card_to == Card(63) and not _empty_inv_from:
                        self.add_move('vis', self.play_visible.index(_deck_from),
                                      _deck_from.list_of_cards.index(_card_from_e), _card_from_e,
                                      'vis', self.play_visible.index(_deck_to), 0, _card_to)
                    # самое интересное, дорабатываем напильником
                    elif len(self.active_move) == 0:
                        q = 0
                        # ввести новый аттрибут - цикличный ход
                        # повторно пройти через все карты виз. Анализ вывести в отдельную функцию
                        #   не забыть о возможности обратного сноса
        # ++++++

        # проверим стек. Пока список ходов не пустой - стек не трогаем
        if self.play_st_i < len(self.play_stack.list_of_cards):
            _y = self.play_stack.list_of_cards[self.play_st_i]
            for _tempJ in self.play_visible:
                _x = _tempJ.see_first_card()
                if (not _y.same_color(_x)) and _y.next_card_for(_x) and _x.range() != 12:
                    self.add_move('stk', 0, self.play_st_i, _y,
                                  'vis', self.play_visible.index(_tempJ), _tempJ.list_of_cards.index(_x), _x)
                # vis пустой и в стеке король
                elif len(_tempJ.list_of_cards) == 0 and _y.range() == 11:
                    self.add_move('stk', 0, self.play_st_i, _y,
                                  'vis', self.play_visible.index(_tempJ), 0, _x)

            # проверим OFF для стека
            _z = _y.suit()
            _x = self.play_off[_z].see_first_card()
            if (_y.range() == 12 and _x.number() == 63) or _x.next_card_for(_y):
                self.add_move('stk', 0, self.play_st_i, _y, 'off', _z, 0, _x)

        # если ходов нет, сдвигаем стек
        if len(self.active_move) == 0:
            if self.play_st_i >= 63:
                self.play_st_i = self.play_st_i - 64

            self.play_st_i = self.play_st_i + 1
            # переворот стека
            if self.play_st_i > len(self.play_stack) - 1:
                self.play_st_i = 0
                #  снизим уровень счетчика проходов стека
                if self.count_stack == 50:
                    self.count_stack = 25
                elif self.count_stack == 25:
                    self.count_stack = 0

        if GLOBAL_TRACE:
            _x = 'Х-> '
            for _tempI in self.active_move:
                _x = _x + _tempI.__str__()
            print(_x)

        return

    def add_move(self, f1='', f2=0, f3=0, f4='', t='', t2=0, t3=0, t4=''):
        self.active_move.append(Move(f1, f2, f3, f4, t, t2, t3, t4))
        # нашли ход, счетчик проходов обнулим
        self.count_stack = 50
        return

    # анализ полученных ходов
    def move_optimize(self):
        return

    # делаем ход
    def do_move(self):
        self.count_moves = self.count_moves + 1
        if len(self.active_move):

            _move = self.active_move.pop(0)
            self.move_history.append(_move)
            _x = DeckOfCards(0)
            if _move.from_name == 'vis':
                _x.list_of_cards.extend(self.play_visible[_move.from_i].list_of_cards[:_move.from_j + 1])
                del self.play_visible[_move.from_i].list_of_cards[:_move.from_j + 1]

                if _move.to_name == 'vis':
                    _y = copy.deepcopy(_x.list_of_cards)
                    _y.reverse()
                    for _tempI in _y:
                        self.play_visible[_move.to_i].app_first_card(_tempI)
                elif _move.to_name == 'off':
                    for _tempI in _x.list_of_cards:
                        self.play_off[_move.to_i].app_first_card(_tempI)

            elif _move.from_name == 'stk':
                _tempI = self.play_stack.list_of_cards[self.play_st_i]
                del self.play_stack.list_of_cards[self.play_st_i]

                if _move.to_name == 'vis':
                    self.play_visible[_move.to_i].app_first_card(_tempI)
                elif _move.to_name == 'off':
                    self.play_off[_move.to_i].app_first_card(_tempI)
                # изменим индекс
                self.play_st_i = self.play_st_i + 63

        # откроем недостающее
        for _tempI in range(0, 7):
            if len(self.play_visible[_tempI]) == 0 and len(self.play_invisible[_tempI]) != 0:
                self.play_visible[_tempI].app_first_card(self.play_invisible[_tempI].get_first_card())

        if GLOBAL_TRACE:
            _x = 'И-> '
            for _tempI in self.move_history:
                _x = _x + _tempI.__str__()
            print(_x)
        return

        # приведение стола в порядок после хода

    def after_move(self):
        return

    # красиво печатаем виз
    def nice_look(self):

        _x = copy.deepcopy(self.play_visible)
        _l = 0
        _s = '\n'
        #  видимые карты
        for _i in _x:
            if len(_i.list_of_cards) > _l:
                _l = len(_i.list_of_cards)
        for _j in range(0, _l):
            for _i in range(0, 7):
                _tempI = _x[_i].get_end_card()
                if _tempI.number() == 63:
                    _s = _s + '|   '
                else:
                    _s = _s + '|' + _tempI.__str__()
            _s = _s + '\n'
        _s = _s + '^^^^^^^^^^^^^^^^^^^^^^^^^^^^'

        #  невидимые карты
        _l = 0
        _x = copy.deepcopy(self.play_invisible)
        _s2 = ''
        for _i in _x:
            if len(_i.list_of_cards) > _l:
                _l = len(_i.list_of_cards)
        for _j in range(0, _l):
            _s1 = ''
            for _i in range(0, 7):
                _tempI = _x[_i].get_first_card()
                if _tempI.number() == 63:
                    _s1 = _s1 + '|   '
                else:
                    _s1 = _s1 + '|' + _tempI.__str__()
            _s2 = _s2 + '\n' + _s1
        _s = _s + _s2

        return _s

    # печатаем игровой стол
    def __str__(self):
        _x = '\n*-----------------------------------------------------------------------------------------\n'
        for _tempI in self.play_off:
            _x = _x + _tempI.__str__()
        _x = '' + _x + '\n\nC->' + self.play_stack.__str__(self.play_st_i) + '\n'
        _x = _x + self.nice_look()
        _x = _x + '\nснос-> ' + str(len(self.move_history)) + '; ходов-> ' + str(self.count_moves)
        return _x


# ------------------------------------------------------------------------------------------
class Move(object):  # класс запись хода для удобства

    def __init__(self, _fromN='non', _fromI=0, _fromJ=0, _card1=Card(63), _toN='non', _toI=0, _toJ=0, _card2=Card(63)):
        # 'off', 'vis', 'stk'
        self.from_name = _fromN
        self.from_i = _fromI
        self.from_j = _fromJ
        self.card1 = _card1
        self.to_name = _toN
        self.to_i = _toI
        self.to_j = _toJ
        self.card2 = _card2
        return

    def __str__(self):
        return '|' + self.card1.__str__() + '->' + self.card2.__str__() + '|'

    def __eq__(self, other):
        return self.card1 == other.card1 and self.card2 == other.card2

    def __ne__(self, other):
        return self.card1 != other.card1 or self.card2 != other.card2
