#!/usr/bin/env python

import Image
import pyglet
import cStringIO as StringIO
from pyglet.window import key
from pyglet.image.codecs.pil import PILImageDecoder

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

    def loadfile(self, filename):
        self.label = pyglet.text.Label(
                                  filename,
                                  font_name='Times New Roman',
                                  font_size=18,
                                  x=0, y=self.height,
                                  anchor_x='left', anchor_y='top')
        im = Image.open(filename)
        s = min(640. / im.size[0], 480. / im.size[1])
        rs = im.resize((int(im.size[0] * s), int(im.size[1] * s)))
        self.rs = pyglet.image.ImageData(rs.size[0], rs.size[1], "RGB", rs.transpose(Image.FLIP_TOP_BOTTOM).tostring())

        self.im = im
        self.scale = s

        # Compute largest 16x9 rectangle
        self.maxrect()

    def maxrect(self):
        (ow, oh) = (w, h) = self.im.size
        aspect = w / float(h)
        if aspect < 16. / 9:
            h = 9 * w / 16
        else:
            w = 16 * h / 9
        self.x0 = (ow - w) / 2
        self.x1 = (ow + w) / 2
        self.y0 = (oh - h) / 2
        self.y1 = (oh + h) / 2

    def on_draw(self):
        self.clear()
        self.rs.blit(0, 0)
        self.label.draw()
        pyglet.graphics.draw(2, pyglet.gl.GL_LINE_LOOP,
            ('v2f', (10., 15., 30., 35.))
        )
        s = self.scale
        cc = (
            s * self.x0, s * self.y0,
            s * self.x0, s * self.y1,
            s * self.x1, s * self.y1,
            s * self.x1, s * self.y0,
            s * self.x0, s * self.y0,
        )
        pyglet.graphics.draw(len(cc) / 2, pyglet.gl.GL_LINE_STRIP,
            ('v2f', cc)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        print 'press'

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

if __name__ == '__main__':
    window = MainWindow()
    window.loadfile("raw/tumblr_npu98o8tLs1sfie3io1_1280.jpg")
    pyglet.app.run()
