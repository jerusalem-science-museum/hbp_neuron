from tkinter import *


class Slide(LabelFrame):
    RADIO_BUTTONS_TEXT = ['Small', 'Medium', 'Big', 'Large']
    PADS = {'padx': 5, 'pady': 5}
    SLIDES = []

    def __init__(self, master=None, size=len(RADIO_BUTTONS_TEXT), command=None, cnf={}, **kw):
        LabelFrame.__init__(self, master=master, cnf=cnf, **kw)
        self.max_value = size - 1
        self.value = IntVar()
        self.scrollbar = Scale(master, showvalue=0, to=self.max_value, variable=self.value,
                               command=command)
        self.scrollbar.pack(in_=self, side=LEFT, fill=Y, **self.PADS)

        self.radio_frame = Frame(master)
        self.radio_frame.pack(in_=self, side=LEFT)

        self.radio_buttons = []
        for i in range(size):
            radio_button = Radiobutton(master, text=self.RADIO_BUTTONS_TEXT[i],
                                       variable=self.value, value=i, command=command)
            radio_button.pack(in_=self.radio_frame, side=TOP, anchor=W)
            self.radio_buttons.append(radio_button)
        self.SLIDES.append(self)

    def set_value(self, value):
        value = int(value)
        if value < 0:
            value = 0
        elif value > self.max_value:
            value = self.max_value

        self.scrollbar.set(value)

    def get_value(self):
        return self.value.get()

    @classmethod
    def get_values(cls):
        values = 0
        for slide in cls.SLIDES:
            values *= slide.max_value + 1
            values += slide.get_value()
        return values
