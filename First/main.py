import copy
import random
import hashlib


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

    def number(self):
        return self.card_num if isinstance(self.card_num, int) and 0 <= self.card_num <= 51 else 63

    def range(self):
        return self.card_num >> 2 if self.card_num != 63 else 63

    # масть 3 -> 000011
    def suit(self):
        return self.card_num & 3 if self.card_num != 63 else 63

    # один цвет
    def same_color(self, _card):
        return self.suit() % 2 == _card.suit() % 2

    # следующая карта
    def next_card(self, _card: object) -> object:
        return (_card.range() - self.range() == 1) or (_card.range() == 0 and self.range() == 12)

    # расшифровка карты
    def __str__(self):
        _tempI = ''
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
        return _tempI


# ---------------------------------------------------------------------------------------------
class PrintStyle:
   UNDER = '\033[4m'
   END = '\033[0m'


# определяем класс колода карт, если вход пустой, то формируем раздачу 52 карты
class DeckOfCards(object):

    def __init__(self, _input_list=[]):  # при инициации, или входной список или последовательный набор карт
        self.list_of_cards = []

        if isinstance(_input_list, int) and _input_list != 0:  # если чиcло, то создаем список длинной _input_list с пустыми картами
            for _tempI in range(_input_list):
                self.list_of_cards.append(Card())
        elif isinstance(_input_list, int) and _input_list == 0:  # создаем пустой список
            self.list_of_cards = []
        else:  # ничего нет - даем 52 карты
            for _tempI in range(52):
                self.list_of_cards.append(Card(_tempI))
        return

    def see_first_card(self):
        return self.list_of_cards[0] if len(self) else Card(63)

    def see_end_card(self):
        return self.list_of_cards[len(self) - 1] if len(self) >= 1 else Card(63)

    def get_first_card(self):
        _x = None
        if len(self) > 0:
            _x = self.list_of_cards.pop(0)
        return _x

    def get_end_card(self):
        _x = None
        if len(self) > 0:
            _x = self.list_of_cards.pop()
        return _x

    def app_first_card(self, _app_card):
        _x = [_app_card]
        _x.extend(self.list_of_cards)
        self.list_of_cards = copy.deepcopy(_x)
        #self.list_of_cards.append(_app_card)
        #self.list_of_cards.reverse()
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
        self.play_off = []
        for _tempI in range(4):  self.play_off.append(DeckOfCards(0))

        self.play_stack = DeckOfCards(0)
        self.play_st_i = 0
        # если 100, значит это первый проход. N - количество проходов стека без сноса
        self.count_stack = 100
        self.play_visible = []
        for _tempI in range(7):  self.play_visible.append(DeckOfCards(0))
        self.play_invisible = []
        for _tempI in range(7):  self.play_invisible.append(DeckOfCards(0))
        self.active_move = []
        self.move_history = []

        if len(_input_deck) == 52:          # раздаем карты
            _x = 0
            self.play_visible[0].app_first_card(_input_deck.get_first_card())
            for _x in range(1, 7):
                for _tempI in range(_x, 7):
                    self.play_invisible[_tempI].app_first_card(_input_deck.get_first_card())
                self.play_visible[_x].app_first_card(_input_deck.get_first_card())
            for _tempI in range(1, len(_input_deck.list_of_cards)+1):
                self.play_stack.app_end_card(_input_deck.get_first_card())
        return

    # анализ текущего состояния и поиск возможных ходов
    def search_moves(self):     # ищем активные шаги
        # следующую карту в стеке если больше нет ходов
        if self.count_stack != 100:
            if len(self.active_move) == 0:
                if self.play_st_i >= 63:
                    self.play_st_i = self.play_st_i - 63
                self.play_st_i = self.play_st_i + 1 if len(self.play_stack) - 2 > j.play_st_i else 0
        else:
            self.count_stack = 0

        # очистим список
        self.active_move.clear()
        # анализируем visible - перебор
        for _heapI in self.play_visible:
            # смотрим карту в столбце
            for _tempI in _heapI.list_of_cards:
                # проверим OFF
                _y = _tempI.suit()
                _x = self.play_off[_y].see_first_card()
                if (_tempI.range() == 12 and _x != Card(63)) or _x.next_card(_tempI):
                    self.active_move.append(Move('vis',
                                                 self.play_visible.index(_heapI),
                                                 _heapI.list_of_cards.index(_tempI), _tempI,
                                                 'off', _y, 0, _x))

                # проходим по визиблу
                for _tempJ in self.play_visible:
                    _x = _tempJ.see_first_card()
                    # это не тот же столбец
                    if _tempJ != _heapI:
                        # разный цвет и следующая
                        if (not _tempI.same_color(_x)) and _tempI.next_card(_x) and _x.range() != 12:
                            self.active_move.append(Move('vis',
                                                    self.play_visible.index(_heapI),
                                                         _heapI.list_of_cards.index(_tempI),
                                                         _tempI,
                                                        'vis',
                                                        self.play_visible.index(_tempJ),
                                                        _tempJ.list_of_cards.index(_x), _x))
                        # проверка возможности сноса Короля на пустое место!!!!!!  доаботать когда пойдут сдвиги
                        if _tempI.range() == 11 and _x.number() == 63 \
                                and len(self.play_invisible[self.play_visible.index(_tempJ)]) == 0:
                            self.active_move.append(Move('vis',
                                                         self.play_visible.index(_heapI),
                                                         _heapI.list_of_cards.index(_tempI),
                                                         _tempI,
                                                         'vis',
                                                         self.play_visible.index(_tempJ),
                                                         0, _x))

        # проверим карту стека. Пока список ходов не пустой - стек не двигаем
        if self.play_st_i >= 63:
            _y = self.play_stack.list_of_cards[self.play_st_i]
            for _tempJ in self.play_visible:
                _x = _tempJ.see_first_card()
                if (not _y.same_color(_x)) and _y.next_card(_x) and _x.range() != 12:
                    self.active_move.append(Move('stk', 0, self.play_st_i, _y,
                                             'vis',
                                             self.play_visible.index(_tempJ),
                                             _tempJ.list_of_cards.index(_x), _x))
            # проверим OFF для стека
            _z = _y.suit()
            _x = self.play_off[_z].see_first_card()
            if (_y.range() == 12 and _x.number() == 63) or _x.next_card(_y):
                self.active_move.append(Move('stk', 0, self.play_st_i, _y,
                                             'off', _z, 0, _x))
        return

    # делаем ход
    def get_move(self):
        if len(self.active_move):
            _move = self.active_move.pop(0)
            self.move_history.append(_move)
            _x = DeckOfCards(0)
            if _move.from_name == 'vis':
                _x.list_of_cards.extend(self.play_visible[_move.from_i].list_of_cards[_move.from_j:])
                del self.play_visible[_move.from_i].list_of_cards[_move.from_j:]

                if _move.to_name == 'vis':
                    for _tempI in _x.list_of_cards:
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
                    for _tempI in _x.list_of_cards:
                        self.play_off[_move.to_i].app_first_card(_tempI)
                # уменьшим счетчик
                self.play_st_i = self.play_st_i + 63

        # откроем недостающее
        for _tempI in range(0, 7):
            if len(self.play_visible[_tempI]) == 0 and len(self.play_invisible[_tempI]) != 0:
                self.play_visible[_tempI].app_first_card(self.play_invisible[_tempI].get_first_card())

    # приведение стола в порядок после хода
    def after_move(self):
        return
    # печатаем игровой стол
    def __str__(self):
        _x = '\n*-----------------------------------------------------------------------------------------\n'
        for _tempI in self.play_off:
            _x = _x + _tempI.__str__()
        _x = '' + _x + ' <|*|> ' + self.play_stack.__str__(self.play_st_i) + '\n'

        for _tempI in self.play_invisible:
            _x = _x + _tempI.__str__()
        _x = _x + '\n'
        for _tempI in self.play_visible:
            _x = _x + _tempI.__str__()
        _x = _x + '\n\n A**> '
        for _tempI in self.active_move:
            _x = _x + _tempI.__str__()
        _x = _x + '\n И**> '
        for _tempI in self.move_history:
            _x = _x + _tempI.__str__()

        return _x


# ------------------------------------------------------------------------------------------
class Move(object):             # класс запись хода для удобства

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
#       return '|' + self.card1.__str__() + '->' + self.card2.__str__() + '(' + self.from_name + '/' + str(self.from_i)+ '-' + str(self.from_j)  \
#               + '->' + self.to_name + '/' + str(self.to_i)+ '-' + str(self.to_j)  + ')|'


# начало программы
if __name__ == '__main__':

    k = DeckOfCards()
    k.rand()

    j = GameTable(k)
    j.search_moves()
    print(j)
    while len(j.active_move) > 0:
        j.get_move()
        j.after_move()
        j.search_moves()
        print(j)

