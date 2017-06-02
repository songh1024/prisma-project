from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "1.0.0"

import platform
import sys,os, scipy.misc
import numpy as np
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt,PYQT_VERSION_STR,QT_VERSION_STR
from ui_MainWindow import Ui_MainWindow,_translate
from PyQt4.QtCore import pyqtSlot as Slot
from PyQt4.QtGui import QFileDialog,QImageReader,QImage,QPixmap,QImageWriter\
    ,QPrintDialog,QPrinter,QPainter,QMessageBox
from style_transform import style_transfer


class MyWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.filename = None
        self.image = None
        self.printer = None
        self.style_image = None
        self.style = None
        self.saved = True

        self.setupUi(self)

        self.init()


    def init(self):
        self.setWindowTitle(_translate("MainWindow", "Style Transfer - chicago.jpg", None))
        self.filename = 'images/chicago.jpg'
        self.image = QImage(self.filename)
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
            self.changeTitleOriginal()

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
    #   nimage = numpy2qimage(self.style_image)

        scipy.misc.imsave("images/temporary.jpg", np.clip(self.style_image, 0, 255).astype(np.uint8))
        nimage = QImage("images/temporary.jpg")
        if nimage.isNull():
            return
        self.image = nimage
        self.showImage()

    def defaultIcon(self):
        icon_lamuse_clicked = QtGui.QIcon()
        icon_lamuse_clicked.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/la_muse.jpg")), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.btn_la_muse.setIcon(icon_lamuse_clicked)
        self.btn_la_muse.setIconSize(QtCore.QSize(80, 80))

        icon_rainprincess = QtGui.QIcon()
        icon_rainprincess.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/rain_princess.jpg")), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.btn_rain_princess.setIcon(icon_rainprincess)
        self.btn_rain_princess.setIconSize(QtCore.QSize(80, 80))

        icon_scream = QtGui.QIcon()
        icon_scream.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/scream.jpg")), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.btn_scream.setIcon(icon_scream)
        self.btn_scream.setIconSize(QtCore.QSize(80, 80))

        icon_udnie = QtGui.QIcon()
        icon_udnie.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/udnie.jpg")), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.btn_udnie.setIcon(icon_udnie)
        self.btn_udnie.setIconSize(QtCore.QSize(80, 80))

        icon_wave = QtGui.QIcon()
        icon_wave.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/wave.jpg")), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.btn_wave.setIcon(icon_wave)
        self.btn_wave.setIconSize(QtCore.QSize(80, 80))

        icon_wreck = QtGui.QIcon()
        icon_wreck.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/wreck.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_wreck.setIcon(icon_wreck)
        self.btn_wreck.setIconSize(QtCore.QSize(80, 80))


    @Slot()
    def on_actionSave_triggered(self):
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
            if self.image.save(self.filename, None):
                self.saved = True
                self.changeTitleOriginal()
                return True
            else:
                return False
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
        if self.saved == False:
            reply = QMessageBox.question(self,
                                 "Image Changer - Unsaved Changes",
                                 "Save unsaved changes?",
                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.on_actionSave_triggered()
        self.image = None
        self.filename=None
        quit()

    def closeEvent(self, QCloseEvent):
        self.on_actionQuit_triggered()

    def changeTitle(self):
        name = "Style Transfer - " + self.filename.split("/")[-1] + "*"
        self.setWindowTitle(_translate("MainWindow", name, None))

    def changeTitleOriginal(self):
        name = "Style Transfer - " + self.filename.split("/")[-1]
        self.setWindowTitle(_translate("MainWindow", name, None))

    @Slot()
    def on_actionla_muse_triggered(self):
        #set icon
        self.defaultIcon()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/la_muse_clicked.jpg")), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btn_la_muse.setIcon(icon)
        self.btn_la_muse.setIconSize(QtCore.QSize(80, 80))

        #style-transfer
        self.style = 'la_muse.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.saved = False
        self.showStyleImage()
        self.changeTitle()
    @Slot()
    def on_actionrain_princess_triggered(self):
        #set icon
        self.defaultIcon()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/rain_princess_clicked.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_rain_princess.setIcon(icon)
        self.btn_rain_princess.setIconSize(QtCore.QSize(80, 80))

        #style-transfer
        self.style = 'rain_princess.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.saved = False
        self.showStyleImage()
        self.changeTitle()
    @Slot()
    def on_actionscream_triggered(self):
        #set icon
        self.defaultIcon()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/scream_clicked.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_scream.setIcon(icon2)
        self.btn_scream.setIconSize(QtCore.QSize(80, 80))

        #style_transfer
        self.style = 'scream.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.saved = False
        self.showStyleImage()
        self.changeTitle()
    @Slot()
    def on_actionudine_triggered(self):
        #set icon
        self.defaultIcon()
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/udnie_clicked.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_udnie.setIcon(icon3)
        self.btn_udnie.setIconSize(QtCore.QSize(80, 80))

        #style-transfer
        self.style = 'udnie.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.saved = False
        self.showStyleImage()
        self.changeTitle()

    @Slot()
    def on_actionwave_triggered(self):
        #set icon
        self.defaultIcon()
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/wave_clicked.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_wave.setIcon(icon4)
        self.btn_wave.setIconSize(QtCore.QSize(80, 80))

        #style-transfer
        self.style = 'wave.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.saved = False
        self.showStyleImage()
        self.changeTitle()

    @Slot()
    def on_actionwreck_triggered(self):
        #set icon
        self.defaultIcon()
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8("images/wreck_clicked.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_wreck.setIcon(icon5)
        self.btn_wreck.setIconSize(QtCore.QSize(80, 80))

        #style-transfer
        self.style = 'wreck.ckpt'
        self.style_image = style_transfer(self.style, self.filename)
        self.saved = False
        self.showStyleImage()
        self.changeTitle()

    @Slot()
    def on_btn_la_muse_clicked(self):
        self.on_actionla_muse_triggered()


    @Slot()
    def on_btn_rain_princess_clicked(self):
        self.on_actionrain_princess_triggered()

    @Slot()
    def on_btn_scream_clicked(self):
        self.on_actionscream_triggered()

    @Slot()
    def on_btn_udnie_clicked(self):
        self.on_actionudine_triggered()

    @Slot()
    def on_btn_wave_clicked(self):
        self.on_actionwave_triggered()

    @Slot()
    def on_btn_wreck_clicked(self):
        self.on_actionwreck_triggered()

    @Slot()
    def on_action_About_triggered(self):
        QMessageBox.about(self, "About Image Style Transfer",
                          """<b>Image Style Transfer</b> v {0}
                          <p>Copyright &copy; 2017-4 Qtrac Ltd.
                          All rights reserved.
                          <p>This application can be used to image style transfer.
                          <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                              __version__, platform.python_version(),
                              QT_VERSION_STR, PYQT_VERSION_STR,
                              platform.system()))

    @Slot()
    def on_action_Help_F1_triggered(self):
        QMessageBox.about(self, "Help about this application",
                          """<b>Image Style Transfer</b>
                          <p>Chose one kind of style,ckick.
                          <p>Then the style image will show.""")
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myShow = MyWindow()
    myShow.show()
    sys.exit(app.exec_())
