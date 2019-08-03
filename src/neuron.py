import sys
import os
import os.path

# hook to import vlc under windows pycharm
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003553400-Load-DLL-raises-an-error-WinError-126-in-PyCharm-version-2019-1-2-
if sys.platform.startswith('win'):
    os.environ['PATH'] += r';C:\Program Files\VideoLAN\VLC'
import vlc

# add BASIC_PATH (GitHub clones path) to PYTHONPATH
BASIC_PATH = os.path.abspath(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))))
sys.path.append(BASIC_PATH)

import pygame
from tkinter import *
from pathlib import Path
from src.slide import Slide
from src.gif import Gif, GifPlayer

BASIC_PATH = Path(BASIC_PATH)


class ControlsWindow(Toplevel):

    WINDOW_TITLE = 'Neuron V1.0.0'
    RES_PATH = BASIC_PATH / 'res'
    IMAGES_PATH = RES_PATH / 'images/{}_{}.gif'
    ANIMATIONS_PATH = RES_PATH / 'animations/{}_{}.gif'
    VIDEO_PATH = RES_PATH / 'videos/{}.mp4'
    VIDEO_JUMP = 'jump'
    VIDEO_GIVE_UP = 'give_up'
    VIDEO_INSTRUCTIONS = 'instructions'
    SLIDES = [['Desire:', 4], ['Fear:', 3]]
    PADS = {'padx': 5, 'pady': 5}
    LEFT_OFFSET = 10
    PYGAME_LOOP_INTERVAL_MS = 20

    def __init__(self, master=None, cnf={}, **kw):
        # save reference to neuron window
        self.neuron = kw.pop('neuron')
        Toplevel.__init__(self, master, cnf, **kw)
        self.geometry('+{}+{}'.format(self.neuron.DISPLAY_SIZE - self.LEFT_OFFSET, 0))
        self.bind('<Destroy>', self.neuron.exit)
        self.title(self.WINDOW_TITLE)

        self.reload_button = Button(self, text='Reload', command=self.load_media)
        self.reload_button.pack(in_=self, fill=BOTH, **self.PADS)

        self.swap_screen_button = Button(self, text='Swap Screen', command=self.neuron.swap_screen)
        self.swap_screen_button.pack(in_=self, fill=BOTH, **self.PADS)

        self.controls_frame = LabelFrame(self, text='Controls:')
        self.controls_frame.pack(**self.PADS)

        self.slides_frame = Frame(self)
        self.slides_frame.pack(in_=self.controls_frame, **self.PADS)

        self.slides = []
        for name, size in self.SLIDES:
            slide = Slide(self, size=size, command=self.slide_command, text=name)
            slide.pack(in_=self.slides_frame, side=LEFT, fill=Y, **self.PADS)
            self.slides.append(slide)

        self.decide_button = Button(self, text='Decide!', command=self.decide_command)
        self.decide_button.pack(in_=self.controls_frame, fill=BOTH, **self.PADS)

        self.images = []
        self.animations = []

        self.vlc_is_idle_media = True
        self.vlc_instance = vlc.get_default_instance()
        self.vlc_list_player = self.vlc_instance.media_list_player_new()
        mp = self.vlc_list_player.get_media_player()
        mp.set_fullscreen(True)
        mp.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.vlc_media_end)

        self.load_media()
        self.gif_player = GifPlayer(self.neuron)
        self.vlc_play_idle()

        pygame.init()
        pygame.joystick.init()
        self.pygame_mainloop()

    def pygame_mainloop(self):
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            button = joystick.get_button(1)
            axes = [joystick.get_axis(i) for i in range(len(self.SLIDES))]
        except Exception:
            self.after(1000, self.pygame_mainloop)
            return

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button:
                    self.decide_command()
            elif event.type == pygame.JOYAXISMOTION:
                for i, (_, size) in enumerate(self.SLIDES):
                    self.slides[i].set_value(axes[i] * size)

        self.after(self.PYGAME_LOOP_INTERVAL_MS, self.pygame_mainloop)

    def load_media(self):
        self.images.clear()
        self.animations.clear()
        for i in range(self.SLIDES[0][1]):
            for j in range(self.SLIDES[1][1]):
                self.images.append(Gif(str(self.IMAGES_PATH).format(i, j)))
                self.animations.append(Gif(str(self.ANIMATIONS_PATH).format(i, j)))

        ml = self.vlc_instance.media_list_new()
        for i in (self.VIDEO_INSTRUCTIONS, self.VIDEO_JUMP, self.VIDEO_GIVE_UP):
            ml.add_media(str(self.VIDEO_PATH).format(i))
        self.vlc_list_player.set_media_list(ml)

    def decide_command(self):
        if self.gif_player.play_count:
            return
        self.gif_player.play(
            self.animations[Slide.get_values()], after_cb=self.slide_command)

        if self.vlc_is_idle_media:
            self.vlc_is_idle_media = False
            if self.slides[0].get_value() - self.slides[1].get_value() >= 2:
                self.vlc_list_player.play_item_at_index(1)
            else:
                self.vlc_list_player.play_item_at_index(2)

    def slide_command(self, *_, **__):
        if self.gif_player.play_count:
            return
        self.gif_player.play(self.images[Slide.get_values()])

    def vlc_media_end(self, _):
        # cant call self.vlc_decide_list_player.stop() from here so call it later
        self.after(10, self.vlc_play_idle)

    def vlc_play_idle(self):
        self.vlc_is_idle_media = True
        self.vlc_list_player.play_item_at_index(0)


class NeuronWindow(Frame):
    DISPLAY_SIZE = 448

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, bd=0, **kw)
        self.pack(fill=BOTH, expand=1)

        # remove window border and put it on top
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True)
        self.master.geometry('+{}+{}'.format(1920, 0))

        # exit on escape key press
        self.bind_all('<Escape>', self.exit)

        self.canvas = Canvas(self, bg='black', height=self.DISPLAY_SIZE,
                             width=self.DISPLAY_SIZE, highlightthickness=0)
        self.canvas.pack(fill=BOTH)

        # show controls window
        self.controls_window = ControlsWindow(self.master, neuron=self)

    def swap_screen(self):
        # get [width, height, left, top] of window
        rect = [int(i) for i in self.master.winfo_geometry().replace('x', '+').split('+')]
        rect[2] = self.master.winfo_screenwidth() - rect[2]
        # set [width, height, left, top] of window
        self.master.geometry('{}x{}+{}+{}'.format(*rect))

    def exit(self, *_, **__):
        if hasattr(self, '_exit'):
            return
        setattr(self, '_exit', True)
        print('exit')
        self.master.quit()


def main():
    root = Tk()
    neuron = NeuronWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
