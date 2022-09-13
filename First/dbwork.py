'''
Функции работы с SQL сервером
'''
from mysql import connector as db
import cardclass as cd
import pickle
import json
import marshal as msh


def save_to_sql(_in_table=cd.GameTable()):
    _in_table: cd.GameTable

    Error = []

    try:
        conn = db.connect(user='vicdb', password='Qweqwe123_', database='ALLCARD', host='192.168.1.168', port=3306)
        cur = conn.cursor()

        # готовим информацию к сохранению
        _deck_num, _k = [], []
        _deck_num.extend(_in_table.start_deck.list_of_cards[i].number() for i in range(0, 52))
        _k = {i + 1: _deck_num[i] for i in range(52)}
        _json = json.dumps(_k)

        # проверим наличие такого ID
        query = "SELECT ID_HASH FROM gametables WHERE ID_HASH = {}".format(_in_table.start_hash)
        cur.execute(query)

        if cur.fetchone():
            query = "UPDATE gametables SET DECISION={}, CARD_DECK='{}', DECK_JSON='{}', DECISION_TIME={}, MOVE_COUNT={} WHERE  ID_HASH={}".format(
                _in_table.win, _deck_num, _json, _in_table.desicion_time, _in_table.count_moves, _in_table.start_hash)
        else:
            query = "INSERT INTO gametables(ID_HASH, DECISION,  CARD_DECK, DECK_JSON, DECISION_TIME, MOVE_COUNT) VALUES ({}, {}, '{}', '{}', {}, {})".format(
                _in_table.start_hash, _in_table.win, _deck_num, _json, _in_table.desicion_time, _in_table.count_moves)

        # print(query)
        cur.execute(query)
        conn.commit()
        conn.close()

    except Error as error:
        print(f'<h2>Ошибка подключения к БД: {error} </h2>')

    return
