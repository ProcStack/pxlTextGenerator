############################################
## pxlTextGenerator v0.2.4                ##
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
   
######
- - v0.2.4 - - 5845 lines of Python & PyQt - -
 Page Output updates-
   %absolute% / %abs% tag is now working
     These are absolute placement of text on page.
     Currently, absolute placement only works on the current line
       It will act like all other tags in the future, but not needed for now
     Much like %offset%, single values only modify Y position.
       %abs:-10% will be a position of
         X -> 0
         Y -> -10
     Alignment works within absolute position tags too.
       %abs:-20%%a:center% Will center align your line, but Y -> -20
   Exporting for OpenGL requires texture resolutions in powers of 2
     Check box added to scale the output pages to the closest smallest power of 2
     IE, a background image of 1536x2048
       will output images with a scaled down resolution of 1024x2048
- - v0.2.3 - - 5733 lines of Python & PyQt - -
 Better default page settings
 Checks for JPG and PNG default page background
 Fixed slider colors
- - v0.2.2 - - 5729 lines of Python & PyQt - -
 Page Output updates-
   Saves weren't picking up pageGroup names
   Exporting all of the found data became rather obtuse
     Was saving all character data found
	 Removed, to avoid 5+ meg pageData files
	 The data wasn't used, but wanted to be used 
	 Might bring back in the future.
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
 
"""
scriptNameText="pxlTextGenerator"
versionText="v0.2.4; Beta"

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
