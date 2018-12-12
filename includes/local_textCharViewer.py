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
		self.res=[256,256]
		
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
			rotationVal=float(self.win.sliderRotate.value())/100.0
			if type(scaleMode) is not int or self.thumbIndex>-1:
				if self.thumbIndex>-1:
					scaleMode=self.win.curImgListBlock.itemAt(self.thumbIndex).widget()
					pmap=QtGui.QPixmap.fromImage(scaleMode.data.toImage())
				else:
					self.thumbIndex=scaleMode.index
					pmap=None
					"""
					if scaleMode.exported==0:
						pmap=QtGui.QPixmap.fromImage(scaleMode.data.toImage())
						pmap.setAlphaChannel(scaleMode.dataAlpha)
					else:
						pmap=QtGui.QPixmap.fromImage(scaleMode.data.toImage())
					"""
					pmap=QtGui.QPixmap.fromImage(scaleMode.data.toImage())
			else:
				pmap=self.win.curImageDisplay.data
				pmap=QtGui.QPixmap.fromImage(pmap.toImage())
				if rotationVal != 0:
					rotation=QtGui.QTransform().rotate(rotationVal)
					pmap=pmap.transformed(rotation, QtCore.Qt.SmoothTransformation)
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
				if rotationVal != 0:
					rotation=QtGui.QTransform().rotate(rotationVal)
					pmapAlpha=pmapAlpha.transformed(rotation, QtCore.Qt.SmoothTransformation)
				if topPadVal!=0 or bottomPadVal!=0:
					baseImg=QtGui.QPixmap( pmapAlpha.width(), max(1, pmapAlpha.height()+topPadVal-bottomPadVal) )
					baseImg.fill(QtGui.QColor(0,0,0,255))
					painter=QtGui.QPainter(baseImg)
					painter.setCompositionMode(painter.CompositionMode_SourceOver)
					painter.drawPixmap(0,topPadVal,pmapAlpha)
					painter.end()
					pmapAlpha=baseImg
					
				pmap.setAlphaChannel(pmapAlpha)
			self.data=pmap.scaled(self.res[0], self.res[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
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
				if self.win.textBaseViewWindow.extendShrinkEdge == 1:
					for xy in self.win.textBaseViewWindow.reachPixels:
						x=xy[0]-rect[0]
						y=xy[1]-rect[1]
						img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
					for xy in self.win.textBaseViewWindow.edgePixels:
						x=xy[0]-rect[0]
						y=xy[1]-rect[1]
						img.setPixel(x,y,QtGui.QColor(0,0,255,255).rgb())
				elif self.win.textBaseViewWindow.extendShrinkEdge == 0:
					reachPixels=[]
					reachPixels.extend(self.win.textBaseViewWindow.reachPixels)
					edgePixels=self.win.textBaseViewWindow.edgePixels
					for e in edgePixels:
						if e in reachPixels:
							reachPixels.remove(e)
					for xy in self.win.textBaseViewWindow.reachPixels:
						x=xy[0]-rect[0]
						y=xy[1]-rect[1]
						img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
				else:
					for xy in self.win.textBaseViewWindow.reachPixels:
						x=xy[0]-rect[0]
						y=xy[1]-rect[1]
						img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
				pmap=QtGui.QPixmap.fromImage(img)
			elif self.mode == 2:
				reachPixels=[]
				reachPixels.extend(self.win.textBaseViewWindow.reachPixels)
				if self.win.textBaseViewWindow.extendShrinkEdge == 1:
					reachPixels.extend(self.win.textBaseViewWindow.edgePixels)
				elif self.win.textBaseViewWindow.extendShrinkEdge == 0:
					edgePixels=self.win.textBaseViewWindow.edgePixels
					for e in edgePixels:
						if e in reachPixels:
							reachPixels.remove(e)
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