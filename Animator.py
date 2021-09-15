'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Animator.py
# Purpose:
# Version:     v1.00
# Author:      Sgt. S. Macintosh - MSC System Engineers
#
# Created:     13/09/2021
# Copyright:   (c) Crown Copyright - MSC System Engineers 2021
# Licence:     MSC System Engineers
#-------------------------------------------------------------------------------------------------------------------------------------------------#'''

#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Imports.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import os
import sys
import clickablelabel
#----------------------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Classes.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
class Animator(QMainWindow):
    '''Main program object.'''

    def __init__(self):
        '''Main program object.'''

        # Show GUI.
        QMainWindow.__init__(self)
        self.gui = uic.loadUi(r"gui.ui")
        self.gui.show()
        self.cols = 4
        self.rows = 4

        # Declare instance variables.
        self.selectedColour = QColor(255, 255, 255)
        self.pixels = []

        # Dialog connections.
        self.gui.btn_openCP.clicked.connect(self.openColourPicker)
        self.gui.sb_cols.valueChanged.connect(self.sbColsFunc)
        self.gui.sb_rows.valueChanged.connect(self.sbRowsFunc)
        self.gui.btn_export.clicked.connect(self.saveFrameData)
        self.gui.btn_load.clicked.connect(self.loadFrameData)

        # Main program logic.
        self.createGrid()
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def createGrid(self):
        '''Method to dynamically create the pixel grid.'''

        self.pixels = []
        for row in range(self.rows):
            for col in range(self.cols):
                label = clickablelabel.ClickableLabel()
                label.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.gui.gl_pixels.addWidget(label, row, col)
                label.clicked.connect(self.setColour)
                self.pixels.append(label)

        # Label the grids.
        count = 0
        if self.rows % 2 == 0:
            for row in range(self.rows)[::-1]:
                for col in range(self.cols):
                    # Odd rows. - Right to left from 0
                    if row % 2 != 0:
                        self.gui.gl_pixels.itemAtPosition(row, col).widget().setText(str(count))
                        count += 1

                    # Even rows. - Left to right from previous + 1
                    else:
                        revCol = self.cols - col - 1
                        self.gui.gl_pixels.itemAtPosition(row, revCol).widget().setText(str(count))
                        count += 1

        else:
            for row in range(self.rows)[::-1]:
                for col in range(self.cols)[::-1]:
                    # Odd rows. - Right to left from 0
                    if row % 2 != 0:
                        self.gui.gl_pixels.itemAtPosition(row, col).widget().setText(str(count))
                        count += 1

                    # Even rows. - Left to right from previous + 1
                    else:
                        revCol = self.cols - col - 1
                        self.gui.gl_pixels.itemAtPosition(row, revCol).widget().setText(str(count))
                        count += 1
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def openColourPicker(self, pixel):
        '''Method to open the QColorDialog.'''

        # Open the colour picker.
        self.colourDlg = QColorDialog()
        self.colourDlg.show()
        # Connections.
        self.colourDlg.accepted.connect(lambda: self.colourAccepted(self.colourDlg.currentColor()))
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def colourAccepted(self, colour):
        '''Method to save the QColorDialog selected colur.'''

        self.selectedColour = colour
        self.setColour(self.gui.lbl_currentColour)
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def setColour(self, sender):
        '''Method that sets the clicked pixel labels to the currently selected colour.'''

        # Convert values.
        realRGB = self.selectedColour.getRgb()
        hexRGB = "#%02x%02x%02x" % (realRGB[0], realRGB[1], realRGB[2])

        # Apply values to GUI.
        sender.setStyleSheet("background-color: rgb(%s, %s, %s);" % (realRGB[0], realRGB[1], realRGB[2]))
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def clearGrid(self):
        '''Method that clears the pixel grid.'''

        for item in reversed(range(self.gui.gl_pixels.count())):
            self.gui.gl_pixels.itemAt(item).widget().setParent(None)
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def sbColsFunc(self, value):
        '''Method that triggers when the columns spinbox value is changed.'''

        self.clearGrid()
        self.cols = value
        self.createGrid()
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def sbRowsFunc(self, value):
        '''Method that triggers when the columns spinbox value is changed.'''

        self.clearGrid()
        self.rows = value
        self.createGrid()
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def saveFrameData(self):
        '''Method saves the colour data for the current frame.'''

        # Save rows and cols data.
        data = [str(self.rows) + "\n", str(self.cols) + "\n"]

        # Save pixel data.
        count = 0
        for pixel in range(self.rows * self.cols):
            for item in reversed(range(self.gui.gl_pixels.count())):
                if self.gui.gl_pixels.itemAt(item).widget().text() == str(count):
                    colour = self.gui.gl_pixels.itemAt(item).widget().styleSheet().replace("background-color: rgb", "")
                    data.append("leds[%s] = CRGB " % count + colour + "\n")
                    count += 1

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        saveName, ext = QFileDialog.getSaveFileName(self, "Save Export File", os.getcwd() + "\\export.txt", "*.txt", options=options)
        with open(saveName, "w") as dataFile:
            dataFile.writelines(data)
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def loadFrameData(self):
        '''Method saves the colour data for the current frame.'''

        # Get the file to be opened.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Pixel Map File", os.getcwd(), "*.txt", options=options)
        if fileName:
            fileName = fileName.replace(r"/", "\\")

            with open(fileName, "r") as dataFile:
                data = dataFile.readlines()

            # Set the rows and cols by popping the first data entry.
            self.rows = int(data.pop(0))
            self.gui.sb_rows.setValue(self.rows)
            self.cols = int(data.pop(0))
            self.gui.sb_cols.setValue(self.cols)

            # Convert to raw hex colour data.
            hexData = []
            for line in data:
                line = line.split("(")[1].replace(");\n", "").split(",")
                newLine = []
                for item in line:
                    newLine.append(int(item))
                hexData.append(newLine)

            # Wipe the grid
            self.clearGrid()
            self.createGrid()

            # Colour the pixels.
            count = 0
            if self.rows % 2 == 0:
                for row in range(self.rows)[::-1]:
                    for col in range(self.cols):
                        # Odd rows. - Right to left from 0
                        if row % 2 != 0:
                            realRGB = hexData[count]
                            self.gui.gl_pixels.itemAtPosition(row, col).widget().setStyleSheet("background-color: rgb(%s, %s, %s);" % (realRGB[0], realRGB[1], realRGB[2]))
                            count += 1

                        # Even rows. - Left to right from previous + 1
                        else:
                            revCol = self.cols - col - 1
                            realRGB = hexData[count]
                            self.gui.gl_pixels.itemAtPosition(row, revCol).widget().setStyleSheet("background-color: rgb(%s, %s, %s);" % (realRGB[0], realRGB[1], realRGB[2]))
                            count += 1

            else:
                for row in range(self.rows)[::-1]:
                    for col in range(self.cols)[::-1]:
                        # Odd rows. - Right to left from 0
                        if row % 2 != 0:
                            realRGB = hexData[count]
                            self.gui.gl_pixels.itemAtPosition(row, col).widget().setStyleSheet("background-color: rgb(%s, %s, %s);" % (realRGB[0], realRGB[1], realRGB[2]))
                            count += 1

                        # Even rows. - Left to right from previous + 1
                        else:
                            revCol = self.cols - col - 1
                            realRGB = hexData[count]
                            self.gui.gl_pixels.itemAtPosition(row, revCol).widget().setStyleSheet("background-color: rgb(%s, %s, %s);" % (realRGB[0], realRGB[1], realRGB[2]))
                            count += 1
        #--------------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Functions.                                                                    #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
# None.


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Main Program.                                                                  #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":

    # Start the QT application.
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    animator = Animator()
    sys.exit(app.exec_())
#----------------------------------------------------------------------------------------------------------------------------------------------------#
