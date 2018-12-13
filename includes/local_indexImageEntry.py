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
		self.outputSize=[256,256]
		
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
				rotationVal=float(self.win.sliderRotate.value())/100.0
				offset=[ int(float(self.outputSize[0]-qtImg[0].data.width())/2.0), int(float(self.outputSize[1]-qtImg[0].data.height())/2.0) ]
				
				pmap=QtGui.QPixmap(self.outputSize[0],self.outputSize[1])
				pmap.fill(QtGui.QColor(0,0,0,0))
				painter=QtGui.QPainter(pmap)
				painter.drawPixmap(offset[0],offset[1],QtGui.QPixmap.fromImage(qtImg[0].data.toImage()))
				painter.end()
				"""if rotationVal != 0:
					rotation=QtGui.QTransform().rotate(rotationVal)
					pmap=pmap.transformed(rotation, QtCore.Qt.SmoothTransformation)
				"""
				self.data=pmap
				"""
				pmap=QtGui.QPixmap(self.outputSize[0],self.outputSize[1])
				pmap.fill(QtGui.QColor(0,0,0,0))
				painter=QtGui.QPainter(pmap)
				painter.drawPixmap(offset[0],offset[1],QtGui.QPixmap.fromImage(qtImg[1].data.toImage()))
				painter.end()
				if rotationVal != 0:
					rotation=QtGui.QTransform().rotate(rotationVal)
					pmap=pmap.transformed(rotation, QtCore.Qt.SmoothTransformation)
				self.dataAlpha=pmap
				"""
				#self.data=qtImg[0].data
				qtImg=qtImg[0].data.scaled(self.imgSizeIndexList[0],self.imgSizeIndexList[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
				"""if rotationVal != 0:
					rotation=QtGui.QTransform().rotate(rotationVal)
					qtImg=qtImg.transformed(rotation, QtCore.Qt.SmoothTransformation)
				"""
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
			self.spacingRight=self.win.rightAlignSlider.value()+128
			self.degRotation=self.win.sliderRotate.value()
			self.contrast=self.win.sliderContrast.value()
			self.alphaReach=self.win.sliderAlphaReach.value()
		
			self.entryStyleSheet()
		# Child QWidgets don't set parent size, must set parent size for correct scroll bar
		self.setFixedSize(self.imgSizeIndexList[0],self.imgSizeIndexList[1]) # Layout size for Placeholder
		self.setLayout(curImgBlock) # Layout to display in parent window
	def entryStyleSheet(self):
		styleSheetCss="""
		* {font-size:10pt;}
		QToolTip {color:#ffffff;background-color:#202020;border: 1px solid #ffffff;}
		QPushButton {color:#ffffff;background-color:#232323;padding:4px;border:1px solid #000000;}
		QLineEdit {color:#111111;selection-color:#cccccc;selection-background-color:#454545;background-color:#909090;padding:2px;border:1px solid #202020;height:25px;}
		QLabel {color:#ffffff}"""
		self.setStyleSheet(styleSheetCss)
		self.img.setStyleSheet("border: 1px solid #555555; padding:3px;")
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
		self.loaded=1
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
				"%":"prc",
				"^":"up",
				"&":"and",
				"*":"str",
				"(":"opr",
				")":"cpr",
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
				".":"per",
				"...":"ell", # Ellipsis
				"-.":"dot", # Center Dot
				"-":"sub",
				"=":"equ",
				"_":"und",
				"+":"pls",
				"/":"bsl",
				"<":"lth",
				">":"gth",
				"?":"qus",
				"\\":"fsl",
				"`":"ftk",
				"b`":"btk",
				"~":"tld",
				"0":"zero",
				"1":"one",
				"2":"two",
				"3":"three",
				"4":"four",
				"5":"five",
				"6":"six",
				"7":"seven",
				"8":"eight",
				"9":"nine",
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
			self.win.unsavedChanges=1
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
				"""
				difData.setAlphaChannel(self.dataAlpha)
				res=[difData.width(), difData.height()]
				offset= [ int(float(self.outputSize[0]-res[0])/2.0), int(float(self.outputSize[1]-res[1])/2.0) ]
				
				baseImg=QtGui.QPixmap( self.outputSize[0], self.outputSize[1] )
				baseImg.fill(QtGui.QColor(0,0,0,0))
				painter=QtGui.QPainter(baseImg)
				painter.setCompositionMode(painter.CompositionMode_SourceOver)
				painter.drawPixmap(offset[0], offset[1], difData)
				painter.end()
				difData=baseImg
				"""
				
				difData.save(path+diffuse, "png")
		return path+diffuse
	def loadFromTextBase(self):
		curTextBasePath=self.textBaseFile
		curTextBaseFile=curTextBasePath.split("/")[-1]
		if curTextBaseFile not in self.imgData.keys():
			print "Loading - "+curTextBaseFile
			print "Not active yet, MAKE IT WORK"
			print "Load image connected to entry, update textBase, scan image"
			#pmap=QtGui.QPixmap()
			#pmap.load(self.imgPath)
			#self.imgData[self.curImage]=pmap
		else:
			print "Found textBase image"
	def mouseReleaseEvent(self, e):
		if self.imgName == "thumb":
			"""if self.exported==0:
				difData=curChar.data
				difData.setAlphaChannel(curChar.dataAlpha)
				charListData[char][title]['imgData']=difData
			"""
			#self.charSamplePoints=self.win.charSamplePoints
			self.win.runValChangeEvent=0
			self.win.sliderBaseLine.setValue(self.baseline)
			self.win.sliderPreMult.setValue(self.premultiply)
			self.win.sliderTopPadding.setValue(self.paddingTop)
			self.win.sliderBottomPadding.setValue(self.paddingBottom)
			self.win.leftAlignSlider.setValue(self.spacingLeft)
			self.win.rightAlignSlider.setValue(self.spacingRight-128)
			self.win.sliderRotate.setValue(self.degRotation)
			self.win.sliderContrast.setValue(self.contrast)
			self.win.sliderAlphaReach.setValue(self.alphaReach)
			self.win.runValChangeEvent=1
			
			self.win.curImageFinalDisplay.thumbIndex=-1
			self.win.charSampled=1
			self.win.curImageFinalDisplay.pullCharacterRect(self)
		else:
			self.win.loadImageEntry(self)