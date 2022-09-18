'''

Исследование многопоточности

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

# счетчик итераций изврат конечно
gl_step_count = mp.Queue()
gl_step_count.put(0)

gl_log_deck = mp.Queue(maxsize=5000)
tasks_flow = mp.Queue()
tasks_flow = mp.Queue(maxsize=5000)

flag_will_new_task = mp.Event()
flag_will_new_task.set()
flag_log_ready = mp.Event()
flag_log_ready.clear()
flag_debug = mp.Event()
flag_debug.set()

gl_base_name: str = 'ALLCARD'



def check_table():

    return


# сохранение в памяти
def realtime_log_in(task_for_log):
    global gl_log_deck
    gl_log_deck.put(task_for_log)
    flag_log_ready.set()
    # print('регистрируем')
    return


# откроем БД
def open_db():
    # connection = None
    global gl_base_name
    connection = db.connect(user='vicdb', password='Qweqwe123_', database=gl_base_name, host='192.168.1.168',
                            port=3306)
    # print('открыли')
    return connection


#  закроем БД
def close_db(connection: object = None) -> object:
    if connection:
        connection.commit()
        connection.close()
        # print('закрыли')
    return


#  сохранение информации об эксперименте
def log_session(_all_time=0.0, _all_steps=0, _count_win=0, _avg_win=0):
    global gl_base_name
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
        # query = "SELECT MAX(ID) FROM {}.attempts".format(gl_base_name)
        # cur.execute(query)
        # _i = cur.fetchone()
        # _id = _i[0] + 1
        # query = "INSERT INTO {}.attempts (ID, ALL_TIME, ALL_STEPS, TIME_DES_AVG, COUNT_WIN, AVG_WIN, NOTE) VALUES ({}, {}, {}, {}, {}, {}, {}, '{}')".format(
        #     gl_base_name, _id, _all_time, _all_steps, _time_des_avg, _count_win, _avg_win, _text)
        # print(query)
        # cur.execute(query)
        close_db(_log_connection)
    return


# сохранение р  аздачи с результатами
def flow_log_step():
    global gl_log_deck
    # tfl: iii
    time_start = time.time()
    bufer_size = 1
    logging.info('{}: logger start...'.format(mp.current_process().name))
    _log_connection = open_db()
    flag_log_ready.wait(1)
    # print('пошел сброс...', )

    while not gl_log_deck.empty() or flag_log_ready.is_set() or flag_will_new_task.is_set():
        _ = 0
        # if gl_log_deck.qsize() > bufer_size or not flag_will_new_task.is_set():
        #     tfl = gl_log_deck.get(timeout=0.1)
            # проверим наличие такого ID
            # cur = _log_connection.cursor()
            # query = "SELECT ID_HASH FROM gametables WHERE ID_HASH = {}".format(tfl.start_hash)
            # cur.execute(query)
            # print(query)
            # if cur.fetchone():
            #     query = "UPDATE ALLCARD.gametables SET DECISION={}, DECK_JSON='{}', DECISION_TIME={}, MOVE_COUNT={} WHERE  ID_HASH={}".format(
            #         tfl.win, _json, tfl.solve_time, tfl.count_moves, tfl.start_hash)
            # else:
            #     query = "INSERT INTO ALLCARD.gametables(ID_HASH, DECISION, DECK_JSON, DECISION_TIME, MOVE_COUNT) VALUES ({}, {}, '{}', {}, {})".format(
            #         tfl.start_hash, tfl.win, _json, tfl.solve_time, tfl.count_moves)
            # cur.execute(query)
            # print(query)
            # print('завершение ID: ', tfl.start_hash)
            # print('переход: ')
        # else:
            # time.sleep(0.1)
            # print('{} не летим {}'.format(mp.current_process().name, gl_log_deck.qsize()))

        # if not flag_will_new_task.is_set() and gl_log_deck.empty() and tasks_flow.empty():
        #     flag_log_ready.clear()
        # elif gl_log_deck.empty():
        #     flag_log_ready.wait(0.1)

    close_db(_log_connection)

    # print('время сброса: ', round(time.time() - time_start, 5))
    logging.info('{}: logger stop ({})'.format(mp.current_process().name, round(time.time() - time_start, 4)))
    return


# генерируем поток раздач tasks_flow
def generator(total_steps=0):
    # global tasks_flow, flag_will_new_task
    logging.info('{}: generator start...'.format(mp.current_process().name))
    #
    # while total_steps != 0:
    #     tasks_flow.put(DeckOfCards([], True))
    #     total_steps = total_steps - 1
    #     flag_will_new_task.set()  # передернем очередь

        # замедлимся, чтобы стек не переполнить ...
        # if tasks_flow.qsize() > 1000:
        #     time.sleep(0.5)

    # flag_will_new_task.clear()
    logging.info('{}: generator stop'.format(mp.current_process().name))
    return


#  решение одной раздачи, данные берем из очереди tasks_flow
def solver():
    # global tasks_flow, flag_will_new_task, gl_step_count, gl_log_deck
    logging.info('{}: solving start '.format(mp.current_process().name))
    # print('{}: еще нет {}{}.'.format(mp.current_process().name, tasks_flow.empty(), flag_will_new_task.is_set()))
    #
    # while not tasks_flow.empty() or flag_will_new_task.is_set():
    #     table_for_solve: GameTable
    #     table_for_solve = GameTable(tasks_flow.get(timeout=0.01))
    #     table_for_solve.solve_table()
    #     gl_step_count.put(gl_step_count.get() + 1)
    #
    #     realtime_log_in(table_for_solve)
    #
    logging.info('{}: solving stop '.format(mp.current_process().name))
    return


#  проведение эксперимента с указанием количества попыток
def master_scheduler(total_steps=0):
    global tasks_flow, flag_will_new_task, gl_step_count
    if total_steps:
        _wins = 0
        all_proc = mp.cpu_count()

        step_start = time.time()
        tasks_flow = mp.Queue(maxsize=total_steps)

        logging.info('{}: Start '.format(mp.current_process().name))

        tasks = [(generator, total_steps)]
        tasks.extend([(flow_log_step,)])
        tasks.extend([(solver,)] * (all_proc))
        tasks.extend([(flow_log_step,)] * (all_proc - 1))

        with pool.ProcessPoolExecutor(max_workers=all_proc) as ex:
            futures = [ex.submit(*task) for task in tasks]

        _j = round(time.time() - step_start, 4)
        total_steps = gl_step_count.get()
        gl_step_count.put(total_steps)
        # realtime_log()
        # log_session(_j, total_steps, _wins, round(_wins / total_steps * 100, 2))
        log_session(_j, total_steps, _wins, 0)
        logging.info('{}: Stop '.format(mp.current_process().name))

    return


# начало программы
if __name__ == '__main__':
    # не сильно заморачиваемся с обработкой параметрогер в работе...
    _param = sys.argv

    round_amount = 10000           # <----- тут
    round_amount = round_amount if len(_param) == 1 else 10 ** (len(_param[1]) - 1)
    start_time = time.time()

    # начнем логгировать..
    logging.basicConfig(level=logging.INFO, filename="second_log.log", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
    logging.info("Start")


    # master_scheduler(round_amount)

    logging.info("Stop, всего {}".format(gl_step_count.get()))

# #  всякое -----------------------------------
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


# Подкласс QMainWindow для настройки основного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
app.exec()