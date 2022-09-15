'''

Функции работы с SQL сервером (mariaDB)

'''
from mysql import connector as db
import cardclass as cd
import json
import os, platform, subprocess, re


# откроем БД
def open_db():
    connection = None
    Error = []
    try:
        connection = db.connect(user='vicdb', password='Qweqwe123_', database='ALLCARD', host='192.168.1.168',
                                port=3306)
    except Error as error:
        print(f'Ошибка подключения к БД: {error}')
    return connection


#  закроем БД
def close_db(connection=None):
    if connection:
        connection.commit()
        connection.close()
    return


def get_debug(_log_connection=None):
    _in_table: cd.GameTable

    if _log_connection:

        if cur.fetchone():
            query = "UPDATE gametables SET DECISION={}, CARD_DECK='{}', DECK_JSON='{}', DECISION_TIME={}, MOVE_COUNT={} WHERE  ID_HASH={}".format(
                _in_table.win, _deck_num, _json, _in_table.desicion_time, _in_table.count_moves, _in_table.start_hash)
        else:
            query = "INSERT INTO gametables(ID_HASH, DECISION,  CARD_DECK, DECK_JSON, DECISION_TIME, MOVE_COUNT) VALUES ({}, {}, '{}', '{}', {}, {})".format(
                _in_table.start_hash, _in_table.win, _deck_num, _json, _in_table.desicion_time, _in_table.count_moves)
        cur.execute(query)
    return


# сохранение раздачи с результатами
def log_deck(_in_table=cd.GameTable(), _log_connection=None):
    _in_table: cd.GameTable

    if _log_connection:
        # готовим информацию к сохранению
        _deck_num, _k = [], []
        _deck_num.extend(_in_table.start_deck.list_of_cards[i].number() for i in range(0, 52))
        _k = {i + 1: _deck_num[i] for i in range(52)}
        _json = json.dumps(_k)

        # проверим наличие такого ID
        cur = _log_connection.cursor()
        query = "SELECT ID_HASH FROM gametables WHERE ID_HASH = {}".format(_in_table.start_hash)
        cur.execute(query)

        if cur.fetchone():
            query = "UPDATE gametables SET DECISION={}, CARD_DECK='{}', DECK_JSON='{}', DECISION_TIME={}, MOVE_COUNT={} WHERE  ID_HASH={}".format(
                _in_table.win, _deck_num, _json, _in_table.desicion_time, _in_table.count_moves, _in_table.start_hash)
        else:
            query = "INSERT INTO gametables(ID_HASH, DECISION,  CARD_DECK, DECK_JSON, DECISION_TIME, MOVE_COUNT) VALUES ({}, {}, '{}', '{}', {}, {})".format(
                _in_table.start_hash, _in_table.win, _deck_num, _json, _in_table.desicion_time, _in_table.count_moves)
        cur.execute(query)
    return


#  сохранение информации об эксперименте
def log_attemp(_log_connection=None, _all_time=0.0, _all_steps=1, _count_win=0, _avg_win=0):
    _id = 0
    if _log_connection:
        cur = _log_connection.cursor()
        _time_des_avg = round(_all_time / _all_steps, 3)
        # соберем инфо по железу
        _text = platform.system()
        if _text == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).decode().strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    _i = re.sub(".*model name.*:", "", line, 1)
            _k = os.uname()
            _text = '(' + _text + ', ' + _k[3] + '):' + _i + '; ' + _k[1]

        # проверим наличие такого ID. Лишних проверок не делаем....
        query = "SELECT MAX(ID) FROM attempts"
        cur.execute(query)
        _i = cur.fetchone()
        _id = _i[0] + 1

        query = "INSERT INTO attempts (ID, ALL_TIME, ALL_STEPS, TIME_DES_AVG, COUNT_WIN, AVG_WIN, NOTE) VALUES ({}, {}, {}, {}, {}, {}, '{}')".format(
            _id, _all_time, _all_steps, _time_des_avg, _count_win, _avg_win, _text)
        cur.execute(query)
    return
