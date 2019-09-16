import curses
from curses import panel

from time import sleep


class Marquee:
    def __init__(self, string, speed, stdscreen, stop_event):
        self.parent = stdscreen
        self.window = stdscreen.subwin(1, self.parent.getmaxyx()[1], 0, 0)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.speed = speed
        self.string = string

        self.scroll = 0

        self.stop_event = stop_event

    def display(self):
        self.panel.top()
        self.panel.show()

        while not self.stop_event.is_set():
            self.window.clear()
            self.window.refresh()

            self.scroll += self.speed

            if self.scroll >= self.parent.getmaxyx()[1]:
                self.scroll = 0

            num_chars_to_show = self.parent.getmaxyx()[1] - self.scroll - 1

            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
            self.window.addstr(0, self.scroll, self.string[:num_chars_to_show], curses.color_pair(2))

            if num_chars_to_show < len(self.string):
                leading_chars = len(self.string[:num_chars_to_show])
                self.window.addstr(0, 0, self.string[leading_chars:], curses.color_pair(2))

            self.window.refresh()

            sleep(0.25)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
