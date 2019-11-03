from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtCore
from PIL import Image
import sys,logging

def GetScreen():
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(QApplication.desktop().winId()).toImage()
    img.save('123.jpg')
    bytes = img.bits().asstring(img.byteCount())

    I = Image.frombuffer('RGBA',(img.width(),img.height()),bytes,'raw', 'RGBA', 0, 1)
    L = I.convert("L")
    L.show()

