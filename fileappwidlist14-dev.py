#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


#from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream, QSize, QRect, QCoreApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence, QStandardItemModel, QStandardItem
#from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        #QMessageBox, QTextEdit)
from PyQt5.QtWidgets import *

import numpy as np
import os
import random
import csv, codecs

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from functools import partial


class MainWindow(QMainWindow):
    MaxRecentFiles = 5
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()

        self.recentFileActs = []
        headers = []
        selecthead = [0, 0, 0, 0, 0, 0]
        #selecthead = []
        x = []
        y = []
        z = []
        r = []
        s = []
        t = []

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        
        # fileName
        #self.fileName = self.open() 

        self.createActions()
        self.createMenus()
        self.statusBar()
# List widget
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   
        
        # A figure instance to plot on
        
        self.graphicsView = QGraphicsView(centralWidget)
        self.graphicsView.setGeometry(QRect(500,0, 500, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.scene= QGraphicsScene(centralWidget)
        
        self.figure = Figure()
        
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        
        self.scene.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.scene.addWidget(self.toolbar)
        self.canvas.setGeometry(500,0,500,500)
        #self.graphicsView.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)
        
        
        
        self.setWindowTitle("Recent Files")
        self.resize(1000, 500)

# Create combobox and add items.
        self.listWidget = QListWidget(centralWidget)
        self.listWidget.setGeometry(QRect(50, 100, 150, 150))
        self.listWidget.setObjectName(("listWidget"))
        #self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        
        headers=self.loadheader()
        print(headers[2])
        i=0
        for i in range(len(headers)):
            item=QListWidgetItem()
            #name='A'+'%04d'%i
            name=headers[i]
            #item.setText(headers[i])                        
            self.listWidget.addItem(name)
            #self.listWidget.item(i).setSelected(True)
            i+=1
           
        print(self.listWidget.count())
        
        self.listWidget2 = QListWidget(centralWidget)
        self.listWidget2.setGeometry(QRect(300, 100, 150, 110))
        self.listWidget2.setObjectName(("listWidget2"))
        self.listWidget2.setSelectionMode(QAbstractItemView.MultiSelection)
        #self.listWidget2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # self 
        self.pushButton3 = QPushButton(centralWidget)
        self.pushButton3.setGeometry(QRect(250, 250, 100, 50))
        self.pushButton3.setObjectName("pushButton")
        translate3 = QCoreApplication.translate
        self.pushButton3.setText(translate3("MainWindow", "Selected indices"))
        
        self.pushButton3.clicked.connect(self.selectionChanged(selecthead))
        #self.pushButton3.clicked.connect(partial(self.selectionChanged, selecthead))
        #selecthead=self.selectionChanged2(selecthead)
        print('selected & sorted list:', selecthead)
        

       
        #call copying if selection changed.
        #item_1=self.selectionChanged()
        #print('widget2 item_1', item_1)
        #self.listWidget2.itemSelectionChanged.connect(self.selectionChanged2)
        # try this
        #while (selectionChanged2(self))
        #print('widget2 count', self.selectionChanged())
        #print(self.listWidget2.count())
        #print(headersorted[1])
        #xi=headers.index(self.listWidget2.item(1))
        #x1=self.listWidget.findItems(self.listWidget2.item(1),Qt.MatchExactly)
        #self.listWidget2.addItem("col1 ")

#  label push button
        self.pushButton = QPushButton(centralWidget)
        self.pushButton.setGeometry(QRect(100, 350, 100, 100))
        self.pushButton.setObjectName("pushButton")
        translate = QCoreApplication.translate
        self.pushButton.setText(translate("MainWindow", "Load Data"))
        
        self.pushButton.clicked.connect(self.loadData(selecthead, x, y, z, r, s, t))
        #self.pushButton.clicked.connect(self.loadCsv)

        print('widget2 count', self.listWidget2.count())
        # TESTING button click again.!
        self.pushButton4 = QPushButton(centralWidget)
        self.pushButton4.setGeometry(QRect(350, 250, 100, 50))
        self.pushButton4.setObjectName("pushButton")
        translate4 = QCoreApplication.translate
        self.pushButton4.setText(translate4("MainWindow", "Show x"))
        
        self.pushButton4.clicked.connect(self.selectionChanged2(x))
        #self.pushButton4.clicked.connect(partial(self.selectionChanged2, selecthead))
        #print('selected & sorted list2:', selecthead)
        
# Just some button connected to `plot` method
        self.pushButton2 = QPushButton(centralWidget)
        self.pushButton2.setGeometry(QRect(200, 350, 100, 100))
        self.pushButton2.setObjectName("pushButton2")
        translate2 = QCoreApplication.translate
        self.pushButton2.setText(translate2("MainWindow", "Plot Data"))
        
        #self.button = QPushButton('Plot')
        self.pushButton2.clicked.connect(self.plot)
        
        

        
    def selectionChanged(self, selecthead):

        def selectchange():
            rows = sorted([index.row() for index in self.listWidget.selectedIndexes()],
                reverse=False)
            print('index row F1:',rows)
            i=0
            for row in rows:
                self.listWidget2.addItem(self.listWidget.takeItem(row))
            #print('item1_F1:',self.listWidget.currentItem().text())
            #mylist = [int(x) for x in rows.strip().split(',') if x.strip().isdigit()]

            for i in range(len(rows)):
                selecthead[i]=rows[i]
                print('item1_F1_i:',i , rows[i])
                #i+=1
            print('select head F1:',selecthead)
        return selectchange
        
    def selectionChanged2(self, x):
        def selectchange2():
        #self.listWidget2.addItems(self, self.listWidget.currentItem().text())
        #print('item1:',self.listWidget2.item(0).text())
            print('item2_SelectHead:', x)
        return selectchange2
        #return 

    def newFile(self, MainWindow):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        #if fileName:
         #   self.loadFile(fileName)
        
        return fileName

    def loadFile(self, fileName):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
        QDir.currentPath(), "CSV (*.csv)")
        #fileName = QFile(self.fileName)
        print(fileName)
#        if not file.open( QFile.ReadOnly | QFile.Text):
#            QMessageBox.warning(self, "Recent Files",
#                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
#            return
        with open(fileName, "r") as data:
            line = data.readline()
            headers = [e for e in line.strip().split(',') if e]
            #i =0
            #for i,values in enumerate(header):
            #   print(i,header[i])    
        return headers

    def loadheader(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
        QDir.currentPath(), "CSV (*.csv)")
        #fileName = QFile(self.fileName)
        print(fileName)
#        if not file.open( QFile.ReadOnly | QFile.Text):
#            QMessageBox.warning(self, "Recent Files",
#                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
#            return
        with open(fileName, "r") as data:
            line = data.readline()
            header = [e for e in line.strip().split(',') if e]
            #i =0
            #for i,values in enumerate(header):
            #   print(i,header[i])    
        self.statusBar().showMessage("Header loaded", 2000)
        return header    

    def loadData(self, selecthead, x, y, z, r, s, t):
    #def loadData(self, fileName):
        
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
        QDir.currentPath(), "CSV (*.csv)")
        #fileName = QFile(self.fileName)
        #print(fileName)
        def loadvalues():
            xi=selecthead[0]
            yi=selecthead[1]
            zi=selecthead[2]
            ri=selecthead[3]
            si=selecthead[4]
            ti=selecthead[5]
        
            with open(fileName, "r") as data:
                line = data.readline()
                header = [e for e in line.strip().split(',') if e]
                x, y, z, r, s, t = np.genfromtxt(data,usecols = (xi,yi,zi,ri,si,ti), delimiter=',', unpack=True)
        
            print(x)       
            print(x[11])
            self.plot(x,y,z,r,s,t)
        self.statusBar().showMessage("Data loaded", 2000)
        return loadvalues
        #return x, y, z, r, s, t
        
        
    def plot(self, x,y,z,r,s,t):
        ''' plot some random stuff '''
        # random data
        #data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)
        
        # discards the old graph
        ax.clear()

        # plot data
        #ax.plot(data, '*-')
        ax.plot(x, '*-')
        ax.plot(y, '-')

        # refresh canvas
        self.canvas.draw()
        
    def save(self):
        if self.curFile:
            self.saveFile(self.curFile)
        else:
            self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            self.saveFile(fileName)

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())

    def about(self):
        QMessageBox.about(self, "About Recent Files",
                "The <b>Recent Files</b> example demonstrates how to provide "
                "a recently used file menu in a Qt application.")

    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        for i in range(MainWindow.MaxRecentFiles):
            self.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.openRecentFile))

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QApplication.instance().closeAllWindows)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.separatorAct = self.fileMenu.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.updateRecentFileActions()

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        
    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open( QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Recent Files",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        if self.curFile:
            self.setWindowTitle("%s - Recent Files" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("Recent Files")

        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        numRecentFiles = min(len(files), MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


    def selectionchange(self,i):
      print("Items in the list are :")

      for count in range(self.cb.count()):
         print(self.cb.itemText(count))
      print("Current index",i,"selection changed ",self.cb.currentText())

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    print('widget2 main count', mainWin.listWidget2.count())
    mainWin.show()
    sys.exit(app.exec_())