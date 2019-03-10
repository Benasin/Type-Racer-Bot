import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
import PIL
from pynput.keyboard import Listener, Controller, Key
import time


def on_press(key):
	keyboard = Controller()
	pytesseract.pytesseract.tesseract_cmd = r'L:\Tesseract-OCR\tesseract.exe'
	img1 = cv2.imread('capture.png')
	gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(gray, (img1.shape[1] * 2,img1.shape[0] * 2))
	text = pytesseract.image_to_string(img)
	text = text.replace('\n',' ')
	text = text.replace('|', 'I')
	words = list(text)
	print(text)
	if key == Key.enter:
		for i in range(len(words)):
			keyboard.type(words[i])
			time.sleep(0.01)
		return False
	else:
		pass
def Type():	
	with Listener(on_press = on_press) as l:
		l.join()	

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        global text
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        cv2.imwrite('capture.png', img)
        print("Press Enter to Type")
        Type() 

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())