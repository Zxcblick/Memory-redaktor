from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QWidget,
    QPushButton,
    QLabel,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
import os

#функций
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'NewFiles/'
    

    def clear(self):
        self.image = None
        self.dir = None
        self.filename = None

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        try:
            self.image = self.image.convert('L')
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            lb_image.setText('Вы не выбраи папку или фото')

    def do_flip(self):   #Зеркало
        try:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            lb_image.setText('Вы не выбраи папку или фото')
        

    def do_right(self):   #Право
        try:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            lb_image.setText('Вы не выбраи папку или фото')
        

    def do_left(self):    #Лево
        try:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            lb_image.setText('Вы не выбраи папку или фото')


    def do_blur(self):    #Резкость
        try:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            lb_image.setText('Вы не выбраи папку или фото')
        
def ShowFilenameList():
    try:
        extensions = ['.jpg', '.jpeg', '.png']
        chooseWordir()
        filenames = filter(os.listdir(workdir), extensions)
        lw_files.clear()
        workimage.clear()
        for filename in filenames:
            lw_files.addItem(filename)
        lb_image.setText('Картинка')

    except:
        lb_image.setText('Вы не выбрали папку!')





def showChosenImage():
    if lw_files.currentRow() >= 0:
        try:
            filename = lw_files.currentItem().text()
            workimage.loadImage(workdir, filename)
            image_path = os.path.join(workimage.dir, workimage.filename)
            workimage.showImage(image_path)
        except:
            lb_image.setText('Фаил не поддерживается или поврежден!')

def chooseWordir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

#глобальные переменные
workdir = ''
app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')


lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')


main_line = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
buttons = QHBoxLayout()
buttons.addWidget(btn_left)
buttons.addWidget(btn_right)
buttons.addWidget(btn_flip)
buttons.addWidget(btn_sharp)
buttons.addWidget(btn_bw)
col2.addLayout(buttons)

main_line.addLayout(col1, 20)
main_line.addLayout(col2, 80)
win.setLayout(main_line)


workimage = ImageProcessor()

#прдпискана событие
btn_dir.clicked.connect(ShowFilenameList)
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_blur)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)


win.show()
app.exec_()