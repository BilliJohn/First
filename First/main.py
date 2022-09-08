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
        return self.list_of_cards[0] if len(self) else None

    def see_end_card(self):
        return self.list_of_cards[len(self) - 1] if len(self) >= 1 else None

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

    def app_first_card(self, _app_card=63):
        self.list_of_cards.reverse()
        self.list_of_cards.append(_app_card)
        self.list_of_cards.reverse()
        return

    def app_end_card(self, _app_card=63):
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

    def __len__(self):
        return len(self.list_of_cards)


# --------------------------------------------------------------------------------------------------

# определяем класс игровой стол (косынка)
class GameTable(object):

    def __init__(self, _input_deck=DeckOfCards(0)):
        self.play_off = []
        for _tempI in range(4):  self.play_off.append(DeckOfCards(0))

        self.play_stack = DeckOfCards(0)
        self.play_stack_index = 0
        self.play_visible = []
        for _tempI in range(7):  self.play_visible.append(DeckOfCards(0))
        self.play_invisible = []
        for _tempI in range(7):  self.play_invisible.append(DeckOfCards(0))
        self.active_move = []

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

    def search_moves(self):     # ищем активные шаги

        self.active_move.append(Move())

        return

    def __str__(self):  # печатаем игровой стол
        _x = ''
        for _tempI in self.play_off: _x = _x + _tempI.__str__()
        _x = '[' + _x + '] <|*|> ' + self.play_stack.__str__(self.play_stack_index) + '\n'

        for _tempI in self.play_invisible:
            _x = _x + _tempI.__str__()
        _x = _x + '\n'
        for _tempI in self.play_visible:
            _x = _x + _tempI.__str__()
        _x = _x + '\n A**> '
        for _tempI in self.active_move:
            _x = _x + _tempI.__str__()

        return _x


# ------------------------------------------------------------------------------------------
class Move(object):             # класс ход для удобства

    def __init__(self, _fromN='non', _fromI=0, _toN='non', _toI=0):
        # 'off', 'vis', 'stk'
        self.from_name = _fromN
        self.from_index = _fromI
        self.to_name = _toN
        self.to_index = _toI
        return

    def __str__(self):
        return '|' + self.from_name + '/' + str(self.from_index) + '->' + self.to_name + '/' + str(self.to_index) + '|'


# начало программы
if __name__ == '__main__':

    k = DeckOfCards()
    #k.rand()

    j = GameTable(k)
    j.search_moves()
    print(j)

