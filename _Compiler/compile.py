'''#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        compile.py
# Purpose:     Used to compile Animator into Animator.exe.
# Version:     v1.00
# Author:      Stuart. Macintosh
#
# Created:     17/01/2021
# Copyright:   Emperor's Hammer
# Licence:     None
#-------------------------------------------------------------------------------------------------------------------------------------------------#'''

#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                      Imports.                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
import PyInstaller.__main__
import os
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
import platform
import sys
#----------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                     Main Program.                                                                  #
#----------------------------------------------------------------------------------------------------------------------------------------------------#
# Detect the location of the Animator folder.
os.chdir("..")
ttt3Dir = os.path.abspath(os.curdir)

# Remove any old builds of Animator.
print("\nRemoving old build files...")
shutil.rmtree(ttt3Dir + "\\_Compiler\\Animator", ignore_errors=True)
try:
    os.remove(ttt3Dir + "\\_Compiler\\Animator.zip")
except FileNotFoundError:
    pass

### Copy the required ttt3.ico file into the _Compiler folder.
##print("\nCopying ttt3.ico icon file...")
##shutil.copy(ttt3Dir + "\\_Resource\\ttt3.ico", ttt3Dir + "\\_Compiler\\")

# Compile Animator.
print("\nCompiling Animator.exe...\n")
PyInstaller.__main__.run([
     "--onefile",
     "--windowed",
##     "--icon=ttt3.ico",
     os.path.join(ttt3Dir, "Animator.py"),
])
print("\nAnimator.exe created.")

# Clean up the build, copy in 'Settings' and 'Data' folders. Remove unnecessary files and renaming 'dist' to 'Animator'.
print("\nCopying 'data' and 'settings' folders...")
shutil.rmtree(ttt3Dir + "\\_Compiler\\build", ignore_errors=True)
os.remove(ttt3Dir + "\\_Compiler\\Animator.spec")
##os.remove(ttt3Dir + "\\_Compiler\\ttt3.ico")
os.rename(ttt3Dir + "\\_Compiler\\dist", ttt3Dir + "\\_Compiler\\Animator")
##shutil.copytree(ttt3Dir + "\\settings", ttt3Dir + "\\_Compiler\\Animator\\settings")
##shutil.copytree(ttt3Dir + "\\data", ttt3Dir + "\\_Compiler\\Animator\\data")
##shutil.copy(ttt3Dir + "\\Animator_readme.htm", ttt3Dir + "\\_Compiler\\Animator\\")
##shutil.copy(ttt3Dir + "\\CHANGELOG.md", ttt3Dir + "\\_Compiler\\Animator\\")
shutil.copy(ttt3Dir + "\\gui.ui", ttt3Dir + "\\_Compiler\\Animator\\")

### Create Animator.zip for distribution.
##print("\nCreating Animator.zip. Please wait...")
##with ZipFile('_Compiler\\Animator.zip', 'w', compression=ZIP_DEFLATED, compresslevel=9) as zipObj:
##   # Iterate over all the files in directory
##    for folderName, subfolders, filenames in os.walk(os.getcwd() + "\\_Compiler\\Animator"):
##        for filename in filenames:
##           # Create complete filepath of file in directory
##           filePath = os.path.join(folderName, filename)
##           # Add file to zip
##           zipObj.write(filePath, filePath.split("_Compiler\\")[1])
##print("\nAnimator.zip created.")
bits = sys.version[ : sys.version.index(" bit")][-3:]
version = platform.platform().split("-")[0] + bits + "-bit"
print("\n\n----------- Compile for %s Complete -----------\n\n" % version)
#----------------------------------------------------------------------------------------------------------------------------------------------------#
