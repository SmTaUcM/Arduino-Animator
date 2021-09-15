'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        ClickableLabel.py
# Purpose:     Overloads the original QLabel class to alow clicking of the label to emit a signal.
# Version:     v1.00
# Author:      Stuart Macintosh
#
# Created:     17/02/2021
#-------------------------------------------------------------------------------------------------------------------------------------------------#'''


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Imports.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal

#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Classes.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
class ClickableLabel(QLabel):
    '''Class overloading the original QLabel class to alow clicking of the label to emit a signal.'''

    # Declare class variables.
    clicked = pyqtSignal(object, str)

    def mousePressEvent(self, event):
        '''Actions to take upon the mouse click event being triggered.'''

        if event.button() == Qt.LeftButton:
            self.clicked.emit(self, "left")

        elif event.button() == Qt.RightButton:
            self.clicked.emit(self, "right")

        elif event.button() == Qt.MiddleButton:
            self.clicked.emit(self, "middle")

        else:
            self.clicked.emit(self, "none")
    #------------------------------------------------------------------------------------------------------------------------------------------------#
