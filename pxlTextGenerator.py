############################################
## pxlTextGenerator v0.2.1                ##
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
- - v0.2.1 - - 5711 lines of Python & PyQt - -
 Page Output updates-
   Added Flip Text check box
     Saves and loads correctly
- - v0.2.0 - - 5676 lines of Python & PyQt - -
 Page Output updates-
   Exporting and Loading pageData working correctly now.
   Special characters working correctly-
    %charName% to output the character you desire
      eg- %str% for a star symbol instead of just a multiply symbol
    Custom special characters not implimented yet,
      Thats a little outside my current needs for this tool.
    Current supported special characters-
      "ocl","ocr","oll","olr","osl","osr","oal","oar","str"
    They can be set to what ever you'd like though,
      Just because it's called 'str' doesn't mean it needs to be a star.
   Text Formatting System implimented-
    %formatting:value% then %formatting% without a value to reset,
    eg-
      %offset:0,100% to offset 100px in Y
      %offset% to being the offset back to 0,0
    Currently supports
      %###% to scale text; %50% is 50 percent scale, %100% to get back to normal
      
      %align:position% - the positions can be `left`, `center`, or `right`
      %align:center% to align your text center then %align% to reset to left alignment.
        Affects whole line until set again or reset with %align%
      %a:position% - Set alignment for current line only
        Any return or `\n` will reset the alignment to `left`
        
      %offset:#,#% - Offset characters in X,Y by pixels
        Relative offset for all following text.
        If you put only one number, it will offset only in Y
          %offset:10% - Will offset the following text [0,10]
        Affects whole lines until set again or reset with %offset% or %o%
      %o:#,#% - To set offset for the next character only
        It will reset to 0,0 offset after the next character.
        
      %rotate:degrees% - Rotate characters in degrees for all following text.
      
      %spaceSize:pixels% - Line space size ixels is relative offset.
        %spaceSize:-10% - If space size is 50, it will be 40
        Affects whole lines until set again or reset with %spaceSize% or %ss%
      %ss:pixels% - Set spaceSize for current line only
        Any return or `\n` will reset the spaceSize to current setting
        
      %kern:pixels% - Line character kerning in relative pixels offset.
        %kern:-10% - If kerning is 0, it will be -10
        Affects whole lines until set again or reset with %kern% or %k%
      %k:pixels% - Set kerning for next character only
        It will reset to a 0 pixel kerning offset after the next character.
        
      %lineHeight:pixels% - pixels is relative offset
        %lineHeight:-20% - If line height is 70, it will be 50
        %lineHeight% to clear offset.
        Affects whole lines until set again or reset with %lineHeight% or %lh%
      %lh:pixels% - Set lineHeight pixels for current line only
        Any return or `\n` will reset the lineHeight to current setting
      
      %seed:#% - Set the seed random for following characters.
        %seed:12.4% to set a random value of 12.4
        %seed% to reset to your set seed
        This is good for changing a lot of characters in a word or line.
      %s% or %s:#% - To set a random or specific seed for the next character only
        If a specific character is a repeat of a near by variation-
          "will" and both 'l's are the same 'l'-
          "wil%s%l" changes the second 'l' to a different variation
          
      %opacity:percent% - Percentage is 0-100
        %opacity:50% - The characters following will be at 50% opacity.
        Affects whole lines until set again or reset with %opacity% or %op%
      %op:percent% - To set opacity for the next character only
        It will reset to 100% opacity after the next character.
          

- - v0.1.3 - - 5239 lines of Python & PyQt - -
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
 
 For the list of existing Issues and To-Do's -
   https://github.com/ProcStack/pxlTextGenerator/issues
 
"""
scriptNameText="pxlTextGenerator"
versionText="v0.2.1; Beta"

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
