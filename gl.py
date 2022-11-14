#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR4

import struct
from obj import *

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(h):
    #2 bytes
    return struct.pack('=h', h)

def dword(l):
    #4 bytes
    return struct.pack('=l', l)

def setColor(r, b, g):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Render(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.clear_color = setColor(1, 1, 1)
        self.render_color = setColor(0, 0, 0)
        self.viewport_color = setColor(1, 1, 1)
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_height = 0
        self.viewport_width = 0

    def glClear(self):
        self.framebuffer = [[self.clear_color for x in range(self.width)]
        for y in range(self.height)]

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewportColor(self, r, g, b):
        self.viewport_color = setColor(r, g, b)

    def glClearColor(self, r, g, b):
        self.clear_color = setColor(r, g, b)

    def glClearViewport(self):
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x,y, self.viewport_color)    
        

    def glColor(self, r, g, b):
        self.render_color = setColor(r, g, b)

    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glVertex(self, x, y):
        if x > 1 or x < -1 or y > 1 or y < -1:
            print('Error')
        else:
            x = int((x + 1) * (self.viewport_width / 2) + self.viewport_x)
            y = int((y + 1) * (self.viewport_height / 2) + self.viewport_y)

            self.glPoint(x, y)

    def glPoint(self, x, y, color = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.framebuffer[x][y] = color or self.render_color

    def glLine(self, x0, x1, y0, y1, color = None):
        
        line_color = color or self.render_color

        x0 = round(x0)
        x1 = round(x1)
        y0 = round(y0)
        y1 = round(y1)

        if x0 == x1:
            if y0 == y1:
                self.glPoint(x0, y0, line_color)
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0

        threshold = dx

        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(x, y, line_color)
            else:
                self.glPoint(y, x, line_color)

            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2

    def transform_vertex(self, vertex, translate, scale):
        return([
            (vertex[0] * scale[0]) + translate[0],
            (vertex[1] * scale[1]) + translate[1]
        ])

    def load(self, filename, translate, scale):
        model = Obj(filename)


        for face in model.faces:
            vcount = len(face)
            
            if vcount == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex(model.vertices[f1], translate, scale)
                v2 = self.transform_vertex(model.vertices[f2], translate, scale)
                v3 = self.transform_vertex(model.vertices[f3], translate, scale)
                v4 = self.transform_vertex(model.vertices[f4], translate, scale)

                self.glLine(v1[0], v2[0], v1[1], v2[1])
                self.glLine(v2[0], v3[0], v2[1], v3[1])
                self.glLine(v3[0], v4[0], v3[1], v4[1])
                self.glLine(v4[0], v1[0], v4[1], v1[1])
            
            elif vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex(model.vertices[f1], translate, scale)
                v2 = self.transform_vertex(model.vertices[f2], translate, scale)
                v3 = self.transform_vertex(model.vertices[f3], translate, scale)

                self.glLine(v1[0], v2[0], v1[1], v2[1])
                self.glLine(v2[0], v3[0], v2[1], v3[1])
                self.glLine(v3[0], v1[0], v3[1], v1[1])

    def glFinish(self, filename):
        f = open(filename, 'bw')

        #pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range (self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()