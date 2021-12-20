import random
import time
import tkinter
from tkinter import Tk, Label, Frame
from typing import Dict, Tuple


class CellFrame(Frame):
    __states = ('RedFlag', '')
    __current_state = ''
    __bombs_next_to_cell = 0

    def __init__(self, *args, x: int, y: int, **kwargs):
        self.posx, self.posy = x, y
        super().__init__(*args, **kwargs)
        self.states = self.iter_states()
        self.grid(row=x, column=y)
        self.frame_label = Label(
            self,
            width=7,
            height=4,
            bg='gray',
            borderwidth=2,
            relief="groove"
        )
        self.frame_label.bind("<Button-1>", self.open)
        self.frame_label.bind("<Button-2>", self.state_before_open)
        self.frame_label.pack()

    @property
    def bombs_counter(self):
        return self.__bombs_next_to_cell

    @bombs_counter.setter
    def bombs_counter(self, value):
        self.__bombs_next_to_cell += 1


    def state_before_open(self, event):
        self.__current_state = next(self.states)
        self.frame_label.config(text=self.__current_state)

    def iter_states(self):
        states = self.__states
        while True:
            for state in states:
                yield state

    def open(self, event):
        if self.__current_state == 'RedFlag':
            return
        self.frame_label.config(
            text=self.bombs_counter if self.bombs_counter else '',
            bg='darkgrey',
        )

    def send_bomb_state(self, matrix: Dict[Tuple[int, int], 'CellFrame']):
        pass


class BombCellFrame(CellFrame):
    def open(self, event):
        self.frame_label.config(
            text="BOOM",
            bg="red"
        )

    def send_bomb_state(self, matrix: Dict[Tuple[int, int], CellFrame]):
        posx, posy = self.posx, self.posy
        increments = (-1, 0, 1)
        for x in increments:
            for y in increments:
                try:
                    key_x, key_y = posx + x, posy + y
                    matrix[(key_x, key_y)].bombs_counter = True
                except KeyError:
                    pass


class App(Tk):
    _title = "SAPER"
    _geometry = "500x500"

    def __init__(self):
        super().__init__()
        self.app_conf()

        bomb = [BombCellFrame for x in range(10)]
        cell = [CellFrame for x in range(54)]
        frame_values = bomb + cell
        random.shuffle(frame_values)

        frames_list = {
            (x, y): frame_values.pop()(x=x, y=y) for x in range(8) for y in range(8)
        }
        for cell in frames_list.values():
            cell.send_bomb_state(frames_list)


    def app_conf(self):
        self.title(string=self._title)
        self.geometry(newGeometry=self._geometry)


if __name__ == "__main__":
    app = App()
    app.mainloop()