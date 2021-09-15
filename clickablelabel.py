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
    clicked = pyqtSignal(object)

    def mousePressEvent(self, event):
        '''Actions to take upon the mouse click event being triggered.'''

        self.clicked.emit(self)
    #------------------------------------------------------------------------------------------------------------------------------------------------#
