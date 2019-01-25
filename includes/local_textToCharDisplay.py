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
			else:
				return None
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
					tags=["ocl","ocr","oll","olr","osl","osr","oal","oar","str"]
					curTag=''
					missingChars=[]
					keepPrinting=1
					for x,c in enumerate(val):
						self.runner+=1.0
						if c=="%":
							if inTag==1:
								inTag=2
								skip=0
							else:
								curTag=''
								for v in range(1,maxTagLength):
									if x+v<len(val):
										curTag+=val[x+v]
										if curTag.lower() in tags:
											curTag=curTag.lower()
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
		self.loadingData=0
		
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
		self.fontKerning=SliderGroup(self,"Font Kerning",[-50,50,0],7,"int",' px', "buildTextOutput(0)")
		self.charTestOptionBlock.addWidget(self.fontKerning)
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
		
		self.pageFlipOutput=QtGui.QCheckBox()
		self.pageFlipOutput.setText("Flip Text Output Horizontally")
		self.pageFlipOutput.stateChanged.connect(self.setFlipOutput)
		self.charTestOptionBlock.addWidget(self.pageFlipOutput)
		
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
		
		newEntryButtonBlock=QtGui.QHBoxLayout()
		newEntryButtonBlock.setSpacing(0)
		newEntryButtonBlock.setMargin(0) 
		###
		emptyNewPage=QtGui.QPushButton('New Empty Page Entry', self)
		emptyNewPage.setFixedHeight(50)
		emptyNewPage.setStyleSheet(self.win.buttonStyle)
		emptyNewPage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		emptyNewPage.setStyleSheet("QPushButton {margin-top:5px;}")
		emptyNewPage.clicked.connect(lambda: self.addPageIndex(1))
		newEntryButtonBlock.addWidget(emptyNewPage)
		###
		buildToNewPage=QtGui.QPushButton('Set as New Page Entry', self)
		buildToNewPage.setFixedHeight(50)
		buildToNewPage.setStyleSheet(self.win.buttonStyle)
		buildToNewPage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		buildToNewPage.setStyleSheet("QPushButton {margin-top:5px;}")
		buildToNewPage.clicked.connect(lambda: self.addPageIndex(0))
		newEntryButtonBlock.addWidget(buildToNewPage)
		###
		self.charTestOptionBlock.addLayout(newEntryButtonBlock)
		
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
	def setFlipOutput(self):
		if self.autoUpdate == True:
			self.buildTextOutput()
	def setAutoReload(self):
		val=self.pageAutoUpdate.isChecked()
		self.autoUpdate=val
		if val==True:
			self.buildTextOutput()
	def buildTextOutput(self, force=1):
		runUpdate=1
		if force==0:
			if self.autoUpdate == False:
				runUpdate=0
		if runUpdate==1 and self.editPrep==False:
			self.pageOutput.buildTextDisplay()
	def loadPageBackground(self,checkLocal=0):
		bgPicker=''
		if checkLocal == 1:
			path=bundleDir+"/pageOutput_pageBackground.png"
			if os.path.exists(path):
				bgPicker=path
			else:
				return None
		if bgPicker=='':
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
				
				self.loadingData=1
				self.pageFileLocation.setText(bgPicker)
				self.pageOutput.loadPageBackground(bgPicker)
				self.buildTextOutput()
				self.loadingData=0
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
			#if self.editPrep==False:
			if thumbIndex==None:
				thumbIndex=self.curPage
			curThumb=None
			if thumbIndex>=self.curPageListBlock.count():
				curThumb=IndexPageEntry(self.win, self, self.curPage, self.pageData[thumbIndex]['pageGroupName'], self.imgPath, [152,152], "H", [self.pageOutput.pageImgData], self.pageData[thumbIndex])
				self.curPageListBlock.addWidget(curThumb)
				if self.loadingData==0:
					curThumb.nameFocus()
			else:
				curThumb=self.curPageListBlock.itemAt(self.curPage).widget()
				curThumb.pageData=self.pageData[self.curPage] # I don't like this method.....
			curThumb.updatePageThumb(self.pageOutput.groupPage,self.pageOutput.pageImgData)
	def addPageIndex(self, resetSettings=0):
		if resetSettings==1:
			self.resetSettings()
		self.pageOutput.buildTextDisplay(1)
		#self.editGroup(1,pageGroup)
	def resetSettings(self):
		self.editPrep=True
		###
		self.inputText.setPlainText('')
		###
		self.pageIndentLeft.resetValue()
		self.pageIndentTop.resetValue()
		self.pageIndentRight.resetValue()
		self.pageIndentBottom.resetValue()
		self.fontScale.resetValue()
		self.spaceSize.resetValue()
		self.lineHeight.resetValue()
		self.lineIndent.resetValue()
		self.charSeed.resetValue()
		###
		self.editPrep=False
	def editGroup(self,mode,groupData):
		self.editPrep=True
		pageDataArray=[]
		if mode==0: # Edit Existing Group
			self.curPage=groupData.group
			pageDataArray=groupData.pageData
			if not hasattr(groupData,"data") or groupData.data==None:
				self.pageOutput.buildTextDisplay()
			self.pageOutput.img.setPixmap(groupData.data[0])
		else:
			pageDataArray=groupData
		pageDataKeysArray=pageDataArray.keys()
		#self.parent.pageData[self.group]=[]
		for k in pageDataKeysArray:
			if k not in ["lineData", "pageFlip", "pageGroupName"]:
				if k == "inputText": # Might need to change this to 'in []'
					eval('self.'+k+'.setPlainText(r"""'+str(pageDataArray[k])+'""")')
				elif k == "pageFlipOutput": # Might need to change this to 'in []'
					checkState=pageDataArray[k]
					if checkState==True:
						checkState="QtCore.Qt.Checked"
					else:
						checkState="QtCore.Qt.Unchecked"
					eval("self."+k+".setCheckState("+checkState+")")
				else:
					eval("self."+k+".setValue(str("+str(pageDataArray[k])+"))")
		self.editPrep=False
		if mode!=-1:
			self.pageOutput.buildTextDisplay()
	def rebuildPageGroupIds(self):
		pageGroupCount=self.curPageListBlock.count()
		for x in range(pageGroupCount):
			curThumb=self.curPageListBlock.itemAt(x).widget()
			curThumb.setGroupId(x)
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
				self.saveImages()
				self.win.statusBarUpdate(" -- Wrote out data to - '"+delimit+self.win.projectName+delimit+"pageListKey.py'; Pages exported to - '"+imgPath+"' --", 10000,1)
			self.win.unsavedChanges=0
		else:
			self.win.statusBarUpdate(" -- No characters found, please 'Load Text Image' to load existing character data -- ", 5000,2)
			
	def saveImages(self):
		path=self.pageOutputDirText.text()
		diffuse="Busted"
		if path[-1] != "/":
			path+="/"
		if not os.path.exists(path):
			buildPath="\\".join(str(path).split("/"))
			os.makedirs(buildPath)
		pageGroupCount=self.curPageListBlock.count()
		for x in range(pageGroupCount):
			self.win.statusBarUpdate(" -- Exporting page group "+str(x+1)+" of "+str(pageGroupCount)+" --", 0,0)
			curPageGroup=self.curPageListBlock.itemAt(x).widget()
			curPagesCount=curPageGroup.pageListBlock.count()
			for c in range(curPagesCount):
				curThumb=curPageGroup.pageListBlock.itemAt(c).widget()
				if curPagesCount==1:
					diffuse=curPageGroup.pageName+".png"
				else:
					diffuse=curPageGroup.pageName+"_"+str(c)+".png"
				difData=curThumb.data
				difData.save(path+diffuse, "png")
	def loadPageDataFile(self, displayError=1):
		path=self.win.dirField.text()
		if path == "":
			if displayError==1:
				self.win.statusBarUpdate(" -- No Page Output directory set; make sure your project is loaded or set an output directory -- ", 5000,2)
		else:
			if path[-1] != "/":
				path+="/"
			path="\\".join(str(path).split("/"))
			path+="pageListKey.py"
			if os.path.exists(path):
				if displayError==1:
					self.win.statusBarUpdate(" -- Reading and building pages from local PageListKey file --", 0,0)
				
				sys.path.append(self.win.projectName)
				import pageListKey
				reload(pageListKey)
				
				if len(pageListKey.pageList)>0:
					curPageEntries=self.curPageListBlock.count()
					for x in range(curPageEntries):
						curEntry=self.curPageListBlock.itemAt(curPageEntries-1-x).widget()
						curEntry.deleteGroup()
					self.curPage=0
					self.pageData=[]
					self.loadingData=1
					self.resetSettings()
					for x in range(len(pageListKey.pageList)):
						pageGroup=pageListKey.pageList[x]
						self.editGroup(-1,pageGroup)
						self.pageOutput.buildTextDisplay(1,pageGroup["pageGroupName"])
					self.loadingData=0
					curThumb=self.curPageListBlock.itemAt(0).widget()
					curThumb.editGroup()
			else:
				if displayError==1:
					self.win.statusBarUpdate(" -- No exported data found '"+self.win.projectName+delimit+	"pageListKey.py'; please export a page first. -- ", 5000,2)
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
		self.baseLine=75.0
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

			pageFlipOutput=self.parent.pageFlipOutput.isChecked()
			textBuild=self.textBuildData.copy()
			if pageFlipOutput==True:
				textBuild=textBuild.transformed(QtGui.QTransform().scale(-1,1))
			painter=QtGui.QPainter(pmap)
			painter.setCompositionMode(painter.CompositionMode_SourceOver)
			painter.drawPixmap(0,0,textBuild)
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
	def buildTextDisplay(self, newPage=0, pageGroupName=None):
		val=self.inputText()
		#if val != self.pastTest or force==1:
		textUpdated=0
		if val != self.pastTest:
			textUpdated=1
		self.pastTest=val
		res=[self.cWOrig, self.cHOrig]
		
		charOffsets=[0.0,0.0]
		prevCharOffsets=[0.0,0.0]
		
		if hasattr(self.win, "curImgListBlock"):
			if self.win.curImgListBlock.count() == 0:
				self.win.statusBarUpdate(" -- No character data found, please create characters first -- ", 5000,2)
				return
		else:
			self.win.statusBarUpdate(" -- Please 'Load Text Image' to load existing character data -- ", 5000,2)
			return
		dir=str(self.win.dirField.text()).strip()
		#if dir != '':
		#if val != '':
		curPageData={}
		curLineData=[]
		pageFlip=0
		#if textUpdated == 1:
		self.buildCharListArray()
		
		fontScale=self.parent.fontScale.value
		fontKerning=float(self.parent.fontKerning.value)
		spaceSize=float(self.parent.spaceSize.value)
		lineHeight=float(self.parent.lineHeight.value)
		lineIndent=self.parent.lineIndent.value
		###
		charSeed=self.parent.charSeed.value
		self.seed=charSeed
		###
		padLeft=self.parent.pageIndentLeft.value
		padRight=self.parent.pageIndentRight.value
		padTop=self.parent.pageIndentTop.value
		padBottom=self.parent.pageIndentBottom.value
		###
		pageFlipOutput=self.parent.pageFlipOutput.isChecked()
		
		curPageData={}
		curPageData['inputText']=val
		curPageData['pageFlip']=pageFlip
		curPageData['fontScale']=fontScale
		curPageData['spaceSize']=spaceSize
		curPageData['fontKerning']=fontKerning
		curPageData['lineHeight']=lineHeight
		curPageData['lineIndent']=lineIndent
		curPageData['charSeed']=charSeed
		curPageData['pageIndentLeft']=padLeft
		curPageData['pageIndentRight']=padRight
		curPageData['pageIndentTop']=padTop
		curPageData['pageIndentBottom']=padBottom
		curPageData['pageFlipOutput']=pageFlipOutput
		curPageGroupName="Page"
		grabName=1
		if pageGroupName!=None:
			pageGroupName=pageGroupName.strip()
			if pageGroupName!='':
				curPageGroupName=pageGroupName
				grabName=0
		if len(self.parent.pageData)>0 and self.parent.curPage <= len(self.parent.pageData):
			if newPage==0 and grabName==1:
				curPageGroupName=self.parent.pageData[self.parent.curPage]['pageGroupName']
		curPageData['pageGroupName']=curPageGroupName
		
		curLineData=[]
		self.runner=0
		val=list(val)
		backChars=["'",'"',"`"]
		skip=0
		inTag=0
		maxTagLength=10
		specialChars=["ocl","ocr","oll","olr","osl","osr","oal","oar","str"]
		textTags=["align","a", "offset","o", "rotate", "kern","k", "spacesize","ss", "lineheight","lh", "seed","s", "opacity","op"]
		tags=[]
		tags+=specialChars
		tags+=textTags
		maxTagLength=len(max(tags, key=len))+2
		checkTagLength=maxTagLength
		curTag=''
		curSingleCharTags=[]
		curSingleLineTags=[]
		fontTag=0
		curTagPerc=1.0
		curTagAlign="left"
		curTagOffset=[0.0,0.0]
		curTagRotate=0.0
		curTagSeed=0.0
		curTagSpaceSize=0.0
		curTagKerning=0.0
		curTagLineHeight=0.0
		curTagOpacity=100.0
		curTagSingleChar=0
		curTagSingleLine=0
		
		paintLine=0
		genNewLine=1
		fontScaleLine=fontScale
		fontScaleChar=fontScale
		continueRun=-1
		for x,c in enumerate(val):
			if x >= continueRun:
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
					newLineData['lineWidth']=-1
					newLineData['fontKerning']=fontKerning

					newLineData['align']=curTagAlign
					curLineData.append(newLineData)
					genNewLine=0
					fontScale=self.parent.fontScale.value
				
				if c=="%":
					if inTag==1:
						inTag=2
						skip=0
					else:
						curTag=''
						setBreak=0
						fontTagBuild=0
						tagReset=0
						for v in range(1,maxTagLength): # Gotta clean this up
							if x+v<len(val):
								if val[x+v] in ["%", "\n"]:
									if val[x+v]=="\n":
										setBreak=1
										fontTag=0
										break;
									if curTag not in tags and fontTag==0:
										setBreak=1
										break;
									if fontTag==2:
										if curTag in textTags:
											tagReset=1
										else:
											fontTag=0
									continueRun=x+v
									break;
								else:
									tagCurChar=val[x+v].lower()
									if curTag=='':
										if tagCurChar.isdigit() == True or tagCurChar==".":
											fontTag=1
									if fontTag==2:
										if tagCurChar == ":":
											fontTagBuild=v+1
											break;
										if (curTag+tagCurChar) not in textTags:
											fontTag=0
									curTag+=tagCurChar
									if fontTag==0:
										if curTag in tags:
											inTag=1
										if curTag in textTags:
											fontTag=2
									elif (fontTag==1 and (tagCurChar.isdigit()==True or tagCurChar==".")):
										inTag=1
									elif fontTag==2:
										continue;
									else:
										inTag=0
										setBreak=1
										break;
							else:
								break;
						curFontMod=''
						if fontTagBuild>0 and setBreak==0:
							for v in range(fontTagBuild,fontTagBuild+maxTagLength): # Gotta clean this up
								if x+v<len(val):
									if val[x+v] in ["%", "\n"]:
										if val[x+v]=="\n":
											setBreak=1
											break;
										continueRun=x+v
										break;
									tagCurChar=val[x+v].lower()
									curFontMod+=tagCurChar
							if curFontMod == '':
								tagReset=1
						checkTagLength=maxTagLength
						if setBreak==0:
							if fontTag==1: # Percent scale font
								curTagPerc=float(curTag)
								if "." not in curTag:
									curTagPerc=curTagPerc/100.0
							elif fontTag==2: # Text modifying tag
								failCheck=map(lambda x: x.isdigit() or x in ['.', ',', '-', ' '], list(curFontMod))
								if curTag not in ["align","a"] and False in failCheck:
									curTag=''
									setBreak=1
								if curTag in ["align","a"]:
									if curTag=='a':
										curTag='align'
										curSingleLineTags.append(curTag)
										curTagSingleLine=1
									if tagReset==1:
										curTagAlign="left"
									else:
										if curFontMod in ['left','center','right']:
											curTagAlign=curFontMod
											curLineData[-1]['align']=curTagAlign
										else:
											setBreak=1
								elif curTag in ["offset","o"]:
									if curTag=='o':
										curTag='offset'
										curSingleCharTags.append(curTag)
										curTagSingleChar=1
									if tagReset==1:
										curTagOffset=[0.0,0.0]
									else:
										buildOffset=[0.0,0.0]
										xyOffsets=0
										if "," in curFontMod:
											if " " in curFontMod:
												curFontMod="".join(curFontMod.split(" "))
											curFontMod=curFontMod.split(",")
										elif " " in curFontMod:
											curFontMod=curFontMod.split(" ")
										else:
											curFontMod=[curFontMod]
										curFontMod=filter(None, curFontMod)
										if len(curFontMod)>2:
											setBreak=1
										else:
											if len(curFontMod)==1:
												buildOffset[1]=float(curFontMod[0])
											else:
												for o in range(len(curFontMod)):
													buildOffset[o]=float(curFontMod[o])
											curTagOffset=[]
											curTagOffset+=buildOffset
								elif curTag in ["kern","k"]:
									if curTag=='k':
										curTag='kern'
										curSingleCharTags.append(curTag)
										curTagSingleChar=1
									if tagReset==1:
										curTagKerning=0.0
									else:
										curTagKerning=float(curFontMod)
								elif curTag=="rotate":
									if tagReset==1:
										curTagRotate=0.0
									else:
										curTagRotate=float(curFontMod)
								elif curTag in ["spacesize","ss"]:
									if curTag=='ss':
										curTag='spacesize'
										curSingleLineTags.append(curTag)
										curTagSingleLine=1
									if tagReset==1:
										curTagSpaceSize=0.0
									else:
										curTagSpaceSize=float(curFontMod)
								elif curTag in ["lineheight","lh"]:
									if curTag=='lh':
										curTag='lineheight'
										curSingleLineTags.append(curTag)
										curTagSingleLine=1
									if tagReset==1:
										curTagLineHeight=0.0
									else:
										curTagLineHeight=float(curFontMod)
										charOffsets[1]=prevCharOffsets[1]+lineHeight+curTagLineHeight
								elif curTag in ["seed","s"]:
									if curTag=='s':
										curTag='seed'
										curSingleCharTags.append(curTag)
										curTagSingleChar=1
										if curFontMod=='':
											tagReset=0
											random.seed(self.runner)
											curFontMod=random.random()
											random.seed(self.runner+curFontMod)
											curFontMod=random.random()
									if tagReset==1:
										curTagSeed=0.0
									else:
										curTagSeed=float(curFontMod)
								elif curTag in ["opacity","op"]:
									if curTag=='op':
										curTag='opacity'
										curSingleCharTags.append(curTag)
										curTagSingleChar=1
									if tagReset==1:
										curTagOpacity=100.0
									else:
										curTagOpacity=float(curFontMod)
								else:
									setBreak=1
								if setBreak==0:
									cc=''
									inTag=0
									continueRun+=1
									continue;
									#inTag=1
						if setBreak==1:
							curTag=''
							curFontMod=''
							inTag=0
							if fontTag>0: # To support broken tags inside altered scales
								fontTag=0
						if inTag==0:
							cc=c
				if inTag==1:
					skip=1
				elif inTag==0:
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
					if inTag==2:
						inTag=0
						if fontTag==0:
							cc=curTag
							curTag=''
					if cc == " ":
						#leftStart=leftStart+spaceSize
						charOffsets[0]=charOffsets[0]+spaceSize+curTagSpaceSize
						newWord={}
						newWord['size']=[0,0]
						newWord['chars']=[]
						newWord['fontScale']=1.0
						curLineData[-1]['wordData'].append(newWord)
					elif cc=="\n":
						inTag=0
						curLineData[-1]['lineWidth']=charOffsets[0]
						prevCharOffsets=[]
						prevCharOffsets.extend(charOffsets)
						genNewLine=1
						if curTagSingleLine==1:
							curTagSingleLine=0
							for tag in curSingleLineTags:
								if tag=="align":
									curTagAlign="left"
								if tag=="lineheight":
									curTagLineHeight=0.0
								if tag=="spacesize":
									curTagSpaceSize=0.0
							curSingleLineTags=[]
						charOffsets=[0,charOffsets[1]+lineHeight+curTagLineHeight]
					else:
						charData=self.pullCharData(cc, fontScaleChar*curTagPerc, charSeed+curTagSeed)
						if charData != None:
							self.runner+=1.0
							curOffset=[ charOffsets[0]-charData['spacingLeft']+curTagOffset[0]+fontKerning+curTagKerning,charOffsets[1]-charData['baseline']+curTagOffset[1]+self.baseLine ]
							charData['offset']=curOffset
							charOffsets[0]=charOffsets[0]-charData['spacingLeft']+charData['spacingRight']+fontKerning+curTagKerning

							charData['charScale']=curTagPerc
							charData['charOffset']=curTagOffset
							charData['rotate']=curTagRotate
							charData['opacity']=curTagOpacity
							
							curLineData[-1]['wordData'][-1]['chars'].append(charData)
					
					if curTagSingleChar==1:
						curTagSingleChar=0
						for tag in curSingleCharTags:
							if tag=="offset":
								curTagOffset=[0.0,0.0]
							if tag=="kern":
								curTagKerning=0.0
							if tag=="seed":
								curTagSeed=0.0
							if tag=="opacity":
								curTagOpacity=100.0
						curSingleCharTags=[]
				else:
					skip+=1
				fontTag=0
		curPageData['lineData']=curLineData
		if newPage==1:
			self.parent.curPage=len(self.parent.pageData)
			self.parent.pageData.append(curPageData)
		else:
			if self.parent.curPage>=len(self.parent.pageData):
				self.parent.pageData.append(curPageData)
			else:
				self.parent.pageData[self.parent.curPage]=curPageData

		baseImg=QtGui.QPixmap(res[0], res[1])
		baseImg.fill(QtGui.QColor(0,0,0,0))
		painter=QtGui.QPainter(baseImg)
		painter.setRenderHint(QtGui.QPainter.Antialiasing,True)
		painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform,True)
		lineWidth=0
		lineOffset=[0,0]
		lineAlign='left'
		
		
		padLeftBuild=padLeft
		padRightBuild=padRight
		padLeft=curPageData['pageIndentLeft']
		padRight=curPageData['pageIndentRight']
		padTop=curPageData['pageIndentTop']
		padBottom=curPageData['pageIndentBottom']
		padLeftBuild=padLeft
		padRightBuild=padRight
		if pageFlipOutput==True:
			padTemp=padLeftBuild
			padLeftBuild=res[0]-padRightBuild
			padRightBuild=res[0]-padTemp
		pageSize=[padRightBuild-padLeftBuild, padBottom-padTop]
		for line in curLineData:
			lineWidth=line['lineWidth']
			lineAlign=line['align']
			deltaX=0
			deltaY=0
			if lineAlign=='center':
				deltaX=(pageSize[0]-lineWidth)/2
				lineOffset=[0,0]
			elif lineAlign=='right':
				deltaX=(pageSize[0]-lineWidth)
			lineOffset=[deltaX,deltaY]
			for word in line['wordData']:
				for char in word['chars']:
					pmap=char['data']
					curOffset=[0,0]
					curOffset[0]=char['offset'][0]+lineOffset[0]
					curOffset[1]=char['offset'][1]+lineOffset[1]
					if char['opacity']!=100.0:
						painter.setOpacity(char['opacity']/100.0)
					painter.drawPixmap(curOffset[0]+padLeftBuild,curOffset[1]+padTop,pmap)
					if char['opacity']!=100.0:
						painter.setOpacity(1.0)
		painter.end()
		self.textBuildData=baseImg
		
		#else:
		#	self.textBuildData=None
		self.updateTextBackground()
	def pullCharData(self,curChar, fontScale, curSeed):
		curChar=str(curChar)
		charKeys=self.charListArray.keys()
		if curChar in charKeys:
			retDict={}
			retDict['char']=curChar
			random.seed( self.runner + curSeed )
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
			pmap=pmap.scaled(res[0],res[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			retDict['res']=[pmap.width(), pmap.height()]
			retDict['data']=pmap
			retDict['baseline']=(float(charVar['baseline'])*retDict['premultiply'])
			retDict['spacingLeft']=(float(charVar['spacingLeft'])*retDict['premultiply'])
			retDict['spacingRight']=(float(charVar['spacingRight'])*retDict['premultiply'])
			
			return retDict
		return None
	def saveImages(self):
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