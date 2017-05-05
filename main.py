from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys,os
from PyQt4.QtCore import Qt, QString,QRect
from PyQt4 import QtGui
from ui_MainWindow import Ui_MainWindow
from PyQt4.QtCore import pyqtSlot as Slot
from PyQt4.QtGui import QFileDialog,QImageReader,QImage,QPixmap,QImageWriter,QPrintDialog,QPrinter,QPainter
from newimagedlg import NewImageDlg

class MyWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.filename = None
        self.image = None
        self.printer = None
        self.setupUi(self)

    @Slot()
    def on_actionNew_File_triggered(self):
        dialog = NewImageDlg(self)
        if dialog.exec_():
            self.image = dialog.image()
            self.filename = None
            self.showImage()

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
            self.filename = None
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
    def on_actionExit_tringgered(self):
        quit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myShow = MyWindow()
    myShow.show()
    sys.exit(app.exec_())
