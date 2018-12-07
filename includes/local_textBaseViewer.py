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
	def setDefaultScroll(self): ### Not running right now
		curScrollH=self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().maximum()
		curScrollV=self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().maximum()
		self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().setValue(curScrollH)
		self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().setValue(curScrollV)
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
								
							self.win.statusBarUpdate("( Press 'Escape' to Cancel ) -- Cross-Checking "+checkedCount+" pixels -- Pixels in Queue ... "+str(queueCount)+warning, 0, 0)
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
					self.win.statusBarUpdate(" -- Character Search Complete! --", 5000, 1)

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