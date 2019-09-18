import curses
from curses import wrapper

import os
import time
import threading
from studentvue import StudentVue

from .Menu import Menu
from .Marquee import Marquee


def run_menu(studentvue, stop_event, screen):
    cache = {}

    def load_class_info(class_):
        def wrapped():
            start_load(screen)
            if class_.name in cache:
                class_info = cache[class_.name]
            else:
                class_info = studentvue.get_class_info(class_)
                cache[class_.name] = class_info

            if class_info is not None:
                class_menu_items = [('%s: %s | %d%% | %s' % (class_.period, class_.name, class_info['score'],
                                                             class_info['mark']), lambda: None)]
                for assignment in class_info['assignments']:
                    assignment_menu_items = [
                        ('Name: %s' % assignment.name, lambda: None),
                        ('Due Date: %s' % assignment.date.strftime('%x'), lambda: None),
                        ('Score: %s/%s' % (assignment.score, assignment.max_score), lambda: None)
                    ]
                    assignment_menu = Menu(assignment_menu_items, stop_event, screen, submenu=True)
                    class_menu_items.append(('%s: %s' % (assignment.date.strftime('%x'), assignment.name),
                                             assignment_menu.display))
                class_menu = Menu(class_menu_items, stop_event, screen, submenu=True)
                cache[class_.name] = class_menu
                class_menu.display()
            else:
                screen.clear()
                y, x = screen.getmaxyx()
                string = 'The Class Has No Grades'
                screen.addstr(round(y / 3), round(x / 2 - len(string) / 2), string, curses.color_pair(2))
                screen.refresh()
                time.sleep(1)
                screen.clear()
                screen.refresh()

        return wrapped

    schedule = studentvue.get_schedule()
    schedule_menu_items = [('%s: %s' % (class_.period, class_.name), load_class_info(class_)) for class_ in schedule]

    schedule_menu = Menu(schedule_menu_items, stop_event, screen, submenu=True)

    main_menu_items = [
        ('SCHEDULE', schedule_menu.display),
    ]

    main_menu = Menu(main_menu_items, stop_event, screen)
    main_menu.display()


def run_marquee(studentvue, stop_event, screen):
    marquee = Marquee('Name: %s - StudentVue - ID: %s' % (studentvue.name, studentvue.id_),
                      1, screen, stop_event)
    marquee.display()


def start_load(stdscreen):
    stdscreen.clear()
    y, x = stdscreen.getmaxyx()
    string = 'Loading...'
    stdscreen.addstr(round(y / 3), round(x / 2 - len(string) / 2), string, curses.color_pair(1))
    stdscreen.refresh()


class Jasper:
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
        stdscreen.scrollok(0)
        stdscreen.keypad(True)

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
        start_load(stdscreen)

        credentials = (os.environ['STUDENTVUE_USER'], os.environ['STUDENTVUE_PASS'], os.environ['STUDENTVUE_DOMAIN'])
        studentvue = StudentVue(*credentials)

        stop_event = threading.Event()

        menu_thread = threading.Thread(target=run_menu, args=(studentvue, stop_event, stdscreen))
        menu_thread.setDaemon(True)
        menu_thread.start()

        marquee_thread = threading.Thread(target=run_marquee, args=(studentvue, stop_event, stdscreen))
        marquee_thread.setDaemon(True)
        marquee_thread.start()

        while not stop_event.is_set():
            pass


def main():
    wrapper(Jasper)
