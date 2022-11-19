#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR4

from gl import Render

r = Render()

r.glCreateWindow(1024, 1024)

r.glClearColor(0.5, 0.6, 0.8)

r.glColor(0, 0, 0)

r.glClear()

r.load('./cup.obj', translate=[300, 300, 0], scale=[50, 50, 10])

r.glFinish("sr4.bmp")