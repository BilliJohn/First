'''
Функции работы с SQL сервером
'''
from mysql import connector as db
# import sqlite3 as sq

import cardclass as cd
import pickle


def save_to_sql(_x=cd.GameTable()):
    _x: GameTable
    print('Подключение к БД MariaDB')
    Error = []

    try:
        conn = db.connect(user='vicdb', password='Qweqwe123_', database='ALLCARD', host='192.168.1.168',
                                     port=3306)
        cursor = conn.cursor()
        query = " INSERT INTO gametables(ID_HASH, CARD_DECK, MOVE_HISTORY, NOTES) VALUES (?, ?, ?, ?)"

        # _x.start_hash, _x.start_deck, _x.move_history, _x.count_moves
        conn.execute(query, (_x.start_hash, _x.start_deck, _x.move_history, _x.count_moves))

        print('<h2>Подключение к базе данных выполнено успешно</h2>')
        conn.close()
    except Error as error:
        print(f'<h2>Ошибка подключения к БД: {error} </h2>')

    return

