from tkinter import *
from PIL import Image, ImageTk, ImageDraw


class Gif(object):
    MODE = 'RGBA'
    DISPLAY_SIZE = 448
    CROSS_COLOR = (128, 128, 128)
    CROSS_WIDTH = 3

    def __init__(self, file_name, mode=MODE):
        try:
            animation = Image.open(file_name)
        except FileNotFoundError:
            self.delay = 0
            image = Image.new('RGB', (self.DISPLAY_SIZE, self.DISPLAY_SIZE))
            draw = ImageDraw.Draw(image)
            for i in (0, self.DISPLAY_SIZE):
                draw.line((0, i, self.DISPLAY_SIZE, self.DISPLAY_SIZE - i),
                          fill=self.CROSS_COLOR, width=self.CROSS_WIDTH)
            seq = [image]
        else:
            self.delay = animation.info.get('duration', 100)
            seq = []
            while 1:
                seq.append(animation.copy())
                try:
                    animation.seek(len(seq))
                except EOFError:
                    break
            animation.close()

        # draw frames
        self.frames = []
        frame = seq[0]
        for diff in seq:
            frame.paste(diff)
            self.frames.append(ImageTk.PhotoImage(frame.convert(mode)))


class GifPlayer(object):

    def __init__(self, frame):
        self.canvas = frame.canvas
        self.after = frame.after
        self.play_count = 0
        self.current_frame = 0
        self.current_gif = None
        self.after_cb = None

    def stop(self):
        self.play_count = 0

    def play(self, gif, times=1, after_cb=None):
        self.after_cb = after_cb
        self.stop()
        self.current_frame = 0
        self.current_gif = gif
        self.play_count = times
        self._play()

    def _play(self):
        if self.play_count == 0:
            return
        self.canvas.delete(ALL)
        self.canvas.create_image(0, 0, anchor=NW, image=self.current_gif.frames[self.current_frame])

        self.current_frame += 1
        if self.current_frame == len(self.current_gif.frames):
            self.current_frame = 0
            if self.play_count is not None:
                self.play_count -= 1
                if self.play_count == 0:
                    if self.after_cb is not None:
                        self.after_cb()
                        self.after_cb = None
                    return
        self.after(self.current_gif.delay, self._play)
