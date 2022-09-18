'''

Исследование сходимости пасьянса косынка

'''
import concurrent.futures as pool
import json
import logging
import multiprocessing as mp
import sys
import time
import pymysql as db
import os
import platform
import re
import subprocess

from cardclass import Card
from cardclass import DeckOfCards
from cardclass import GameTable

# КАКие-ТО ХРЕНОВАЯ ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ. НЕ РАБОТАЕТ МЕЖДУ МОДУЛЯМИ
gl_deck_new = []
gl_deck_new.extend(Card(_I) for _I in range(0, 52))

# счетчик итераций изврат конечно
gl_step_count = mp.Queue()
gl_step_count.put(0)

# card_deck_list = mp.Queue()
card_deck_list = mp.Queue(maxsize=1000)
gl_log_deck = mp.Queue()
# gl_log_deck = mp.Queue(maxsize=1000)

flag_will_be_new = mp.Event()
flag_will_be_new.set()
flag_log_ready = mp.Event()
flag_log_ready.clear()
flag_debug = mp.Event()
flag_debug.set()


# сохранение в памяти
def realtime_log_in(table_for_log):
    global gl_log_deck
    gl_log_deck.put(table_for_log)
    flag_log_ready.set()
    return


# откроем БД
def open_db():
    # connection = None
    connection = db.connect(user='vicdb', password='Qweqwe123_', database='ALLCARD', host='192.168.1.168',
                            port=3306)
    # print('открыли')
    return connection


#  закроем БД
def close_db(connection=None):
    if connection:
        connection.commit()
        connection.close()
        # print('закрыли')
    return


#  сохранение информации об эксперименте
def log_trial(_all_time=0.0, _all_steps=0, _count_win=0, _avg_win=0):
    _log_connection = open_db()
    if _log_connection:
        _id = 0
        cur = _log_connection.cursor()
        _time_des_avg = round(_all_time / _all_steps, 5)
        _i = ''

        # соберем инфо по железу
        _text = platform.system()
        if _text == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).decode().strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    _i = re.sub('.*model name.*:', "", line, 1)
            _k = os.uname()
            _text = '(' + _text + ', ' + _k[3] + '):' + _i + '; ' + _k[1]
        # проверим наличие такого ID. Лишних проверок не делаем....
        query = "SELECT MAX(ID) FROM ALLCARD.attempts"
        cur.execute(query)
        _i = cur.fetchone()
        _id = _i[0] + 1
        query = "INSERT INTO ALLCARD.attempts (ID, ALL_TIME, ALL_STEPS, TIME_DES_AVG, COUNT_WIN, AVG_WIN, NOTE) VALUES ({}, {}, {}, {}, {}, {}, '{}')".format(
            _id, _all_time, _all_steps, _time_des_avg, _count_win, _avg_win, _text)
        # print(query)
        cur.execute(query)
        close_db(_log_connection)
    return


# сохранение р  аздачи с результатами
def realtime_log_out():
    global gl_log_deck
    tfl: GameTable
    time_start = time.time()
    bufer_size = 10
    logging.info('{}: logger start...'.format(mp.current_process().name))
    _log_connection = open_db()
    flag_log_ready.wait(1)

    while not gl_log_deck.empty() or flag_log_ready.is_set() or flag_will_be_new.is_set():
        if gl_log_deck.qsize() > bufer_size or not flag_will_be_new.is_set():

            tfl = gl_log_deck.get(timeout=0.1)
            _json = {i + 1: tfl.start_deck.list_of_cards[i].number() for i in range(52)}
            _json = json.dumps(_json)

            # проверим наличие такого ID
            cur = _log_connection.cursor()
            query = "SELECT ID_HASH FROM gametables WHERE ID_HASH = {}".format(tfl.start_hash)
            cur.execute(query)
            if cur.fetchone():
                query = "UPDATE ALLCARD.gametables SET DECISION={}, DECK_JSON='{}', DECISION_TIME={}, MOVE_COUNT={} WHERE  ID_HASH={}".format(
                    tfl.win, _json, tfl.solve_time, tfl.count_moves, tfl.start_hash)
            else:
                query = "INSERT INTO ALLCARD.gametables(ID_HASH, DECISION, DECK_JSON, DECISION_TIME, MOVE_COUNT) VALUES ({}, {}, '{}', {}, {})".format(
                    tfl.start_hash, tfl.win, _json, tfl.solve_time, tfl.count_moves)
            cur.execute(query)
        else:
            time.sleep(0.1)

        if not flag_will_be_new.is_set() and gl_log_deck.empty() and card_deck_list.empty():
            flag_log_ready.clear()
        elif gl_log_deck.empty():
            flag_log_ready.wait(0.1)

    close_db(_log_connection)

    logging.info('{}: logger stop ({})'.format(mp.current_process().name, round(time.time() - time_start, 4)))
    return


# генерируем поток раздач card_deck_list
def create_decks(total_steps=0):
    global card_deck_list, flag_will_be_new
    logging.info('{}: generator start...'.format(mp.current_process().name))

    while total_steps != 0:
        card_deck_list.put(DeckOfCards([], True))
        total_steps = total_steps - 1
        flag_will_be_new.set()  # передернем очередь

        # замедлимся, чтобы стек не переполнить ...
        if card_deck_list.qsize() > 1000:
            time.sleep(0.5)

    flag_will_be_new.clear()
    logging.info('{}: generator stop'.format(mp.current_process().name))
    return


#  решение одной раздачи, данные берем из очереди card_deck_list
def solve_tables():
    global card_deck_list, flag_will_be_new, gl_step_count, gl_log_deck
    logging.info('{}: solving start '.format(mp.current_process().name))

    while not card_deck_list.empty() or flag_will_be_new.is_set():
        table_for_solve: GameTable
        table_for_solve = GameTable(card_deck_list.get(timeout=0.01))
        table_for_solve.solve_table()
        gl_step_count.put(gl_step_count.get() + 1)

        realtime_log_in(table_for_solve)

    logging.info('{}: solving stop '.format(mp.current_process().name))
    return


#  проведение эксперимента с указанием количества попыток
def start_solving(total_steps=0):
    global card_deck_list, flag_will_be_new, gl_step_count
    if total_steps:
        _wins = 0
        all_proc = mp.cpu_count()

        step_start = time.time()
        card_deck_list = mp.Queue(maxsize=total_steps)

        logging.info('{}: Start '.format(mp.current_process().name))

        # сначала запускаем лог, он самый медленный
        tasks = [(realtime_log_out,)]
        tasks.extend([(create_decks, total_steps)])
        tasks.extend([(solve_tables,)] * (all_proc-1))
        tasks.extend([(realtime_log_out,)] * (all_proc - 1))

        with pool.ProcessPoolExecutor(max_workers=all_proc) as ex:
            futures = [ex.submit(*task) for task in tasks]

        _j = round(time.time() - step_start, 4)
        total_steps = gl_step_count.get()
        gl_step_count.put(total_steps)
        log_trial(_j, total_steps, _wins, 0)
        logging.info('{}: Stop '.format(mp.current_process().name))

    return


# начало программы
if __name__ == '__main__':
    # не сильно заморачиваемся с обработкой параметрогер в работе...
    _param = sys.argv
    print("СТАРТ.")

    round_amount = 10           # <----- тут
    round_amount = round_amount if len(_param) == 1 else 10 ** (len(_param[1]) - 1)
    start_time = time.time()

    # начнем логгировать..
    logging.basicConfig(level=logging.INFO, filename="first_log.log", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
    logging.info("Start")

    start_solving(round_amount)

    logging.info("Stop, всего {}".format(gl_step_count.get()))
    print("ВСЕ.")

# #  всякое
