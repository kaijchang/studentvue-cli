import curses
from curses import panel


# https://stackoverflow.com/a/14205494
class Menu:
    def __init__(self, items, stop_event, stdscreen, submenu=False):
        self.window = stdscreen.subwin(1, 0)
        self.window.keypad(True)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.stop_event = stop_event

        if submenu:
            self.items.append(('Back', 'BACK'))
        else:
            self.items.append(('Exit', 'EXIT'))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while not self.stop_event.is_set():
            self.window.refresh()

            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = item[0]
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                action = self.items[self.position][1]
                if action == 'BACK':
                    break
                elif action == 'EXIT':
                    self.stop_event.set()
                else:
                    action()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
