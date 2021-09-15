'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Animator.py
# Purpose:
# Version:     v1.01
# Author:      S. Macintosh
#
# Created:     13/09/2021
# Copyright:   Stuart Macintosh 2021
# Licence:     GNU
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

        # Settings.
        self.defaultColourStyleRight = "background-color: rgb(0, 0, 0);"
        self.defaultColourRight = QColor(0, 0, 0)
        self.defaultColourStyleLeft = "background-color: rgb(255, 255, 255);"
        self.defaultColourLeft = QColor(255, 255, 255)

        # Show GUI.
        QMainWindow.__init__(self)
        self.gui = uic.loadUi(r"gui.ui")
        self.gui.show()
        self.cols = 10
        self.rows = 10
        self.gui.setWindowTitle("Arduino Animator v1.0.2a")
        self.gui.btn_exportSelection.setEnabled(False)

        # Declare instance variables.
        self.selectedColourLeft = self.defaultColourLeft
        self.selectedColourRight = self.defaultColourRight
        self.selectedPixels = 0

        # Dialog connections.
        self.gui.btn_openCPLeft.clicked.connect(self.openColourPickerLeft)
        self.gui.lbl_currentColourLeft.clicked.connect(self.openColourPickerLeft)
        self.gui.btn_openCPRight.clicked.connect(self.openColourPickerRight)
        self.gui.lbl_currentColourRight.clicked.connect(self.openColourPickerRight)
        self.gui.sb_cols.valueChanged.connect(self.sbColsFunc)
        self.gui.sb_rows.valueChanged.connect(self.sbRowsFunc)
        self.gui.btn_export.clicked.connect(self.saveFrameData)
        self.gui.btn_load.clicked.connect(self.loadFrameData)
        self.gui.btn_copy.clicked.connect(self.copy2clip)
        self.gui.btn_exportSelection.clicked.connect(self.exportSelection)

        # Main program logic.
        self.createGrid()
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def createGrid(self):
        '''Method to dynamically create the pixel grid.'''

        for row in range(self.rows):
            for col in range(self.cols):
                label = clickablelabel.ClickableLabel()
                label.setStyleSheet(self.defaultColourStyleRight)
                self.gui.gl_pixels.addWidget(label, row, col)
                label.clicked.connect(self.setColour)

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


    def openColourPickerLeft(self):
        '''Method to open the Left QColorDialog.'''

        # Open the colour picker.
        self.colourDlg = QColorDialog()
        self.colourDlg.show()
        # Connections.
        self.colourDlg.accepted.connect(lambda: self.colourAcceptedLeft(self.colourDlg.currentColor()))
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def openColourPickerRight(self):
        '''Method to open the Right QColorDialog.'''

        # Open the colour picker.
        self.colourDlg = QColorDialog()
        self.colourDlg.show()
        # Connections.
        self.colourDlg.accepted.connect(lambda: self.colourAcceptedRight(self.colourDlg.currentColor()))
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def colourAcceptedLeft(self, colour):
        '''Method to save the QColorDialog selected colur.'''

        self.selectedColourLeft = colour
        self.setColour(self.gui.lbl_currentColourLeft, "left")
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def colourAcceptedRight(self, colour):
        '''Method to save the QColorDialog selected colur.'''

        self.selectedColourRight = colour
        self.setColour(self.gui.lbl_currentColourRight, "right")
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def setColour(self, sender, value):
        '''Method that sets the clicked pixel labels to the currently selected colour.'''

        if value == "left":
            realRGB = self.selectedColourLeft.getRgb()
        elif value == "right":
            realRGB = self.selectedColourRight.getRgb()
        elif value == "middle":
            self.selectPixel(sender)
            return # Stops the rest of this function from triggering.

        # Convert values.
        hexRGB = "#%02x%02x%02x" % (realRGB[0], realRGB[1], realRGB[2])

        # Apply values to GUI.
        selection = sender.styleSheet().split("\n")[1::]
        colour = "background-color: rgb(%s, %s, %s);" % (realRGB[0], realRGB[1], realRGB[2])
        for item in selection:
            colour += "\n" + item
        sender.setStyleSheet(colour)
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def selectPixel(self, pixel):
        '''Method that selects or deselects a pixel upon middle mouse click.'''

        currentStyle = pixel.styleSheet()
        border = "\nborder-style: outset;\nborder-width: 6px;\nborder-color: rgb(0, 255, 0);"

        if border in currentStyle:
            pixel.setStyleSheet(currentStyle.split("\n")[0])
            self.selectedPixels -= 1
        else:
            pixel.setStyleSheet(currentStyle + border)
            self.selectedPixels += 1

        if self.selectedPixels == 0:
            self.gui.btn_exportSelection.setEnabled(False)
        else:
            self.gui.btn_exportSelection.setEnabled(True)
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def exportSelection(self):
        '''Method saves the colour data for the selected pixels.'''

        data = []

        # Save pixel data.
        count = 0
        for pixel in range(self.rows * self.cols):
            for item in reversed(range(self.gui.gl_pixels.count())):
                if self.gui.gl_pixels.itemAt(item).widget().text() == str(count):
                    if "border" in self.gui.gl_pixels.itemAt(item).widget().styleSheet():
                        colour = self.gui.gl_pixels.itemAt(item).widget().styleSheet().split("\n")[0].replace("background-color: rgb", "")
                        data.append("leds[%s] = CRGB " % count + colour + "\n")
                    count += 1

        # Parse data to text.
        text = ""
        for item in data:
            text += item

        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(text, mode=cb.Clipboard)
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
                    colour = self.gui.gl_pixels.itemAt(item).widget().styleSheet().split("\n")[0].replace("background-color: rgb", "")
                    data.append("leds[%s] = CRGB " % count + colour + "\n")
                    count += 1

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        saveName, ext = QFileDialog.getSaveFileName(self, "Save Export File", os.getcwd() + "\\export.txt", "*.txt", options=options)
        if saveName:
            with open(saveName, "w") as dataFile:
                dataFile.writelines(data)
        #--------------------------------------------------------------------------------------------------------------------------------------------#


    def loadFrameData(self):
        '''Method saves the colour data for the current frame.'''

        # Reset any selections.
        self.selectedPixels = 0
        self.gui.btn_exportSelection.setEnabled(False)

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


    def copy2clip(self):
        '''Method copies a string to the clipboard.'''

        text = ""
        data = []
        bgColour = self.selectedColourRight.getRgb()
        bgStyle = "background-color: rgb(%s, %s, %s);" % (bgColour[0], bgColour[1], bgColour[2])

        # Save pixel data.
        count = 0
        for pixel in range(self.rows * self.cols):
            for item in reversed(range(self.gui.gl_pixels.count())):
                if self.gui.gl_pixels.itemAt(item).widget().text() == str(count):
                    if self.gui.gl_pixels.itemAt(item).widget().styleSheet().split("\n")[0] != bgStyle:
                        colour = self.gui.gl_pixels.itemAt(item).widget().styleSheet().split("\n")[0].replace("background-color: rgb", "")
                        data.append("leds[%s] = CRGB " % count + colour + "\n")
                    count += 1

        # Parse data to text.
        for item in data:
            text += item

        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(text, mode=cb.Clipboard)
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
