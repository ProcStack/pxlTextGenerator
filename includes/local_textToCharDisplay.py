class TextToCharDisplay(QtGui.QWidget):	
	def __init__(self, win):
		QtGui.QWidget.__init__(self)
		self.win=win
		self.imgName=None
		self.imgPath=None
		self.backgroundData=None
		self.displayData=None
		self.textBuildData=None
		self.pastTest=''
		self.bgW=0
		self.bgH=0
		self.cW=[500,1500]
		self.cH=180
		self.baseLine=120
		self.runner=0.0
		self.seed=0.0
		self.autoUpdate=True
		
		self.charListArray=None
		
		self.offset=[0,0]
		self.curOffset=[0,0]
		self.startPos=[0,0]
		self.curPos=[0,0]
		self.mouseDown=0
		
		######
		
		self.setFixedHeight(self.cH)
		
		self.charTestBlock=QtGui.QHBoxLayout()
		self.charTestBlock.setSpacing(0)
		self.charTestBlock.setMargin(0) 
		
		
		charTestButtonBlock=QtGui.QVBoxLayout()
		charTestButtonBlock.setSpacing(0)
		charTestButtonBlock.setMargin(3) 
		###
		charTestButton=QtGui.QPushButton('Load Text Image', self)
		charTestButton.setStyleSheet(self.win.buttonStyle)
		charTestButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestButton.clicked.connect(self.loadTextBackground)
		charTestButtonBlock.addWidget(charTestButton)
		###
		charTestReloadButton=QtGui.QPushButton('Reload Text', self)
		charTestReloadButton.setStyleSheet(self.win.buttonStyle)
		charTestReloadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestReloadButton.clicked.connect(self.reloadText)
		charTestButtonBlock.addWidget(charTestReloadButton)
		###
		self.charTestBlock.addLayout(charTestButtonBlock)
		
		charTextSeedBlockWidget=QtGui.QWidget()
		charTextSeedBlockWidget.setFixedHeight(140)
		###
		self.charTestOptionBlock=QtGui.QVBoxLayout()
		self.charTestOptionBlock.setSpacing(0)
		self.charTestOptionBlock.setMargin(0) 
		
		charInputTextBlock=QtGui.QHBoxLayout()
		charInputTextBlock.setSpacing(5)
		charInputTextBlock.setMargin(0)
		charInputText=QtGui.QLabel()
		charInputText.setText('Input Test Text - ')
		charInputText.setStyleSheet("QLabel {margin:5px;}")
		charInputTextBlock.addWidget(charInputText)
		self.charTestText=QtGui.QLineEdit()
		self.charTestText.installEventFilter(self.win)
		self.charTestText.editingFinished.connect(self.buildTextDisplay)
		charInputTextBlock.addWidget(self.charTestText)
		self.charTestOptionBlock.addLayout(charInputTextBlock)
		
		charTestBuildCharListBlock=QtGui.QHBoxLayout()
		charTestBuildCharListBlock.setSpacing(5)
		charTestBuildCharListBlock.setMargin(0)
		###
		charTestCapitalButton=QtGui.QPushButton('Pull Capital Letters', self)
		charTestCapitalButton.setStyleSheet(self.win.buttonStyle)
		charTestCapitalButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestCapitalButton.clicked.connect(lambda: self.pullCharacters("capital"))
		charTestBuildCharListBlock.addWidget(charTestCapitalButton)
		###
		charTestLowerButton=QtGui.QPushButton('Pull Lower Letter', self)
		charTestLowerButton.setStyleSheet(self.win.buttonStyle)
		charTestLowerButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestLowerButton.clicked.connect(lambda: self.pullCharacters("lower"))
		charTestBuildCharListBlock.addWidget(charTestLowerButton)
		###
		charTestNumberButton=QtGui.QPushButton('Pull Numbers', self)
		charTestNumberButton.setStyleSheet(self.win.buttonStyle)
		charTestNumberButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestNumberButton.clicked.connect(lambda: self.pullCharacters("numbers"))
		charTestBuildCharListBlock.addWidget(charTestNumberButton)
		###
		charTestNonAlphaButton=QtGui.QPushButton('Pull Non-Alphanumeric', self)
		charTestNonAlphaButton.setStyleSheet(self.win.buttonStyle)
		charTestNonAlphaButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestNonAlphaButton.clicked.connect(lambda: self.pullCharacters("special"))
		charTestBuildCharListBlock.addWidget(charTestNonAlphaButton)
		###
		self.charTestOptionBlock.addLayout(charTestBuildCharListBlock)
		######
		charMissingListBlock=QtGui.QHBoxLayout()
		charMissingListBlock.setSpacing(5)
		charMissingListBlock.setMargin(0)
		charMissingText=QtGui.QLabel()
		charMissingText.setText('Missing Characters - ')
		charMissingText.setStyleSheet("QLabel {margin:5px;}")
		charMissingListBlock.addWidget(charMissingText)
		self.charMissingList=QtGui.QLineEdit()
		self.charMissingList.setStyleSheet("QLineEdit {background-color:#454545; color:#aaaaaa}")
		self.charMissingList.setDisabled(True)
		charMissingListBlock.addWidget(self.charMissingList)
		self.charTestOptionBlock.addLayout(charMissingListBlock)
		###
		self.charTestAutoReload=QtGui.QCheckBox()
		self.charTestAutoReload.setText("Auto Update")
		self.charTestAutoReload.setCheckState(QtCore.Qt.Checked)
		self.charTestAutoReload.stateChanged.connect(self.setAutoReload)
		self.charTestOptionBlock.addWidget(self.charTestAutoReload)
		###
		self.charTestBlock.addWidget(charTextSeedBlockWidget)
		charTextSeedBlockWidget.setLayout(self.charTestOptionBlock)

		capPadLinesBlock=QtGui.QVBoxLayout()
		capPadLinesBlock.setSpacing(4)
		capPadLinesBlock.setMargin(4) 
		###
		self.sliderCapLineSlider=QtGui.QSlider()
		self.sliderCapLineSlider.setOrientation(QtCore.Qt.Vertical)
		self.sliderCapLineSlider.setMinimum(0)
		self.sliderCapLineSlider.setMaximum(self.baseLine)
		self.sliderCapLineSlider.setFixedHeight(150)
		curVal=self.baseLine-int(self.baseLine*.1)
		self.sliderCapLineSlider.setValue(curVal)
		capPadLinesBlock.addWidget(self.sliderCapLineSlider)
		###
		self.sliderCapLineValText=QtGui.QLabel()
		self.sliderCapLineValText.setText(str(self.baseLine-curVal))
		self.sliderCapLineValText.setAlignment(QtCore.Qt.AlignCenter)
		self.sliderCapLineValText.setFixedWidth(40)
		capPadLinesBlock.addWidget(self.sliderCapLineValText)
		self.charTestBlock.addLayout(capPadLinesBlock)
		self.sliderCapLineSlider.valueChanged.connect(self.updateCapLowLines)
		
		lowPadLinesBlock=QtGui.QVBoxLayout()
		lowPadLinesBlock.setSpacing(4)
		lowPadLinesBlock.setMargin(4) 
		###
		self.sliderLowLineSlider=QtGui.QSlider()
		self.sliderLowLineSlider.setOrientation(QtCore.Qt.Vertical)
		self.sliderLowLineSlider.setMinimum(0)
		self.sliderLowLineSlider.setMaximum(self.baseLine)
		self.sliderLowLineSlider.setFixedHeight(150)
		curVal=self.baseLine-int(self.baseLine*.5)
		self.sliderLowLineSlider.setValue(curVal)
		lowPadLinesBlock.addWidget(self.sliderLowLineSlider)
		###
		self.sliderLowLineValText=QtGui.QLabel()
		self.sliderLowLineValText.setText(str(self.baseLine-curVal))
		self.sliderLowLineValText.setAlignment(QtCore.Qt.AlignCenter)
		self.sliderLowLineValText.setFixedWidth(40)
		lowPadLinesBlock.addWidget(self.sliderLowLineValText)
		self.charTestBlock.addLayout(lowPadLinesBlock)
		self.sliderLowLineSlider.valueChanged.connect(self.updateCapLowLines)
		
		textBedDisplayLayout=QtGui.QVBoxLayout()
		textBedDisplayLayout.setSpacing(0)
		textBedDisplayLayout.setMargin(0) 
		###
		self.charTestDisplay=QtGui.QLabel()
		self.charTestDisplay.setText("[ Character TextBed Display ]")
		self.charTestDisplay.setMinimumWidth(self.cW[0])
		#self.charTestDisplay.setMaximumWidth(self.cW[1])
		self.charTestDisplay.setMinimumHeight(self.cH)
		self.charTestDisplay.setAlignment(QtCore.Qt.AlignCenter)
		textBedDisplayLayout.addWidget(self.charTestDisplay)
		###
		spacer=QtGui.QSpacerItem(self.cW[1],0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		textBedDisplayLayout.addItem(spacer)
		self.charTestBlock.addLayout(textBedDisplayLayout)
		
		self.loadTextBackground(1) # Check for existing `bgPaperTest.jpg` BG image
		
		self.setLayout(self.charTestBlock) # Layout to display in parent window
	def pullCharacters(self, pullType):
		charList=[]
		for c in range(self.win.curImgListBlock.count()):
			curChar=self.win.curImgListBlock.itemAt(c).widget()
			charList.append(str(curChar.charBase))
		outputStr=""
		if pullType=="capital":
			for c in charList:
				if c.isupper():
					outputStr+=c
		elif pullType=="lower":
			for c in charList:
				if c.islower() and c not in ['b"',"b'","b`"]:
					outputStr+=c
		elif pullType=="numbers":
			for c in charList:
				if c.isdigit():
					outputStr+=c
		elif pullType=="special":
			for c in charList:
				if (not c.isupper() and not c.islower() and not c.isdigit()) or c in ['b"',"b'","b`"]:
					outputStr+=c
		self.charTestText.setText(outputStr)
		self.reloadText()
	def updateCapLowLines(self):
		capVal=self.baseLine-self.sliderCapLineSlider.value()
		lowVal=self.baseLine-self.sliderLowLineSlider.value()
		strCapVal=str(capVal)
		strLowVal=str(lowVal)
		self.sliderCapLineValText.setText(strCapVal)
		self.sliderLowLineValText.setText(strLowVal)
		self.updateTextBackground()
	def setPaddingLine(self,pmap):
		capVal=self.baseLine-int(self.sliderCapLineSlider.value())
		lowVal=self.baseLine-int(self.sliderLowLineSlider.value())
		baseVal=self.baseLine
		img=pmap.toImage()
		for x in range(pmap.width()):
			img.setPixel(x,capVal,QtGui.QColor(255,0,0,255).rgba())
			if x%30<15:
				img.setPixel(x,lowVal,QtGui.QColor(255,0,0,255).rgba())
			img.setPixel(x,baseVal,QtGui.QColor(255,0,0,255).rgba())
		pmap=QtGui.QPixmap.fromImage(img)
		return pmap
	def reloadText(self):
		self.buildTextDisplay(1)
	def setAutoReload(self):
		val=self.charTestAutoReload.isChecked()
		self.autoUpdate=val
		self.reloadText()
	def updateRandomSeed(self):
		val=float(self.seedSlider.value())/100.00
		self.seedSliderVal.setText(str(val))
		self.seed=val
		self.reloadText()
	def buildCharListArray(self):
		if hasattr(self.win, "curImgListBlock"):
			charListData={}
			for c in range(self.win.curImgListBlock.count()):
				curChar=self.win.curImgListBlock.itemAt(c).widget()
				if type(curChar)==IndexImageEntry:
					char=curChar.charBase
					if char not in charListData.keys():
						charListData[char]={}
					
					buildImageData=0
					titleExists=1
					
					title=curChar.charFileName
					exported=curChar.exported
					if title not in charListData[char].keys():
						titleExists=0
						charListData[char][title]={}
						
						charListData[char][title]['exported']=exported
						charListData[char][title]['imgData']=None
						if exported == 0:
							buildImageData=1
						
					charListData[char][title]['imgIndex']=c
					charListData[char][title]['baseline']=curChar.baseline
					charListData[char][title]['premultiply']=curChar.premultiply
					charListData[char][title]['spacingLeft']=curChar.spacingLeft
					charListData[char][title]['spacingRight']=curChar.spacingRight
					charListData[char][title]['rect']=str(curChar.rect)
					
					if titleExists == 1 and buildImageData==0 and exported==0:
						if charListData[char][title]['paddingTop'] != curChar.paddingTop:
							buildImageData=1
						if charListData[char][title]['paddingBottom'] != curChar.paddingBottom:
							buildImageData=1
					charListData[char][title]['paddingTop']=curChar.paddingTop
					charListData[char][title]['paddingBottom']=curChar.paddingBottom
					
					if buildImageData == 1:
						difData=curChar.data
						#difData.setAlphaChannel(curChar.dataAl	pha)
						charListData[char][title]['imgData']=difData
			self.charListArray=charListData
		else:
			self.win.statusBarUpdate(" -- Please 'Load Text Image' to load existing character data -- ", 5000,1)
	def mousePressEvent(self, event):
		pos=event.globalPos()
		self.startPos=[pos.x(), pos.y()]
		self.curPos=[pos.x(), pos.y()]
		self.curOffset=[self.offset[0], self.offset[1]]
		self.mouseDown=1
		self.charTestDisplay.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
	def mouseMoveEvent(self, event):
		if self.mouseDown > 0:
			pos=event.globalPos()
			self.curPos=[pos.x(), pos.y()]
			offsetY=max(0, min( self.curOffset[1] + self.startPos[1]-self.curPos[1], self.bgH-self.cH ))
			self.offset=[0, offsetY]
			self.updateTextBackground()
		else:
			self.charTestDisplay.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
	def mouseReleaseEvent(self, event):
		if self.mouseDown>0:
			### I'm doing something wrong here
			### Fix it dang it!
			"""pos=event.pos()
			posX=pos.x()
			posY=pos.y()
			self.curPos=[pos.x(), pos.y()]
			print self.curPos
			print self.curOffset
			print "-----"
			print "||",self.startPos[1],self.curPos[1], self.bgH,self.cH
			offsetY=max(0, min( self.curOffset[1] + self.startPos[1]-self.curPos[1], self.bgH-self.cH ))
			self.offset=[0, offsetY]"""
			self.charTestDisplay.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
			self.mouseDown=0
			self.updateTextBackground()
	def loadTextBackground(self,checkLocal=0):
		bgPicker=''
		if checkLocal == 1:
			path=bundleDir+"/textBed_paperBackground.jpg"
			if os.path.exists(path):
				bgPicker=path
		if bgPicker=='':
			ext=("jpg", "jpeg", "png", "bmp")
			bgPicker=QtGui.QFileDialog.getOpenFileName(self,"Select Background Image",curDir, "Image files (*.jpg *.jpeg *.png *.bmp)")
		if bgPicker != "":
			pmap=QtGui.QPixmap()
			pmap.load(bgPicker)
			self.backgroundData=pmap
			self.bgW=pmap.width()
			self.bgH=pmap.height()
			self.buildTextDisplay(1)
	def updateTextBackground(self):
		set=0
		label=self.charTestDisplay
		res=[label.width(), label.height()]
		if self.backgroundData != None:
			copyRes=[min(res[0], self.bgW), res[1]]
			
			pmap=QtGui.QPixmap.fromImage(self.backgroundData.toImage()).copy(self.offset[0],self.offset[1],copyRes[0],copyRes[1])
			if res[0] != copyRes[0]:
				pmap=pmap.scaled(res[0],res[1], QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
			pmap=self.setPaddingLine(pmap)
			palpha=QtGui.QPixmap(res[0],res[1])
			palpha.fill(QtGui.QColor(255,255,255))
			pmap.setAlphaChannel(palpha)
			self.displayData=QtGui.QPixmap.fromImage(pmap.toImage())
			set=1
		if self.textBuildData != None:
			if set==0:
				pmap=QtGui.QPixmap(res[0], res[1])
				pmap.fill(QtGui.QColor(0,0,0,255))

			painter=QtGui.QPainter(pmap)
			painter.setCompositionMode(painter.CompositionMode_SourceOver)
			painter.drawPixmap(0,0,self.textBuildData)
			painter.end()
			set=1
			
		if set==1:
			self.charTestDisplay.setPixmap(pmap)
	def buildTextDisplay(self, force=0):
		val=str(self.charTestText.text())
		if val != self.pastTest or force==1:
			self.pastTest=val
			self.charTestText.clearFocus()
			label=self.charTestDisplay
			res=[label.width(), label.height()]
			
			leftStart=20
			
			if hasattr(self.win, "curImgListBlock"):
				if self.win.curImgListBlock.count() == 0:
					return
			else:
				self.win.statusBarUpdate(" -- Please 'Load Text Image' to load existing character data -- ", 5000,2)
				return
			dir=str(self.win.dirField.text()).strip()
			if dir != '':
				if val != '':
					self.buildCharListArray()
					baseImg=QtGui.QPixmap(res[0], res[1])
					baseImg.fill(QtGui.QColor(0,0,0,0))
					painter=QtGui.QPainter(baseImg)
					
					self.runner=0
					printText=[]
					counter=[]
					val=list(val)
					backChars=["'",'"',"`"]
					skip=0
					inTag=0
					maxTagLength=10
					tags=["ocl","ocr","oll","olr","osl","osr","oal","oar"]
					curTag=''
					missingChars=[]
					keepPrinting=1
					for x,c in enumerate(val):
						self.runner+=1.0
						if c == "b":
							if x < len(val)-1:
								if val[x+1] in backChars:
									skip=1
									cc=c
						elif c=="%":
							if inTag==1:
								inTag=2
								skip=0
							else:
								for v in range(1,maxTagLength):
									if x+v<maxTagLength:
										curTag+=val[x+v]
										if curTag in tags:
											inTag=1
											break;
										if val[x+v] == "%":
											inTag=0
											cc=c
											break;
									else:
										break;
						if inTag==1:
							skip=1
						elif inTag==0:
							if skip==0:
								cc=c
							elif skip==2:
								skip=0
								cc+=c
						if skip == 0:
							if inTag==2:
								inTag=0
								cc=curTag
								curTag=''
							if cc == " ":
								leftStart=leftStart+50
								printText.append(' ')
							else:
								count=counter.count(cc)
								charData=self.pullCharData(cc,count)
								if charData == None:
									missingChars.append(cc)
									continue;
								if keepPrinting == 1:
									offset=[ leftStart-charData['spacingLeft'],-charData['baseline']+self.baseLine ]
									leftStart=leftStart-charData['spacingLeft']+charData['spacingRight']
									painter.drawPixmap(offset[0],offset[1],charData['data'])
									printText.append("_".join(charData['name'].split("_")[1::]))
									if offset[0] > res[0]:
										keepPrinting=0
							counter.append(cc)
						else:
							skip+=1
					painter.end()
					self.textBuildData=baseImg
					printText=", ".join(printText)
					missingCharStr=" ".join(missingChars)
					
					self.charMissingList.setDisabled(False) #I dunno, testing
					self.charMissingList.setText(missingCharStr)
					self.charMissingList.setDisabled(True)
				else:
					self.textBuildData=None
		self.updateTextBackground()
	def pullCharData(self,curChar,entry):
		curChar=str(curChar)
		charKeys=self.charListArray.keys()
		if curChar in charKeys:
			retDict={}
			random.seed( self.runner + self.seed )
			#charVar=random.choice(self.charListArray[curChar].keys())
			curCharKeys=self.charListArray[curChar].keys()
			charVar=curCharKeys[entry%len(curCharKeys)]
			retDict['name']=charVar
			charVar=self.charListArray[curChar][charVar]
			export=charVar['exported']
			pmap=None
			if export == 0:
				pmap=charVar['imgData']
			else:
				pmap=self.win.curImgListBlock.itemAt(charVar['imgIndex']).widget().data
			retDict['premultiply']=charVar['premultiply']/100.0
			mm=int(float(max(pmap.width(), pmap.height()))*retDict['premultiply'])
			retDict['resMax']=[mm,mm]
			res=[ int(float(pmap.width())*retDict['premultiply']), int(float(pmap.height())*retDict['premultiply']) ]
			pmap=pmap.scaled(res[0],res[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			retDict['res']=[pmap.width(), pmap.height()]
			retDict['data']=pmap
			retDict['baseline']=int(float(charVar['baseline'])*retDict['premultiply'])
			retDict['spacingLeft']=int(float(charVar['spacingLeft'])*retDict['premultiply'])
			retDict['spacingRight']=int(float(charVar['spacingRight'])*retDict['premultiply'])
			
			return retDict
		return None

#####################################################################
#####################################################################
#####################################################################

class PageBuilder(QtGui.QWidget):	
	def __init__(self, win):
		QtGui.QWidget.__init__(self)
		self.win=win
		self.imgName=None
		self.imgPath=None
		self.backgroundData=None
		#self.displayData=None
		self.pageImgData=[]
		self.textBuildData=None
		self.pastTest=''
		self.bgW=0
		self.bgH=0
		self.cW=1000
		self.cH=100
		self.baseLine=75
		self.runner=0.0
		self.seed=0.0
		self.autoUpdate=True
		self.editPrep=False
		
		self.charListArray=None
		
		self.offset=[0,0]
		self.curOffset=[0,0]
		self.startPos=[0,0]
		self.curPos=[0,0]
		self.mouseDown=0
		
		self.pageData=[]
		self.curPage=0
		
		######
		
		self.charTestBlock=QtGui.QHBoxLayout()
		self.charTestBlock.setSpacing(0)
		self.charTestBlock.setMargin(0) 
		
		charTextSeedBlockWidget=QtGui.QWidget()
		charTextSeedBlockWidget.setFixedWidth(800)
		
		self.charTestOptionBlock=QtGui.QVBoxLayout()
		self.charTestOptionBlock.setSpacing(0)
		self.charTestOptionBlock.setMargin(0) 
		###
		loadPageDataFile=QtGui.QPushButton('Load Page Data File', self)
		loadPageDataFile.setFixedHeight(50)
		loadPageDataFile.setStyleSheet(self.win.buttonStyle)
		loadPageDataFile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		loadPageDataFile.setStyleSheet("QPushButton {margin-top:5px;}")
		loadPageDataFile.clicked.connect(self.loadPageDataFile)
		self.charTestOptionBlock.addWidget(loadPageDataFile)
		###
		spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
		self.charTestOptionBlock.addItem(spacer)
		###
		self.pageFileLocationBlock=QtGui.QHBoxLayout()
		self.pageFileLocationBlock.setSpacing(0)
		self.pageFileLocationBlock.setMargin(0) 
		self.pageFileLocation=QtGui.QLineEdit()
		self.pageFileLocation.installEventFilter(self.win)
		self.pageFileLocationBlock.addWidget(self.pageFileLocation)
		###
		charTestButton=QtGui.QPushButton('Load Page BG Image', self)
		charTestButton.setStyleSheet(self.win.buttonStyle)
		charTestButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		charTestButton.clicked.connect(self.loadPageBackground)
		self.pageFileLocationBlock.addWidget(charTestButton)
		###
		self.charTestOptionBlock.addLayout(self.pageFileLocationBlock)
		
		hBar=HorizontalBar()#[0,30],2) ## For custome bar
		self.charTestOptionBlock.addWidget(hBar)
		
		pageIndentBlock=QtGui.QHBoxLayout()
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("- -")
		pageIndentBlock.addWidget(pageSpacer)
		###
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("Input Page Text")
		pageIndentBlock.addWidget(pageSpacer)
		###
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("- -")
		pageIndentBlock.addWidget(pageSpacer)
		###
		self.charTestOptionBlock.addLayout(pageIndentBlock)
		
		self.inputTextBlock=QtGui.QVBoxLayout()
		self.inputTextBlock.setSpacing(0)
		self.inputTextBlock.setMargin(0) 
		self.inputTextBlock.setAlignment(QtCore.Qt.AlignCenter)
		self.inputText=QtGui.QPlainTextEdit()
		self.inputText.installEventFilter(self.win)
		self.inputText.setStyleSheet("QPlainTextEdit {margin:5px;selection-color:#ffffff;selection-background-color:#454545;background-color:#909090;}")
		self.inputText.resize(700,400)
		self.inputTextBlock.addWidget(self.inputText)
		self.charTestOptionBlock.addLayout(self.inputTextBlock)
		
		hBar=HorizontalBar()#[0,30],2) ## For custome bar
		self.charTestOptionBlock.addWidget(hBar)
		
		pageIndentBlock=QtGui.QHBoxLayout()
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("- -")
		pageIndentBlock.addWidget(pageSpacer)
		###
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("Page Indentation")
		pageIndentBlock.addWidget(pageSpacer)
		###
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("- -")
		pageIndentBlock.addWidget(pageSpacer)
		###
		self.charTestOptionBlock.addLayout(pageIndentBlock)
		
		self.pageIndentLeft=SliderGroup(self,"Left",[0,2048,150],7,"int",' px',"updatePaddingBars()")
		self.charTestOptionBlock.addWidget(self.pageIndentLeft)
		self.pageIndentTop=SliderGroup(self,"Top",[0,2048,100],7,"int",' px',"updatePaddingBars()")
		self.charTestOptionBlock.addWidget(self.pageIndentTop)
		self.pageIndentRight=SliderGroup(self,"Right",[0,2048,1500],7,"int",' px',"updatePaddingBars()")
		self.charTestOptionBlock.addWidget(self.pageIndentRight)
		self.pageIndentBottom=SliderGroup(self,"Bottom",[0,2048,1948],7,"int",' px',"updatePaddingBars()")
		self.charTestOptionBlock.addWidget(self.pageIndentBottom)
		
		hBar=HorizontalBar()#[0,30],2) ## For custome bar
		self.charTestOptionBlock.addWidget(hBar)
		
		pageIndentBlock=QtGui.QHBoxLayout()
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("- -")
		pageIndentBlock.addWidget(pageSpacer)
		###
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("Text Options")
		pageIndentBlock.addWidget(pageSpacer)
		###
		pageSpacer=QtGui.QLabel()
		pageSpacer.setAlignment(QtCore.Qt.AlignCenter)
		pageSpacer.setText("- -")
		pageIndentBlock.addWidget(pageSpacer)
		###
		self.charTestOptionBlock.addLayout(pageIndentBlock)
		### Page Options ###
		self.fontScale=SliderGroup(self,"Font Scale",[0,2,.75],7,"float",' %', "buildTextOutput(0)")
		self.charTestOptionBlock.addWidget(self.fontScale)
		self.spaceSize=SliderGroup(self,"Space Size",[0,200,50],7,"int",' px', "buildTextOutput(0)")
		self.charTestOptionBlock.addWidget(self.spaceSize)
		self.lineHeight=SliderGroup(self,"Line Height",[0,200,75],7,"int",' px', "buildTextOutput(0)")
		self.charTestOptionBlock.addWidget(self.lineHeight)
		self.lineIndent=SliderGroup(self,"Line Indent",[0,200,50],7,"int",' px', "buildTextOutput(0)")
		self.charTestOptionBlock.addWidget(self.lineIndent)
		self.charSeed=SliderGroup(self,"Random Seed",[0,200,0],7,"float",'', "buildTextOutput(0)")
		self.charTestOptionBlock.addWidget(self.charSeed)
		
		self.charTestBlock.addWidget(charTextSeedBlockWidget)
		charTextSeedBlockWidget.setLayout(self.charTestOptionBlock)
		
		hBar=HorizontalBar()#[0,30],2) ## For custome bar
		self.charTestOptionBlock.addWidget(hBar)
		
		self.pageAutoUpdate=QtGui.QCheckBox()
		self.pageAutoUpdate.setText("Auto Update Page")
		self.pageAutoUpdate.setCheckState(QtCore.Qt.Checked)
		self.pageAutoUpdate.stateChanged.connect(self.setAutoReload)
		self.charTestOptionBlock.addWidget(self.pageAutoUpdate)

		spacer=QtGui.QSpacerItem(10,50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.charTestOptionBlock.addItem(spacer)
		
		###
		convertInputText=QtGui.QPushButton('Update Output Text to Writing', self)
		convertInputText.setFixedHeight(50)
		convertInputText.setStyleSheet(self.win.buttonStyle)
		convertInputText.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		convertInputText.setStyleSheet("QPushButton {margin-top:5px;}")
		convertInputText.clicked.connect(self.buildTextOutput)
		self.charTestOptionBlock.addWidget(convertInputText)
		###
		
		spacer=QtGui.QSpacerItem(10,50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		self.charTestOptionBlock.addItem(spacer)
		
		buildToNewPage=QtGui.QPushButton('Set to New Page Entry', self)
		buildToNewPage.setFixedHeight(50)
		buildToNewPage.setStyleSheet(self.win.buttonStyle)
		buildToNewPage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		buildToNewPage.setStyleSheet("QPushButton {margin-top:5px;}")
		buildToNewPage.clicked.connect(self.addPageIndex)
		self.charTestOptionBlock.addWidget(buildToNewPage)
		
		spacer=QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.charTestOptionBlock.addItem(spacer)
		
		######
		self.pageOutputDirBlock=QtGui.QVBoxLayout()
		self.pageOutputDirBlock.setSpacing(0)
		self.pageOutputDirBlock.setMargin(0) 
		###
		self.pageOutputDirTextBlock=QtGui.QHBoxLayout()
		self.pageOutputDirTextBlock.setSpacing(0)
		self.pageOutputDirTextBlock.setMargin(0) 
		self.pageOutputDirText=QtGui.QLineEdit()
		self.pageOutputDirText.installEventFilter(self.win)
		self.pageOutputDirTextBlock.addWidget(self.pageOutputDirText)
		###
		pageOutputSetDir=QtGui.QPushButton('Output Directory', self)
		pageOutputSetDir.setStyleSheet(self.win.buttonStyle)
		pageOutputSetDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		pageOutputSetDir.clicked.connect(self.setPageOutputDir)
		self.pageOutputDirTextBlock.addWidget(pageOutputSetDir)
		###
		self.pageOutputDirBlock.addLayout(self.pageOutputDirTextBlock)
		self.charTestOptionBlock.addLayout(self.pageOutputDirBlock)
		
		outputButtonBlock=QtGui.QHBoxLayout()
		outputButtonBlock.setSpacing(3)
		outputButtonBlock.setMargin(0)
		###
		exportPageDataFile=QtGui.QPushButton('Write Page Data File', self)
		exportPageDataFile.setStyleSheet(self.win.buttonStyle)
		exportPageDataFile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		exportPageDataFile.setStyleSheet("QPushButton {margin-top:5px;}")
		exportPageDataFile.clicked.connect(lambda: self.writePageDataFile(1,0))
		outputButtonBlock.addWidget(exportPageDataFile)
		###
		exportAllPages=QtGui.QPushButton('Export All Page Data && Images', self)
		exportAllPages.setStyleSheet(self.win.buttonStyle)
		exportAllPages.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		exportAllPages.setStyleSheet("QPushButton {margin-top:5px;}")
		exportAllPages.clicked.connect(lambda: self.writePageDataFile(1,1))
		outputButtonBlock.addWidget(exportAllPages)
		###
		self.charTestOptionBlock.addLayout(outputButtonBlock)
		######
		######
		pagePanel=QtGui.QVBoxLayout()
		self.pageOutputBlock=QtGui.QScrollArea() #QAbstractScrollArea()
		self.pageOutputBlock.setWidgetResizable(True)
		pageOutputInner=QtGui.QWidget(self.pageOutputBlock)
		pageOutputInner.setStyleSheet("QWidget {background-color:#2a2a2a;}")

		### Page Builder Output Viewer ###
		self.curPageBlock=QtGui.QVBoxLayout()
		self.curPageBlock.setAlignment(QtCore.Qt.AlignCenter)
		pageOutputInner.setLayout(self.curPageBlock)
		self.curPageBlock.setSpacing(0)
		self.curPageBlock.setMargin(0)
		self.pageOutput=PageBuilderViewer(self)
		self.curPageBlock.addWidget(self.pageOutput)
		
		self.pageOutputBlock.setWidget(pageOutputInner)
		pagePanel.addWidget(self.pageOutputBlock)
		
		##### PAGE ENTRY LIST ######
		bottomBarHeight=200
		self.sideBarBlock=QtGui.QHBoxLayout()
		self.sideBarTextBase=QtGui.QVBoxLayout()
		self.sideBarTextBase.setAlignment(QtCore.Qt.AlignCenter)
		self.sideBarTextBaseWidget=QtGui.QWidget()
		self.sideBarTextBaseWidget.setLayout(self.sideBarTextBase)
		self.sideBarBlock.addWidget(self.sideBarTextBaseWidget)
		###
		self.scrollIndexBlock=QtGui.QScrollArea()
		self.scrollIndexBlock.setWidgetResizable(True)
		self.scrollIndexBlock.setFixedHeight(bottomBarHeight)
		self.scrollIndexBlock.setStyleSheet("QWidget {background-color:#2a2a2a;}")
		#self.scrollIndexBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollIndexBlock.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		scrollInner=QtGui.QWidget(self.scrollIndexBlock)
		###
		self.curPageListBlock=QtGui.QHBoxLayout(scrollInner)
		#self.curPageListBlock.setAlignment(QtCore.Qt.AlignCenter)
		scrollInner.setLayout(self.curPageListBlock)
		self.curPageListBlock.setSpacing(0)
		self.curPageListBlock.setMargin(0)
		###
		size=self.scrollIndexBlock.frameGeometry()
		size=[128,128]
		scrollOffset=0
		scrollAdd=0
		loadObj=-1
		self.scrollIndexBlock.setWidget(scrollInner)
		self.sideBarBlock.addWidget(self.scrollIndexBlock)
		pagePanel.addLayout(self.sideBarBlock)
		
		self.charTestBlock.addLayout(pagePanel)
		
		self.setLayout(self.charTestBlock) # Layout to display in parent window
	def resetSettings(self):
		### I need to set a better method to reset values ... ###
		self.fontScale.setVale(.75)
		self.spaceSize.setVale(50)
		self.lineHeight.setVale(75)
		self.lineIndent.setVale(50)
		self.charSeed.setVale(0)
		self.pageIndentLeft.setVale(150)
		self.pageIndentTop.setVale(100)
		self.pageIndentRight.setVale(1500)
		self.pageIndentBottom.setVale(1948)
		self.inputText.setPlainText("")
	def updatePaddingBars(self):
		if self.editPrep==False:
			#self.pageOutput.updateTextBackground()
			self.pageOutput.buildTextDisplay()
	def updateRandomSeed(self):
		val=float(self.seedSlider.value())/100.00
		self.seedSliderVal.setText(str(val))
		self.seed=val
		self.buildTextDisplay()
	def setAutoReload(self):
		val=self.pageAutoUpdate.isChecked()
		self.autoUpdate=val
		self.buildTextOutput()
	def buildTextOutput(self, force=1):
		runUpdate=1
		if force==0:
			if self.autoUpdate == False:
				runUpdate=0
		if runUpdate==1 and self.editPrep==False:
			self.pageOutput.buildTextDisplay()
	def loadPageBackground(self):
		ext=("jpg", "jpeg", "png", "bmp")
		bgPicker=QtGui.QFileDialog.getOpenFileName(self,"Select Background Image",curDir, "Image files (*.jpg *.jpeg *.png *.bmp)")
		if bgPicker != "":
			if os.path.exists(bgPicker):
				bgPicker=str(bgPicker)
				self.imgPath=bgPicker
				self.pageOutput.imgPath=bgPicker
				bgSplit=bgPicker.split('/') # Delimitter gets corrected in pyqt
				bgBaseFile=bgSplit[-1]
				self.imgName=bgBaseFile
				self.pageOutput.imgName=bgBaseFile
				
				bgPath='/'.join(bgSplit[:-1])
				self.imgFolder=bgPath
				self.pageOutput.imgFolder=bgPath
				
				self.pageFileLocation.setText(bgPicker)
				self.pageOutput.loadPageBackground(bgPicker)
				self.buildTextOutput()
	def setPageOutputDir(self, setDir=None):
		if setDir == None or setDir == False:
			folderPicker=QtGui.QFileDialog.getExistingDirectory(self,"Set Output Directory")
			if folderPicker != "":
				folderPicker=str(folderPicker)
				if "\\" in folderPicker:
					folderPicker="/".join(filter(None, folderPicker.split("\\"))+[''])
				self.pageOutputDirText.setText(folderPicker)
		else:
			self.pageOutputDirText.setText(setDir)
	def updatePageIndex(self, thumbIndex=None):
		if len(self.pageData)>0:
			if self.editPrep==False:
				if thumbIndex==None:
					thumbIndex=self.curPage
				curThumb=None
				if thumbIndex>=self.curPageListBlock.count():
					curThumb=IndexPageEntry(self.win, self, self.curPage, "Page_"+str(thumbIndex), self.imgPath, [152,152], "H", [self.pageOutput.pageImgData], self.pageData[thumbIndex])
					self.curPageListBlock.addWidget(curThumb)
				else:
					curThumb=self.curPageListBlock.itemAt(self.curPage).widget()
					curThumb.pageData=self.pageData[self.curPage] # I don't like this method.....
				curThumb.updatePageThumb(self.pageOutput.groupPage,self.pageOutput.pageImgData)
	def addPageIndex(self):
		self.pageOutput.buildTextDisplay(1)
	def editGroup(self,mode,groupData):
		self.editPrep=True
		pageDataArray=[]
		if mode==0: # Edit Existing Group
			self.pageOutput.img.setPixmap(groupData.data[0])
			self.curPage=groupData.group
			pageDataArray=groupData.pageData
		else:
			pageDataArray=groupData
		pageDataKeysArray=pageDataArray.keys()
		#self.parent.pageData[self.group]=[]
		for k in pageDataKeysArray:
			if k not in ["lineData", "pageFlip"]:
				if k == "inputText": # Might need to change this to 'in []'
					eval('self.'+k+'.setPlainText(r"""'+str(pageDataArray[k])+'""")')
				else:
					eval("self."+k+".setValue(str("+str(pageDataArray[k])+"))")
		self.editPrep=False
		self.pageOutput.buildTextDisplay()
	def writePageDataFile(self, exportFile=1, exportImages=0):
		### When I get multi pages going, this might become an issue here ###
		### The line data will be set within a Page dictionary ###
		if self.curPageListBlock.count() > 0:
			path=str(self.win.dirField.text()).strip()
			if path == "":
				self.win.statusBarUpdate(" -- No Page Output directory set; make sure your project is loaded or set an output directory -- ", 5000,2)
				return
			self.win.statusBarUpdate(" -- Prepping Page Data and Images --", 0,0)
			if exportFile==1:
				exportData=[]
				for e in range(self.curPageListBlock.count()):
					curEntry=self.curPageListBlock.itemAt(e).widget()
					exportData.append( curEntry.pageData )
				for group in exportData:
					for line in group['lineData']:
						for wordData in line['wordData']:
							for char in wordData['chars']:
								char['data']=None
				export=formatArrayToString(0, exportData)
				export="pageList="+export
				
				filePath=path
				if filePath[-1] != "/":
					filePath+="/"
				filePath="\\".join(str(filePath).split("/"))
				filePath+="pageListKey.py"
				with open(filePath, "w") as f:
					f.write(export)
				
				if exportImages==0:
					self.win.statusBarUpdate(" -- Wrote out data to - '"+delimit+self.win.projectName+delimit+"pageListKey.py' --", 10000,1)
				curTime=dt.datetime.now().strftime("%H:%M - %m/%d/%Y")
			if exportImages==1:
				imgPath=str(self.pageOutputDirText.text()).strip()
				
				lim="/"
				if delimit in imgPath:
					lim=delimit
				if imgPath[-1]  != lim:
					imgPath+=lim
					
				imgPath=delimit+delimit.join(imgPath.split(lim)[-3:])
				self.win.statusBarUpdate(" -- Starting export of Page Images --", 0,0)
				self.pageOutput.saveImage()
				self.win.statusBarUpdate(" -- Wrote out data to - '"+delimit+self.win.projectName+delimit+"pageListKey.py'; Pages exported to - '"+imgPath+"' --", 10000,1)
			self.win.unsavedChanges=0
		else:
			self.win.statusBarUpdate(" -- No characters found, please 'Load Text Image' to load existing character data -- ", 5000,2)
	def loadPageDataFile(self):
		path=self.win.dirField.text()
		if path == "":
			self.win.statusBarUpdate(" -- No Page Output directory set; make sure your project is loaded or set an output directory -- ", 5000,2)
		else:
			if path[-1] != "/":
				path+="/"
			path="\\".join(str(path).split("/"))
			path+="pageListKey.py"
			if os.path.exists(path):
				self.win.statusBarUpdate(" -- Reading and building pages from local PageListKey file --", 0,0)
				
				sys.path.append(self.win.projectName)
				import pageListKey
				reload(pageListKey)
				
				for pageGroup in pageListKey.pageList:
					self.pageOutput.buildTextDisplay(1)
					self.editGroup(1,pageGroup)
			else:
				self.win.statusBarUpdate(" -- No exported data found '"+self.win.projectName+delimit+"pageListKey.py'; please export a page first. -- ", 5000,2)
	def buildTextDisplay(self, newPage=0):
		self.win.statusBarUpdate(" -- All pages from local PageListKey file built --", 5000,1)
class PageBuilderViewer(QtGui.QWidget):	
	def __init__(self, win):
		QtGui.QWidget.__init__(self)
		self.parent=win
		self.win=win.win
		self.imgName=None
		self.imgFolder=None
		self.imgPath=None
		self.loaded=0
		self.displayData=None
		self.backgroundData=None
		self.pageImgData=None
		self.group=0
		self.groupPage=0
		self.textBuildData=None
		self.pastTest=''
		self.cW=0
		self.cH=0
		self.zoom=1.0
		self.cWOrig=0
		self.cHOrig=0
		self.baseLine=75
		self.runner=0.0
		self.seed=0.0
		self.pageFileName="pageBuildExport"
		self.exported=0
		
		self.charListArray=None
		
		self.offset=[0,0]
		self.curOffset=[0,0]
		self.startPos=[0,0]
		self.curPos=[0,0]
		
		self.mousePressStart=[]
		self.scrollStart=[]
		self.mouseDown=0
		self.mouseDrag=0
		
		self.curImgBlock=QtGui.QVBoxLayout()
		self.curImgBlock.setSpacing(0) # Spacing & Margin was giving me trouble calculating dynamic loading in window
		self.curImgBlock.setMargin(0) # ||
		
		self.img=QtGui.QLabel()
		self.img.setText("( 1 ) Have characters built or loaded in 'Character Builder'\n( 2 ) Load a Page Background Image")
		self.img.setStyleSheet("QLabel {padding:200px;}")
		self.img.setAlignment(QtCore.Qt.AlignCenter)
		self.curImgBlock.addWidget(self.img)
		self.setLayout(self.curImgBlock)
	def loadPageBackground(self,imgPath):
		self.imgPath=imgPath
		pmap=QtGui.QPixmap()
		pmap.load(imgPath)
		self.backgroundData=pmap
		self.img.setPixmap(pmap)
		self.loaded=1
		res=[pmap.width(),pmap.height()]
		self.cW=res[0]
		self.cH=res[1]
		self.cWOrig=res[0]
		self.cHOrig=res[1]
		self.updateTextBackground()
		"""
		pmap=QtGui.QPixmap()
		pmap.load(bgPicker)
		self.backgroundData=pmap
		self.bgW=pmap.width()
		self.bgH=pmap.height()
		#self.updateTextBackground()
		"""
	def buildCharListArray(self):
		if hasattr(self.win, "curImgListBlock"):
			charListData={}
			for c in range(self.win.curImgListBlock.count()):
				curChar=self.win.curImgListBlock.itemAt(c).widget()
				if type(curChar)==IndexImageEntry:
					char=curChar.charBase
					if char not in charListData.keys():
						charListData[char]={}
					
					buildImageData=0
					titleExists=1
					
					title=curChar.charFileName
					exported=curChar.exported
					if title not in charListData[char].keys():
						titleExists=0
						charListData[char][title]={}
						
						charListData[char][title]['exported']=exported
						charListData[char][title]['imgData']=None
						if exported == 0:
							buildImageData=1
						
					charListData[char][title]['imgIndex']=c
					charListData[char][title]['baseline']=curChar.baseline
					charListData[char][title]['premultiply']=curChar.premultiply
					charListData[char][title]['spacingLeft']=curChar.spacingLeft
					charListData[char][title]['spacingRight']=curChar.spacingRight
					charListData[char][title]['rect']=str(curChar.rect)
					
					if titleExists == 1 and buildImageData==0 and exported==0:
						if charListData[char][title]['paddingTop'] != curChar.paddingTop:
							buildImageData=1
						if charListData[char][title]['paddingBottom'] != curChar.paddingBottom:
							buildImageData=1
					charListData[char][title]['paddingTop']=curChar.paddingTop
					charListData[char][title]['paddingBottom']=curChar.paddingBottom
					
					if buildImageData == 1:
						difData=curChar.data
						#difData.setAlphaChannel(curChar.dataAlpha)
						charListData[char][title]['imgData']=difData
			self.charListArray=charListData
		else:
			self.win.statusBarUpdate(" -- Please 'Load Text Image' to load existing character data -- ", 5000,1)
	def updateTextBackground(self):
		set=0
		if self.backgroundData != None:
			res=[self.cWOrig, self.cHOrig]
			pmap=QtGui.QPixmap.fromImage(self.backgroundData.toImage())#.copy(self.offset[0],self.offset[1],res[0],res[1])
			palpha=QtGui.QPixmap(self.cWOrig, self.cHOrig)
			palpha.fill(QtGui.QColor(255,255,255))
			pmap.setAlphaChannel(palpha)
			self.pageImgData=QtGui.QPixmap.fromImage(pmap.toImage())
			set=1
		if self.textBuildData != None:
			if set==0:
				pmap=QtGui.QPixmap(self.cWOrig, self.cHOrig)
				pmap.fill(QtGui.QColor(0,0,0,255))

			painter=QtGui.QPainter(pmap)
			painter.setCompositionMode(painter.CompositionMode_SourceOver)
			painter.drawPixmap(0,0,self.textBuildData)
			painter.end()
			set=1
			
		if set==1:
			#self.img.setPixmap(pmap)
			self.pageImgData=QtGui.QPixmap.fromImage(pmap.toImage())
			pmap=self.setPaddingLine(pmap)
			self.displayData=QtGui.QPixmap.fromImage(pmap.toImage())
			self.setZoom()
			self.parent.updatePageIndex()
	def setPaddingLine(self,pmap):
		topPad=self.parent.pageIndentTop.value
		bottomPad=self.parent.pageIndentBottom.value
		leftPad=self.parent.pageIndentLeft.value
		rightPad=self.parent.pageIndentRight.value
		"""
		capVal=self.baseLine-int(self.sliderCapLineSlider.value())
		lowVal=self.baseLine-int(self.sliderLowLineSlider.value())
		baseVal=self.baseLine
		"""
		img=pmap.toImage()
		for x in range(pmap.width()):
			img.setPixel(x,topPad,QtGui.QColor(255,0,0,255).rgba())
			img.setPixel(x,bottomPad,QtGui.QColor(255,0,0,255).rgba())
		for y in range(pmap.height()):
			img.setPixel(leftPad,y,QtGui.QColor(255,0,0,255).rgba())
			img.setPixel(rightPad,y,QtGui.QColor(255,0,0,255).rgba())
		pmap=QtGui.QPixmap.fromImage(img)
		return pmap
	def inputText(self):
		return str(self.parent.inputText.toPlainText())
	def buildTextDisplay(self, newPage=0):
		val=self.inputText()
		#if val != self.pastTest or force==1:
		textUpdated=0
		if val != self.pastTest:
			textUpdated=1
		self.pastTest=val
		res=[self.cWOrig, self.cHOrig]
		
		charOffsets=[0,0]
		
		if hasattr(self.win, "curImgListBlock"):
			if self.win.curImgListBlock.count() == 0:
				self.win.statusBarUpdate(" -- No character data found, please create characters first -- ", 5000,2)
				return
		else:
			self.win.statusBarUpdate(" -- Please 'Load Text Image' to load existing character data -- ", 5000,2)
			return
		dir=str(self.win.dirField.text()).strip()
		if dir != '':
			#if val != '':
			curPageData={}
			curLineData=[]
			pageFlip=0
			#if textUpdated == 1:
			self.buildCharListArray()
			
			fontScale=self.parent.fontScale.value
			spaceSize=self.parent.spaceSize.value
			lineHeight=self.parent.lineHeight.value
			lineIndent=self.parent.lineIndent.value
			###
			charSeed=self.parent.charSeed.value
			self.seed=charSeed
			###
			padLeft=self.parent.pageIndentLeft.value
			padRight=self.parent.pageIndentRight.value
			padTop=self.parent.pageIndentTop.value
			padBottom=self.parent.pageIndentBottom.value
			
			curPageData={}
			curPageData['inputText']=val
			curPageData['pageFlip']=pageFlip
			curPageData['fontScale']=fontScale
			curPageData['spaceSize']=spaceSize
			curPageData['lineHeight']=lineHeight
			curPageData['lineIndent']=lineIndent
			curPageData['charSeed']=charSeed
			curPageData['pageIndentLeft']=padLeft
			curPageData['pageIndentRight']=padRight
			curPageData['pageIndentTop']=padTop
			curPageData['pageIndentBottom']=padBottom
			
			curLineData=[]
			self.runner=0
			val=list(val)
			backChars=["'",'"',"`"]
			skip=0
			
			paintLine=0
			genNewLine=1
			fontScaleLine=fontScale
			fontScaleChar=fontScale
			for x,c in enumerate(val):
				self.runner+=1.0
				if genNewLine==1:
					newLineData={}
					newLineData['wordData']=[]
					newWord={}
					newWord['size']=[0,0]
					newWord['chars']=[]
					newWord['fontScale']=1.0
					newLineData['wordData'].append(newWord)
					newLineData['spaceWidth']=spaceSize
					newLineData['fontScale']=1.0
					newLineData['lineOffsets']=charOffsets
					curLineData.append(newLineData)
					genNewLine=0
				
					fontScale=self.parent.fontScale.value
				
				if c == "b":
					if x < len(val)-1:
						if val[x+1] in backChars:
							skip=1
							cc=c
				if skip==0:
					cc=c
				elif skip==2:
					skip=0
					cc+=c
				if skip == 0:
					if cc == " ":
						#leftStart=leftStart+spaceSize
						charOffsets[0]=charOffsets[0]+spaceSize
						newWord={}
						newWord['size']=[0,0]
						newWord['chars']=[]
						newWord['fontScale']=1.0
						curLineData[-1]['wordData'].append(newWord)
					elif cc=="\n":
						charOffsets=[0,charOffsets[1]+lineHeight]
						genNewLine=1
					else:
						charData=self.pullCharData(cc,fontScaleChar)
						if charData != None:
							curOffset=[ charOffsets[0]-charData['spacingLeft'],charOffsets[1]-charData['baseline']+self.baseLine ]
							charData['offset']=curOffset
							charOffsets[0]=charOffsets[0]-charData['spacingLeft']+charData['spacingRight']

							curLineData[-1]['wordData'][-1]['chars'].append(charData)
				else:
					skip+=1
			curPageData['lineData']=curLineData
			if self.parent.curPage>=len(self.parent.pageData):
				self.parent.pageData.append(curPageData)
			else:
				self.parent.pageData[self.parent.curPage]=curPageData
			"""else:
				if len(self.parent.pageData)==0:
					return None
				curPageData=self.parent.pageData[self.parent.curPage]
				curLineData=curPageData['lineData']
				pageFlip=curPageData['pageFlip']
				padLeft=curPageData['pageIndentLeft']
				padRight=curPageData['pageIndentRight']
				padTop=curPageData['pageIndentTop']
				padBottom=curPageData['pageIndentBottom']
			"""
			baseImg=QtGui.QPixmap(res[0], res[1])
			baseImg.fill(QtGui.QColor(0,0,0,0))
			painter=QtGui.QPainter(baseImg)
			for line in curLineData:
				for word in line['wordData']:
					for char in word['chars']:
						pmap=char['data']
						curOffset=char['offset']
						painter.drawPixmap(curOffset[0]+padLeft,curOffset[1]+padTop,pmap)
			painter.end()
			self.textBuildData=baseImg
			if newPage==1:
				self.parent.curPage+=1
				self.parent.pageData.append(curPageData)
			#else:
			#	self.textBuildData=None
			self.updateTextBackground()
	def pullCharData(self,curChar, fontScale):
		curChar=str(curChar)
		charKeys=self.charListArray.keys()
		if curChar in charKeys:
			retDict={}
			retDict['char']=curChar
			random.seed( self.runner + self.seed )
			charVar=random.choice(self.charListArray[curChar].keys())
			retDict['key']=charVar
			charVar=self.charListArray[curChar][charVar]
			export=charVar['exported']
			pmap=None
			if export == 0:
				pmap=charVar['imgData']
			else:
				pmap=self.win.curImgListBlock.itemAt(charVar['imgIndex']).widget().data
			retDict['premultiply']=charVar['premultiply']/100.0*fontScale
			mm=int(float(max(pmap.width(), pmap.height()))*retDict['premultiply'])
			retDict['resMax']=[mm,mm]
			res=[ int(float(pmap.width())*retDict['premultiply']), int(float(pmap.height())*retDict['premultiply']) ]
			pmap=pmap.scaled(res[0],res[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			retDict['res']=[pmap.width(), pmap.height()]
			retDict['data']=pmap
			retDict['baseline']=int(float(charVar['baseline'])*retDict['premultiply'])
			retDict['spacingLeft']=int(float(charVar['spacingLeft'])*retDict['premultiply'])
			retDict['spacingRight']=int(float(charVar['spacingRight'])*retDict['premultiply'])
			
			return retDict
		return None
	def saveImage(self):
		path=self.parent.pageOutputDirText.text()
		diffuse="Busted"
		if path[-1] != "/":
			path+="/"
		if not os.path.exists(path):
			buildPath="\\".join(str(path).split("/"))
			os.makedirs(buildPath)
		if self.pageFileName != "_":
			diffuse=self.pageFileName+".png"
			if self.exported == 0:
				difData=self.pageImgData
				#difData.setAlphaChannel(self.dataAlpha)
				difData.save(path+diffuse, "png")
		return path+diffuse
	def mousePressEvent(self, event):
		pos=event.globalPos()
		self.mousePressStart=[pos.x(), pos.y()]
		self.mouseDown=1
		scrollH=self.parent.pageOutputBlock.horizontalScrollBar().value()
		scrollV=self.parent.pageOutputBlock.verticalScrollBar().value()
		self.scrollStart=[scrollH, scrollV]
	def mouseMoveEvent(self, event):
		if self.mouseDown > 0:
			self.mouseDown+=1
			if self.mouseDown == 5:
				self.mouseDrag=1
			if self.mouseDrag == 1:
				pos=event.globalPos()
				curXY=[ self.mousePressStart[0]-pos.x(), self.mousePressStart[1]-pos.y() ]
				maxScrollH=self.parent.pageOutputBlock.horizontalScrollBar().maximum()
				maxScrollV=self.parent.pageOutputBlock.verticalScrollBar().maximum()
				curScrollH=min( maxScrollH, max(0, self.scrollStart[0]+curXY[0] ))
				curScrollV=min( maxScrollV, max(0, self.scrollStart[1]+curXY[1] ))
				self.parent.pageOutputBlock.horizontalScrollBar().setValue(curScrollH)
				self.parent.pageOutputBlock.verticalScrollBar().setValue(curScrollV)
	def mouseReleaseEvent(self, event):
		if self.mouseDrag==0:
			pos=event.pos()
			posX=int(pos.x()*(1.0/self.zoom))
			posY=int(pos.y()*(1.0/self.zoom))
		self.mouseDown=0
		self.mouseDrag=0
	def wheelEvent(self, event):
		val = event.delta() / abs(event.delta())
		targetZoom= self.zoom + val*.1
		self.setZoom(targetZoom)
	def setZoom(self, targetZoom=None):
		if targetZoom==None:
			targetZoom=self.zoom
		targetW=int(float(self.cWOrig)*targetZoom)
		targetH=int(float(self.cHOrig)*targetZoom)
		targetMax=max(targetW, targetH)
		if targetMax < 10000 and targetMax>0:
			self.cW=targetW
			self.cH=targetH
			self.zoom=targetZoom
			pmap=self.displayData
			pmap=QtGui.QPixmap.fromImage(pmap.toImage())
			pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			self.img.setPixmap(pmap)