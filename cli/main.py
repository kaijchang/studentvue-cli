import curses
from curses import wrapper

from colorama import init, Fore, Back, Style
import threading

from .Menu import Menu
from .Marquee import Marquee


stop_event = threading.Event()


class MenuThread(threading.Thread):
    def __init__(self, stdscreen):
        super().__init__()
        self.screen = stdscreen

    def run(self):
        submenu_items = [
            ('beep', curses.beep),
            ('flash', curses.flash)
        ]
        submenu = Menu(submenu_items, self.screen, True)

        main_menu_items = [
            ('beep', curses.beep),
            ('flash', curses.flash),
            ('submenu', submenu.display),
            ('exit', stop_event.set)
        ]

        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()


class MarqueeThread(threading.Thread):
    def __init__(self, stdscreen, stop_event):
        super().__init__()
        self.screen = stdscreen
        self.stop_event = stop_event

    def run(self):
        marquee = Marquee('StudentVue - by Kai Chang', 1, self.screen, self.stop_event)
        marquee.display()


class Jasper:
    def __init__(self, stdscreen):
        self.screen = stdscreen
        init()
        curses.curs_set(0)

        menu_thread = MenuThread(stdscreen)
        menu_thread.setDaemon(True)
        menu_thread.start()

        marquee_thread = MarqueeThread(stdscreen, stop_event)
        marquee_thread.setDaemon(True)
        marquee_thread.start()

        while not stop_event.is_set():
            pass


def main():
    wrapper(Jasper)
