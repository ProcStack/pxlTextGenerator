############################################
## pxlTextGenerator v0.1.2                ##
## Text to Handwriting Generator          ##
##  Written by Kevin Edzenga; ~2018-2019  ##
##   http://metal-asylum.net              ##
##                                        ##
## For aditional work, see my github-     ##
##  https://github.com/procstack          ##
############################################
"""
 This tool is designed to allow users to gather hand written characters,
  (Or I guess, any connected mass)
  In photos and export them to an image library.
 A database is built so later iterations of this tool can take the exported
  characters and use them to convert typed text into an image that is seemingly hand written.
 Currently, You can save out hand written characters into individual PNG files with options
   to modify the alpha fall off from the dynamically built mask of the ink.
 Since I have an intended purpose for this, it is expecting white/tan/beige paper and dark ink.
 Being that, the color threshold will tell the script to select only neighboring pixels of color
   darker than the designated magnitude of brightness set.
   
 The long term goal is to adapt this to be more of an OCR for many books I've written that other's have failed on.
 To actually train the system, where it builds vectors and quadratic curves to make assumptions
  for what characters are what.
 It is slow right now, but hoping to expand this out toward OpenGL or C++ in the future.
 Python and PyQt was just the easy route to start with.
  
 Help if you'd like!
 Submit bugs; make a branch and send in pull requests;
 Get this working for the less knowledgeable  out there!!
 
 Stay awesome and open source for life!

######
- - v0.1.3 - - #### lines of Python & PyQt - -
 Main window Python code has been moved to `includes/local_mainWindow.py`
 Option to not exit from current Work Area upon Finishing Character
 Sample Threshold by Color is now toggleable
 After you Set Working Area, it will auto Crop To Work Area
 Exit Work Area on Reset checkbox moved next to the Work Area buttons
 Add Brush now finds Edge Pixels of the added areas
 Fixed bug edge bug in Read Found Character Data
   Edge Pixels were getting cleared, requiring Grow/Shrink Edge to run again
 Added Hotkey support-
	P - Load a Project Folder
	T - Sample Threshold Color; toggle
	S - Select Mode
	A - Set to Add Brush
	R - Set to Remove Brush
	W - Set Working Area; toggle
	C - Crop to Work Area; toggle
	O - Show Outline Only; toggle

- - v0.1.2 - - 5049 lines of Python & PyQt - -
 Tons and Tons of checks for Errors, Cancels, and Parameter updates
   Search Clean Up Pass supports canceling by hittin Escape
     _Also displays progress in the status bar now
   Grow / Shrink supports canceling now
     _Also checks if the parameter value changes and restarts the function
   Zooming too far or too many setPixel edits would case QImage to run out of memory,
     Causing the TextBase Viewer image to disapear.
	 Now checks if the image failed to render and zooms out until the image displays
 Working Area is fully functional
   When searching for Character Data with a set Work Area,
     The image will crop to the Work Area to speed up efficiency and time.
   With a smaller image, you'll be able to zoom in further.
   Zooming in further, makes Add/Remove Brushes easier and faster to use
   Resetting Character Data and Finishing Character will clear current working area
 Finished Characters will highlight in red
   These highlights will remain/show up -
     -When gathering new Character Data
     -Switching between TextBase Images
	 -Exporting Character List and show up when you re-open pxlTextGenerator
 More bug fixes as always.
 I'm sure there is more, I updated a lot
 
- - v0.1.1 - -
 Support for windows smaller than 2200x1200 like it was restricted to in the past!!
 Allowing me to do that resorted to-
   -Reorganized the Character Entry Editor layout to allow scrolling
   -Dynamic scale of the TextBed
   With this, the window can now be shrunk without an issue with the layout
 Upgraded all sliders to SliderGroup's
   This allows users to click the corresponding text to input values manually.
 New buttons on the TextBase viewer-
   Set Work Area - You can select an area that will be cropped down during character searching
   Show Outline Only - Only renders the outline of the found characters ONCE, clears on redraw
   Show Normal Display - Render the found character data like normal; filled in green
 Auto-load the TextBed background image if exists
   This way, you don't need to manually load up the background.
 Finally got 'Help...' pointing to the pxlTextGenerator GitHub repo ReadMe.md
 
 For the list of existing Issues and To-Do's -
   https://github.com/ProcStack/pxlTextGenerator/issues
 
"""
scriptNameText="pxlTextGenerator"
versionText="v0.1.3; Alpha"

import sys, os
import re
import datetime as dt
import Xlib.XK
import Xlib.display
from PIL import Image
from PyQt4 import QtGui, QtCore
from functools import partial
import math
import random
import ast

### Local Imports ###
execfile("includes/local_mainWindow.py")
execfile("includes/local_indexImageEntry.py")
execfile("includes/local_textBaseViewer.py")
execfile("includes/local_textCharViewer.py")
execfile("includes/local_textToCharDisplay.py")
execfile("includes/local_guiWidgets.py")

frozen=0
curDir='.'
bundleDir='.'
if getattr(sys, 'frozen', False):
	frozen=1
	bundleDir=sys._MEIPASS
else:
	bundleDir=os.path.dirname(os.path.abspath(__file__))
	curDir=bundleDir

platforms={
	"win32":"win",
	"linux1":"linux",
	"linux2":"linux",
	"darwin":"osx"
	}
curOS=sys.platform
curOS=curOS if curOS not in platforms.keys() else platforms[curOS]

delimit="/"
if curOS == "win":
	delimit="\\"

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	galGen=ImageProcessor()
	galGen.show()
	try:
		sys.exit(app.exec_())
	except:
		pass;
