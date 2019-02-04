class ImageProcessor(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(ImageProcessor,self).__init__(parent)
		global woVersion
		
		self.scriptNameText=scriptNameText
		self.versionText=versionText
		self.setTitleBar()
		
		self.winSize=[1920,1080]
		#self.setMinimumSize(self.winSize[0],self.winSize[1])
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
		self.scanRangeStorage={}
		self.curImage=None
		self.curImagePath=None
		self.sampleMode=1
		self.zoom=1.0
		self.runValChangeEvent=1
		self.loopLatch=0
		self.textBaseToolMode=0
		self.prevBrushMode=0
		self.selectColorMode=0
		self.selectColorSamples=[]
		self.checkerBoard=None
		self.displayCheckerBoard=1
		self.buttonStyle="height:25px;padding-left:10px;padding-right:10px;"
		self.bgBrushStyle="margin:3px;padding:3px;"
		bgBrushStyleSelected="font-weight:bold;border:1px solid #232323;color:#eeeeee;"
		self.bgBrushColor=["background-color:#229022;","background-color:#228060;font-weight:bold;","background-color:#8f227a;font-weight:bold;"]
		self.bgBrushColor=map(lambda x: x+bgBrushStyleSelected, self.bgBrushColor)
		self.curImageFull=512
		self.curImageHelpers=196
		self.unsavedChanges=0
		self.charSampled=0
		self.sampleThreshold=0
		self.setWorkingAreaButtonText=["Set &Working Area", "Remove &Work Area"]
		self.cropWorkingAreaButtonText=["&Crop To Work Area", "Exit Work Area &Crop"]
		self.showOutlineButtonText=["Show &Outline Only", "Exit &Outline Only"]
		self.workAreaCrop=0
		self.outlineToggle=0
		self.hotkeyEventsActive=1
		
		self.setWindowStyleSheet()
		self.statusBarMsg=''
		self.statusBarFade=25
		self.statusBarFadeMax=25
		self.statusBarPerc=0
		self.statusBarLength=1
		self.statusBarMode=0
		self.statusBarModeSet=0
		
		self.curEntryObj=-1
		self.loadIndexList=[]
		self.loadScrollList=[]
		self.charSamplePoints=[]
		self.scrollIndexVal=0
		self.scrollIndexHeight=-1
		self.mainWidget=QtGui.QWidget(self)
		
		### Menu Bar ###
		self.menuBar=self.menuBar()
		fileMenu=self.menuBar.addMenu('File')
		fileMenu.addSeparator()
		quitItem=QtGui.QAction("Exit",self)
		quitItem.triggered.connect(self.quitPromptCreate)
		fileMenu.addAction(quitItem)
		self.infoMenu=self.menuBar.addMenu('Info')
		scriptInfoItem=QtGui.QAction(self.scriptNameText+" - "+self.versionText,self)
		self.infoMenu.addAction(scriptInfoItem)
		authorItem=QtGui.QAction("Written by - Kevin Edzenga",self)
		self.infoMenu.addAction(authorItem)
		infoItem=QtGui.QAction("Personal Site - www.Metal-Asylum.net",self)
		infoItem.triggered.connect(lambda: self.launchURL(1))
		self.infoMenu.addAction(infoItem)
		self.infoMenu.addSeparator()
		totalLineCount=self.findTotalLineCount()
		lineCountItem=QtGui.QAction("Total Python/PyQt Line Count - "+str(totalLineCount),self)
		self.infoMenu.addAction(lineCountItem)
		self.infoMenu.addSeparator()
		helpItem=QtGui.QAction("Help...",self)
		helpItem.triggered.connect(lambda: self.launchURL(0))
		self.infoMenu.addAction(helpItem)
		# Status Bar
		self.statusBar=self.statusBar()
		self.statusBar.messageChanged.connect(self.statusBarChange)

		self.mainLayout=QtGui.QVBoxLayout(self.mainWidget)
		self.mainLayout.setSpacing(0)
		self.mainLayout.setMargin(0)
		
		# Load directory text field
		self.dirBlock=QtGui.QHBoxLayout()
		self.dirField=QtGui.QLineEdit()
		self.dirField.installEventFilter(self)
		self.dirBlock.addWidget(self.dirField)
		# Create Load Dir button
		self.loadDir=QtGui.QPushButton('Set &Project Folder', self)
		self.loadDir.setStyleSheet(self.buttonStyle)
		self.loadDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.loadDir.clicked.connect(self.loadAndScanDir)
		self.dirBlock.addWidget(self.loadDir)
		#tab0.addLayout(self.dirBlock)
		self.mainLayout.addLayout(self.dirBlock)
		
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
		self.imageDisplayBlock=QtGui.QVBoxLayout()
		self.imgField=QtGui.QLabel()
		self.imgField.setText("""\n
- - Please select your 'Project Folder' containing - -\n\n\n
( 1 ) - Folder with your full sized images for a fresh build.\n
( Supported - jpg, jpeg, png, bmp )\n\n\n\n
( 2 ) - Project Folder containing 'Character List' or 'Page Data' exports.\n
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
		
		self.autoAlt()
		"""def newButton(self,name,txt,cmd,layout):
		eval(str(name)+"=QtGui.QPushButton('"+str(txt)+"', self)")
		eval(str(name)+".clicked.connect("+cmd+")")
		eval(str(layout)+".addWidget("+str(name)+")")"""
	def eventFilter(self, obj, e):
		if e.type() == QtCore.QEvent.FocusIn:
			self.hotkeyEventsActive=0
		if e.type() == QtCore.QEvent.FocusOut:
			self.hotkeyEventsActive=1
		return QtGui.QWidget.eventFilter(self, obj, e)
	def setTitleBar(self,custDisp=[]):
		disp=[]
		disp.extend(custDisp)
		disp.extend([self.scriptNameText])
		if self.versionText != '':
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
		QPushButton {color:#ffffff;background-color:#535353;padding:4px;border:2px groove #353535;}
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
		QLabel {color:#ffffff}
		QListWidget {background-color:#222222;color:#ffffff;padding:2px;margin:2px;border:1px solid #2f2f2f}
		QListWidgetItem {background-color:#565656;margin:3px}"""
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
		if self.statusBarMode != 0 and self.statusBarModeSet==0:
			grey=96.0
			r=g=b=int(grey)
			perc=self.statusBarPerc/self.statusBarFadeMax
			
			if self.statusBarMode == 1: # Good
				g=int(grey*(1.0-perc) + 200.0*perc)
				b=int(grey*(1.0-perc) + 50.0*perc)
			elif self.statusBarMode == 2: # Error
				r= int(grey*(1.0-perc) + 255.0*perc)
			elif self.statusBarMode == 3: # Alert
				r=int(grey*(1.0-perc) + 200.0*perc)
				g=int(grey*(1.0-perc) + 180.0*perc)
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
				
				self.setTitleBar(["Project '"+self.projectName+"'"])
				
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
				resetCharTopBlock=QtGui.QHBoxLayout()
				resetCharButton=QtGui.QPushButton("Reset Character Data",self)
				resetCharButton.setStyleSheet(self.buttonStyle)
				#resetCharButton.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred))
				resetCharButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				resetCharButton.clicked.connect(self.resetCurTextCharacter)
				resetCharTopBlock.addWidget(resetCharButton)
				###
				resetCharBlock.addLayout(resetCharTopBlock)
				entryEditBlock.addLayout(resetCharBlock)
				######
				thresholdColorRes=[150,50]
				fill=QtGui.QColor(66,67,67)
				###
				
				spacer=QtGui.QSpacerItem(10,3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				resetCharBlock.addItem(spacer)
				###
				self.baseListOptions=QtGui.QListWidget()
				self.baseListOptions.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
				self.baseListOptions.itemClicked.connect(self.updateTextBase)
				self.baseListOptions.setMaximumHeight(400)
				resetCharBlock.addWidget(self.baseListOptions)
				###
				self.toggleTextBaseListButton=QtGui.QPushButton("^^^  Hide TextBase List  ^^^",self)
				self.toggleTextBaseListButton.visCheck=1
				self.toggleTextBaseListButton.setFixedHeight(25)
				self.toggleTextBaseListButton.setStyleSheet(self.buttonStyle)
				self.toggleTextBaseListButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				self.toggleTextBaseListButton.clicked.connect(self.toggleTextBaseListVis)
				resetCharBlock.addWidget(self.toggleTextBaseListButton)
				###
				spacer=QtGui.QSpacerItem(10,8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				resetCharBlock.addItem(spacer)
				
				thresholdColorBlock=QtGui.QHBoxLayout()
				###
				self.thresholdColorSlider=SliderGroup(self,"Searching Threshold", [0,765,205],7,"int"," #", "thresholdColorMagTextUpdate()", 1)
				thresholdColorBlock.addWidget(self.thresholdColorSlider)
				###
				self.thresholdColor=QtGui.QLabel()
				baseImg=QtGui.QPixmap(thresholdColorRes[0],thresholdColorRes[1])
				baseImg.fill(fill)
				self.thresholdColor.setPixmap(baseImg)
				thresholdColorBlock.addWidget(self.thresholdColor)
				###
				self.thresholdColorSampleButton=QtGui.QPushButton("Sample &Threshold by Color",self)
				self.thresholdColorSampleButton.setStyleSheet(self.buttonStyle)
				self.thresholdColorSampleButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				self.thresholdColorSampleButton.clicked.connect(self.sampleNewThresholdColor)
				thresholdColorBlock.addWidget(self.thresholdColorSampleButton)
				resetCharBlock.addLayout(thresholdColorBlock)
				######
				textBaseModeBlock=QtGui.QHBoxLayout()
				textBaseModeBlock.setSpacing(3)
				self.textBaseMode_select=QtGui.QRadioButton("&Select Area")
				self.textBaseMode_select.setChecked(True)
				self.textBaseMode_select.setStyleSheet(self.bgBrushStyle+self.bgBrushColor[0])
				self.textBaseMode_select.mode="sel"
				self.textBaseMode_select.toggled.connect(lambda: self.setTextBaseMode(self.textBaseMode_select))
				textBaseModeBlock.addWidget(self.textBaseMode_select)
				###
				spacer=QtGui.QSpacerItem(10,8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				textBaseModeBlock.addItem(spacer)
				###
				self.textBaseMode_add=QtGui.QRadioButton("&Add Brush")
				self.textBaseMode_add.setStyleSheet(self.bgBrushStyle)
				self.textBaseMode_add.mode="add"
				self.textBaseMode_add.toggled.connect(lambda: self.setTextBaseMode(self.textBaseMode_add))
				textBaseModeBlock.addWidget(self.textBaseMode_add)
				###
				spacer=QtGui.QSpacerItem(10,8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				textBaseModeBlock.addItem(spacer)
				###
				self.textBaseMode_subtract=QtGui.QRadioButton("&Remove Brush")
				self.textBaseMode_subtract.setStyleSheet(self.bgBrushStyle)
				self.textBaseMode_subtract.mode="rem"
				self.textBaseMode_subtract.toggled.connect(lambda: self.setTextBaseMode(self.textBaseMode_subtract))
				textBaseModeBlock.addWidget(self.textBaseMode_subtract)
				######
				spacer=QtGui.QSpacerItem(20,8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				textBaseModeBlock.addItem(spacer)
				###
				self.brushSizeSlider=SliderGroup(self,"Add/Rem Brush Size", [1,10,5],2,"int","px")
				textBaseModeBlock.addWidget(self.brushSizeSlider)
				resetCharBlock.addLayout(textBaseModeBlock)
				###
				self.edgeGrowthSlider=SliderGroup(self,"Edge Grow/Shrink", [-10,10,0],7,"int","px", "extendEdges()")
				resetCharBlock.addWidget(self.edgeGrowthSlider)
				#entryEditBlock.addWidget(self.edgeGrowthSlider)
				
				displayOptionBlock=QtGui.QHBoxLayout()
				displayOptionBlock.setSpacing(3)
				displayOptionBlock.setMargin(0)
				###
				self.setWorkingAreaButton=QtGui.QPushButton(self.setWorkingAreaButtonText[0],self)
				self.setWorkingAreaButton.setStyleSheet(self.buttonStyle)
				self.setWorkingAreaButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				self.setWorkingAreaButton.clicked.connect(self.setWorkingArea)
				displayOptionBlock.addWidget(self.setWorkingAreaButton)
				###
				self.cropWorkingAreaButton=QtGui.QPushButton(self.cropWorkingAreaButtonText[0],self)
				self.cropWorkingAreaButton.setStyleSheet(self.buttonStyle)
				self.cropWorkingAreaButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				self.cropWorkingAreaButton.clicked.connect(lambda: self.cropWorkingArea())
				displayOptionBlock.addWidget(self.cropWorkingAreaButton)
				###
				self.resetWorkAreaToggle=QtGui.QCheckBox()
				self.resetWorkAreaToggle.setText("Exit Work Area on Reset")
				#self.resetWorkAreaToggle.setCheckState(QtCore.Qt.Checked)
				displayOptionBlock.addWidget(self.resetWorkAreaToggle)
				###
				spacer=QtGui.QSpacerItem(10,8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				resetCharBlock.addItem(spacer)
				###
				self.showOutlineOnly=QtGui.QPushButton(self.showOutlineButtonText[0],self)
				self.showOutlineOnly.setStyleSheet(self.buttonStyle)
				self.showOutlineOnly.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				self.showOutlineOnly.clicked.connect(self.displayOutlineToggle)
				displayOptionBlock.addWidget(self.showOutlineOnly)
				###
				resetCharBlock.addLayout(displayOptionBlock)
				######
				
				##### textBase Viewer Gui #####
				curTextBaseEditScrollBlock=QtGui.QScrollArea() #QAbstractScrollArea()
				curTextBaseEditScrollBlock.setWidgetResizable(True)
				#curTextBaseEditScrollBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				curTextBaseEditScrollInner=QtGui.QWidget(curTextBaseEditScrollBlock)
				#curTextBaseEditScrollBlock.setStyleSheet("QWidget {background-color:#2a2a2a;}")

				self.curEntryBlock=QtGui.QVBoxLayout()
				self.curEntryBlock.setAlignment(QtCore.Qt.AlignCenter)
				curTextBaseEditScrollInner.setLayout(self.curEntryBlock)
				self.curEntryBlock.setSpacing(pad)
				self.curEntryBlock.setMargin(pad)
				tmpEntry=QtGui.QLabel()
				tmpEntry.setText("Placeholder")
				tmpEntry.setAlignment(QtCore.Qt.AlignCenter)
				self.curEntryBlock.addWidget(tmpEntry)
				
				curTextBaseEditScrollBlock.setWidget(curTextBaseEditScrollInner)
				#entryEditBlock.addWidget(curTextBaseEditScrollBlock)
				resetCharBlock.addWidget(curTextBaseEditScrollBlock)
				
				
				################################
				### Character Entry Settings ###
				################################
				#self.curImageDisplayEditParent=QtGui.QVBoxLayout()
				self.curImageDisplayEditBlockWidget=QtGui.QWidget()
				#self.curImageDisplayEditBlockWidget.setMinimumWidth(600)
				self.curImageDisplayEditBlockWidget.setMaximumWidth(850)
				entryEditBlock.addWidget(self.curImageDisplayEditBlockWidget)
				self.curImageDisplayEditBlock=QtGui.QVBoxLayout()
				self.curImageDisplayEditBlock.setSpacing(0)
				self.curImageDisplayEditBlock.setMargin(0)
				self.curImageDisplayEditBlockWidget.setLayout(self.curImageDisplayEditBlock)
				
				self.curImageButtonBlock=QtGui.QVBoxLayout()
				updateButton=QtGui.QPushButton("Read Found Character Data",self)
				updateButton.setStyleSheet(self.buttonStyle)
				updateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
				updateButton.clicked.connect(self.pullFittedScale)
				self.curImageButtonBlock.addWidget(updateButton)
				###
				self.curImageDisplayEditBlock.addLayout(self.curImageButtonBlock)
		
		
				scrollCharacterEntryBlock=QtGui.QScrollArea()
				scrollCharacterEntryBlock.setWidgetResizable(True)
				scrollCharacterEntryBlock.setStyleSheet("""QWidget {background-color:#323232;}
				QScrollBar:vertical {height:20px;background-color:#808080;border:1px solid #202020;}""")
				scrollCharacterEntryBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				self.curImageDisplayEditBlock.addWidget(scrollCharacterEntryBlock)
				###
				curEntryEditScrollInner=QtGui.QWidget(scrollCharacterEntryBlock)
				#curEntryEditScrollInner.setStyleSheet("QWidget {background-color:#2a2a2a;}")
		
				scrollCharacterEntryLayout=QtGui.QVBoxLayout()
				scrollCharacterEntryLayout.setSpacing(3)
				scrollCharacterEntryLayout.setMargin(0)
				curEntryEditScrollInner.setLayout(scrollCharacterEntryLayout)
				scrollCharacterEntryBlock.setWidget(curEntryEditScrollInner)
				
				spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
				scrollCharacterEntryLayout.addItem(spacer)
				
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
				scrollCharacterEntryLayout.addLayout(self.curImageHelperBlock)
				
				spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
				scrollCharacterEntryLayout.addItem(spacer)
				
				######
				self.curImageDisplayWidget=QtGui.QWidget()
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
				self.curImageDisplayWidget.setLayout(self.curImageDisplayBlock)
				scrollCharacterEntryLayout.addWidget(self.curImageDisplayWidget)
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
				scrollCharacterEntryLayout.addLayout(leftRightAlignBlockWidgetBlock)
				######
				spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
				scrollCharacterEntryLayout.addItem(spacer)
				
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
				self.filterCharVal.installEventFilter(self)
				self.filterCharVal.editingFinished.connect(self.filterCharacters)
				self.filterCharBlock.addWidget(self.filterCharVal)
				self.sideBarBlock.addLayout(self.filterCharBlock)
				
				self.scrollIndexBlock=QtGui.QScrollArea()
				self.scrollIndexBlock.setWidgetResizable(True)
				self.scrollIndexBlock.setFixedWidth(sideBarWidth)
				self.scrollIndexBlock.setStyleSheet("""QWidget {background-color:#2a2a2a;}
				QScrollBar:vertical {height:20px;background-color:#808080;border:1px solid #202020;}""")
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
					
					## Help with QTimer from
					## https://stackoverflow.com/questions/21897322/pyqt-application-load-complete-event
					timer=QtCore.QTimer()
					timer.singleShot(0,lambda: self.textCharDisplay.buildTextDisplay(1))
				
					###### OUTPUT AND EXPORT ######
					# Load directory text field
					self.outDirBlock=QtGui.QHBoxLayout()
					self.outDirField=QtGui.QLineEdit()
					self.outDirField.installEventFilter(self)
					self.outDirBlock.addWidget(self.outDirField)
					# Create Load Dir button
					self.setOutDir=QtGui.QPushButton('Output Dir', self)
					self.setOutDir.setStyleSheet(self.buttonStyle)
					self.setOutDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
					self.setOutDir.clicked.connect(lambda: self.setOutputDir())
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
				textBasePaths,textBaseAbsPaths=self.prepProjectFolder(activeList[0])	
				if textBasePaths == None:
					self.statusBarUpdate(" -- Could not create directory '"+activeList[0]+"', Check for correct File Permissions that pxl can write to disk.  -- ", 5000,2)
				else:
					activeList=[textBasePaths[0]]
					for x,p in enumerate(activeList):
						scrollOffset+=scrollAdd+pad
						if loadObj==-1:
							curImg=IndexImageEntry(self,x,p,folderPicker+"/",size,None, None)
							loadObj=curImg
							self.sideBarTextBase.addWidget(curImg)
							curImg.offset=scrollOffset
							self.loadIndexList.append(curImg)
							self.loadScrollList.append([])
							self.loadScrollList[-1].append(scrollOffset)
							self.loadScrollList[-1].append(scrollOffset+curImg.imgSizeIndexList[1])
							scrollAdd=curImg.imgSizeIndexList[1]
					### textBase Relative Image Paths List Generation ###
					for x,tbpath in enumerate( textBasePaths ):
						formatted=self.formatPath(tbpath)
						item=QtGui.QListWidgetItem(formatted)
						item.raw=tbpath
						item.formatted=formatted
						item.absPath=textBaseAbsPaths[x]
						self.baseListOptions.addItem(item)
					self.scrollIndexBlock.setWidget(scrollInner)
					self.sideBarBlock.addWidget(self.scrollIndexBlock)
					entryBlock.addLayout(self.sideBarBlock)
					self.imageDisplayBlock.addLayout(entryBlock)
					loadObj.loadImage()
					self.textBasePath=loadObj.imgPath
					self.loadImageEntry(loadObj,1)
					self.baseListOptions.setCurrentRow(0)
					self.updateTextBase()
					
					self.loadExistingData(0)
					self.dispCheckerBoard(self.curImageFull,1)
					self.autoAlt()
					#self.textBaseViewWindow.setDefaultScroll() ### GET THIS WORKING
	def formatPath(self, name=None, relPath=0):
		if name != None:
			buildRelPath=repr(name)
			buildRelPath="".join(filter(None, buildRelPath.split("'")))
			if delimit in buildRelPath:
				buildRelPath=buildRelPath.split(delimit)
			elif '/' in buildRelPath:
				buildRelPath=buildRelPath.split('/')
			else:
				buildRelPath=None
			if buildRelPath != None:
				buildRelPath=filter(None, buildRelPath)
				if ":" not in name or relPath==1:
					if self.projectName in buildRelPath:
						projectIndex=buildRelPath.index(self.projectName)
						buildRelPath=buildRelPath[projectIndex:]
					buildRelPath=['']+buildRelPath
				buildRelPath='/'.join(buildRelPath)
				name=str(buildRelPath)
		return name
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
		textBaseAbsPaths=map(lambda x: curDir+delimit+scanFolder+delimit+x, textBaseNames)
		#textBaseNames=[]
		#textBaseNames.extend(textBasePaths)

		if genTextBaseOutputFolder==1:
			textBaseMoveToPaths=map(lambda x: curDir+delimit+scanFolder+delimit+self.textBaseImages+delimit+x, textBaseNames)
			for x,v, in enumerate(textBaseAbsPaths):
				curTo=textBaseMoveToPaths[x]
				os.rename(v,curTo)
			textBaseRelPaths=map(lambda x: delimit+scanFolder+delimit+self.textBaseImages+delimit+x, textBaseNames)
			textBaseAbsPaths=map(lambda x: curDir+delimit+scanFolder+delimit+self.textBaseImages+delimit+x, textBaseNames)
			
			self.statusBarUpdate(" -- Project Folder '"+scanFolder+"' Built; "+str(len(textBaseNames))+" Images moved to - "+scanFolder+delimit+self.textBaseImages+delimit+" -- ", 6500,1)
		else:
			textBaseRelPaths=map(lambda x: delimit+scanFolder+delimit+x, textBaseNames)

		return [textBaseRelPaths,textBaseAbsPaths]
	def setTextBaseMode(self, modeRadio):
		mode=modeRadio.mode
		self.textBaseMode_select.setStyleSheet(self.bgBrushStyle)
		self.textBaseMode_add.setStyleSheet(self.bgBrushStyle)
		self.textBaseMode_subtract.setStyleSheet(self.bgBrushStyle)
		if mode=="sel":
			self.textBaseMode_select.setStyleSheet(self.bgBrushStyle+self.bgBrushColor[0])
			self.textBaseToolMode=0
			self.prevBrushMode=0
		if mode=="add":
			self.textBaseMode_add.setStyleSheet(self.bgBrushStyle+self.bgBrushColor[1])
			self.textBaseToolMode=1
			self.prevBrushMode=1
		if mode=="rem":
			self.textBaseMode_subtract.setStyleSheet(self.bgBrushStyle+self.bgBrushColor[2])
			self.textBaseToolMode=2
			self.prevBrushMode=2
			
		if hasattr(self, "textBaseViewWindow"):
			self.textBaseViewWindow.drawBrushRadius(self.textBaseToolMode,None)
	def extendEdges(self):
		self.textBaseViewWindow.extendReachEdges()
	def updateTextBase(self):
		sel=str(self.baseListOptions.selectedItems()[0].text())
		raw=self.baseListOptions.selectedItems()[0].raw
		formatted=self.baseListOptions.selectedItems()[0].formatted
		absPath=self.baseListOptions.selectedItems()[0].absPath
		absPathFormatted=self.formatPath(absPath)
		folderPath="/".join(absPathFormatted.split("/")[:-1]+[''])
		imgName=absPathFormatted.split("/")[-1]
		
		#IndexImageEntry(win, index, name, relativePath, scaleSize, qtImg):
		size=[128,128]
		ClearLayout(self.sideBarTextBase)
		curImg=IndexImageEntry(self,0,imgName,folderPath,size,None, None)
		#self.curImgListBlock.addWidget(curImg)
		self.sideBarTextBase.addWidget(curImg)
		self.loadIndexList=[curImg]
		curImg.loadImage()
		self.textBasePath=formatted
		curImg.textBaseEntry=formatted
		self.curImage=formatted
		self.curImagePath=absPath
		self.loadImageEntry(curImg,0)
		self.resetCurTextCharacter()
	def toggleTextBaseListVis(self):
		self.toggleTextBaseListButton.visCheck=(self.toggleTextBaseListButton.visCheck+1)%2
		if self.toggleTextBaseListButton.visCheck==0:
			self.baseListOptions.setMaximumHeight(0)
			self.toggleTextBaseListButton.setText("vvv  Show TextBase List  vvv")
			###
			#self.toggleTextBaseListButton=QtGui.QPushButton("^ Hide ^",self)
			#self.toggleTextBaseListButton=QtGui.QPushButton("^ Hide ^",self)
		else:
			self.baseListOptions.setMaximumHeight(400)
			self.toggleTextBaseListButton.setText("^^^  Hide TextBase List  ^^^")
			
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
	def loadImageEntry(self,obj,boot=0):
		ClearLayout(self.curImageSettings)
		
		### SETTINGS ###
		self.curEntryObj=obj
		imgFull=obj.imgSizeFull

		### MAIN ENTRY ###
		ClearLayout(self.curEntryBlock)
		
		if boot==1:
			self.dirField.setText(obj.imgFolder+self.projectName+'/')
			outPath=str(self.dirField.text())+"pxl_textCharacterOutput/"
			self.setOutputDir(outPath)
			outPath=str(self.dirField.text())+"pxl_pageBuilderOutput/"
			self.pageViewer.setPageOutputDir(outPath)

		spacer=QtGui.QSpacerItem(10,5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		self.curImageSettings.addItem(spacer)
		
		self.textBaseViewWindow=TextBaseViewer(self,obj)
		self.curEntryBlock.addWidget(self.textBaseViewWindow)
		self.curEntryBlock.setSpacing(0)
		self.curEntryBlock.setMargin(0)
		
		### Sliders and Jazz ###
		self.sliderBaseLine=SliderGroup(self,"Base Line", [0,1024,210],3,"int"," px", "baseLineSliderChange()",1)
		self.curImageSettings.addWidget(self.sliderBaseLine)
		
		spacer=QtGui.QSpacerItem(10,3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		###
		self.sliderPreMult=SliderGroup(self,"PreMultiply Scale", [0,200,100],3,"float"," %", "preMultScaleSliderChange()",1)
		self.curImageSettings.addWidget(self.sliderPreMult)
		###
		spacer=QtGui.QSpacerItem(10,3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		
		### Alpha Reach Settings ###
		self.sliderAlphaReach=SliderGroup(self,"Alpha Fade Reach", [0,10,2],3,"int"," px", "alphaReachSliderReleased()",0)
		self.curImageSettings.addWidget(self.sliderAlphaReach)
		self.sliderContrast=SliderGroup(self,"Alpha Contrast", [0,110,70],3,"float"," %", "contrastSliderReleased()",0)
		self.curImageSettings.addWidget(self.sliderContrast)
		###
		spacer=QtGui.QSpacerItem(10,3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.curImageSettings.addItem(spacer)
		self.sliderRotate=SliderGroup(self,"Degree Rotation", [-20,20,0],3,"float"," *", "degreesSliderReleased()",0)
		self.curImageSettings.addWidget(self.sliderRotate)
		
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
		scanRange=[]
		scanRange.extend(self.textBaseViewWindow.scanRange)
		scanRange[2]=scanRange[2]-scanRange[0]
		scanRange[3]=scanRange[3]-scanRange[1]
		curChar=IndexImageEntry(self,1,'thumb','local',[128,128],scanRange, [self.curImageFinalDisplay])#[self.curImageDisplay, self.curImageMaskDisplay])
		self.curImgListPushTop(curChar)
		curChar.charField.setFocus()
		curChar.charField.selectAll()
		#self.curImgListBlock.addWidget(curChar)
		
		scanRangeKeys=self.scanRangeStorage.keys()
		if self.curImage not in scanRangeKeys:
			self.scanRangeStorage[self.curImage]=[]
		self.scanRangeStorage[self.curImage].append(scanRange)
		
		self.resetCurTextCharacter()
		curChar.loadEntry()
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
		resetWorkArea=self.resetWorkAreaToggle.isChecked()
		if self.textBaseViewWindow.workAreaActive==1 and resetWorkArea==1:
			self.setWorkingArea()
		self.textBaseViewWindow.resetScanRange()
		self.charSamplePoints=[]
	def paddingTopSliderChange(self):
		val=self.sliderTopPadding.value()
		strVal=str(val)
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
		val=self.sliderBaseLine.value
		if self.runValChangeEvent == 1 and self.charSampled==1:
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.baseline=val
			self.curImageFinalDisplay.setPaddingLine()
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def degreesSliderReleased(self):
		val=self.sliderRotate.value
		#self.rotateSliderVal.setText(str(val/100.0)+" deg")
		if self.runValChangeEvent == 1 and self.charSampled==1:
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.degRotation=val
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def preMultScaleSliderChange(self):
		val=self.sliderPreMult.value
		if self.runValChangeEvent == 1 and self.charSampled==1:
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.premultiply=val
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def contrastSliderReleased(self):
		val=self.sliderContrast.value
		#self.contrastVal.setText(str(val))
		if self.runValChangeEvent == 1 and self.charSampled==1:
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.contrast=val
			self.unsavedChanges=1
			if self.textCharDisplay.autoUpdate==True:
				self.textCharDisplay.reloadText()
	def alphaReachSliderReleased(self):
		val=self.sliderAlphaReach.value
		if self.runValChangeEvent == 1 and self.charSampled==1:
			self.curImageDisplay.pullCharacterRect(1)
			self.curImageOverlayDisplay.pullCharacterRect(1)
			self.curImageMaskDisplay.pullCharacterRect(1)
			self.curImageFinalDisplay.pullCharacterRect(1)
			thumbIndex=self.curImageFinalDisplay.thumbIndex
			if thumbIndex>-1:
				thumbWidget=self.curImgListBlock.itemAt(thumbIndex).widget()
				thumbWidget.alphaReach=val
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
	def sampleNewThresholdColor(self, exitSampleThresh=0):
		if self.sampleThreshold == 0 and exitSampleThresh==0:
			self.sampleThreshold=1
			self.selectColorMode=1
			self.textBaseToolMode=3
			self.selectColorSamples=[[0,0,0]]
			self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
			self.thresholdColorSampleButton.setStyleSheet(self.buttonStyle+"background-color:#0077cc;")
			self.statusBarUpdate(" -- Select a new threshold color ... Clicking and draging will blend colors together -- ", 0,1)
		else:
			self.sampleThreshold=0
			self.selectColorMode=0
			self.textBaseToolMode=self.prevBrushMode
			self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.thresholdColorSampleButton.setStyleSheet(self.buttonStyle)
	def setWorkingArea(self):
		workAreaActive=self.textBaseViewWindow.workAreaActive
		if self.textBaseToolMode==4 or workAreaActive==1:
			self.textBaseToolMode=self.prevBrushMode
			self.setWorkingAreaButton.setText(self.setWorkingAreaButtonText[0])
			self.setWorkingAreaButton.setStyleSheet(self.buttonStyle)
			if self.workAreaCrop==1:
				self.cropWorkingArea()
			self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.textBaseViewWindow.workAreaActiveToggle(0)
			self.statusBarUpdate(" -- Canceled selecting a 'Work Area' -- ", 3000,1)
		else:
			self.textBaseToolMode=4
			self.setWorkingAreaButton.setText(self.setWorkingAreaButtonText[1])
			self.setWorkingAreaButton.setStyleSheet(self.buttonStyle+"background-color:#0077cc;")
			self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
			self.textBaseViewWindow.workAreaActiveToggle(1)
			self.statusBarUpdate(" -- Select a larger area than your character ... Clicking and draging to make bounds -- ", 0,1)
	def cropWorkingArea(self, setStyle=1):
		workArea=self.textBaseViewWindow.workingRectArea
		if workArea[0] < workArea[2]:
			self.workAreaCrop=(self.workAreaCrop+1)%2
			if setStyle==1 or 1:
				curStyle=self.buttonStyle
				if self.workAreaCrop==1:
					curStyle+="background-color:#0077cc;"
				self.cropWorkingAreaButton.setStyleSheet(curStyle)
				self.cropWorkingAreaButton.setText(self.cropWorkingAreaButtonText[self.workAreaCrop])
			self.textBaseViewWindow.workAreaCropVis(self.workAreaCrop)
		else:
			self.statusBarUpdate(" -- No valid Work Area found - Use 'Set Work Area' before cropping -- ", 5000,3)
	def displayOutlineToggle(self):
		outlineToggle=self.outlineToggle
		curStyle=self.buttonStyle
		if outlineToggle==0:
			if len(self.textBaseViewWindow.reachPixels) == 0 and self.textBaseViewWindow.workAreaActive==0:
				self.statusBarUpdate(" -- No Character Data found - Select a character first -- ", 5000,3)
			else:
				curStyle+="background-color:#00af46;"
				self.outlineToggle=1
				self.textBaseViewWindow.checkOutlineUpdate()
		else:
			self.outlineToggle=0
			self.textBaseViewWindow.drawReachMask()
		self.showOutlineOnly.setStyleSheet(curStyle)
		self.showOutlineOnly.setText(self.showOutlineButtonText[self.outlineToggle])
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
			#self.selectColorSamples.pop(0)
			blendLen=float(len(self.selectColorSamples)-1)
			blendedValues=map(lambda x: int(float(x)/blendLen),self.selectColorSamples[0])
			self.textBaseViewWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.statusBarUpdate(" -- Threshold Color Updated -- ", 5000,1)

			setMag=int(float(sum(blendedValues))/3.0)
			fill=QtGui.QColor(setMag,setMag,setMag)
			
			baseImg=self.thresholdColor.pixmap()
			baseImg.fill(fill)
			setMag=sum(blendedValues)
			self.thresholdColorSlider.setValue(setMag)
			self.sampleNewThresholdColor(1)
		self.thresholdColor.setPixmap(baseImg)
	def thresholdColorMagTextUpdate(self):
		setMag=self.thresholdColorSlider.value
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
		if self.hotkeyEventsActive==1:
			if e.key()==QtCore.Qt.Key_P:
				self.loadAndScanDir()
			if self.curImage != None:
				if e.key()==QtCore.Qt.Key_T:
					self.sampleNewThresholdColor()
				if e.key()==QtCore.Qt.Key_S:
					self.textBaseMode_select.setChecked(True)
					#self.setTextBaseMode(self.textBaseMode_select)
				if e.key()==QtCore.Qt.Key_A:
					self.textBaseMode_add.setChecked(True)
					#self.setTextBaseMode(self.textBaseMode_add)
				if e.key()==QtCore.Qt.Key_R:
					self.textBaseMode_subtract.setChecked(True)
					#self.setTextBaseMode(self.textBaseMode_subtract)
				if e.key()==QtCore.Qt.Key_W:
					self.setWorkingArea()
				if e.key()==QtCore.Qt.Key_C:
					self.cropWorkingArea()
				if e.key()==QtCore.Qt.Key_O:
					self.displayOutlineToggle()
	def autoAlt(self):
		event=QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Alt, QtCore.Qt.NoModifier)
		QtCore.QCoreApplication.postEvent(self, event)
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
	def loadExistingData(self, displayError=1):
		### Do I really want to start making things backwards compatable during an Alpha?
		### How many people would have really downloaded it, except just to muck around?
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
					curChar=IndexImageEntry(self,1,'thumb','local',[128,128],None, 'preload')
					curChar.charBase=letter
					curCharNameKeys=charListKey.charList[letter][char].keys()
					buildRelPath=0
					if 'textBaseEntry' not in curCharNameKeys:
						buildRelPath=1
					buildRectData=0
					if 'rect' in curCharNameKeys:
						buildRectData=1
					for data in curCharNameKeys:
						curCharData=charListKey.charList[letter][char][data]
						### I shouldn't care about this....
						### Are people seriously downloading my script yet?
						### Hell with it.
						if data in ["premultiply","contrast","degRotation"]:
							if "." not in str(curCharData):
								curCharData=float(curCharData)/100.0
						if data=='textBaseFile':
							if buildRelPath==1:
								buildRelPath=self.formatPath(curCharData,1)
								setattr(curChar,'textBaseEntry',buildRelPath)
						if data=='textBaseEntry':
							if buildRectData==1:
								curRect=charListKey.charList[letter][char]['rect']
								if curRect[0]>-1 and curRect[1]>-1:
									srStorageKeys=self.scanRangeStorage.keys()
									if curCharData not in srStorageKeys:
										self.scanRangeStorage[curCharData]=[]
									self.scanRangeStorage[curCharData].append(curRect)
						setattr(curChar,data,curCharData)
					curTextBasePath=charListKey.charList[letter][char]['textBaseFile']
					curChar.textBaseFile=curTextBasePath
					curChar.exported=1
					curChar.loadImage()
					curChar.charFileName=char
					curChar.charField.setText(char)
					self.curImgListPushTop(curChar, mode='fast')
			self.curImgListPushTop(curChar, mode='update')
		
		self.pageViewer.loadPageBackground(1)
		self.pageViewer.loadPageDataFile(0)
		self.statusBarUpdate(" -- All data loaded for Project `"+self.projectName+"` --", 5000,1)
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
						exportData[char][title]['textBaseEntry']=curChar.textBaseEntry
						
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
				self.statusBarUpdate(" -- Wrote out to - "+path+" --", 10000,1)
				curTime=dt.datetime.now().strftime("%H:%M - %m/%d/%Y")
				self.unsavedChanges=0
			else:
				self.statusBarUpdate(" -- No created characters, please select and 'Finish Character' first -- ", 5000,2)
		else:
			self.statusBarUpdate(" -- No characters found, please 'Load Text Image' to load existing character data -- ", 5000,2)
	def launchURL(self,site):
		url=None
		if site==0:
			url=QtCore.QUrl('https://github.com/ProcStack/pxlTextGenerator')
		elif site==1:
			url=QtCore.QUrl('http://www.Metal-Asylum.net/')
		if url != None:
			QtGui.QDesktopServices.openUrl(url)
	def resizeEvent(self,e):
		if hasattr(self, "textCharDisplay"):
			self.textCharDisplay.buildTextDisplay(1)
	def closeEvent(self,e):
		self.quitPromptCreate()
		### Was used to javascript, attempted simply return False, yeah, that didn't work
		### https://stackoverflow.com/questions/18256459/qdialog-prevent-closing-in-python-and-pyqt
		e.ignore()
	def quitPromptCreate(self):
		self.closePrompt=QtGui.QMessageBox()
		self.closePrompt.setIcon(QtGui.QMessageBox.Question)
		self.closePrompt.setWindowTitle("Quit?")
		quitButton=None
		if self.unsavedChanges==1:
			self.closePrompt.addButton("Save and Quit", QtGui.QMessageBox.YesRole)
			self.closePrompt.addButton("Discard Changes and Quit", QtGui.QMessageBox.YesRole)
			msg="Are you sure you want to quit?"
		else:
			quitButton=self.closePrompt.addButton("Quit", QtGui.QMessageBox.YesRole)
			msg="There are no changes to save.\nAre you sure you want to quit?"
		self.closePrompt.setText(msg)
		cancelButton=self.closePrompt.addButton("Cancel", QtGui.QMessageBox.RejectRole)
		if self.unsavedChanges==1:
			cancelButton.setStyleSheet("text-decoration:underline;")
			self.closePrompt.setDefaultButton(cancelButton)
		else:
			quitButton.setStyleSheet("text-decoration:underline;")
			self.closePrompt.setDefaultButton(quitButton)
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
			e.ignore()
	def quitPromptReply(self, button):
		self.loopLatch=0
		try:
			if button.text() == "Save & Quit":
				self.exportCharList()
				self.quitApp()
			elif button.text() in ["Quit", "Discard Changes and Quit"]:
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
	