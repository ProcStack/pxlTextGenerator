############################################
## Website Optimizer v0.0.1               ##
## Image and Web Site Compressor          ##
##  Written by Kevin Edzenga; ~2017       ##
##   http://metal-asylum.net              ##
##                                        ##
## For aditional work, see my github-     ##
##  https://github.com/procstack          ##
############################################
"""
 This tool has been designed to reduce bandwidth from web servers.
 Transferring most of the strain to the user themselves.
 By reducing requested data from the server, websites can load much faster
   all the while, maintaining the same ammount of information as before.
 But requires that visitors decompile and load appropriate data as needed.
 Not all at once, which is where I see potential slowdowns moving forward.
 
 With the pending loss of Net Neutrality in USA (December 19th, 2017), small time websites might be hit
   with far less bandwidth from the ISPs.
 I'd like to combat this however I can.
 
 Web sites were the core reason I got into scriptings and I find great joy in the ever growing tech.
 As such, the web should be a source of inspiration for youngsters and curious bodies trying to learning something new.
 Especially that web scripting isn't so low level, not causing their heads to spin. (C, C++, Java, Pearl, Bash, etc...)
   
 We should not be forced to give up on new social/technological/commercial outlets
   because the ISPs decide bandwidth allotments now.
   
 Please help how ever you can!
 Submit bugs; make a branch and send in pull requests;
 Get this working for the less knowledgable out there!!
 
 Stay awesome and open source for life!
 
"""

import zlib
import bz2

import sys, os
import re
from PIL import Image
from PyQt4 import QtGui, QtCore
from functools import partial
import math
import random

frozen=0
curDir='.'
if getattr(sys, 'frozen', False):
	frozen=1
	bundleDir=sys._MEIPASS
else:
	bundleDir=os.path.dirname(os.path.abspath(__file__))
	curDir=bundleDir
woVersion="0.0.1"

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
		scriptNameText="Text Generator "
		versionText=scriptNameText+" - v"+str(woVersion)
		self.setWindowTitle(versionText)
		self.winSize=[2200,1200]
		self.setMinimumSize(self.winSize[0],self.winSize[1])
		self.resize(self.winSize[0],self.winSize[1])
		# Create custom top bar styles and widgets
		# Then set existing window as frame inside the main window
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
		#self.setStyleSheet("padding:0px;")
		
		self.textBase=''
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
		
		### Menu Bar ###
		self.menuBar=self.menuBar()
		fileMenu=self.menuBar.addMenu('File')
		fileMenu.addSeparator()
		quitItem=QtGui.QAction("Exit",self)
		quitItem.triggered.connect(self.quitPromptCreate)
		fileMenu.addAction(quitItem)
		self.infoMenu=self.menuBar.addMenu('Info')
		scriptInfoItem=QtGui.QAction(versionText,self)
		self.infoMenu.addAction(scriptInfoItem)
		authorItem=QtGui.QAction("Written by Kevin Edzenga",self)
		self.infoMenu.addAction(authorItem)
		infoItem=QtGui.QAction("www.Metal-Asylum.net",self)
		self.infoMenu.addAction(infoItem)
		self.infoMenu.addSeparator()
		helpItem=QtGui.QAction("Help...",self)
		self.infoMenu.addAction(helpItem)
		# Status Bar
		self.statusBar=self.statusBar()

		self.mainLayout=QtGui.QVBoxLayout(self.mainWidget)
		pad=2
		self.mainLayout.setSpacing(pad)
		self.mainLayout.setMargin(pad)
		selfSize=self.geometry()
		menuSize=self.menuBar.geometry()
		selfSize=[selfSize.width(), selfSize.height()-menuSize.height()]

		# Load directory text field
		self.dirBlock=QtGui.QHBoxLayout()
		self.dirField=QtGui.QLineEdit()
		self.dirBlock.addWidget(self.dirField)
		# Create Load Dir button
		self.loadDir=QtGui.QPushButton('Load Text Image', self)
		self.loadDir.setStyleSheet(self.buttonStyle)
		self.loadDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.loadDir.clicked.connect(self.loadAndScanDir)
		self.dirBlock.addWidget(self.loadDir)
		#tab0.addLayout(self.dirBlock)
		self.mainLayout.addLayout(self.dirBlock)
		
		# Load directory text field
		self.imageDisplayBlock=QtGui.QVBoxLayout()
		self.imgField=QtGui.QLabel()
		self.imgField.setText("Please select the folder containing\n your full sized images.")
		self.imgField.setAlignment(QtCore.Qt.AlignCenter)
		self.imageDisplayBlock.addWidget(self.imgField)
		self.imgSpacer=QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.imageDisplayBlock.addItem(self.imgSpacer)
		#tab0.addLayout(self.imageDisplayBlock)
		self.mainLayout.addLayout(self.imageDisplayBlock)
		
		### Process Block ###
		pad=1
		self.processLayout=QtGui.QVBoxLayout()
		self.processLayout.setSpacing(pad)
		self.processLayout.setMargin(pad)
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
		self.mainLayout.addLayout(self.processLayout)

		self.setCentralWidget(self.mainWidget)
		
		"""def newButton(self,name,txt,cmd,layout):
		eval(str(name)+"=QtGui.QPushButton('"+str(txt)+"', self)")
		eval(str(name)+".clicked.connect("+cmd+")")
		eval(str(layout)+".addWidget("+str(name)+")")"""
	def setCursorPointing(self):
		QtGui.QWidget.setCursor(self.infoMenu,QtCore.Qt.PointingHandCursor)
	def setCursorArrow(self):
		QtGui.QWidget.setCursor(self.infoMenu,QtCore.Qt.ArrowCursor)
	def setWindowStyleSheet(self):
		self.winPalette=QtGui.QPalette()
		self.winPalette.setColor(QtGui.QPalette().Window, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Base, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Background, QtGui.QColor(50,50,50))
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
	def loadAndScanDir(self):
		ext=("jpg", "jpeg", "png", "bmp")
		folderPicker=QtGui.QFileDialog.getOpenFileName(self,"Select Text Image",curDir, "Image files (*.jpg, *.jpeg, *.png *.bmp)")
		if folderPicker != "":
			folderPicker=str(folderPicker)
			activeList=[]
			if os.path.exists(folderPicker):
				self.textBase=folderPicker
				folderSplit=folderPicker.split('/') # Delimitter gets corrected in pyqt
				textBaseFile=folderSplit[-1]
				folderPicker='/'.join(folderSplit[:-1])
				activeList.append(textBaseFile)
			self.clearLayout(self.imageDisplayBlock)
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
				
				curEntryEditScrollBlock=QtGui.QScrollArea() #QAbstractScrollArea()
				curEntryEditScrollBlock.setWidgetResizable(True)
				#curEntryEditScrollBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				curEntryEditScrollInner=QtGui.QWidget(curEntryEditScrollBlock)

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
				self.sideBarBlock=QtGui.QVBoxLayout()
				self.sideBarTextBase=QtGui.QVBoxLayout()
				self.sideBarTextBase.setAlignment(QtCore.Qt.AlignCenter)
				self.sideBarTextBaseWidget=QtGui.QWidget()
				self.sideBarTextBaseWidget.setLayout(self.sideBarTextBase)
				self.sideBarBlock.addWidget(self.sideBarTextBaseWidget)

				self.scrollIndexBlock=QtGui.QScrollArea()
				self.scrollIndexBlock.setWidgetResizable(True)
				self.scrollIndexBlock.setFixedWidth(152)
				self.scrollIndexBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				scrollInner=QtGui.QWidget(self.scrollIndexBlock)
				
				self.curImgListBlock=QtGui.QVBoxLayout(scrollInner)
				self.curImgListBlock.setAlignment(QtCore.Qt.AlignCenter)
				scrollInner.setLayout(self.curImgListBlock)
				self.curImgListBlock.setSpacing(pad)
				self.curImgListBlock.setMargin(pad)
				
				size=self.scrollIndexBlock.frameGeometry()
				#size=[size.width()-sizeSub, size.height()]
				size=[128,128]
				scrollOffset=0
				scrollAdd=0
				self.loadIndexList=[]
				self.loadScrollList=[]
				loadObj=-1
				for x,p in enumerate(activeList):
					scrollOffset+=scrollAdd+pad
					curImg=IndexImageEntry(self,x,p,folderPicker+'/',size, None)
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
	def loadExistingData(self):
		path=self.dirField.text()
		if path[-1] != "/":
			path+="/"
		path="\\".join(str(path).split("/"))
		path+="charListKey.py"
		if os.path.exists(path):
			self.statusBar.showMessage(" -- Reading and building characters from local CharListKey file --", 0)
			from charListKey import charList
			#print " -- Found & Loading from --"
			#print "  "+path
			charListKeys=charList.keys()
			charListKeys=sorted( charListKeys, key=lambda k: k.lower() )
			for letter in charListKeys:
				for char in charList[letter].keys():
					curChar=IndexImageEntry(self,1,'thumb','local',[128,128], 'preload')
					curChar.charBase=letter
					for data in charList[letter][char].keys():
						curCharData=charList[letter][char][data]
						setattr(curChar,data,curCharData)
					curTextBasePath=charList[letter][char]['textBaseFile']
					curChar.textBaseFile=curTextBasePath
					curChar.exported=1
					curChar.loadImage()
					curChar.charFileName=char
					curChar.charField.setText(char)
					self.curImgListPushTop(curChar)
					#self.curImgListBlock.addWidget(curChar)
			#print " -- All characters from local CharListKey file built --"
			self.statusBar.showMessage(" -- All characters from local CharListKey file built --", 5000)

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
		self.clearLayout(self.curImageSettings)
		
		### SETTINGS ###
		self.curEntryObj=obj
		imgFull=obj.imgSizeFull

		### MAIN ENTRY ###
		self.clearLayout(self.curEntryBlock)
		
		### Set Output Dir ###
		##outPath="/".join(self.dirField.text().split("/")[:-1])+"/"+str(self.galleryName)+"_compressed"
		self.dirField.setText(obj.imgFolder)
		outPath=str(self.dirField.text())+"textCharacterOutput/"
		self.setOutputDir(outPath)

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
		self.sliderBaseLine.setMaximum(512)
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
		self.sliderRotate.setMinimum(-20)
		self.sliderRotate.setMaximum(20)
		self.sliderRotate.setValue(0)
		curImageMedSettings.addWidget(self.sliderRotate)
		###
		self.medSizeVal=QtGui.QLabel()
		self.medSizeVal.setText("0 deg")
		self.medSizeVal.setMinimumWidth(90)
		self.medSizeVal.setAlignment(QtCore.Qt.AlignRight)
		curImageMedSettings.addWidget(self.medSizeVal)
		self.curImageSettings.addLayout(curImageMedSettings)
		self.sliderRotate.valueChanged.connect(self.degreesSliderChange)
		
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
		self.sliderContrast.setValue(65)
		curImageThumbSettings.addWidget(self.sliderContrast)
		###
		self.contrastVal=QtGui.QLabel()
		self.contrastVal.setText("65")	
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
		curChar=IndexImageEntry(self,1,'thumb','local',[128,128], [self.curImageDisplay, self.curImageMaskDisplay])
		self.curImgListPushTop(curChar)
		curChar.charField.setFocus()
		curChar.charField.selectAll()
		#self.curImgListBlock.addWidget(curChar)
		self.resetCurTextCharacter()
		self.unsavedChanges=1
	def curImgListPushTop(self, addChar):
		childRebuildArr=[addChar]
		for c in range(self.curImgListBlock.count()):
			curChar=self.curImgListBlock.itemAt(c).widget()
			childRebuildArr.append(curChar)
		for x,c in enumerate(childRebuildArr):
			c.setParent(None)
			c.index=x
			self.curImgListBlock.addWidget(c)
	def resetCurTextCharacter(self):
		self.textBaseViewWindow.resetScanRange()
		self.charSamplePoints=[]
	def updateGalleryVariables(self):
		self.galleryName=self.globalGalleryName.text()
		######
	def paddingTopSliderChange(self):
		val=self.sliderTopPadding.value()
		strVal=str(val)
		for x in range(len(strVal),4):
			strVal=" "+strVal
		strVal='\n'.join(strVal)
		self.paddingTopVal.setText(strVal+"\np\nx")
		if self.runValChangeEvent == 1:
			try:
				self.curImageFinalDisplay.pullCharacterRect(1)
				self.unsavedChanges=1
			except:
				pass;
	def paddingBottomSliderChange(self):
		val=-self.sliderBottomPadding.value()
		strVal=str(val)
		for x in range(len(strVal),4):
			strVal=" "+strVal
		strVal='\n'.join(strVal)
		self.paddingBottomVal.setText(strVal+"\np\nx")
		if self.runValChangeEvent == 1:
			try:
				self.curImageFinalDisplay.pullCharacterRect(1)
				self.unsavedChanges=1
			except:
				pass;
	def leftRightAlignSliderChange(self):
		if self.runValChangeEvent == 1:
			try:
				thumbIndex=self.curImageFinalDisplay.thumbIndex
				if thumbIndex>-1:
					thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
					thumbWidget.spacingLeft=self.leftAlignSlider.value()
					thumbWidget.spacingRight=self.rightAlignSlider.value()
				self.curImageFinalDisplay.pullCharacterRect(1)
				self.unsavedChanges=1
			except:
				pass;
		######
	def baseLineSliderChange(self):
		val=self.sliderBaseLine.value()
		self.fullSizeVal.setText(str(val)+" px")
		if self.runValChangeEvent == 1:
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.baseline=val
			self.curImageFinalDisplay.setPaddingLine()
			self.unsavedChanges=1
	def degreesSliderChange(self):
		val=self.sliderRotate.value()
		self.medSizeVal.setText(str(val)+" deg")
	def preMultScaleSliderChange(self):
		val=float(self.sliderPreMult.value())
		self.preMultVal.setText(str(val/100.0)+" %")
		self.unsavedChanges=1
	def contrastSliderChange(self):
		val=self.sliderContrast.value()
		self.contrastVal.setText(str(val))
	def contrastSliderReleased(self):
		val=self.sliderContrast.value()
		self.contrastVal.setText(str(val))
		if self.runValChangeEvent == 1:
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			self.unsavedChanges=1
	def alphaReachSliderChange(self):
		val=self.sliderAlphaReach.value()
		self.qualityVal.setText(str(val)+" px")
	def alphaReachSliderReleased(self):
		val=self.sliderAlphaReach.value()
		self.qualityVal.setText(str(val)+" px")
		if self.runValChangeEvent == 1:
			self.curImageDisplay.pullCharacterRect(1)
			self.curImageOverlayDisplay.pullCharacterRect(1)
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			self.unsavedChanges=1
	def clearLayout(self, layout):
		children=[]
		postRemoveItem=[]
		for l in range(layout.count()):
			if type(layout.itemAt(l)) in [QtGui.QHBoxLayout, QtGui.QVBoxLayout]:
				self.clearLayout(layout.itemAt(l)) # Recurse through sub layouts
				children.append(layout.itemAt(l))
			else:
				typ=type(layout.itemAt(l))
				if typ == QtGui.QWidgetItem:
					layout.itemAt(l).widget().close()
				if typ == QtGui.QSpacerItem: # Spacers, I need to find a better way to remove
					postRemoveItem.append(layout.itemAt(l))
		if len(postRemoveItem) > 0: # Removing spacers in the loop will skip widgets after that point in the array
			for i in postRemoveItem: # So delete them after the fact
				layout.removeItem(i)
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
		self.statusBar.showMessage(" -- Select a new threshold color ... Clicking and draging will blend colors together -- ", 0)
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
			self.statusBar.showMessage(" -- Threshold Color Updated -- ", 5000)
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
	def exportCharList(self):
		exportData={}
		for c in range(self.curImgListBlock.count()):
			curChar=self.curImgListBlock.itemAt(c).widget()
			if type(curChar)==IndexImageEntry:
				char=curChar.charBase
				print "Exporting -"+char
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
		self.statusBar.showMessage(" -- Wrote out to - "+path+" --", 10000)
		self.unsavedChanges=0
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
class IndexImageEntry(QtGui.QWidget): #Individual indexList image entries
	def __init__(self, win, index, name, path, scaleSize, qtImg):
		super(IndexImageEntry,self).__init__(win)
		self.win=win
		self.offset=0 # Offset from 0 scroll in indexList side bar
		
		self.imgName=name
		self.imgFolder=path
		self.imgPath=path+name # Path to image on disk
		self.loaded=0 # Current state, reading from disk, keeps ram usage and load time lower
		
		self.imgSize=[-1,-1] # Disk image size
		self.imgSizeFull=[-1,-1] # Full size image for web
		self.imgSizeIndexList=[-1,-1] # Size of indexList image in qt window
		
		curImgBlock=QtGui.QVBoxLayout()
		curImgBlock.setSpacing(0) # Spacing & Margin was giving me trouble calculating dynamic loading in window
		curImgBlock.setMargin(0) # ||
		self.index=-1
		self.data=None
		self.dataAlpha=None
		self.img=QtGui.QLabel()
		self.charField=None
		self.charBase=None
		self.charFileName=None
		self.charSamplePoints=[]
		self.paddingTop=0
		self.paddingBottom=0
		self.spacingLeft=None
		self.spacingRight=None
		self.baseline=-1
		self.degRotation=0
		self.premultiply=1
		self.contrast=100
		self.alphaReach=-1
		self.textBaseFile=None
		self.exported=0
		self.fileName=None #Export file name
		self.rect=[0,0,256,256]

		if qtImg == None:
			# Using PyQt's Pixmap is great for displaying image, but really slow just for reading basic info
			# Since loading an image into a Pixmap loads the image into memory.
			# Using PIL.Image reads the fist 16 characters of the image to retrieve size info
			# TLDR; SO MUCH FASTER THROUGH PIL!!1!
			self.win.curImage=name
			self.win.curImagePath=self.imgPath
			imageStats=Image.open(str(self.imgPath)) # PIL.Image
			
			self.imgSize=[imageStats.size[0], imageStats.size[1]] # Disk image size
			self.imgSizeFull=self.imgSize # Full size image for web
			
			self.imgSizeIndexList=[imageStats.size[0],imageStats.size[1]]
			ratio=1
			if scaleSize[0] < imageStats.size[0]: # If the full image is larger than scrollArea
				ratio=float(scaleSize[0])/float(imageStats.size[0])
				ymath=float(imageStats.size[1])*ratio
				self.imgSizeIndexList=[int(scaleSize[0]), int(ymath)] # Store indexThumbnail scale for scroll offset math & placeholder
				
			self.img.setText("Loading - "+str(self.imgPath.split(delimit)[-1])+"\n"+str(ratio)[0:5]+"% - [ "+str(self.imgSizeIndexList[0])+" x "+str(self.imgSizeIndexList[1])+" ]") # Stand-in for image, pre load
			self.img.setAlignment(QtCore.Qt.AlignCenter)
			self.img.setGeometry(0,0,self.imgSizeIndexList[0],self.imgSizeIndexList[1]) # Placeholder
			curImgBlock.addWidget(self.img)
		else:
			self.imgSize=scaleSize # Disk image size
			self.imgSizeFull=self.imgSize # Full size image for web
			
			self.imgSizeIndexList=scaleSize
			self.img.setAlignment(QtCore.Qt.AlignCenter)
			self.img.setGeometry(0,0,self.imgSizeIndexList[0],self.imgSizeIndexList[1]) # Placeholder
			if type(qtImg) == list:
				self.data=qtImg[0].data
				self.dataAlpha=qtImg[1].data
				self.rect=qtImg[0].rect
				qtImg=qtImg[0].data.scaled(self.imgSizeIndexList[0],self.imgSizeIndexList[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
				self.img.setPixmap(qtImg)
			else:
				self.img.setText("[ Placeholder ]") # Stand-in for image, pre load
			curImgBlock.addWidget(self.img)
			
			self.charField=QtGui.QLineEdit()
			self.charField.setText("_")
			self.charField.editingFinished.connect(self.charCheck)
			curImgBlock.addWidget(self.charField)
			
			self.textBaseFile=self.win.curImagePath
			
			self.charSamplePoints=self.win.charSamplePoints
			self.baseline=self.win.sliderBaseLine.value()
			self.premultiply=self.win.sliderPreMult.value()
			self.paddingTop=self.win.sliderTopPadding.value()
			self.paddingBottom=self.win.sliderBottomPadding.value()
			self.spacingLeft=self.win.leftAlignSlider.value()
			self.spacingRight=self.win.rightAlignSlider.value()
			self.degRotation=self.win.sliderRotate.value()
			self.contrast=self.win.sliderContrast.value()
			self.alphaReach=self.win.sliderAlphaReach.value()
		
		
			self.img.setStyleSheet("border: 1px solid #555555; padding:3px;")
		# Child QWidgets don't set parent size, must set parent size for correct scroll bar
		self.setFixedSize(self.imgSizeIndexList[0],self.imgSizeIndexList[1]) # Layout size for Placeholder
		self.setLayout(curImgBlock) # Layout to display in parent window
	def loadImage(self):
		pmap=QtGui.QPixmap()
		if self.imgPath=='localthumb':
			pmap.load(self.fileName) #Load existing char PNG
			self.data=pmap
		else:
			pmap.load(self.imgPath) #Load image, currently disk path only
		# I feel this is too limiting, encase I change how height is calculated in the future
		#pmap=pmap.scaledToWidth(scaleSize[0])
		pmap=pmap.scaled(self.imgSizeIndexList[0],self.imgSizeIndexList[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
		self.img.setPixmap(pmap)
	def charCheck(self):
		val=self.charField.text()
		val=str(val)
		valCheck=val.split("_")
		if valCheck[0] != "char":
			self.charBase=val
			special={
				"!":"exc",
				"@":"at",
				"#":"num",
				"$":"dol",
				"%":"per",
				"^":"up",
				"&":"and",
				"*":"str",
				"(":"opr",
				")":"cpr",
				"-":"sub",
				"=":"equ",
				"_":"und",
				"+":"pls",
				"[":"obr",
				"]":"cbr",
				"{":"ocr",
				"}":"ccr",
				";":"sem",
				"'":"osg",
				"b'":"csg",
				":":"col",
				'"':"odb",
				'b"':"cdb",
				",":"com",
				".":"dot",
				"/":"bsl",
				"<":"lth",
				">":"gth",
				"?":"qus",
				"\\":"fsl",
				"`":"ftk",
				"b`":"btk",
				"~":"tld",
				"...":"ell",
				}
			if val in special.keys():
				val="char_"+special[val]
			else:
				if len(val) == 0:
					val="_"
				elif len(val) == 1:
					if val.islower():
						val = "char_"+val+"_low"
					elif val.isupper():
						val = "char_"+val+"_cap"
					else:
						val="_"
				else:
					val="_"
			if val != "_":
				hitCount=0
				for c in range(self.win.curImgListBlock.count()):
					curChar=self.win.curImgListBlock.itemAt(c).widget()
					if type(curChar)==IndexImageEntry:
						char=curChar.charBase
						if char == self.charBase:
							hitCount+=1
				val+="_"+str(hitCount)
				self.charField.clearFocus()
			self.charField.setText(val)
			self.charFileName=val
	def saveImage(self):
		path=self.win.outDirField.text()
		diffuse="Busted"
		if path[-1] != "/":
			path+="/"
		if not os.path.exists(path):
			buildPath="\\".join(str(path).split("/"))
			os.makedirs(buildPath)
		if self.charFileName != "_":
			diffuse=self.charFileName+".png"
			if self.exported == 0:
				difData=self.data
				difData.setAlphaChannel(self.dataAlpha)
				difData.save(path+diffuse, "png")
		return path+diffuse
	def loadFromTextBase(self):
		curTextBasePath=self.textBaseFile
		curTextBaseFile=curTextBasePath.split("/")[-1]
		if curTextBaseFile not in self.imgData.keys():
			print "Loading - "+curTextBaseFile
			print "Not active yet, MAKE IT WORK"
			#pmap=QtGui.QPixmap()
			#pmap.load(self.imgPath)
			#self.imgData[self.curImage]=pmap
		else:
			print "Found textBase image"
	def mouseReleaseEvent(self, e):
		if self.imgName == "thumb":
			if self.exported==1:
				#self.charSamplePoints=self.win.charSamplePoints
				self.win.runValChangeEvent=0
				self.win.sliderBaseLine.setValue(self.baseline)
				self.win.sliderPreMult.setValue(self.premultiply)
				self.win.sliderTopPadding.setValue(self.paddingTop)
				self.win.sliderBottomPadding.setValue(self.paddingBottom)
				self.win.leftAlignSlider.setValue(self.spacingLeft)
				self.win.rightAlignSlider.setValue(self.spacingRight)
				self.win.sliderRotate.setValue(self.degRotation)
				self.win.sliderContrast.setValue(self.contrast)
				self.win.sliderAlphaReach.setValue(self.alphaReach)
				self.win.runValChangeEvent=1
				
				self.win.curImageFinalDisplay.thumbIndex=-1
				self.win.curImageFinalDisplay.pullCharacterRect(self)
		else:
			self.win.loadImageEntry(self)

class TextBaseViewer(QtGui.QWidget):	
	def __init__(self, win, entryObj):
		QtGui.QWidget.__init__(self)
		self.entry=entryObj
		self.win=win
		self.imgSize=entryObj.imgSize
		self.cWOrig=(entryObj.imgSize[0])
		self.cHOrig=(entryObj.imgSize[1])
		self.cW=(entryObj.imgSize[0])
		self.cH=(entryObj.imgSize[1])
		self.zoom=1.0
		self.imgName=entryObj.imgName
		self.imgPath=entryObj.imgPath
		self.img=QtGui.QLabel()
		self.img.setAlignment(QtCore.Qt.AlignCenter)
		self.img.setGeometry(0,0,self.cW,self.cH) # Placeholder
		self.scanRange=[self.cW,self.cH,0,0]
		self.rect=[0,0,256,256]
		self.reachPixels=[]
		self.mouseDown=0
		self.mousePressStart=[]
		self.scrollStart=[]
		self.mouseDrag=0
		
		self.curImgBlock=QtGui.QVBoxLayout()
		self.curImgBlock.setSpacing(0) # Spacing & Margin was giving me trouble calculating dynamic loading in window
		self.curImgBlock.setMargin(0) # ||
		
		pmap=QtGui.QPixmap()
		pmap.load(self.imgPath)
		self.win.imgData[self.win.curImage]=pmap
		self.img.setPixmap(pmap)
		self.curImgBlock.addWidget(self.img)
		self.setLayout(self.curImgBlock) # Layout to display in parent window
	def resetScanRange(self):
		pmap=QtGui.QPixmap()
		pmap.load(self.imgPath)
		self.img.setPixmap(pmap)
		self.scanRange=[self.cW,self.cH,0,0]
		self.reachPixels=[]
		self.setZoom(self.win.zoom)
	def mousePressEvent(self, event):
		pos=event.globalPos()
		self.mousePressStart=[pos.x(), pos.y()]
		self.mouseDown=1
		scrollH=self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().value()
		scrollV=self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().value()
		self.scrollStart=[scrollH, scrollV]
	def mouseMoveEvent(self, event):
		if self.win.selectColorMode>0:
			pos=event.pos()
			posX=int(pos.x()*(1.0/self.zoom))
			posY=int(pos.y()*(1.0/self.zoom))
			self.win.setNewThresholdColor([posX,posY])
			self.win.selectColorMode+=1
		else:
			if self.mouseDown > 0:
				self.mouseDown+=1
				if self.mouseDown == 5:
					self.mouseDrag=1
				if self.mouseDrag == 1:
					pos=event.globalPos()
					curXY=[ self.mousePressStart[0]-pos.x(), self.mousePressStart[1]-pos.y() ]
					maxScrollH=self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().maximum()
					maxScrollV=self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().maximum()
					curScrollH=min( maxScrollH, max(0, self.scrollStart[0]+curXY[0] ))
					curScrollV=min( maxScrollV, max(0, self.scrollStart[1]+curXY[1] ))
					self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().setValue(curScrollH)
					self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().setValue(curScrollV)
	def mouseReleaseEvent(self, event):
		if self.mouseDrag==0 or self.win.selectColorMode>0:
			pos=event.pos()
			posX=int(pos.x()*(1.0/self.zoom))
			posY=int(pos.y()*(1.0/self.zoom))
			if self.win.selectColorMode>0:
				self.win.selectColorMode=0
				self.win.setNewThresholdColor([posX,posY])
			else:
				posArr=[posX,posY]
				if posArr not in self.reachPixels:
					self.win.charSamplePoints.append(posArr)
					img=self.win.imgData[self.win.curImage]#self.img.pixmap()
					#img=QtGui.QPixmap.fromImage(img.toImage())
					img=img.toImage()
					#img=img.scaled(self.cWOrig,self.cHOrig, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					
					#midRun=QtGui.QPixmap.fromImage(self.img.pixmap().toImage())
					midRun=self.img.pixmap()
					midRun=midRun.scaled(self.cWOrig,self.cHOrig, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					midRun=midRun.toImage()
					#midRun=self.img.pixmap().toImage()
					#img=img.toImage()
					rangeDist=10
					posRange=[]
					posRange.append(max(posX-rangeDist,0))
					posRange.append(max(posY-rangeDist,0))
					posRange.append(min(posX+rangeDist, self.cWOrig))
					posRange.append(min(posY+rangeDist, self.cHOrig))
					# Make this better
					# Add string of x,y and find in array
					# If not in array, add to pixelQueue
					pixelQueue=[]
					pixelQueue.extend(self.win.charSamplePoints)
					tempScanRange=[]
					tempScanRange.extend(self.scanRange)
					#tempScanRange.extend()
					caps=[]
					caps.append( max(1, tempScanRange[0]-2) )
					caps.append( max(1, tempScanRange[1]-2) )
					caps.append( min(self.cW-1, tempScanRange[2]+2) )
					caps.append( min(self.cW-1, tempScanRange[3]+2) )
					thresh=max(0, self.win.thresholdColorSlider.value()-20)
					runner=0
					killCheck=1000
					growArr=[[1,1],[1,0],[1,-1], [0,1],[0,-1], [-1,1],[-1,0],[-1,-1]]
					latch=-1
					refreshRunner=0
					refreshItter=100
					refreshDraw=100
					refreshHit=100
					runawayLatch=0
					self.win.loopLatch=1
					while latch != 0 and self.win.loopLatch == 1:
						runner+=1
						refreshRunner+=1
						if refreshRunner%refreshItter==0:
							checkedCount=str(len(self.reachPixels))
							queueCount=len(pixelQueue)
							warning=""
							if queueCount>300 or runawayLatch==1:
								runawayLatch=1
								warning=" --  !! Run away search detected, set background threshold color to reduce calculations !!"
								
							self.win.statusBar.showMessage("( Press 'Escape' to Cancel ) -- Cross-Checking "+checkedCount+" pixels -- Pixels in Queue ... "+str(queueCount)+warning, 0)
							QtGui.QApplication.processEvents()
						if refreshRunner == refreshDraw:
							refreshDraw+=refreshItter+int(15*(refreshDraw/refreshItter))
							
							midRunFull=midRun.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
							pxmap=QtGui.QPixmap.fromImage(midRunFull)
							self.img.setPixmap(pxmap)
						if runner >= killCheck:
							print "Kicking out"
							latch=0
						else:
							xyPos=pixelQueue.pop(0)
							x=xyPos[0]
							y=xyPos[1]
							#curStr=str(x)+","+str(y)
							self.reachPixels.append(xyPos)
							
							#############################################
							r,g,b,a=QtGui.QColor(img.pixel(x,y)).getRgb()
							
							val=(r+g+b)
							if val<thresh:
								latch=1
								#caps[0]= max(1, tempScanRange[0]-2) 
								#caps[1]= max(1, tempScanRange[1]-2) 
								#caps[2]= min(self.cW-1, tempScanRange[2]+2) 
								#caps[3]= min(self.cW-1, tempScanRange[3]+2) 
								
							tempScanRange[0]=min(tempScanRange[0], x)
							tempScanRange[1]=min(tempScanRange[1], y)
							tempScanRange[2]=max(tempScanRange[2], x)
							tempScanRange[3]=max(tempScanRange[3], y)
							caps=[]
							caps.append( max(1, tempScanRange[0]-2) )
							caps.append( max(1, tempScanRange[1]-2) )
							caps.append( min(self.cW-1, tempScanRange[2]+2) )
							caps.append( min(self.cW-1, tempScanRange[3]+2) )
								
							#############################################
							if latch==1 and (x<caps[0] or y<caps[1] or x>caps[2] or y>caps[3]):
								latch=0
							else:
								if (latch == 1 and val<thresh) or latch==0:
									midRun.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
									runner=0
									hit=0
									for xy in growArr:
										nextX=max(0, min(x+xy[0], self.cWOrig))
										nextY=max(0, min(y+xy[1], self.cHOrig))
										nextArr=[nextX,nextY]#str(nextX)+","+str(nextY)
										if nextArr not in self.reachPixels:
											hit+=1
											self.reachPixels.append(nextArr)
											pixelQueue.append(nextArr)
							if len(pixelQueue) == 0:
								latch=0
					for xy in self.reachPixels:
						x=xy[0]
						y=xy[1]
						img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
					if self.win.loopLatch==1:
						self.win.loopLatch=0
					# Update scanRange to display bounding box better
					alphaPadding=1
					self.scanRange[0]=max(tempScanRange[0]-alphaPadding, 0) if tempScanRange[0] != self.scanRange[0] else self.scanRange[0]
					self.scanRange[1]=max(tempScanRange[1]-alphaPadding, 0) if tempScanRange[1] != self.scanRange[1] else self.scanRange[1]
					self.scanRange[2]=min(tempScanRange[2]+alphaPadding, self.cWOrig) if tempScanRange[2] != self.scanRange[2] else self.scanRange[2]
					self.scanRange[3]=min(tempScanRange[3]+alphaPadding, self.cHOrig) if tempScanRange[3] != self.scanRange[3] else self.scanRange[3]
					
					img=self.drawBoundingBox(img)
					
					pxmap=QtGui.QPixmap.fromImage(img)
					pxmap=pxmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					self.img.setPixmap(pxmap)
					self.win.statusBar.showMessage(" -- Character Search Complete! --", 5000)

		self.mouseDown=0
		self.mouseDrag=0
	def wheelEvent(self, event):
		val = event.delta() / abs(event.delta())
		targetZoom= self.zoom + val*.1
		self.setZoom(targetZoom)
	def setZoom(self, targetZoom):
		targetW=int(float(self.cWOrig)*targetZoom)
		targetH=int(float(self.cHOrig)*targetZoom)
		targetMax=max(targetW, targetH)
		if targetMax < 10000 and targetMax>0:
			self.cW=targetW
			self.cH=targetH
			self.zoom=targetZoom
			self.win.zoom=targetZoom
			pmap=self.win.imgData[self.win.curImage]
			pmap=QtGui.QPixmap.fromImage(pmap.toImage())
			if len(self.reachPixels) > 0:
				#img=img.scaled(self.cWOrig,self.cHOrig, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
				img=pmap.toImage()
				for xy in self.reachPixels:
					x=xy[0]
					y=xy[1]
					img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
				img=self.drawBoundingBox(img)
				pmap=QtGui.QPixmap.fromImage(img)
			pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			self.img.setPixmap(pmap)
	def drawBoundingBox(self, img):
		# Build Bounding Box
		# Might be cool to make this interactive
		# Still don't know why I try to avoid QPainter so much
		# Something about QPainter bothers me, and can't put my finger on it....
		bboxRun=[]
		bboxRun.append( [[self.scanRange[0]-1, self.scanRange[0]], [ self.scanRange[1], self.scanRange[3]] ] )
		bboxRun.append( [[self.scanRange[2], self.scanRange[2]+1], [ self.scanRange[1], self.scanRange[3]] ] )
		bboxRun.append( [[self.scanRange[0], self.scanRange[2]], [ self.scanRange[1]-1, self.scanRange[1]] ] )
		bboxRun.append( [[self.scanRange[0], self.scanRange[2]], [ self.scanRange[3], self.scanRange[3]+1] ] )
		for xy in bboxRun:
			for x in range(xy[0][0],xy[0][1]):
				for y in range(xy[1][0],xy[1][1]):
					img.setPixel(x,y,QtGui.QColor(255,0,0,255).rgb())
		return img
##	self.curImageDisplay=TextCharacterViewer(self,self.textBase,0)
##	self.curImageOverlayDisplay=TextCharacterViewer(self,self.textBase,1)
##	self.curImageMaskDisplay=TextCharacterViewer(self,self.textBase,2)
##	self.curImageFinalDisplay=TextCharacterViewer(self,self.textBase,3)
class TextCharacterViewer(QtGui.QWidget):	
	def __init__(self, win, path, genMode, baseScale):
		QtGui.QWidget.__init__(self)
		self.win=win
		self.imgPath=path
		self.cW=baseScale
		self.cH=baseScale
		self.scanRange=[self.cW,self.cH,0,0]
		self.rect=[0,0,baseScale,baseScale]
		self.mode=genMode
		self.mouseDown=0
		self.baseScale=baseScale
		self.thumbIndex=-1
		self.valAdjustLock=-1
		
		self.img=QtGui.QLabel()
		self.img.setGeometry(0,0,self.cW,self.cH) # Placeholder
		self.img.setFixedSize(self.cW,self.cH)
		if genMode == 3:
			self.img.setText("[ Select Character ]")
			self.img.setStyleSheet("border: 1px solid #555555;")
		else:
			self.img.setText("--")
		self.img.setAlignment(QtCore.Qt.AlignCenter)
		self.data=None
		self.displayData=None
		self.preScaleData=None
		
		curImgBlock=QtGui.QVBoxLayout()
		curImgBlock.setSpacing(0) # Spacing & Margin was giving me trouble calculating dynamic loading in window
		curImgBlock.setMargin(0) # ||
		curImgBlock.addWidget(self.img)
		self.setLayout(curImgBlock) # Layout to display in parent window
		
	def pullCharacterRect(self, scaleMode):
		if self.mode == 3:
			init=0
			if type(scaleMode) is not int or self.thumbIndex>-1:
				if self.thumbIndex>-1:
					scaleMode=self.win.curImgListBlock.itemAt(self.thumbIndex).widget()
					pmap=QtGui.QPixmap.fromImage(scaleMode.data.toImage())
				else:
					self.thumbIndex=scaleMode.index
					pmap=QtGui.QPixmap.fromImage(scaleMode.data.toImage())
			else:
				pmap=self.win.curImageDisplay.data
				pmap=QtGui.QPixmap.fromImage(pmap.toImage())
				wVal=256-pmap.width()
				if self.displayData == None:
					init=1
				
				topPadVal=self.win.sliderTopPadding.value()
				bottomPadVal=self.win.sliderBottomPadding.value()
				if topPadVal!=0 or bottomPadVal!=0:
					baseImg=QtGui.QPixmap( pmap.width(), max(1, pmap.height()+topPadVal-bottomPadVal) )
					baseImg.fill(QtGui.QColor(0,0,0,0))
					painter=QtGui.QPainter(baseImg)
					painter.setCompositionMode(painter.CompositionMode_SourceOver)
					painter.drawPixmap(0,topPadVal,pmap)
					painter.end()
					pmap=baseImg
					###
					fromScale=max(pmap.width(),max(1, pmap.height()+topPadVal+bottomPadVal))
					premult=(float(fromScale)/256.0)*10000.0
					self.win.sliderPreMult.setValue(premult)
			
				pmapAlpha=self.win.curImageMaskDisplay.data
				pmapAlpha=QtGui.QPixmap.fromImage(pmapAlpha.toImage())
				if topPadVal!=0 or bottomPadVal!=0:
					baseImg=QtGui.QPixmap( pmapAlpha.width(), max(1, pmapAlpha.height()+topPadVal-bottomPadVal) )
					baseImg.fill(QtGui.QColor(0,0,0,255))
					painter=QtGui.QPainter(baseImg)
					painter.setCompositionMode(painter.CompositionMode_SourceOver)
					painter.drawPixmap(0,topPadVal,pmapAlpha)
					painter.end()
					pmapAlpha=baseImg
					
				pmap.setAlphaChannel(pmapAlpha)
			self.data=pmap
			self.displayData=pmap.scaled(self.baseScale,self.baseScale, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			
			if self.win.displayCheckerBoard == 1:
				baseImg=QtGui.QPixmap(self.baseScale,self.baseScale)
				baseImg.fill()
				painter=QtGui.QPainter(baseImg)
				painter.drawPixmap(0,0,self.win.checkerBoard)
				offset=[ float(self.baseScale-self.displayData.width())/2, float(self.baseScale-self.displayData.height())/2 ]
				painter.drawPixmap(offset[0],offset[1],self.displayData)
				painter.end()
				self.displayData=baseImg
				self.img.setPixmap(baseImg)
			else:
				self.img.setPixmap(self.displayData)
				
			if init == 1:
				pre=2
				post=1.5
				mmin=min( 116, max(15, int((wVal*pre)/2)))
				mmax=min( 116, max(15, int(128-(wVal*post)/2)))
				
				self.win.runValChangeEvent=0
				self.win.leftAlignSlider.setValue(mmin)
				self.win.rightAlignSlider.setValue(mmax)
				self.win.runValChangeEvent=1
			self.setPaddingLine()
			######
			######
			######
		else:
			blurLevels=self.win.sliderAlphaReach.value()
			self.scanRange=[]
			self.scanRange.extend(self.win.textBaseViewWindow.scanRange)
			if scaleMode==0:
				centroid=[(self.scanRange[2]+self.scanRange[0])/2, (self.scanRange[3]+self.scanRange[1])/2]
				rect=[centroid[0]-64, centroid[1]-64, self.win.curImageHelpers, self.win.curImageHelpers]
			elif scaleMode==1:
				size=[self.scanRange[2]-self.scanRange[0], self.scanRange[3]-self.scanRange[1]]
				rect=[self.scanRange[0]-blurLevels,self.scanRange[1]-blurLevels, size[0]+blurLevels*2,size[1]+blurLevels*2]
			pmap=self.win.imgData[self.win.curImage]
			pmap=pmap.copy(rect[0],rect[1], rect[2],rect[3])
			self.rect=rect
			if self.mode == 0:
				fromScale=max(rect[2],rect[3])
				premult=(float(fromScale)/256.0)*10000.0
				self.win.sliderPreMult.setValue(premult)
			elif self.mode == 1:
				img=pmap.toImage()
				for xy in self.win.textBaseViewWindow.reachPixels:
					x=xy[0]-rect[0]
					y=xy[1]-rect[1]
					img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
				pmap=QtGui.QPixmap.fromImage(img)
			elif self.mode == 2:
				reachPixels=[]
				reachPixels.extend(self.win.textBaseViewWindow.reachPixels)
				reachPixels=map(lambda x: [ max(0, min(rect[2]-1,x[0]-rect[0])), max(0, min(rect[3]-1,x[1]-rect[1])) ], reachPixels)
				#reachPixels=map(lambda x: [int(x.split(",")[0])-rect[0], int(x.split(",")[1])-rect[1]] , reachPixels)
				contrast=float(self.win.sliderContrast.value())/100.0
				pmap.fill(QtCore.Qt.black)
				mask=pmap.toImage()
				for xy in reachPixels:
					x= xy[0]
					y= xy[1]
					mask.setPixel(x,y,QtGui.QColor(255,255,255,255).rgb())
				growArr=[[1,1],[1,0],[1,-1], [0,1],[0,-1], [-1,1],[-1,0],[-1,-1]]
				
				if blurLevels > 0:
					reachPixels=[reachPixels]
					for c in range(blurLevels):
						reachPixels.append([])
						checkArr=max(0, c-1)
						for xy in reachPixels[c]:
							edge=0
							curPixelList=[]
							for checkXY in growArr:
								curXY=[ max(0, min(rect[2]-1, xy[0]+checkXY[0] )), max(0, min(rect[3]-1, xy[1]+checkXY[1])) ]
								curPixelList.append(curXY)
								if curXY not in reachPixels[-1] and curXY not in reachPixels[0]:
									reachPixels[-1].append(curXY)
						if c > 0:
							reachPixels[0].extend(reachPixels[-1])
					for c in range(1,blurLevels):
						curArr=reachPixels[c]
						fade= 1.0 - (float(c) / (float(blurLevels)+1.0))
						if fade != 1.0:
							fade*=contrast
						for v in curArr:
							val=min(255, max(0, int(255.0*fade) ))
							mask.setPixel(v[0],v[1],QtGui.QColor(val,val,val,val).rgba())
					# Running into a weird thing
					# Can't seem to run the first iteration
					# Like it wants to be ran backwards
					# ... Bleh ...
					# (Few days later)
					# Good chance its the alpha in what ever default RGB image format it is
					# Don't care to look into this, it works, haha
					c=1
					curArr=reachPixels[c]
					fade= 1.0 - (float(c) / (float(blurLevels)+1.0))
					fade*=fade
					if fade != 1.0:
						fade*=contrast
					for v in curArr:
						val=min(255, max(0, int(255.0*fade) ))
						mask.setPixel(v[0],v[1],QtGui.QColor(val,val,val,val).rgba())
				for x in range(rect[2]-1):
					for y in range(rect[3]-1):
						rand=random.choice(growArr)
						r,g,b,a=QtGui.QColor(mask.pixel(x,y)).getRgb()
						if r>0:
							mr,mg,mb,ma=QtGui.QColor(mask.pixel(rand[0]+x,rand[1]+y)).getRgb()
							r=max(0, min( 255, int((float(r)+float(r)+float(mr))/3.0) ))
							mask.setPixel(x,y,QtGui.QColor(r,r,r,r).rgba())
				pmap=QtGui.QPixmap.fromImage(mask)
				self.preScaleData=pmap
				
			self.data=pmap.scaled(256,256, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			self.displayData=self.data.scaled(self.baseScale,self.baseScale, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			self.img.setPixmap(self.displayData)
	def mousePressEvent(self, event):
		pos=event.pos()
		self.mouseDown=1
	def mouseMoveEvent(self, event):
		pos=event.pos()
		self.setPaddingLine(pos)
	def mouseReleaseEvent(self, event):
		pos=event.pos()
		self.setPaddingLine(pos)
		self.paddingLatch=0
		self.mouseDown=0
		self.valAdjustLock=-1
	def setPaddingLine(self,pos=None):
		if self.mode == 3:
			size=[self.scanRange[2]-self.scanRange[0], self.scanRange[3]-self.scanRange[1]]
			rect=[self.scanRange[0],self.scanRange[1], size[0],size[1]]
			scaler=[ float(self.scanRange[2]-self.scanRange[0])/float(rect[2]), float(self.scanRange[3]-self.scanRange[1])/float(rect[3]) ]

			baseLine=self.win.sliderBaseLine.value()*2
			padL=self.win.leftAlignSlider.value()*2
			padR=self.win.rightAlignSlider.value()*2+256
			
			leftRightPadValues=[]
			if pos != None:
				posX=int(float(pos.x())*(1/scaler[1]))
				posX=min(self.cW-1, max(0, posX))
				posY=int(float(pos.y())*(1/scaler[1]))
				posY=min(self.cH-1, max(0, posY))
				
				if self.valAdjustLock==-1:
					blDist=abs(baseLine-posY)
					padLDist=abs(padL-posX)
					padRDist=abs(padR-posX)
					mm=min(padLDist, padRDist)
					if blDist < mm or mm > 50:
						baseLine=posY
						self.valAdjustLock=0
						self.win.sliderBaseLine.setValue(int(posY/2))
					else:
						if posX<256:
							self.valAdjustLock=1
							padL=posX
							self.win.leftAlignSlider.setValue(posX/2)
						else:
							self.valAdjustLock=2
							padR=posX
							self.win.rightAlignSlider.setValue((posX/2)-256)
				else:
					if self.valAdjustLock==0:
						self.win.sliderBaseLine.setValue(int(posY/2))
					elif self.valAdjustLock==1:
						posX=max(0, min(255, posX))
						padL=posX
						self.win.leftAlignSlider.setValue(posX/2)
					elif self.valAdjustLock==2:
						posX=max(256, min(511, posX))
						padR=posX
						self.win.rightAlignSlider.setValue((posX-256)/2)
				leftRightPadValues.append(padL)
				leftRightPadValues.append(padR)
			else:
				leftRightPadValues.append(padL)
				leftRightPadValues.append(padR)
			img=self.displayData.toImage()
			if 0<baseLine<self.cH:
				for x in range(self.displayData.width()):
					#r,g,b,a=QtGui.QColor(img.pixel(x,y)).getRgb()
					img.setPixel(x,baseLine,QtGui.QColor(255,0,0,255).rgba())
			for x in leftRightPadValues:
				for y in range(self.displayData.height()):
					if 0<x<511 and 0<y<511:
						#r,g,b,a=QtGui.QColor(img.pixel(x,y)).getRgb()
						img.setPixel(x,y,QtGui.QColor(255,0,0,255).rgba())
			pxmap=QtGui.QPixmap.fromImage(img)
			self.img.setPixmap(pxmap)
			
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	galGen=ImageProcessor()
	galGen.show()
	try:
		sys.exit(app.exec_())
	except:
		pass;
