############################################
## pxlTextGenerator v0.0.1                ##
## Text to Handwriting Generator          ##
##  Written by Kevin Edzenga; ~2018       ##
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
 
"""

import sys, os
import re
import datetime as dt
from PIL import Image
from PyQt4 import QtGui, QtCore
from functools import partial
import math
import random

### Local Imports ###
execfile("includes/local_guiWidgets.py")
execfile("includes/local_indexImageEntry.py")
execfile("includes/local_textBaseViewer.py")
execfile("includes/local_textCharViewer.py")
execfile("includes/local_textToCharDisplay.py")

frozen=0
curDir='.'
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
	
class ImageProcessor(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(ImageProcessor,self).__init__(parent)
		global woVersion
		
		self.scriptNameText="pxlTextGenerator"
		self.versionText="v0.0.8"
		self.setTitleBar()
		
		self.winSize=[2200,1200]
		self.setMinimumSize(self.winSize[0],self.winSize[1])
		self.resize(self.winSize[0],self.winSize[1])
		# Create custom top bar styles and widgets
		# Then set existing window as frame inside the main window
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
		#self.setStyleSheet("padding:0px;")
		
		self.textBase=''
		self.textBaseImages='pxl_textBases_origImages'
		self.textCharacterOutput='pxl_textCharacterOutput'
		self.pageBuilderOutput='pxl_pageBuilderOutput'
		self.projectName="Untitled"
		self.textBaseViewWindow=''
		self.textBasePath=''
		self.imgData={}
		self.curImage=None
		self.curImagePath=None
		self.sampleMode=1
		self.zoom=1.0
		self.runValChangeEvent=1
		self.loopLatch=0
		self.selectColorMode=0
		self.selectColorSamples=[]
		self.checkerBoard=None
		self.displayCheckerBoard=1
		self.buttonStyle="height:25px;padding-left:10px;padding-right:10px;"
		self.curImageFull=512
		self.curImageHelpers=196
		self.unsavedChanges=0
		self.charSampled=0
		
		## BELOW IS OLD ##
		self.websiteName=""
		self.websiteSettingsFile=""
		self.galleryName=""
		self.galleryPath=""
		self.curEntryObj=-1
		self.dirImageList={}
		self.loadIndexList=[]
		self.loadScrollList=[]
		self.charSamplePoints=[]
		self.scrollIndexVal=0
		self.scrollIndexHeight=-1
		self.mainWidget=QtGui.QWidget(self)
		
		self.imgFullPerc=50
		self.imgFullTilePerc=5
		self.imgMedPerc=25
		self.imgThumbPerc=10
		self.imgQualityPerc=50
		
		self.setWindowStyleSheet()
		self.statusBarMsg=''
		self.statusBarFade=25
		self.statusBarFadeMax=25
		self.statusBarPerc=0
		self.statusBarLength=1
		self.statusBarMode=0
		self.statusBarModeSet=0
		
		### Menu Bar ###
		self.menuBar=self.menuBar()
		fileMenu=self.menuBar.addMenu('File')
		fileMenu.addSeparator()
		quitItem=QtGui.QAction("Exit",self)
		quitItem.triggered.connect(self.quitPromptCreate)
		fileMenu.addAction(quitItem)
		self.infoMenu=self.menuBar.addMenu('Info')
		scriptInfoItem=QtGui.QAction(self.versionText,self)
		self.infoMenu.addAction(scriptInfoItem)
		authorItem=QtGui.QAction("Written by Kevin Edzenga",self)
		self.infoMenu.addAction(authorItem)
		infoItem=QtGui.QAction("www.Metal-Asylum.net",self)
		self.infoMenu.addAction(infoItem)
		self.infoMenu.addSeparator()
		totalLineCount=self.findTotalLineCount()
		lineCountItem=QtGui.QAction("Total Line Count - "+str(totalLineCount),self)
		self.infoMenu.addAction(lineCountItem)
		self.infoMenu.addSeparator()
		helpItem=QtGui.QAction("Help...",self)
		self.infoMenu.addAction(helpItem)
		# Status Bar
		self.statusBar=self.statusBar()
		self.statusBar.messageChanged.connect(self.statusBarChange)

		self.mainLayout=QtGui.QVBoxLayout(self.mainWidget)
		self.mainLayout.setSpacing(0)
		self.mainLayout.setMargin(0)
		
		self.tabWidget=QtGui.QTabWidget()
		###
		self.tabLayout_processing=QtGui.QWidget()
		###
		self.tabLayout_pageOutput=QtGui.QWidget()
		###
		self.tabWidget.addTab(self.tabLayout_processing, "Characters Builder")
		self.tabWidget.addTab(self.tabLayout_pageOutput, "Page Output")
		self.mainLayout.addWidget(self.tabWidget)
		
		######
		self.processingTabLayout=QtGui.QVBoxLayout()
		pad=2
		self.processingTabLayout.setSpacing(pad)
		self.processingTabLayout.setMargin(pad)
		selfSize=self.geometry()
		menuSize=self.menuBar.geometry()
		selfSize=[selfSize.width(), selfSize.height()-menuSize.height()]

		# Load directory text field
		self.dirBlock=QtGui.QHBoxLayout()
		self.dirField=QtGui.QLineEdit()
		self.dirBlock.addWidget(self.dirField)
		# Create Load Dir button
		self.loadDir=QtGui.QPushButton('Set Project Folder', self)
		self.loadDir.setStyleSheet(self.buttonStyle)
		self.loadDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.loadDir.clicked.connect(self.loadAndScanDir)
		self.dirBlock.addWidget(self.loadDir)
		#tab0.addLayout(self.dirBlock)
		self.processingTabLayout.addLayout(self.dirBlock)
		
		# Load directory text field
		self.imageDisplayBlock=QtGui.QVBoxLayout()
		self.imgField=QtGui.QLabel()
		self.imgField.setText("""\n
- - Please select your 'Project Folder' containing - -\n\n
1) Folder with your full sized images for a fresh build.
( Supported - jpg, jpeg, png, bmp )\n\n\n
2) Project Folder containing 'Character List' or 'Page Data' exports.\n
( charListKey.py / pageListKey.py )""")
		self.imgField.setAlignment(QtCore.Qt.AlignCenter)
		self.imageDisplayBlock.addWidget(self.imgField)
		self.imgSpacer=QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.imageDisplayBlock.addItem(self.imgSpacer)
		#tab0.addLayout(self.imageDisplayBlock)
		self.processingTabLayout.addLayout(self.imageDisplayBlock)
		
		### Character Test ###
		self.textCharDisplayBlock=QtGui.QVBoxLayout()
		self.textCharDisplayBlock.setSpacing(0)
		self.textCharDisplayBlock.setMargin(0)
		self.processingTabLayout.addLayout(self.textCharDisplayBlock)
		
		### Process Block ###
		pad=1
		self.processLayout=QtGui.QVBoxLayout()
		self.processLayout.setSpacing(pad)
		self.processLayout.setMargin(pad)
		self.processingTabLayout.addLayout(self.processLayout)
		self.tabLayout_processing.setLayout(self.processingTabLayout)
		
		######
		pageBuilderTabLayout=QtGui.QVBoxLayout()
		pageBuilderTabLayout.setSpacing(0)
		pageBuilderTabLayout.setMargin(0) 
		self.pageViewer=PageBuilder(self)
		pageBuilderTabLayout.addWidget(self.pageViewer)
		self.tabLayout_pageOutput.setLayout(pageBuilderTabLayout)
		
		######
		self.setCentralWidget(self.mainWidget)
		
		"""def newButton(self,name,txt,cmd,layout):
		eval(str(name)+"=QtGui.QPushButton('"+str(txt)+"', self)")
		eval(str(name)+".clicked.connect("+cmd+")")
		eval(str(layout)+".addWidget("+str(name)+")")"""
		
	def setTitleBar(self,custDisp=[]):
		disp=[]
		disp.extend(custDisp)
		disp.extend([self.scriptNameText])
		disp.extend([self.versionText])
		disp=" - ".join(disp)
		self.windowText=disp
		self.setWindowTitle(self.windowText)
	def findTotalLineCount(self):
		files=[]
		files.append(__file__)
		dir="/".join(bundleDir.split("\\"))
		dirScan=map(lambda x: "includes/"+x, os.listdir("includes/"))
		dirScan=filter(	os.path.isfile, dirScan)
		files.extend(dirScan)
		lineCount=0
		for file in files:
			read=open(file,'r')
			lineCount+=len(read.readlines())
		return lineCount
	def setCursorPointing(self):
		QtGui.QWidget.setCursor(self.infoMenu,QtCore.Qt.PointingHandCursor)
	def setCursorArrow(self):
		QtGui.QWidget.setCursor(self.infoMenu,QtCore.Qt.ArrowCursor)
	def setWindowStyleSheet(self):
		self.winPalette=QtGui.QPalette()
		self.winPalette.setColor(QtGui.QPalette().Window, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Base, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Background, QtGui.QColor(30,30,30))
		self.winPalette.setColor(QtGui.QPalette().Button, QtGui.QColor(60,60,60))
		self.winPalette.setColor(QtGui.QPalette().ToolTipBase, QtGui.QColor(20,20,20))
		self.winPalette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(80,80,80))
		self.winPalette.setColor(QtGui.QPalette().WindowText, QtGui.QColor(200,200,200))
		self.winPalette.setColor(QtGui.QPalette().ButtonText, QtGui.QColor(200,200,200))
		self.winPalette.setColor(QtGui.QPalette().ToolTipText, QtGui.QColor(200,200,200))
		self.winPalette.setColor(QtGui.QPalette().BrightText, QtGui.QColor(255,255,255))
		self.winPalette.setColor(QtGui.QPalette().HighlightedText, QtGui.QColor(80,80,80))
		self.winPalette.setColor(QtGui.QPalette().Link, QtGui.QColor(100,100,200))
		self.winPalette.setColor(QtGui.QPalette().Dark, QtGui.QColor(32,32,32))
		self.winPalette.setColor(QtGui.QPalette().Light, QtGui.QColor(32,32,32))
		#self.winPalette.setCurrentColorGroup(QtGui.QPalette.Normal)
		
		self.setPalette(self.winPalette)
		QtGui.QApplication.setPalette(self.winPalette)
		styleSheetCss="""
		* {font-size:10pt;}
		QToolTip {color:#ffffff;background-color:#202020;border: 1px solid #ffffff;}
		QPushButton {color:#ffffff;background-color:#232323;padding:4px;border:1px solid #000000;}
		QLineEdit {color:#111111;background-color:#909090;padding:2px;border:1px solid #202020;height:25px;}
		QScrollArea {color:#ffffff;background-color:#808080;border:1px solid #202020;}
		QTabWidget::pane {color:#ffffff;background-color:#323232;border:0px;}
		QTabWidget::tab-bar {color:#ffffff;background-color:#101010;}
		QTabBar::tab {color:#777777;background-color:#242424;border:1px solid #202020;padding:7px 10px 3px 10px;}
		QTabBar::tab:selected {color:#ffffff;background-color:#323232;border:1px solid #2a2a2a;padding:7px 10px 3px 10px;}
		QAction {color:#ffffff;background-color:#808080;border:1px solid #202020;}
		QMenuBar {color:#ffffff;background-color:#606060;border:1px solid #202020;}
		QMenuBar::item {color:#ffffff;background-color:#707070;padding:2px;border:1px solid #505050;}
		QMenu {color:#ffffff;background-color:#707070;border:1px solid #404040;}
		QMenu::item {color:#ffffff;background-color:#707070;padding:2px;}
		QMenu::item:selected {color:#ffffff;background-color:#9c9c9c;padding:2px;}
		QSlider {background-color:#323232;}
		QScrollBar:vertical {width:20px;background-color:#808080;border:1px solid #202020;}
		QScrollBar:horizontal {height:20px;background-color:#808080;border:1px solid #202020;}
		QStatusBar {color:#ffffff;font-weight:bold;background-color:#606060;border:1px solid #202020;}
		QMessageBox {background-color:#505050;color:#ffffff}
		QLabel {color:#ffffff}"""
		self.setStyleSheet(styleSheetCss)
	def statusBarUpdate(self, msg=None, length=5000, mode=1):
		self.statusBarMode=mode
		if mode==0:
			self.statusBarModeSet=-1
			self.statusBar.showMessage(msg, length)
		else:
			self.statusBarMsg=msg
			self.statusBarLength=length
			self.statusBarPerc=self.statusBarFadeMax
			self.statusBarModeSet=0
			self.statusBar.showMessage(msg, self.statusBarFade)

	def statusBarChange(self):
		if self.statusBarMode > 0 and self.statusBarModeSet==0:
			grey=96.0
			r=g=b=int(grey)
			perc=self.statusBarPerc/self.statusBarFadeMax
			
			if self.statusBarMode == 1: # Good / Alert
				g=int(grey*(1.0-perc) + 200.0*perc)
				b=int(grey*(1.0-perc) + 50.0*perc)
			elif self.statusBarMode == 2: # Error
				r= int(grey*(1.0-perc) + 255.0*perc)
			rgb=QtGui.QColor(r,g,b)
			rgb=rgb.name()
			self.statusBar.setStyleSheet("QStatusBar {color:#ffffff;font-weight:bold;background-color:"+rgb+";border:1px solid #202020;}")
			if self.statusBarPerc > 0:
				length=self.statusBarFade
				self.statusBarPerc-=1.0
			else:
				length=self.statusBarLength
				self.statusBarMode=0
			self.statusBarModeSet=1
			self.statusBar.showMessage(self.statusBarMsg, length)
		else:
			if self.statusBarModeSet==1:
				self.statusBarModeSet=0
	def loadAndScanDir(self):
		### Choose a Project Folder here ###
		folderPicker=QtGui.QFileDialog.getExistingDirectory(self,"Select Project Folder",curDir)
		if folderPicker != "":
			folderPicker=str(folderPicker)
			activeList=[]
			if os.path.isdir(folderPicker):
				if curOS == "win":
					folderPicker="/".join(folderPicker.split("\\"))
				self.textBase=folderPicker
				folderSplit=folderPicker.split('/') # Delimitter gets corrected in pyqt
				textBaseFile=folderSplit[-1]
				self.projectName=textBaseFile
				
				self.setTitleBar([self.projectName])
				
				folderPicker='/'.join(folderSplit[:-1])
				activeList.append(textBaseFile)
			ClearLayout(self.imageDisplayBlock)
			if len(activeList) == 0:
				extListStr=""
				for x in extList:
					extListStr+=str(x)+", "
				extListStr=extListStr[0:-2]
				fBold=QtGui.QFont()
				fBold.setBold(True)
				
				tmpBlock=QtGui.QVBoxLayout()
				tmpText=QtGui.QLabel()
				tmpText.setText("No usable images found in-")
				tmpBlock.addWidget(tmpText)
				tmpText=QtGui.QLabel()
				tmpText.setText(folderPicker)
				tmpText.setAlignment(QtCore.Qt.AlignCenter)
				tmpText.setFont(fBold)
				tmpBlock.addWidget(tmpText)
				self.imageDisplayBlock.addWidget(self.imgField)
				self.imgSpacer=QtGui.QSpacerItem(20,10,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				tmpBlock.addItem(self.imgSpacer)
				tmpText=QtGui.QLabel()
				tmpText.setText("Please use a folder containing images using extentions-")
				tmpBlock.addWidget(tmpText)
				tmpText=QtGui.QLabel()
				tmpText.setText(extListStr)
				tmpText.setAlignment(QtCore.Qt.AlignCenter)
				tmpText.setFont(fBold)
				tmpBlock.addWidget(tmpText)
				imgSpacer=QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
				tmpBlock.addItem(imgSpacer)
				self.imageDisplayBlock.addLayout(tmpBlock)
			else:
				sizeSub=100
				pad=0#5
				
				entryBlock=QtGui.QHBoxLayout()
				entryEditBlock=QtGui.QHBoxLayout()
				entryEditBlock.setSpacing(0)
				
				##### ENTRY EDITED IMAGE DISPLAY #####
				
				resetCharBlock=QtGui.QVBoxLayout()
				resetCharButton=QtGui.QPushButton("Reset Character Data",self)
				resetCharButton.setStyleSheet(self.buttonStyle)
				resetCharButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				resetCharButton.clicked.connect(self.resetCurTextCharacter)
				resetCharBlock.addWidget(resetCharButton)
				entryEditBlock.addLayout(resetCharBlock)
				######
				thresholdColorRes=[150,50]
				fill=QtGui.QColor(66,67,67)
				###
				thresholdColorBlock=QtGui.QHBoxLayout()
				###
				self.thresholdColorNameText=QtGui.QLabel()
				self.thresholdColorNameText.setText("Color Threshold")
				self.thresholdColorNameText.setMinimumWidth(90)
				self.thresholdColorNameText.setAlignment(QtCore.Qt.AlignRight)
				thresholdColorBlock.addWidget(self.thresholdColorNameText)
				###
				self.thresholdColorSlider=QtGui.QSlider()
				self.thresholdColorSlider.setOrientation(QtCore.Qt.Horizontal)
				self.thresholdColorSlider.setMinimum(0)
				self.thresholdColorSlider.setMaximum(765)
				self.thresholdColorSlider.setValue(230)
				thresholdColorBlock.addWidget(self.thresholdColorSlider)
				###
				thresholdColorMagTextBlock=QtGui.QVBoxLayout()
				##
				self.thresholdColorMagText=QtGui.QLabel()
				self.thresholdColorMagText.setText("230 #\n-20")
				self.thresholdColorMagText.setStyleSheet("QLabel {font-size:10pt; line-height:50%}")
				self.thresholdColorMagText.setMinimumWidth(90)
				self.thresholdColorMagText.setAlignment(QtCore.Qt.AlignRight)
				self.thresholdColorMagText.setMaximumHeight(thresholdColorRes[1])
				thresholdColorMagTextBlock.addWidget(self.thresholdColorMagText)
				##
				thresholdColorBlock.addLayout(thresholdColorMagTextBlock)
				self.thresholdColorSlider.valueChanged.connect(self.thresholdColorMagTextUpdate)
				###
				self.thresholdColor=QtGui.QLabel()
				baseImg=QtGui.QPixmap(thresholdColorRes[0],thresholdColorRes[1])
				baseImg.fill(fill)
				self.thresholdColor.setPixmap(baseImg)
				thresholdColorBlock.addWidget(self.thresholdColor)
				###
				thresholdColorSample=QtGui.QPushButton("Sample Color",self)
				thresholdColorSample.setStyleSheet(self.buttonStyle)
				thresholdColorSample.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				thresholdColorSample.clicked.connect(self.sampleNewThresholdColor)
				thresholdColorBlock.addWidget(thresholdColorSample)
				###
				resetCharBlock.addLayout(thresholdColorBlock)
				######
				
				self.edgeGrowthSlider=SliderGroup(self,"Edge Grow/Shrink", [-10,10,0],7,"int","px", "extendEdges()")
				resetCharBlock.addWidget(self.edgeGrowthSlider)
				
				curEntryEditScrollBlock=QtGui.QScrollArea() #QAbstractScrollArea()
				curEntryEditScrollBlock.setWidgetResizable(True)
				#curEntryEditScrollBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				curEntryEditScrollInner=QtGui.QWidget(curEntryEditScrollBlock)
				curEntryEditScrollInner.setStyleSheet("QWidget {background-color:#2a2a2a;}")

				self.curEntryBlock=QtGui.QVBoxLayout()
				self.curEntryBlock.setAlignment(QtCore.Qt.AlignCenter)
				curEntryEditScrollInner.setLayout(self.curEntryBlock)
				self.curEntryBlock.setSpacing(pad)
				self.curEntryBlock.setMargin(pad)
				tmpEntry=QtGui.QLabel()
				tmpEntry.setText("Placeholder")
				tmpEntry.setAlignment(QtCore.Qt.AlignCenter)
				self.curEntryBlock.addWidget(tmpEntry)
				
				curEntryEditScrollBlock.setWidget(curEntryEditScrollInner)
				#entryEditBlock.addWidget(curEntryEditScrollBlock)
				resetCharBlock.addWidget(curEntryEditScrollBlock)
				
				##### ENTRY EDIT PARAMETERS #####
				#self.curImageDisplayEditParent=QtGui.QVBoxLayout()
				self.curImageDisplayEditBlockWidget=QtGui.QWidget()
				self.curImageDisplayEditBlockWidget.setMinimumWidth(650)
				self.curImageDisplayEditBlockWidget.setMaximumWidth(850)
				entryEditBlock.addWidget(self.curImageDisplayEditBlockWidget)
				self.curImageDisplayEditBlock=QtGui.QVBoxLayout()
				self.curImageDisplayEditBlock.setSpacing(0)
				self.curImageDisplayEditBlock.setMargin(0)
				self.curImageDisplayEditBlockWidget.setLayout(self.curImageDisplayEditBlock)
				
				self.curImageButtonBlock=QtGui.QVBoxLayout()
				updateButton=QtGui.QPushButton("Read Fitted Scaling",self)
				updateButton.setStyleSheet(self.buttonStyle)
				updateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				updateButton.clicked.connect(self.pullFittedScale)
				self.curImageButtonBlock.addWidget(updateButton)
				###
				self.curImageDisplayEditBlock.addLayout(self.curImageButtonBlock)
		
				spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
				self.curImageDisplayEditBlock.addItem(spacer)
				
				######
				self.curImageDisplayBlock=QtGui.QHBoxLayout()
				###
				curImageTopPaddingBlock=QtGui.QVBoxLayout()
				curImageTopPadding=QtGui.QLabel()
				curImageTopPadding.setText("T\nO\nP")
				curImageTopPadding.setMinimumWidth(10)
				curImageTopPadding.setAlignment(QtCore.Qt.AlignCenter)
				curImageTopPaddingBlock.addWidget(curImageTopPadding)
				###
				self.sliderTopPadding=QtGui.QSlider()
				self.sliderTopPadding.setOrientation(QtCore.Qt.Vertical)
				self.sliderTopPadding.setMinimum(-128)
				self.sliderTopPadding.setMaximum(128)
				self.sliderTopPadding.setValue(0)
				curImageTopPaddingBlock.addWidget(self.sliderTopPadding)
				###
				self.paddingTopVal=QtGui.QLabel()
				self.paddingTopVal.setText(" \n \n \n0\np\nx")
				self.paddingTopVal.setAlignment(QtCore.Qt.AlignCenter)
				curImageTopPaddingBlock.addWidget(self.paddingTopVal)
				self.curImageDisplayBlock.addLayout(curImageTopPaddingBlock)
				self.sliderTopPadding.valueChanged.connect(self.paddingTopSliderChange)
				###
				###
				self.curImageFinalDisplay=TextCharacterViewer(self,self.textBase,3,self.curImageFull)
				self.curImageDisplayBlock.addWidget(self.curImageFinalDisplay)
				self.curImageDisplayBlock.setAlignment(QtCore.Qt.AlignCenter)
				self.curImageDisplayEditBlock.addLayout(self.curImageDisplayBlock)
				###
				###
				curImageBottomPaddingBlock=QtGui.QVBoxLayout()
				curImageBottomPadding=QtGui.QLabel()
				curImageBottomPadding.setText("B\nO\nT")
				curImageBottomPadding.setMinimumWidth(10)
				curImageBottomPadding.setAlignment(QtCore.Qt.AlignCenter)
				curImageBottomPaddingBlock.addWidget(curImageBottomPadding)
				###
				self.sliderBottomPadding=QtGui.QSlider()
				self.sliderBottomPadding.setOrientation(QtCore.Qt.Vertical)
				self.sliderBottomPadding.setMinimum(-128)
				self.sliderBottomPadding.setMaximum(128)
				self.sliderBottomPadding.setValue(0)
				curImageBottomPaddingBlock.addWidget(self.sliderBottomPadding)
				###
				self.paddingBottomVal=QtGui.QLabel()
				self.paddingBottomVal.setText(" \n \n \n0\np\nx")
				self.paddingBottomVal.setAlignment(QtCore.Qt.AlignCenter)
				curImageBottomPaddingBlock.addWidget(self.paddingBottomVal)
				self.curImageDisplayBlock.addLayout(curImageBottomPaddingBlock)
				self.sliderBottomPadding.valueChanged.connect(self.paddingBottomSliderChange)
				######
				### Left / Right Align ###
				leftRightAlignBlockWidgetBlock=QtGui.QVBoxLayout()
				leftRightAlignBlockWidgetBlock.setAlignment(QtCore.Qt.AlignCenter)
				leftRightAlignBlockWidget=QtGui.QWidget()
				leftRightAlignBlockWidget.setFixedWidth(530)
				leftRightAlignBlock=QtGui.QVBoxLayout()
				leftRightAlignBlock.setSpacing(0)
				leftRightAlignBlock.setMargin(0)
				leftRightAlignBlock.setAlignment(QtCore.Qt.AlignCenter)
				leftRightAlign=QtGui.QHBoxLayout()
				leftRightAlign.setSpacing(0)
				leftRightAlign.setMargin(0)
				###
				self.leftAlignSlider=QtGui.QSlider()
				self.leftAlignSlider.setOrientation(QtCore.Qt.Horizontal)
				self.leftAlignSlider.setFixedWidth(253)
				self.leftAlignSlider.setMinimum(0)
				self.leftAlignSlider.setMaximum(128)
				self.leftAlignSlider.setValue(64)
				leftRightAlign.addWidget(self.leftAlignSlider)
				###
				spaceSpacerAlignText=QtGui.QLabel()
				spaceSpacerAlignText.setAlignment(QtCore.Qt.AlignCenter)
				spaceSpacerAlignText.setFixedWidth(5)
				leftRightAlign.addWidget(spaceSpacerAlignText)
				###
				self.rightAlignSlider=QtGui.QSlider()
				self.rightAlignSlider.setOrientation(QtCore.Qt.Horizontal)
				self.rightAlignSlider.setFixedWidth(253)
				self.rightAlignSlider.setMinimum(0)
				self.rightAlignSlider.setMaximum(128)
				self.rightAlignSlider.setValue(64)
				leftRightAlign.addWidget(self.rightAlignSlider)
				######
				leftRightAlignBlock.addLayout(leftRightAlign)
				self.leftAlignSlider.valueChanged.connect(self.leftRightAlignSliderChange)
				self.leftAlignSlider.sliderReleased.connect(self.leftRightAlignSliderChange)
				self.rightAlignSlider.valueChanged.connect(self.leftRightAlignSliderChange)
				self.rightAlignSlider.sliderReleased.connect(self.leftRightAlignSliderChange)
				######
				### Left / Right Align Text ###
				leftRightAlignText=QtGui.QHBoxLayout()
				leftRightAlignText.setSpacing(0)
				leftRightAlignText.setMargin(0)
				leftAlignText=QtGui.QLabel()
				leftAlignText.setText("Left Align")
				leftRightAlignText.addWidget(leftAlignText)
				###
				rightAlignText=QtGui.QLabel()
				rightAlignText.setAlignment(QtCore.Qt.AlignRight)
				rightAlignText.setText("Right Align")
				leftRightAlignText.addWidget(rightAlignText)
				######
				leftRightAlignBlock.addLayout(leftRightAlignText)
				leftRightAlignBlockWidget.setLayout(leftRightAlignBlock)
				leftRightAlignBlockWidgetBlock.addWidget(leftRightAlignBlockWidget)
				self.curImageDisplayEditBlock.addLayout(leftRightAlignBlockWidgetBlock)
				######
				
				spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
				self.curImageDisplayEditBlock.addItem(spacer)
				
				self.curImageHelperBlock=QtGui.QHBoxLayout()
				self.curImageHelperBlock.setSpacing(3)
				self.curImageHelperBlock.setMargin(3)
				self.curImageDisplay=TextCharacterViewer(self,self.textBase,0,self.curImageHelpers)
				self.curImageHelperBlock.addWidget(self.curImageDisplay)
				self.curImageOverlayDisplay=TextCharacterViewer(self,self.textBase,1,self.curImageHelpers)
				self.curImageHelperBlock.addWidget(self.curImageOverlayDisplay)
				self.curImageMaskDisplay=TextCharacterViewer(self,self.textBase,2,self.curImageHelpers)
				self.curImageHelperBlock.addWidget(self.curImageMaskDisplay)
				self.curImageHelperBlock.setAlignment(QtCore.Qt.AlignCenter)
				self.curImageDisplayEditBlock.addLayout(self.curImageHelperBlock)
				
				self.curImageSettings=QtGui.QVBoxLayout()
				self.curImageDisplayEditBlock.addLayout(self.curImageSettings)
				
				#entryEditBlock.addLayout(self.curImageDisplayEditBlock)
				entryBlock.addLayout(entryEditBlock)
				
				##### ENTRY INDEX LIST ######
				sideBarWidth=152
				self.sideBarBlock=QtGui.QVBoxLayout()
				self.sideBarTextBase=QtGui.QVBoxLayout()
				self.sideBarTextBase.setAlignment(QtCore.Qt.AlignCenter)
				self.sideBarTextBaseWidget=QtGui.QWidget()
				self.sideBarTextBaseWidget.setLayout(self.sideBarTextBase)
				self.sideBarBlock.addWidget(self.sideBarTextBaseWidget)

				self.filterCharBlock=QtGui.QVBoxLayout()
				self.filterCharText=QtGui.QLabel()
				self.filterCharText.setText("Filter:")
				self.filterCharText.setFixedWidth(sideBarWidth)
				self.filterCharBlock.addWidget(self.filterCharText)
				self.filterCharVal=QtGui.QLineEdit()
				self.filterCharVal.setFixedWidth(sideBarWidth)
				self.filterCharVal.editingFinished.connect(self.filterCharacters)
				self.filterCharBlock.addWidget(self.filterCharVal)
				self.sideBarBlock.addLayout(self.filterCharBlock)
				
				self.scrollIndexBlock=QtGui.QScrollArea()
				self.scrollIndexBlock.setWidgetResizable(True)
				self.scrollIndexBlock.setFixedWidth(sideBarWidth)
				self.scrollIndexBlock.setStyleSheet("QWidget {background-color:#2a2a2a;}")
				self.scrollIndexBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				scrollInner=QtGui.QWidget(self.scrollIndexBlock)
				
				self.curImgListBlock=QtGui.QVBoxLayout(scrollInner)
				self.curImgListBlock.setAlignment(QtCore.Qt.AlignCenter)
				scrollInner.setLayout(self.curImgListBlock)
				self.curImgListBlock.setSpacing(pad)
				self.curImgListBlock.setMargin(pad)
				
				###### ADD TEXTBED ######
				try:
					exists=self.textCharDisplay
				except:
					self.textCharDisplay=TextToCharDisplay(self)
					self.textCharDisplayBlock.addWidget(self.textCharDisplay)
				
					###### OUTPUT AND EXPORT ######
					# Load directory text field
					self.outDirBlock=QtGui.QHBoxLayout()
					self.outDirField=QtGui.QLineEdit()
					self.outDirBlock.addWidget(self.outDirField)
					# Create Load Dir button
					self.setOutDir=QtGui.QPushButton('Output Dir', self)
					self.setOutDir.setStyleSheet(self.buttonStyle)
					self.setOutDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
					self.setOutDir.clicked.connect(self.setOutputDir)
					self.outDirBlock.addWidget(self.setOutDir)
					#tab0.addLayout(self.dirBlock)
					self.processLayout.addLayout(self.outDirBlock)

					# Process Full Button #
					self.processSiteButton=QtGui.QPushButton('Export Character List', self)
					self.processSiteButton.setStyleSheet(self.buttonStyle)
					self.processSiteButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
					self.processSiteButton.clicked.connect(self.exportCharList)
					self.processLayout.addWidget(self.processSiteButton)
				
				size=self.scrollIndexBlock.frameGeometry()
				#size=[size.width()-sizeSub, size.height()]
				size=[128,128]
				scrollOffset=0
				scrollAdd=0
				self.loadIndexList=[]
				self.loadScrollList=[]
				loadObj=-1
				textBasePaths=[]
				#files=os.listdir(activeList[0])
				textBasePaths=self.prepProjectFolder(activeList[0])
				if textBasePaths == None:
					self.statusBarUpdate(" -- Could not create directory '"+activeList[0]+"', Check for correct File Permissions that pxl can write to disk.  -- ", 5000,2)
				else:
					activeList=[textBasePaths[0]]
					
					
					for x,p in enumerate(activeList):
						scrollOffset+=scrollAdd+pad
						
						#IndexImageEntry(win, index, name, relativePath, scaleSize, qtImg):
						curImg=IndexImageEntry(self,x,p,folderPicker+"/",size, None)
						
						#self.curImgListBlock.addWidget(curImg)
						self.sideBarTextBase.addWidget(curImg)
						curImg.offset=scrollOffset
						self.loadIndexList.append(curImg)
						self.loadScrollList.append([])
						self.loadScrollList[-1].append(scrollOffset)
						self.loadScrollList[-1].append(scrollOffset+curImg.imgSizeIndexList[1])
						scrollAdd=curImg.imgSizeIndexList[1]
						if loadObj==-1:
							loadObj=curImg
					self.scrollIndexBlock.setWidget(scrollInner)
					self.sideBarBlock.addWidget(self.scrollIndexBlock)
					entryBlock.addLayout(self.sideBarBlock)
					self.imageDisplayBlock.addLayout(entryBlock)
					#self.updateScrollIndex()
					loadObj.loadImage()
					self.textBasePath=loadObj.imgPath
					self.loadImageEntry(loadObj)
					
					self.loadExistingData()
					self.dispCheckerBoard(self.curImageFull,1)
					#self.textBaseViewWindow.setDefaultScroll() ### GET THIS WORKING
	def prepProjectFolder(self, scanFolder):
		ext=("jpg", "jpeg", "png", "bmp")
		
		### Pretty good easy-access Dir / File Opperation examples -
		###  https://stackabuse.com/creating-and-deleting-directories-with-python/
		textBaseOutput=curDir+delimit+scanFolder+delimit+self.textBaseImages+delimit
		exst=os.path.isdir(textBaseOutput)
		genTextBaseOutputFolder=0
		if exst == False:
			try:
				os.mkdir(textBaseOutput, 0x755)
				genTextBaseOutputFolder=1
			except:
				self.statusBarUpdate(" -- Cheack that there are correct File Permissions for pxl to save built Projects to disk. -- ", 5000,2)
				return None
			textCharacterOutput=curDir+delimit+scanFolder+delimit+self.textCharacterOutput
			os.mkdir(textCharacterOutput, 0x755)
			pageBuilderOutput=curDir+delimit+scanFolder+delimit+self.pageBuilderOutput
			os.mkdir(pageBuilderOutput, 0x755)
		else:
			scanFolder+=delimit+self.textBaseImages
			
		files=os.listdir(scanFolder)
		textBaseNames= filter(lambda x: x.split(".")[-1].lower() in ext, files)
		#textBaseNames=[]
		#textBaseNames.extend(textBasePaths)

		if genTextBaseOutputFolder==1:
			textBaseAbsPaths=map(lambda x: curDir+delimit+scanFolder+delimit+x, textBaseNames)
			textBaseMoveToPaths=map(lambda x: curDir+delimit+scanFolder+delimit+self.textBaseImages+delimit+x, textBaseNames)
			for x,v, in enumerate(textBaseAbsPaths):
				curTo=textBaseMoveToPaths[x]
				os.rename(v,curTo)
			textBaseRelPaths=map(lambda x: scanFolder+'/'+self.textBaseImages+'/'+x, textBaseNames)
			
			self.statusBarUpdate(" -- Project Folder '"+scanFolder+"' Built; "+str(len(textBaseNames))+" Images moved to - "+scanFolder+delimit+self.textBaseImages+delimit+" -- ", 6500,1)
		else:
			textBaseRelPaths=map(lambda x: scanFolder+'/'+x, textBaseNames)

		return textBaseRelPaths
	def extendEdges(self):
		self.textBaseViewWindow.extendReachEdges()
	def setOutputDir(self, setDir=None):
		if setDir == None:
			folderPicker=QtGui.QFileDialog.getExistingDirectory(self,"Set Output Directory")
			if folderPicker != "":
				self.outDirField.setText(folderPicker)
		else:
			self.outDirField.setText(setDir)
	def updateScrollIndex(self):
		self.scrollIndexVal=self.scrollIndexBlock.verticalScrollBar().value()
		self.scrollIndexHeight=self.scrollIndexBlock.size().height()
		if len(self.loadScrollList) > 0:
			minCheck=self.scrollIndexVal-self.scrollIndexHeight*.5
			maxCheck=self.scrollIndexVal+self.scrollIndexHeight*1.5
			popList=[]
			for x,i in enumerate(self.loadScrollList):
				if i[0] < maxCheck and i[1] > minCheck:
					self.loadIndexList[x].loadImage()
					popList.append(x)
			if len(popList) > 0:
				for p in range(len(popList)): # Delete backwards to no delete the wrong index, since everything falls back 1 on delete
					rp=len(popList)-1-p
					del self.loadIndexList[rp]
					del self.loadScrollList[rp]
	def loadImageEntry(self,obj):
		ClearLayout(self.curImageSettings)
		
		### SETTINGS ###
		self.curEntryObj=obj
		imgFull=obj.imgSizeFull

		### MAIN ENTRY ###
		ClearLayout(self.curEntryBlock)
		
		### Set Output Dir ###
		##outPath="/".join(self.dirField.text().split("/")[:-1])+"/"+str(self.galleryName)+"_compressed"
		self.dirField.setText(obj.imgFolder+self.projectName+'/')
		outPath=str(self.dirField.text())+"textCharacterOutput/"
		self.setOutputDir(outPath)
		outPath=str(self.dirField.text())+"pageBuilderOutput/"
		self.pageViewer.setPageOutputDir(outPath)

		spacer=QtGui.QSpacerItem(10,100, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		
		### WebView Image Viwer ###
		
		self.textBaseViewWindow=TextBaseViewer(self,obj)
		self.curEntryBlock.addWidget(self.textBaseViewWindow)
		self.curEntryBlock.setSpacing(0)
		self.curEntryBlock.setMargin(0)
		
		### Sliders and Jazz ###
		### Full ###
		curImageFullSettings=QtGui.QHBoxLayout()
		fullSizeText=QtGui.QLabel()
		fullSizeText.setText("Base Line -")
		fullSizeText.setMinimumWidth(150)
		curImageFullSettings.addWidget(fullSizeText)
		###
		self.sliderBaseLine=QtGui.QSlider()
		self.sliderBaseLine.setOrientation(QtCore.Qt.Horizontal)
		self.sliderBaseLine.setMinimum(0)
		self.sliderBaseLine.setMaximum(1024)
		self.sliderBaseLine.setValue(210)
		curImageFullSettings.addWidget(self.sliderBaseLine)
		###
		self.fullSizeVal=QtGui.QLabel()
		self.fullSizeVal.setText("210 px")
		self.fullSizeVal.setMinimumWidth(90)
		self.fullSizeVal.setAlignment(QtCore.Qt.AlignRight)
		curImageFullSettings.addWidget(self.fullSizeVal)
		###
		self.curImageSettings.addLayout(curImageFullSettings)
		self.sliderBaseLine.valueChanged.connect(self.baseLineSliderChange)
		
		spacer=QtGui.QSpacerItem(10,3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		### Medium ###
		curImageMedSettings=QtGui.QHBoxLayout()
		medSizeText=QtGui.QLabel()
		medSizeText.setText("Degree Rotation -")
		medSizeText.setMinimumWidth(150)
		curImageMedSettings.addWidget(medSizeText)
		###
		self.sliderRotate=QtGui.QSlider()
		self.sliderRotate.setOrientation(QtCore.Qt.Horizontal)
		self.sliderRotate.setMinimum(-6000)
		self.sliderRotate.setMaximum(6000)
		self.sliderRotate.setValue(0)
		curImageMedSettings.addWidget(self.sliderRotate)
		###
		self.rotateSliderVal=QtGui.QLabel()
		self.rotateSliderVal.setText("0.0 deg")
		self.rotateSliderVal.setMinimumWidth(90)
		self.rotateSliderVal.setAlignment(QtCore.Qt.AlignRight)
		curImageMedSettings.addWidget(self.rotateSliderVal)
		self.curImageSettings.addLayout(curImageMedSettings)
		self.sliderRotate.valueChanged.connect(self.degreesSliderChange)
		self.sliderRotate.sliderReleased.connect(self.degreesSliderReleased)
		
		curImageThumbSettings=QtGui.QHBoxLayout()
		thumbSizeText=QtGui.QLabel()
		thumbSizeText.setText("PreMultiply Scale-\n(When added to page)")
		thumbSizeText.setMinimumWidth(150)
		curImageThumbSettings.addWidget(thumbSizeText)
		###
		self.sliderPreMult=QtGui.QSlider()
		self.sliderPreMult.setOrientation(QtCore.Qt.Horizontal)
		self.sliderPreMult.setMinimum(1)
		self.sliderPreMult.setMaximum(20000)
		curVal=self.imgThumbPerc
		self.sliderPreMult.setValue(10000)
		curImageThumbSettings.addWidget(self.sliderPreMult)
		###
		self.preMultVal=QtGui.QLabel()
		self.preMultVal.setText("100.00 %")	
		self.preMultVal.setMinimumWidth(90)
		self.preMultVal.setAlignment(QtCore.Qt.AlignRight)
		curImageThumbSettings.addWidget(self.preMultVal)
		self.curImageSettings.addLayout(curImageThumbSettings)
		self.sliderPreMult.valueChanged.connect(self.preMultScaleSliderChange)
		
		spacer=QtGui.QSpacerItem(10,3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		
		### Alpha Reach Settings ###
		curAlphaReachSettings=QtGui.QHBoxLayout()
		qualityText=QtGui.QLabel()
		qualityText.setText("Alpha Fade Reach -")
		qualityText.setMinimumWidth(100)
		curAlphaReachSettings.addWidget(qualityText)
		###
		self.sliderAlphaReach=QtGui.QSlider()
		self.sliderAlphaReach.setOrientation(QtCore.Qt.Horizontal)
		self.sliderAlphaReach.setMinimum(1)
		self.sliderAlphaReach.setMaximum(10)
		self.sliderAlphaReach.setValue(2)
		curAlphaReachSettings.addWidget(self.sliderAlphaReach)
		###
		self.qualityVal=QtGui.QLabel()
		self.qualityVal.setText("2 px")	
		self.qualityVal.setMinimumWidth(90)
		self.qualityVal.setAlignment(QtCore.Qt.AlignRight)
		curAlphaReachSettings.addWidget(self.qualityVal)
		self.curImageSettings.addLayout(curAlphaReachSettings)
		self.sliderAlphaReach.valueChanged.connect(self.alphaReachSliderChange)
		self.sliderAlphaReach.sliderReleased.connect(self.alphaReachSliderReleased)
		###
		
		### Medium ###
		curImageThumbSettings=QtGui.QHBoxLayout()
		thumbSizeText=QtGui.QLabel()
		thumbSizeText.setText("Alpha Contrast -")
		thumbSizeText.setMinimumWidth(150)
		curImageThumbSettings.addWidget(thumbSizeText)
		###
		self.sliderContrast=QtGui.QSlider()
		self.sliderContrast.setOrientation(QtCore.Qt.Horizontal)
		self.sliderContrast.setMinimum(0)
		self.sliderContrast.setMaximum(200)
		self.sliderContrast.setValue(70)
		curImageThumbSettings.addWidget(self.sliderContrast)
		###
		self.contrastVal=QtGui.QLabel()
		self.contrastVal.setText("70")	
		self.contrastVal.setMinimumWidth(90)
		self.contrastVal.setAlignment(QtCore.Qt.AlignRight)
		curImageThumbSettings.addWidget(self.contrastVal)
		self.curImageSettings.addLayout(curImageThumbSettings)
		self.sliderContrast.valueChanged.connect(self.contrastSliderChange)
		self.sliderContrast.sliderReleased.connect(self.contrastSliderReleased)
		
		spacer=QtGui.QSpacerItem(10,50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		
		updateButton=QtGui.QPushButton("Finish Character",self)
		updateButton.setStyleSheet(self.buttonStyle)
		updateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		updateButton.clicked.connect(self.finishCurTextCharacter)
		self.curImageSettings.addWidget(updateButton)
	def pullFittedScale(self):
		self.charSampled=1
		self.sliderRotate.setValue(0)
		self.sliderTopPadding.setValue(0)
		self.paddingTopVal.setText(" \n \n \n0\np\nx")
		self.sliderBottomPadding.setValue(0)
		self.paddingBottomVal.setText(" \n \n \n0\np\nx")
		
		self.curImageDisplay.pullCharacterRect(1)
		self.curImageOverlayDisplay.pullCharacterRect(1)
		self.curImageMaskDisplay.pullCharacterRect(1)
		self.curImageFinalDisplay.thumbIndex=-1
		self.curImageFinalDisplay.pullCharacterRect(1)
		
		self.curImageFinalDisplay.setPaddingLine()
	def finishCurTextCharacter(self):
		##self.curImageDisplay.addCharacterToList()
		#charData=TextCharacterViewer(self,self.textBase,4)
		#charData.pullCharacterRect(1)
		curChar=IndexImageEntry(self,1,'thumb','local',[128,128], [self.curImageFinalDisplay])#[self.curImageDisplay, self.curImageMaskDisplay])
		self.curImgListPushTop(curChar)
		curChar.charField.setFocus()
		curChar.charField.selectAll()
		#self.curImgListBlock.addWidget(curChar)
		self.resetCurTextCharacter()
		self.unsavedChanges=1
	def curImgListPushTop(self, addChar, mode='top'):
		if mode == 'top':
			childRebuildArr=[addChar]
			for c in range(self.curImgListBlock.count()):
				curChar=self.curImgListBlock.itemAt(c).widget()
				childRebuildArr.append(curChar)
			for x,c in enumerate(childRebuildArr):
				c.setParent(None)
				c.index=x
				self.curImgListBlock.addWidget(c)
		elif mode=='fast':
			self.curImgListBlock.addWidget(addChar)
		elif mode=='update':
			for c in range(self.curImgListBlock.count()):
				curChar=self.curImgListBlock.itemAt(c).widget()
				curChar.index=c
	def filterCharacters(self):
		filterVar=str(self.filterCharVal.text()).strip()
		if filterVar != '':
			filterVar=list(filterVar)
			for c in range(self.curImgListBlock.count()):
				curChar=self.curImgListBlock.itemAt(c).widget()
				curChar.hide()
			for f in filterVar:
				for c in range(self.curImgListBlock.count()):
					curChar=self.curImgListBlock.itemAt(c).widget()
					curBase=str(curChar.charBase)
					if f in curBase:
						curChar.show()
		else:
			for c in range(self.curImgListBlock.count()):
				curChar=self.curImgListBlock.itemAt(c).widget()
				curChar.show()
	def resetCurTextCharacter(self):
		self.textBaseViewWindow.resetScanRange()
		self.charSamplePoints=[]
	def updateGalleryVariables(self):
		self.galleryName=self.globalGalleryName.text()
		######
	def paddingTopSliderChange(self):
		val=self.sliderTopPadding.value()
		strVal=str(val)
		#else:
		#self.charSampled=1
		#	self.win.statusBarUpdate(" -- Please 'Load Text Image' to load existing character data -- ", 5000,1)
		for x in range(len(strVal),4):
			strVal=" "+strVal
		strVal='\n'.join(strVal)
		self.paddingTopVal.setText(strVal+"\np\nx")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			try:
				self.curImageFinalDisplay.pullCharacterRect(1)
				self.unsavedChanges=1
				if self.textCharDisplay.autoUpdate==True:
					self.textCharDisplay.reloadText()
			except:
				pass;
	def paddingBottomSliderChange(self):
		val=-self.sliderBottomPadding.value()
		strVal=str(val)
		for x in range(len(strVal),4):
			strVal=" "+strVal
		strVal='\n'.join(strVal)
		self.paddingBottomVal.setText(strVal+"\np\nx")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			try:
				self.curImageFinalDisplay.pullCharacterRect(1)
				self.unsavedChanges=1
				if self.textCharDisplay.autoUpdate==True:
					self.textCharDisplay.reloadText()
			except:
				pass;
	def leftRightAlignSliderChange(self):
		if self.runValChangeEvent == 1 and self.charSampled==1:
			try:
				thumbIndex=self.curImageFinalDisplay.thumbIndex
				if thumbIndex>-1:
					thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
					thumbWidget.spacingLeft=self.leftAlignSlider.value()
					thumbWidget.spacingRight=self.rightAlignSlider.value()+128
				self.curImageFinalDisplay.pullCharacterRect(1)
				self.unsavedChanges=1
				if self.textCharDisplay.autoUpdate==True:
					self.textCharDisplay.reloadText()
			except:
				pass;
		######
	def baseLineSliderChange(self):
		val=self.sliderBaseLine.value()
		self.fullSizeVal.setText(str(val)+" px")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.baseline=val
			self.curImageFinalDisplay.setPaddingLine()
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def degreesSliderChange(self):
		val=float(self.sliderRotate.value())
		self.rotateSliderVal.setText(str(val/100.0)+" deg")
	def degreesSliderReleased(self):
		val=float(self.sliderRotate.value())
		self.rotateSliderVal.setText(str(val/100.0)+" deg")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def preMultScaleSliderChange(self):
		val=float(self.sliderPreMult.value())
		self.preMultVal.setText(str(val/100.0)+" %")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.premultiply=self.sliderPreMult.value()
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def contrastSliderChange(self):
		val=self.sliderContrast.value()
		self.contrastVal.setText(str(val))
	def contrastSliderReleased(self):
		val=self.sliderContrast.value()
		self.contrastVal.setText(str(val))
		if self.runValChangeEvent == 1 and self.charSampled==1:
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def alphaReachSliderChange(self):
		val=self.sliderAlphaReach.value()
		self.qualityVal.setText(str(val)+" px")
	def alphaReachSliderReleased(self):
		val=self.sliderAlphaReach.value()
		self.qualityVal.setText(str(val)+" px")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			self.curImageDisplay.pullCharacterRect(1)
			self.curImageOverlayDisplay.pullCharacterRect(1)
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def dispCheckerBoard(self,res,vis):
		if self.checkerBoard==None:
			size=8
			baseImg=QtGui.QPixmap(res,res)
			baseImg.fill()
			painter=QtGui.QPainter(baseImg)
			painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
			tick=[0,0]
			for x in range(0, res, size):
				tick[0]+=1
				tick[1]=0
				for y in range(0, res, size):
					tick[1]+=1
					curTick=(tick[0]+tick[1])%2
					fill=QtGui.QColor(0,0,0)
					if curTick==0:
						fill.setNamedColor('#555555')
					if curTick==1:
						fill.setNamedColor('#cccccc')
					painter.setBrush(fill)
					painter.drawRect(x,y,size,size)
			painter.end()
			self.checkerBoard=baseImg
	def sampleNewThresholdColor(self):
		self.selectColorMode=1
		self.selectColorSamples=[[0,0,0]]
		self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
		self.statusBarUpdate(" -- Select a new threshold color ... Clicking and draging will blend colors together -- ", 0,1)
	def setNewThresholdColor(self, posXY):
		img=self.imgData[self.curImage]#self.img.pixmap()
		#img=QtGui.QPixmap.fromImage(img.toImage())
		img=img.toImage()
		r,g,b,a=QtGui.QColor(img.pixel(posXY[0],posXY[1])).getRgb()
		setColor=[r,g,b]
		self.selectColorSamples.append(setColor)
		self.selectColorSamples[0]=map(sum, zip(self.selectColorSamples[0], setColor))
		baseImg=None
		if self.selectColorMode==1:
			fill=QtGui.QColor(setColor[0],setColor[1],setColor[2])
			baseImg=self.thresholdColor.pixmap()
			baseImg.fill(fill)
		elif self.selectColorMode>1:
			baseImg=self.thresholdColor.pixmap()
			xyRes=[baseImg.width(), baseImg.height()]
			baseImg=baseImg.toImage()
			
			x=self.selectColorMode%xyRes[0]
			for y in range(xyRes[1]):
				baseImg.setPixel(x,y,QtGui.QColor(setColor[0],setColor[1],setColor[2]).rgb())
			baseImg=QtGui.QPixmap.fromImage(baseImg)

		else:
			blendLen=float(len(self.selectColorSamples)-1)
			blendedValues=map(lambda x: int(float(x)/blendLen),self.selectColorSamples[0])
			self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.statusBarUpdate(" -- Threshold Color Updated -- ", 5000,1)
			setColor=blendedValues
			fill=QtGui.QColor(setColor[0],setColor[1],setColor[2])
			baseImg=self.thresholdColor.pixmap()
			baseImg.fill(fill)
			setMag=sum(blendedValues)
			self.thresholdColorSlider.setValue(setMag)
		self.thresholdColor.setPixmap(baseImg)
	def thresholdColorMagTextUpdate(self):
		setMag=self.thresholdColorSlider.value()
		self.thresholdColorMagText.setText(str(setMag)+" #\n-20")
		setColor=[int(setMag/3),int(setMag/3),int(setMag/3)]
		fill=QtGui.QColor(setColor[0],setColor[1],setColor[2])
		baseImg=self.thresholdColor.pixmap()
		baseImg.fill(fill)
		self.thresholdColor.setPixmap(baseImg)
	def keyPressEvent(self, e):
		if e.key()==QtCore.Qt.Key_Escape:
			if self.loopLatch > 0:
				self.loopLatch=2
	def keyReleaseEvent(self, e):
		if e.key()==QtCore.Qt.Key_Escape:
			if self.loopLatch > 0:
				self.loopLatch=0
			else:
				self.quitPromptCreate()
	def progressBar(self,init):
		if init == -1:
			val=0
		elif init == -2:
			val=0
		elif init >= 0:
			val=0
		return None
	def processImage(self):
		compressorPath= bundleDir+"/compressor.py"
		with open(compressorPath, 'r') as f:
			fread=f.read()
		exec(fread)
		patternRecognition(self,self.curEntryObj,self.textBaseViewWindow)
	def loadExistingData(self):
		dirField=str(self.dirField.text())
		path=dirField
		if path[-1] != "/":
			path+="/"
		if curOS=="win":
			path="\\".join(str(path).split("/"))
		path+="charListKey.py"
		if os.path.exists(path):
			self.statusBarUpdate(" -- Reading and building characters from local CharListKey file --", 0,0)
			
			sys.path.append(self.projectName)
			import charListKey
			reload(charListKey)
			
			charListKeys=charListKey.charList.keys()
			charListKeys=sorted( charListKeys, key=lambda k: k.lower() )
			for letter in charListKeys:
				curCharKeys=charListKey.charList[letter].keys()
				curCharKeys.sort()
				for char in curCharKeys:
					curChar=IndexImageEntry(self,1,'thumb','local',[128,128], 'preload')
					curChar.charBase=letter
					for data in charListKey.charList[letter][char].keys():
						curCharData=charListKey.charList[letter][char][data]
						setattr(curChar,data,curCharData)
					curTextBasePath=charListKey.charList[letter][char]['textBaseFile']
					curChar.textBaseFile=curTextBasePath
					curChar.exported=1
					curChar.loadImage()
					curChar.charFileName=char
					curChar.charField.setText(char)
					self.curImgListPushTop(curChar, mode='fast')
			self.curImgListPushTop(curChar, mode='update')
			self.statusBarUpdate(" -- All characters from local CharListKey file built --", 5000,1)
	def exportCharList(self):
		if hasattr(self, "curImgListBlock"):
			if self.curImgListBlock.count()>0:
				exportData={}
				for c in range(self.curImgListBlock.count()):
					curChar=self.curImgListBlock.itemAt(c).widget()
					if type(curChar)==IndexImageEntry:
						char=curChar.charBase
						if char not in exportData.keys():
							exportData[char]={}
						title=curChar.charFileName
						exportData[char][title]={}
						exportData[char][title]['fileName']=str(curChar.saveImage())
						exportData[char][title]['textBaseFile']=curChar.textBaseFile
						exportData[char][title]['imgName']=curChar.imgName
						exportData[char][title]['imgFolder']=curChar.imgFolder
						exportData[char][title]['imgPath']=curChar.imgPath
						
						exportData[char][title]['baseline']=curChar.baseline
						exportData[char][title]['premultiply']=curChar.premultiply
						exportData[char][title]['paddingTop']=curChar.paddingTop
						exportData[char][title]['paddingBottom']=curChar.paddingBottom
						exportData[char][title]['spacingLeft']=curChar.spacingLeft
						exportData[char][title]['spacingRight']=curChar.spacingRight
						exportData[char][title]['degRotation']=curChar.degRotation
						exportData[char][title]['contrast']=curChar.contrast
						exportData[char][title]['alphaReach']=curChar.alphaReach
						exportData[char][title]['charSamplePoints']=curChar.charSamplePoints
						exportData[char][title]['rect']=str(curChar.rect)
						
						curChar.img.setStyleSheet("border: 1px solid #000055")
				export='charList={\n'
				exportDataKeys=exportData.keys()
				exportDataKeys=sorted( exportDataKeys, key=lambda k: k.lower() )
				for k in exportDataKeys:
					if k in ["'", "b'"]:
						export+='\t"'+k+'":{\n'
					elif k == "\\":
						export+="\t'\\\\':{\n"
					else:
						export+="\t'"+k+"':{\n"
					for title in exportData[k].keys():
						export+="\t\t'"+title+"':{\n"
						for sub in exportData[k][title].keys():
							curSub=exportData[k][title][sub]
							if type(curSub)==str and "[" not in curSub:
								export+="\t\t\t'"+sub+"':'"+exportData[k][title][sub]+"',\n"
							else:
								export+="\t\t\t'"+sub+"':"+str(exportData[k][title][sub])+",\n"
						export+="\t\t},\n"
					export+="\t},\n"
				export+='}\n'
				
				path=self.dirField.text()
				if path[-1] != "/":
					path+="/"
				path="\\".join(str(path).split("/"))
				path+="charListKey.py"
				with open(path, "w") as f:
					f.write(export)
				#print "Wrote out to - "+path
				self.statusBarUpdate(" -- Wrote out to - "+path+" --", 10000,1)
				curTime=dt.datetime.now().strftime("%H:%M - %m/%d/%Y")
				self.unsavedChanges=0
			else:
				self.statusBarUpdate(" -- No created characters, please select and 'Finish Character' first -- ", 5000,2)
		else:
			self.statusBarUpdate(" -- No characters found, please 'Load Text Image' to load existing character data -- ", 5000,2)
	def closeEvent(self,event):
		self.quitPromptCreate()
	def quitPromptCreate(self):
		self.closePrompt=QtGui.QMessageBox()
		self.closePrompt.setIcon(QtGui.QMessageBox.Question)
		self.closePrompt.setWindowTitle("Quit?")
		if self.unsavedChanges==1:
			self.closePrompt.addButton("Save & Quit", QtGui.QMessageBox.YesRole)
			self.closePrompt.addButton("Discard Changes & Quit", QtGui.QMessageBox.YesRole)
			msg="Are you sure you want to quit?"
		else:
			self.closePrompt.addButton("Quit", QtGui.QMessageBox.YesRole)
			msg="There are no changes to save.\nAre you sure you want to quit?"
		self.closePrompt.setText(msg)
		cancelButton=self.closePrompt.addButton("Cancel", QtGui.QMessageBox.RejectRole)
		self.closePrompt.setEscapeButton(cancelButton)
		self.closePrompt.buttonClicked.connect(self.quitPromptReply)
		self.closePrompt.keyPressEvent=self.quitPromptEscape
		styleSheetCss="""
		* {font-size:10pt;}
		QPushButton {color:#ffffff;background-color:#323232;padding:4px;border:1px solid #151515;}
		QMessageBox {background-color:#505050;color:#ffffff}
		QLabel {color:#ffffff}"""
		self.closePrompt.setStyleSheet(styleSheetCss)
		
		self.loopLatch=1
		self.closePrompt.exec_()
	def quitPromptEscape(self, e):
		if e.key()==QtCore.Qt.Key_Escape:
			self.loopLatch=2
			self.closePrompt.close()
	def quitPromptReply(self, button):
		self.loopLatch=0
		try:
			if button.text() == "Save & Quit":
				self.exportCharList()
				self.quitApp()
			if button.text() in ["Quit", "Discard Changes & Quit"]:
				self.quitApp()
		except:
			pass;
	def quitApp(self):
		QtGui.qApp.quit()
	#######
	### Should move to new script
	### Or at least, would be a good idea to do that
	### This is just the test area
	### Can be expanded to full output all within this python script though
	
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	galGen=ImageProcessor()
	galGen.show()
	try:
		sys.exit(app.exec_())
	except:
		pass;
