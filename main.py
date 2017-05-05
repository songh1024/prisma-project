from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys,os
from PyQt4.QtCore import Qt, QString,QRect
from PyQt4 import QtGui
from ui_MainWindow import Ui_MainWindow
from PyQt4.QtCore import pyqtSlot as Slot
from PyQt4.QtGui import QFileDialog,QImageReader,QImage,QPixmap,QImageWriter\
    ,QPrintDialog,QPrinter,QPainter,QColor,QMessageBox
from newimagedlg import NewImageDlg
from style_transform import style_transfer
from qimage2ndarray import numpy2qimage

class MyWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.filename = None
        self.image = None
        self.printer = None
        self.style_image = None
        self.style = None
        self.setupUi(self)

    @Slot()
    def on_actionOpen_File_triggered(self):
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{0}".format(unicode(format).lower())
                    for format in QImageReader.supportedImageFormats()])
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "Image Changer - Choose Image",
                                                    dir,
                                                    "Image files ({0})".format(" ".join(formats))))
        if fname:
            self.loadFile(fname)

    def loadFile(self, fname=None):
        if fname:
            self.filename = fname
            image = QImage(fname)
            if image.isNull():
                message = "Failed to read {0}".format(fname)
            else:
                self.image = image
                self.filename = fname
                self.showImage()
                message = "Loaded {0}".format(os.path.basename(fname))

    def showImage(self):
        if self.image.isNull():
            return
        width = self.imageLabel.geometry().width()
        height = self.imageLabel.geometry().height()
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

    def showStyleImage(self):
        if self.style_image == None:
            msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Please configure the baseline!")
            msg_box.show()
            return
        nimage = numpy2qimage(self.style_image)
        if nimage.isNull():
            return
        width = self.imageLabel.geometry().width()
        height = self.imageLabel.geometry().height()
        image = nimage.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))


    @Slot()
    def on_actionSave_triggered(self):
        if self.filename is None:
            return True
        else:
            if self.image.save(self.filename, None):

                return True
            else:
                return False

    @Slot()
    def on_actionSave_As_triggered(self):
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{0}".format(unicode(format).lower())
                for format in QImageWriter.supportedImageFormats()])
        fname = unicode(QFileDialog.getSaveFileName(self,
                "Image Changer - Save Image", fname,
                "Image files ({0})".format(" ".join(formats))))
        if fname:
            if "." not in fname:
                fname += ".png"
            self.filename = fname
            return self.on_actionSave_triggered()
        return False


    @Slot()
    def on_actionPrint_triggered(self):
        if self.printer is None:
            self.printer = QPrinter(QPrinter.HighResolution)
            self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)

    @Slot()
    def on_actionQuit_triggered(self):
        msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Please configure the baseline!")
        msg_box.show()
        quit()
    @Slot()
    def on_actionla_muse_triggered(self):
        self.style = 'la_muse.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.showStyleImage()
    @Slot()
    def on_actionrain_princess_triggered(self):
        self.style = 'rain_princess.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.showStyleImage()
    @Slot()
    def on_actionscream_triggered(self):
        self.style = 'scream.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.showStyleImage()
    @Slot()
    def on_actionudine_triggered(self):
        self.style = 'udnie.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.showStyleImage()

    @Slot()
    def on_actionwave_triggered(self):
        self.style = 'wave.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.showStyleImage()

    @Slot()
    def on_actionwreck_triggered(self):
        self.style = 'wreck.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.showStyleImage()





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myShow = MyWindow()
    myShow.show()
    sys.exit(app.exec_())
