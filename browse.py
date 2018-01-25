#!/usr/bin/env python

import Image
import pyglet
import cStringIO as StringIO
from pyglet.window import key
from pyglet.image.codecs.pil import PILImageDecoder

class CropWindow(pyglet.window.Window):
    def __init__(self):
        super(CropWindow, self).__init__(width = 480, height = 272)
        self.im = None
        self.label = pyglet.text.Label(
                                  "foo",
                                  font_name='Times New Roman',
                                  font_size=18,
                                  x=0, y=self.height,
                                  anchor_x='left', anchor_y='top')

    def on_draw(self):
        self.clear()
        if self.im:
            self.im.blit(0, 0)
        self.label.draw()

class MainWindow(pyglet.window.Window):
    def __init__(self, cropwindow):
        self.cropwindow = cropwindow
        super(MainWindow, self).__init__()

    def loadfile(self, filename):
        self.label = pyglet.text.Label(
                                  filename,
                                  font_name='Times New Roman',
                                  font_size=18,
                                  x=0, y=self.height,
                                  anchor_x='left', anchor_y='top')
        im = Image.open(filename)
        s = min(float(self.width) / im.size[0], float(self.height) / im.size[1])
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
        self.update()

    def update(self):
        x0 = int(self.x0)
        x1 = int(self.x1)
        y0 = self.im.size[1] - int(self.y0)
        y1 = self.im.size[1] - int(self.y1)
        rs = self.im.crop((x0, y1, x1, y0)).resize((480, 272), Image.BILINEAR)
        self.cropwindow.im = pyglet.image.ImageData(rs.size[0], rs.size[1], "RGB", rs.transpose(Image.FLIP_TOP_BOTTOM).tostring())
        # self.cropwindow.switch_to()
        # self.cropwindow.on_draw()

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
        self.dragging = (x, y)
        s = self.scale
        self.resize = (x - s * self.x1)**2 + (y - s * self.y1)**2 < 40**2

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        (ox, oy) = self.dragging
        dx = (x - ox) / self.scale
        dy = (y - oy) / self.scale
        if not self.resize:
            w = self.x1 - self.x0
            h = self.y1 - self.y0
            xm = self.im.size[0] - w
            ym = self.im.size[1] - h

            self.x0 += dx
            self.y0 += dy
            self.x0 = max(0, min(self.x0, xm))
            self.y0 = max(0, min(self.y0, ym))
            self.x1 = self.x0 + w
            self.y1 = self.y0 + h
        else:
            s = self.scale
            nx = x / s
            ny = self.y0 + (self.x1 - self.x0) * 9 / 16
            xx,yy = self.im.size
            if nx < xx and ny < yy:
                (self.x1, self.y1) = (nx, ny)

        self.dragging = (x, y)
        self.update()

def update(dt):
    pass 

if __name__ == '__main__':
    crop = CropWindow()
    window = MainWindow(crop)
    window.loadfile("raw/tumblr_npu98o8tLs1sfie3io1_1280.jpg")
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
