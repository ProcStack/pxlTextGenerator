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
		self.zoomPrevWorking=1.0
		self.zoomRate=.15
		self.zoomMax=-1
		self.imgName=entryObj.imgName
		self.imgPath=entryObj.imgPath
		self.img=QtGui.QLabel()
		self.img.setAlignment(QtCore.Qt.AlignCenter)
		self.img.setGeometry(0,0,self.cW,self.cH) # Placeholder
		
		self.curCanvasData=None
		self.curCanvasPreWorkAreaData=None
		self.workAreaData=None
		self.scanRange=[self.cW,self.cH,0,0]
		self.workingRectArea=[self.cW,self.cH,0,0]
		self.initWorkingRectArea=[self.cW,self.cH,0,0]
		self.workAreaActive=0
		self.workAreaCrop=0 # Maybe I should just leave this on the main window
		self.rect=[0,0,256,256]
		self.reachPixelsBase=[]
		self.reachPixels=[]
		self.edgePixelsBase=[]
		self.edgePixels=[]
		self.customPixels={}
		self.customPixels['add']=[]
		self.customPixels['rem']=[]
		self.customPixels['temp']=[]
		self.extendShrinkEdge=-1
		self.prevXY=[0,0]
		self.mouseDown=0
		self.mousePressStart=[]
		self.scrollStart=[]
		self.mouseDrag=0
		self.brushSize=-1
		self.brushPixelData=[]
		self.brushEdgePixelData=[]
		self.curButton=-1
		self.updateEdges=0
		
		self.curImgBlock=QtGui.QVBoxLayout()
		self.curImgBlock.setSpacing(0) # Spacing & Margin was giving me trouble calculating dynamic loading in window
		self.curImgBlock.setMargin(0) # ||
		
		pmap=QtGui.QPixmap()
		pmap.load(self.imgPath)
		self.win.imgData[self.win.curImage]=pmap
		self.img.setPixmap(pmap)
		self.curCanvasData=pmap
		self.curImgBlock.addWidget(self.img)
		
		#self.setMouseTracking(True)
		self.setLayout(self.curImgBlock) # Layout to display in parent window
		#self.setMouseMoveEventDelegate(self)
		#self.setMouseMoveEventDelegate(self.img)
		self.img.setMouseTracking(True)
		self.img.mouseMoveEvent=self.mouseMoveEvent

	def workAreaCropVis(self, workAreaVis=None, rebuild=0):
		if workAreaVis == None:
			workAreaVis=self.workAreaCrop
		else:
			self.workAreaCrop=workAreaVis
		if workAreaVis == 1 or rebuild==1:
			curWA=self.workingRectArea
			if curWA[0] < curWA[2]:
				img=self.win.imgData[self.win.curImage]
				img=img.copy(curWA[0],curWA[1], (curWA[2]-curWA[0]),(curWA[3]-curWA[1]))
				offset=[curWA[0],curWA[1],[1,1,curWA[2]-curWA[0],curWA[3]-curWA[1]]]
				img=img.toImage()
				self.workAreaData=QtGui.QPixmap.fromImage(img)
				self.img.setPixmap(self.workAreaData)
				"""if workAreaActive==1:
					textBaseViewSize=[]
					textBaseViewSize.append(float(self.parent().parent().width()-25))
					textBaseViewSize.append(float(self.parent().parent().height()-25))
					displaySize=[float(midRun.width()), float(midRun.height())]
					
					ratio=textBaseViewSize[0]/displaySize[0]
					xScale=[displaySize[0]*ratio, displaySize[1]*ratio]
					ratio=textBaseViewSize[1]/displaySize[1]
					yScale=[displaySize[0]*ratio, displaySize[1]*ratio]
					if xScale[0]>textBaseViewSize[0] or xScale[1]>textBaseViewSize[1]:
						displaySize=yScale
					else:
						displaySize=xScale
					displaySize=[int(displaySize[0]*(1.0/self.zoom)), int(displaySize[1]*(1.0/self.zoom))]
				"""
		if rebuild==0:
			self.drawReachMask()
	def workAreaActiveToggle(self,workAreaActive=None):
		if workAreaActive == None:
			workAreaActive=self.workAreaActive
		else:
			self.workAreaActive=workAreaActive
		if self.workAreaActive==0:
			self.workingRectArea=[self.cW,self.cH,0,0]
			self.initWorkingRectArea=[self.cW,self.cH,0,0]
		self.setZoom(self.zoom-self.zoomRate)
		self.setZoom(self.zoom+self.zoomRate)
	def resetScanRange(self):
		pmap=QtGui.QPixmap()
		pmap.load(self.imgPath)
		self.img.setPixmap(pmap)
		self.curCanvasData=pmap
		self.scanRange=[self.cW,self.cH,0,0]
		resetWorkArea=self.win.resetWorkAreaToggle.isChecked()
		if resetWorkArea==1:
			self.workingRectArea=[self.cW,self.cH,0,0]
		self.reachPixelsBase=[]
		self.reachPixels=[]
		self.edgePixelsBase=[]
		self.edgePixels=[]
		self.customPixels={}
		self.customPixels['add']=[]
		self.customPixels['rem']=[]
		self.customPixels['temp']=[]
		
		self.updateEdges=0
		self.setZoom(self.win.zoom)
	def mousePressEvent(self, event):
		pos=event.globalPos()
		self.mousePressStart=[pos.x(), pos.y()]
		self.mouseDown=1
		self.curButton=event.buttons()
		if self.win.textBaseToolMode==4:
			self.initWorkingRectArea=[-1,-1]
			self.workingRectArea=[self.cW,self.cH,0,0]
			self.workAreaActive=1
			self.win.workAreaCrop=0
		scrollH=self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().value()
		scrollV=self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().value()
		self.scrollStart=[scrollH, scrollV]
	def mouseMoveEvent(self, event):
		self.curButton=event.buttons()
		if self.curButton == QtCore.Qt.NoButton:
			if self.win.textBaseToolMode in [1,2]: # Add / Remove Brushes
				pos=event.pos()
				posX=pos.x()
				posY=pos.y()
				self.drawBrushRadius(self.win.textBaseToolMode, [posX,posY])
		elif self.curButton == QtCore.Qt.LeftButton:
			if self.win.textBaseToolMode in [1,2]: # Add / Remove Brushes
				pos=event.pos()
				posX=pos.x()
				posY=pos.y()
				self.setCustomPixels( self.win.textBaseToolMode, [posX,posY], self.win.brushSizeSlider.value )
			elif self.win.textBaseToolMode==3 and self.win.selectColorMode>0: # Sample Color
				pos=event.pos()
				#posX=int(pos.x()*(1.0/self.zoom))
				#posY=int(pos.y()*(1.0/self.zoom))
				posX=pos.x()
				posY=pos.y()
				if self.workAreaCrop==1:
					origRes=[self.workingRectArea[2]-self.workingRectArea[0], self.workingRectArea[3]-self.workingRectArea[1]]
					posX=int((float(posX)/float(self.img.pixmap().width()))*float(origRes[0]))+self.workingRectArea[0]
					posY=int((float(posY)/float(self.img.pixmap().height()))*float(origRes[1]))+self.workingRectArea[1]
				else:
					posX=int(posX*(1.0/self.zoom))
					posY=int(posY*(1.0/self.zoom))

				self.win.setNewThresholdColor([posX,posY])
				self.win.selectColorMode+=1
			elif self.win.textBaseToolMode==4: # Set Working Bounding Box
				pos=event.pos()
				posX=int(pos.x()*(1.0/self.zoom))
				posY=int(pos.y()*(1.0/self.zoom))
				if self.initWorkingRectArea[0] == -1:
					self.initWorkingRectArea=[posX,posY]
				self.workingRectArea[0]=max(1, min(self.initWorkingRectArea[0], posX) )
				self.workingRectArea[1]=max(1, min(self.initWorkingRectArea[1], posY) )
				self.workingRectArea[2]=min(self.cWOrig-1, max(self.initWorkingRectArea[0], posX) )
				self.workingRectArea[3]=min(self.cHOrig-1, max(self.initWorkingRectArea[1], posY) )
				self.drawWorkingRectArea()
			else:
				if self.mouseDown > 0:
					self.mouseDown+=1
					if self.mouseDown == 5:
						self.mouseDrag=1
		elif self.curButton == QtCore.Qt.RightButton:
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
		if (self.mouseDrag==0 or self.win.selectColorMode>0) and self.curButton == QtCore.Qt.LeftButton:
			self.curButton=-1
			pos=event.pos()
			posX=pos.x()
			posY=pos.y()
			
			if self.win.textBaseToolMode==1 or self.win.textBaseToolMode==2:
				self.setCustomPixels( self.win.textBaseToolMode, [posX,posY], self.win.brushSizeSlider.value )
			elif self.win.textBaseToolMode==3:
				if self.win.selectColorMode>0:
					self.win.setNewThresholdColor([posX,posY])
				self.win.sampleNewThresholdColor(1)
			elif self.win.textBaseToolMode==4:
				posX=int(pos.x()*(1.0/self.zoom))
				posY=int(pos.y()*(1.0/self.zoom))
				if self.initWorkingRectArea[0] == -1:
					self.initWorkingRectArea=[posX,posY]
				self.win.textBaseToolMode=self.win.prevBrushMode
				self.workingRectArea[0]=max(1, min(self.initWorkingRectArea[0], posX) )
				self.workingRectArea[1]=max(1, min(self.initWorkingRectArea[1], posY) )
				self.workingRectArea[2]=min(self.cWOrig-1, max(self.initWorkingRectArea[0], posX) )
				self.workingRectArea[3]=min(self.cHOrig-1, max(self.initWorkingRectArea[1], posY) )
				
				self.workAreaCropVis(self.win.workAreaCrop,1)
				self.win.cropWorkingArea()
				self.win.statusBarUpdate(" ", 10,-1)
				#self.drawReachMask()
			else:
				### Search for Character Data ###

				origRes=[self.cWOrig,self.cHOrig]
				limits=[0,0,self.cWOrig,self.cHOrig]
				limits=[0,0,self.cW-1, self.cH-1]
				if self.workAreaCrop==1:
					origRes=[self.workingRectArea[2]-self.workingRectArea[0], self.workingRectArea[3]-self.workingRectArea[1]]
					posX=int((float(posX)/float(self.img.pixmap().width()))*float(origRes[0]))+self.workingRectArea[0]
					posY=int((float(posY)/float(self.img.pixmap().height()))*float(origRes[1]))+self.workingRectArea[1]
					limits=[self.workingRectArea[0]-1,self.workingRectArea[1]-1,self.workingRectArea[2],self.workingRectArea[3]]
				else:
					posX=int(posX*(1.0/self.zoom))
					posY=int(posY*(1.0/self.zoom))

				posArr=[posX,posY]
				setCropView=0
				drawScale=[self.cW, self.cH]
				if self.workingRectArea[0] > self.workingRectArea[2]:
					self.workAreaActive=0
					self.workAreaCrop=0
				if self.workAreaActive==1:
					if self.workAreaCrop==0:
						if posArr[0]<=self.workingRectArea[0] or posArr[1]<=self.workingRectArea[1] or posArr[0]>=self.workingRectArea[2] or posArr[1]>=self.workingRectArea[3]:
							self.win.statusBarUpdate(" -- You selected a pixel outside of your Work Area; Work within or expand your Work Area -- ", 5000,3)
							return None
					drawScale=[self.workingRectArea[2]-self.workingRectArea[0], self.workingRectArea[3]-self.workingRectArea[1]]
					if self.workAreaCrop==1:
						waRes=[self.img.pixmap().width(), self.img.pixmap().height()]
						##waRes=[self.workAreaData.width(), self.workAreaData.height()]
						#posX=float(posX)*float(drawScale[0])/float(waRes[0])
						#posY=float(posY)*float(drawScale[1])/float(waRes[1])
						#posArr=[int(posX+.5)+self.workingRectArea[0],int(posY+.5)+self.workingRectArea[1]]
					else:
						setCropView=1
						self.win.cropWorkingArea(0)
						waRes=[self.img.pixmap().width(), self.img.pixmap().height()]
				if posArr not in self.reachPixels:
					offset=[0,0,[1,1,self.cW-1,self.cH-1]]
					self.win.charSamplePoints.append(posArr)
					img=self.win.imgData[self.win.curImage]
					if self.workAreaActive==1:
						img=img.copy(self.workingRectArea[0],self.workingRectArea[1], drawScale[0], drawScale[1])
						offset=[self.workingRectArea[0],self.workingRectArea[1],[1,1, drawScale[0]-1, drawScale[1]-1]]
					#limits=[img.width()-1, img.height()-1]
					#limits=[self.cW-1, self.cH-1]
					img=img.toImage()
					
					midRun=self.img.pixmap()
					midRun=midRun.scaled(self.cWOrig,self.cHOrig, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					if self.workingRectArea[0] < self.workingRectArea[2]:
						if self.workAreaCrop==0:
							midRun=midRun.copy(self.workingRectArea[0],self.workingRectArea[1], (drawScale[0], drawScale[1]))
						else:
							midRun=QtGui.QPixmap.fromImage( self.img.pixmap().toImage().copy() )
						midRun=midRun.scaled(drawScale[0], drawScale[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					midRun=midRun.toImage()
					rangeDist=10
					# Make this better
					# Add string of x,y and find in array
					# If not in array, add to pixelQueue
					pixelQueue=[]
					pixelQueue.extend(self.win.charSamplePoints)
					tempScanRange=[]
					tempScanRange.append(self.scanRange[0]-offset[0])
					tempScanRange.append(self.scanRange[1]-offset[1])
					tempScanRange.append(self.scanRange[2]-offset[0])
					tempScanRange.append(self.scanRange[3]-offset[1])
					#tempScanRange.extend()
					caps=[]
					caps.append( max(offset[2][0], tempScanRange[0]-2) )
					caps.append( max(offset[2][1], tempScanRange[1]-2) )
					caps.append( min(offset[2][2], tempScanRange[2]+2) )
					caps.append( min(offset[2][3], tempScanRange[3]+2) )
					thresh=max(0, self.win.thresholdColorSlider.value)
					
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
							checkedCount=str(len(self.reachPixelsBase))
							queueCount=len(pixelQueue)
							warning=""
							if queueCount>300 or runawayLatch==1:
								runawayLatch=1
								warning=" --  !! Run away search detected, set background threshold color to reduce calculations !!"
								
							self.win.statusBarUpdate("( Press 'Escape' to Cancel ) -- Cross-Checking "+checkedCount+" pixels -- Pixels in Queue ... "+str(queueCount)+warning, 0, 0)
							QtGui.QApplication.processEvents()
						if refreshRunner == refreshDraw:
							refreshDraw+=refreshItter#+int(15*(refreshDraw/refreshItter))
							midRunFull=midRun.scaled(self.cW, self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
							pxmap=QtGui.QPixmap.fromImage(midRunFull)
							self.img.setPixmap(pxmap)
							self.checkImageMemory(0,0)
						if runner >= killCheck:
							print "Error - Runaway train"
							print "Ran too long without finding anything."
							latch=0
						else:
							xyPos=pixelQueue.pop(0)
							x=xyPos[0]
							y=xyPos[1]
							xImg=xyPos[0]
							yImg=xyPos[1]
							if self.workAreaCrop==1:
								xImg=(xyPos[0]-offset[0])
								yImg=(xyPos[1]-offset[1])
							
							#############################################
							r,g,b,a=QtGui.QColor(img.pixel(xImg,yImg)).getRgb()
							
							val=(r+g+b)
							edgeHit=0
							if val<thresh:
								latch=1
							else:
								edgeHit=1
								
							if edgeHit==0:
								self.reachPixelsBase.append([x,y])
							else:
								edgePos=[x,y]
								if edgePos not in self.edgePixelsBase:
									self.edgePixelsBase.append(edgePos)
								
							tempScanRange[0]=min(tempScanRange[0], xImg)
							tempScanRange[1]=min(tempScanRange[1], yImg)
							tempScanRange[2]=max(tempScanRange[2], xImg)
							tempScanRange[3]=max(tempScanRange[3], yImg)
							caps=[]
							caps.append( max(offset[2][0], tempScanRange[0]-2) )
							caps.append( max(offset[2][1], tempScanRange[1]-2) )
							caps.append( min(offset[2][2], tempScanRange[2]+2) )
							caps.append( min(offset[2][3], tempScanRange[3]+2) )
							
							if ((latch == 1 and val<thresh) or latch==0) and edgeHit==0:
								midRun.setPixel(xImg,yImg,QtGui.QColor(0,255,0,255).rgb())
								runner=0
								hit=0
								### Do I even want this?
								#if xImg in caps or yImg in caps:
								#	if nextArr not in self.edgePixelsBase:
								#		self.edgePixelsBase.append(nextArr)
								for xy in growArr:
									#nextX=max(0, min(x+xy[0], limits[0]))
									#nextY=max(0, min(y+xy[1], limits[1]))
									nextX=max(limits[0], min(x+xy[0], limits[2]))
									nextY=max(limits[1], min(y+xy[1], limits[3]))
									nextArr=[nextX,nextY]
									if nextX-offset[0]>caps[0] and nextY-offset[1]>caps[1] and nextX-offset[0]<caps[2] and nextY-offset[1]<caps[3]:
										if nextArr not in self.reachPixelsBase:
											hit+=1
											self.reachPixelsBase.append(nextArr)
											pixelQueue.append(nextArr)
							if len(pixelQueue) == 0:
								latch=0

					midRunFull=midRun.scaled(self.cW, self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					pxmap=QtGui.QPixmap.fromImage(midRunFull)
					self.img.setPixmap(pxmap)
					self.checkImageMemory()
					self.win.statusBarUpdate("-- Cleanup Pass - Fixing holes --", 0, 0)
							
					self.reachPixels.extend(self.reachPixelsBase)
					
					newEdgeBuild=self.findEdgePixels(self.edgePixelsBase)
					self.edgePixelsBase=newEdgeBuild
					self.edgePixels=[]
					self.edgePixels.extend(self.edgePixelsBase)
					
					QtGui.QApplication.processEvents()
					
					tempScanRange[0]+=offset[0]
					tempScanRange[1]+=offset[1]
					tempScanRange[2]+=offset[0]
					tempScanRange[3]+=offset[1]
					img,tempScanRange=self.extendReachEdges(img,tempScanRange)
					
					if self.win.loopLatch==1:
						self.win.loopLatch=0
					# Update scanRange to display bounding box better
					alphaPadding=self.win.sliderAlphaReach.value
					self.scanRange[0]=max(tempScanRange[0]-alphaPadding, 0) if tempScanRange[0] != self.scanRange[0] else self.scanRange[0]
					self.scanRange[1]=max(tempScanRange[1]-alphaPadding, 0) if tempScanRange[1] != self.scanRange[1] else self.scanRange[1]
					self.scanRange[2]=min(tempScanRange[2]+alphaPadding, self.cWOrig-1) if tempScanRange[2] != self.scanRange[2] else self.scanRange[2]
					self.scanRange[3]=min(tempScanRange[3]+alphaPadding, self.cHOrig-1) if tempScanRange[3] != self.scanRange[3] else self.scanRange[3]
					
					if setCropView==1:
						self.win.cropWorkingArea(0)
					self.drawReachMask()
					self.win.statusBarUpdate(" -- Character Search Complete! --", 5000, 1)
				else:
					if setCropView==1:
						self.win.cropWorkingArea(0)
					self.win.statusBarUpdate(" -- Pixel is already included in your Character Data; Select a different pixel --", 5000, 3)

		self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.mouseDown=0
		self.mouseDrag=0
	def findEdgePixels(self, searchArr=[], onlyAddArr=0):
		growArr=[[1,1],[1,0],[1,-1], [0,1],[0,-1], [-1,1],[-1,0],[-1,-1]]
		newEdgeBuild=[]
		if len(searchArr)==0:
			searchArr.extend(self.edgePixels)
		#if onlyAddArr==0:
		#	searchArr.extend(self.customPixels['add'])
		searchArr=map(lambda x: ",".join(map(str,x)), searchArr)
		searchArr=list(set(searchArr))
		searchArr=map(lambda x: list(ast.literal_eval(x)), searchArr)
		
		runLen=len(searchArr)
		fRunLen=float(runLen)
		statusUpdateIttr=max(1, int(float(runLen)/20.0))
		reachArr=[]
		reachArr.extend(self.reachPixels)
		#reachArr.extend(self.customPixels['add'])
		self.win.loopLatch=1
		ret=1
		for v in range(runLen):
			if v%statusUpdateIttr==0:
				percDisp=str(float(int(float(v)/fRunLen*1000.0))/10.0)
				self.win.statusBarUpdate("-- Finding edge pixels - "+percDisp+" % --", 0, 0)
				QtGui.QApplication.processEvents()
				if self.win.loopLatch==0:
					ret=0
					break;
			p=searchArr[v]
			for a in growArr:
				xy=map(lambda x,c: x+c, p,a)
				xy[0]=min(self.cW-1, max(1, xy[0]))
				xy[1]=min(self.cH-1, max(1, xy[1]))
				if xy not in reachArr:
					newEdgeBuild.append(p)
		if ret==1:
			self.win.statusBarUpdate("-- Completed finding edge pixels --", 5000, 1)
			self.win.loopLatch=0
			return newEdgeBuild
		else:
			self.win.statusBarUpdate(" ", 10, -1)
			return []
	def setCustomPixels(self,mode,xy,brushSize):
		self.win.loopLatch=0 #If mid searching for edges
		brushSize=float(brushSize)/2.0
		alphaPadding=self.win.sliderAlphaReach.value
		origRangePixels=[[0,0]]
		if brushSize > 1:
			self.buildBrushPixels()
			origRangePixels=self.brushPixelData
			
		origRes=[self.cWOrig,self.cHOrig]
		limits=[0,0,self.cWOrig,self.cHOrig]
		if self.workAreaCrop==1:
			origRes=[self.workingRectArea[2]-self.workingRectArea[0], self.workingRectArea[3]-self.workingRectArea[1]]
			xy[0]=int((float(xy[0])/float(self.img.pixmap().width()))*float(origRes[0]))+self.workingRectArea[0]
			xy[1]=int((float(xy[1])/float(self.img.pixmap().height()))*float(origRes[1]))+self.workingRectArea[1]
			limits=[self.workingRectArea[0],self.workingRectArea[1],self.workingRectArea[2],self.workingRectArea[3]]
		else:
			xy[0]=int(xy[0]*(1.0/self.zoom))
			xy[1]=int(xy[1]*(1.0/self.zoom))
			
		origRangePixels=map(lambda x: [ max(limits[0], min(limits[2], x[0]+xy[0])), max(limits[1], min(limits[3], x[1]+xy[1])) ], origRangePixels)
		curRangePixels=map(lambda x: ",".join(map(str,x)), origRangePixels)
		
		rangePixels=map(lambda x: ",".join(map(str,x)), self.reachPixels)
		customPixelsAdd=map(lambda x: ",".join(map(str,x)), self.customPixels['add'])
		customPixelsRem=map(lambda x: ",".join(map(str,x)), self.customPixels['rem'])
		if mode == 1: # Add
			customPixelsRem=list(set(customPixelsRem).difference(curRangePixels))
			customPixelsAdd=list(set(customPixelsAdd+curRangePixels))
			rangePixels=list(set(rangePixels+curRangePixels))
		elif mode == 2: # Remove
			customPixelsAdd=list(set(customPixelsAdd).difference(curRangePixels))
			rangePixels=list(set(rangePixels).difference(curRangePixels))
			customPixelsRem=list(set(customPixelsRem+curRangePixels))
		else:
			self.win.statusBarUpdate(" -- Tried setting custom pixels outside of propper mode! --", 5000, 2)
			return None
		rangePixels= map(lambda x: list(ast.literal_eval(x)), rangePixels)
		self.reachPixels=rangePixels
		self.customPixels['add']= map(lambda x: list(ast.literal_eval(x)), customPixelsAdd)
		self.customPixels['rem']= map(lambda x: list(ast.literal_eval(x)), customPixelsRem)
		if mode == 1:
			curRangePixels= map(lambda x: list(ast.literal_eval(x)), curRangePixels)
			if "temp" not in self.customPixels.keys():
				self.customPixels['temp']=[]
			self.customPixels['temp'].extend(curRangePixels)
			if mode == 1: # Add
				alphaPadding=self.win.sliderAlphaReach.value
				for xy in curRangePixels:
					self.scanRange[0]=max(min(xy[0]-alphaPadding, self.scanRange[0]), 0)
					self.scanRange[1]=max(min(xy[1]-alphaPadding, self.scanRange[1]), 0)
					self.scanRange[2]=min(max(xy[0]+alphaPadding, self.scanRange[2]), self.cWOrig-1)
					self.scanRange[3]=min(max(xy[1]+alphaPadding, self.scanRange[3]), self.cHOrig-1)
		self.drawReachMask()
		"""
		if self.win.outlineToggle == 1 and mode == 1:
			### This can become extremely slow....
			### During the findEdgePixels definition
			curRangePixels.extend(self.edgePixels)
			curRangePixels.extend(self.customPixels['temp'])
			### This seems to fix the slow down, too many dupelicates in the array it seems
			### Still testing...
			curRangePixels=map(lambda x: ",".join(map(str,x)), curRangePixels)
			curRangePixels=list(set(curRangePixels))
			curRangePixels=map(lambda x: list(ast.literal_eval(x)), curRangePixels)
			curEdge=self.findEdgePixels(curRangePixels,1)
			if len(curEdge)>0:
				self.edgePixels=[]
				self.edgePixels.extend(curEdge)
				self.customPixels['temp']=[]
				alphaPadding=self.win.sliderAlphaReach.value
				for xy in self.edgePixels:
					self.scanRange[0]=max(min(xy[0]-alphaPadding, self.scanRange[0]), 0)
					self.scanRange[1]=max(min(xy[1]-alphaPadding, self.scanRange[1]), 0)
					self.scanRange[2]=min(max(xy[0]+alphaPadding, self.scanRange[2]), self.cWOrig-1)
					self.scanRange[3]=min(max(xy[1]+alphaPadding, self.scanRange[3]), self.cHOrig-1)
				self.drawReachMask()
		else:
			self.updateEdges=1
		"""
	def checkOutlineUpdate(self, force=0):
		if 0:#self.updateEdges==1 or force==1:
			self.drawReachMask(1,0,1)
			curEdge=self.findEdgePixels()
			self.edgePixels=[]
			self.edgePixels.extend(curEdge)
			self.updateEdges=0
		self.drawReachMask()
	def buildBrushPixels(self, force=0):
		if self.brushSize != self.win.brushSizeSlider.value or force==1:
			### Find pixels within brushSize radius
			### ...I'm sure there is a better way to do this
			### Like... I'm sure.... My brain is telling me this is wrong
			### Or is it my gut?  Maybe heart since they found neurons in the heart?
			### Is anything really a concious choice in the end?
			brushSize=max(1.0, float(self.win.brushSizeSlider.value)/2.0)
			curRangePixels=[]
			for x in range(-int(brushSize+.5), int(brushSize+1.5)):
				for y in range(-int(brushSize+.5), int(brushSize+1.5)):
					dx=float(x)#-pos[0])
					dy=float(y)#-pos[1])
					delta=math.sqrt( dx*dx + dy*dy )
					if delta<=brushSize:
						curRangePixels.append([x,y])
			self.brushPixelData=curRangePixels
			
			curBrushEdge=[]
			#growArr=[[1,1],[1,0],[1,-1], [0,1],[0,-1], [-1,1],[-1,0],[-1,-1]]
			growArr=[[1,0], [0,1],[0,-1],[-1,0]]
			for xy in curRangePixels:
				for grow in growArr:
					nextArr=[ xy[0]+grow[0], xy[1]+grow[1] ]
					if nextArr not in curRangePixels:
						curBrushEdge.append(xy)
						break;
			self.brushEdgePixelData=curBrushEdge
			self.brushSize=self.win.brushSizeSlider.value
	def drawReachMask(self,bbox=1,ret=0,outlineBuilding=0):
		img=None
		offset=[0,0]
		if self.workAreaCrop==1:
			if self.workAreaData == None:
				self.workAreaCropVis(None, 1)
			img=self.workAreaData
			offset=[self.workingRectArea[0],self.workingRectArea[1]]
		else:
			img=self.win.imgData[self.win.curImage]
		res=[img.width(), img.height()]
		img=img.toImage()
		if self.win.outlineToggle == 0:
			for xy in self.reachPixels:
				x=xy[0]-offset[0]
				y=xy[1]-offset[1]
				if x>0 and x<res[0] and y>0 and y<res[1]:
					img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
			if self.extendShrinkEdge==1:
				for xy in self.edgePixelsBase:
					x=xy[0]-offset[0]
					y=xy[1]-offset[1]
					if x>0 and x<res[0] and y>0 and y<res[1]:
						img.setPixel(x,y,QtGui.QColor(0,255,150,255).rgb())
		else:
			#for xy in self.edgePixelsBase:
			#if self.updateEdges==1 and outlineBuilding==0:
			#	self.checkOutlineUpdate()
			#	return None
			for xy in self.edgePixels:
				x=xy[0]-offset[0]
				y=xy[1]-offset[1]
				if x>0 and x<res[0] and y>0 and y<res[1]:
					img.setPixel(x,y,QtGui.QColor(0,255,150,150).rgb())
		if bbox==1:
			img=self.drawBoundingBox(img,res)
			self.curCanvasPreWorkAreaData=QtGui.QPixmap.fromImage(img)
			img=self.drawWorkingRectArea(img)
		pmap=QtGui.QPixmap.fromImage(img)
		self.curCanvasData=pmap
		pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
		if ret == 1:
			return pmap
		else:
			self.img.setPixmap(pmap)
			self.checkImageMemory()
			return None
	def drawBoundingBox(self, img,res):
		# Build Bounding Box
		# Might be cool to make this interactive
		# Still don't know why I try to avoid QPainter so much
		# Something about QPainter bothers me, and can't put my finger on it....
		
		offset=[0,0]
		pmap=None
		if self.workAreaCrop==1:
			if self.workAreaData == None:
				self.workAreaCropVis(None, 1)
			offset=[self.workingRectArea[0],self.workingRectArea[1]]
		runScanRangeBBox=0
		queue=[]
		if self.scanRange[0] < self.scanRange[2]:
			queue.append([])
			queue[-1].extend(self.scanRange)
			queue[-1][2]=queue[-1][2]-queue[-1][0]
			queue[-1][3]=queue[-1][3]-queue[-1][1]
			runScanRangeBBox=1
		if self.workAreaCrop==0:
			srStorageKeys=self.win.scanRangeStorage.keys()
			if self.win.curImage in srStorageKeys:
				for r in self.win.scanRangeStorage[self.win.curImage]:
					queue.append(r)
		if len(queue) > 0:
			if pmap==None:
				pmap=QtGui.QPixmap.fromImage(img)
			painter=QtGui.QPainter(pmap)
			for x in range(len(queue)):
				tempRange=[]
				tempRange.append(queue[x][0]-offset[0])
				tempRange.append(queue[x][1]-offset[1])
				tempRange.append(queue[x][2])
				tempRange.append(queue[x][3])
				if x==0 and runScanRangeBBox==1:
					painter.setPen(QtGui.QPen(QtGui.QColor(255,0,0,220)))
				elif x==1 or (x==0 and runScanRangeBBox==0):
					painter.setPen(QtGui.QPen(QtGui.QColor(110,10,30,190)))
					painter.setBrush(QtGui.QColor(140,70,70,170))
				painter.drawRect(tempRange[0],tempRange[1],tempRange[2],tempRange[3])
			painter.end()
			return pmap.toImage()
		return img
	def drawWorkingRectArea(self, img=None):
		if self.workAreaActive==1 and self.workAreaCrop==0:
			if self.workingRectArea[0] < self.workingRectArea[2]:
				offset=[0,0]
				pmap=None
				
				queue=[]
				queue.append([])
				queue[-1].extend(self.workingRectArea)
				queue[-1][2]=queue[-1][2]-queue[-1][0]
				queue[-1][3]=queue[-1][3]-queue[-1][1]
				runScanRangeBBox=1
				
				inputImg=1
				if img == None:
					inputImg=0
					img=self.curCanvasPreWorkAreaData.toImage()
				pmap=QtGui.QPixmap.fromImage(img.copy())
				if len(queue) > 0:
					painter=QtGui.QPainter(pmap)
					painter.setPen(QtGui.QPen(QtGui.QColor(0,100,255,200)))
					for x in range(len(queue)):
						tempRange=[]
						tempRange.append(queue[x][0]-offset[0])
						tempRange.append(queue[x][1]-offset[1])
						tempRange.append(queue[x][2]-offset[0])
						tempRange.append(queue[x][3]-offset[1])
						painter.drawRect(tempRange[0],tempRange[1],tempRange[2],tempRange[3])
					painter.end()
				if inputImg == 0:
					pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
					self.img.setPixmap(pmap)
				return pmap.toImage()
		return img
	def wheelEvent(self, event):
		val = event.delta() / abs(event.delta())
		targetZoom= self.zoom + val*self.zoomRate
		self.setZoom(targetZoom)
	def setZoom(self, targetZoom, redraw=1):
		if (targetZoom <= self.zoomMax or self.zoomMax==-1) and targetZoom>0:
			targetW=int(float(self.cWOrig)*targetZoom)
			targetH=int(float(self.cHOrig)*targetZoom)
			self.cW=targetW
			self.cH=targetH
			self.zoom=targetZoom
			self.win.zoom=targetZoom
			if redraw==1:
				self.drawReachMask()
	def checkImageMemory(self, redraw=1, errorMode=3):
		if self.img.pixmap().width()==0:
			self.win.statusBarUpdate(" -- Maximum zoom hit; use Work Areas or crop down your images into chunks -- ", 5000,errorMode)
			self.zoomPrevWorking=self.zoomPrevWorking-self.zoomRate
			self.zoomMax=self.zoomPrevWorking
			self.setZoom( self.zoomPrevWorking, redraw )
		else:
			self.zoomPrevWorking=max(self.zoomPrevWorking, self.zoom)
	def rebuildReachPixels(self,baseArr=[], draw=0):
		rangePixels=baseArr
		if len(rangePixels)==0:
			rangePixels=self.reachPixelsBase
		rangePixels=map(lambda x: ",".join(map(str,x)), rangePixels)
		customPixelsAdd=map(lambda x: ",".join(map(str,x)), self.customPixels['add'])
		customPixelsRem=map(lambda x: ",".join(map(str,x)), self.customPixels['rem'])
		
		if self.extendShrinkEdge!=-1 and len(self.edgePixelsBase)>0:
			edgePixels=map(lambda x: ",".join(map(str,x)), self.edgePixelsBase)
			if self.extendShrinkEdge<0:
				rangePixels=list(set(rangePixels).difference(edgePixels))
			elif self.extendShrinkEdge>0:
				rangePixels=list(set(rangePixels+edgePixels))
		
		rangePixels=list(set(rangePixels).difference(customPixelsRem))
		rangePixels=list(set(rangePixels+customPixelsAdd))
		rangePixels= map(lambda x: list(ast.literal_eval(x)), rangePixels)
		self.reachPixels=rangePixels
		
		if draw==1:
			self.drawReachMask()
			
		return True
	def drawBrushRadius(self, mode, xy=None):
		self.buildBrushPixels()
		if xy==None:
			xy=[]
			xy.extend(self.prevXY)
		else:
			self.prevXY=[]
			self.prevXY.extend(xy)
			
		if mode == 0:
			img=self.curCanvasData.toImage()
			img=img.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			pmap=QtGui.QPixmap.fromImage(img)
			self.img.setPixmap(pmap)
			self.checkImageMemory(0)
			return None
		if len(self.brushEdgePixelData)>0:
			img=self.curCanvasData
			origRes=[self.cWOrig,self.cHOrig]
			if self.workAreaCrop==1:
				origRes=[self.workingRectArea[2]-self.workingRectArea[0], self.workingRectArea[3]-self.workingRectArea[1]]
				xy[0]=int((float(xy[0])/float(self.img.pixmap().width()))*float(origRes[0]))
				xy[1]=int((float(xy[1])/float(self.img.pixmap().height()))*float(origRes[1]))
			else:
				xy[0]=int(xy[0]*(1.0/self.zoom))
				xy[1]=int(xy[1]*(1.0/self.zoom))
			img=img.scaled(origRes[0],origRes[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			img=img.toImage()
			curBrushPixels=self.brushEdgePixelData
			curBrushPixels=map(lambda x: [ max(0, min(origRes[0]-1, x[0]+xy[0])), max(0, min(origRes[1]-1, x[1]+xy[1])) ], curBrushPixels)
			rgb=QtGui.QColor(150,0,0,150).rgb()
			if mode == 1:
				rgb=QtGui.QColor(0,150,50,150).rgb()
			if mode == 2:
				rgb=QtGui.QColor(150,0,150,150).rgb()
			for xy in curBrushPixels:
				x=xy[0]
				y=xy[1]
				img.setPixel(x,y,rgb)
			img=img.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			pmap=QtGui.QPixmap.fromImage(img)
			self.img.setPixmap(pmap)
			self.checkImageMemory(0)
	def extendReachEdges(self,img=None, tempScanRange=None):
		edgeGrowth=int(self.win.edgeGrowthSlider.value)
		edgeGrowthInit=edgeGrowth
		imgLoaded=1
		self.edgePixels=[]
		self.edgePixels.extend(self.edgePixelsBase)
		self.rebuildReachPixels()
		if len(self.reachPixelsBase)>0 and len(self.edgePixelsBase)>0:
			if img == None:
				tempScanRange=[]
				tempScanRange.extend(self.scanRange)
				imgLoaded=0
				img=self.win.imgData[self.win.curImage]
				img=img.toImage()
				for xy in self.reachPixelsBase:
					img.setPixel(xy[0],xy[1],QtGui.QColor(0,255,0,255).rgb())
			else:
				tempScanRange[0]=max(1, tempScanRange[0]-edgeGrowth)
				tempScanRange[1]=max(1, tempScanRange[1]-edgeGrowth)
				tempScanRange[2]=min(self.cW-1, tempScanRange[2]+edgeGrowth) 
				tempScanRange[3]=min(self.cW-1, tempScanRange[3]+edgeGrowth)
			if edgeGrowth != 0:
				growArr=[[1,1],[1,0],[1,-1], [0,1],[0,-1], [-1,1],[-1,0],[-1,-1]]
				refreshRunner=0
				refreshDraw=200
				refreshItter=200
				if edgeGrowth>0:
					self.extendShrinkEdge=1
					curRun=self.edgePixelsBase
					self.win.loopLatch=1
					for e in range(1,edgeGrowth+1):
						self.win.statusBarUpdate("( Press 'Escape' to Cancel ) -- Extending Edge - "+str(e)+" of "+str(edgeGrowth)+" - - Total Edge Pixels - "+str(len(self.edgePixelsBase)), 0, 0)
						QtGui.QApplication.processEvents()
						edgeGrowthCheck=int(self.win.edgeGrowthSlider.value)
						if edgeGrowthInit != edgeGrowthCheck:
							self.win.loopLatch=0
						if self.win.loopLatch==0:
							break;
						curGrowArr=growArr
						refreshRunner=0
						refreshDraw=200
						curExtend=[]
						for xy in curRun:
							#if xy not in self.customPixels['add']: # This... Shouldn't be needed.... But is
							for g in curGrowArr:
								refreshRunner+=1
								cur=map(sum,zip(xy,g))
								if cur not in self.reachPixelsBase and cur not in self.edgePixelsBase and cur not in curExtend:
									img.setPixel(cur[0],cur[1],QtGui.QColor(0,0,255,255).rgb())
									curExtend.append(cur)
									if imgLoaded==0:
										tempScanRange[0]=min(tempScanRange[0], cur[0])
										tempScanRange[1]=min(tempScanRange[1], cur[1])
										tempScanRange[2]=max(tempScanRange[2], cur[0])
										tempScanRange[3]=max(tempScanRange[3], cur[1])
								if refreshRunner == refreshDraw:
									refreshDraw+=refreshItter
									pmap=QtGui.QPixmap.fromImage(img)
									pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
									self.img.setPixmap(pmap)
									self.checkImageMemory(0,0)
									QtGui.QApplication.processEvents()
									edgeGrowthCheck=int(self.win.edgeGrowthSlider.value)
									if edgeGrowthInit != edgeGrowthCheck:
										self.win.loopLatch=0
									if self.win.loopLatch==0:
										break;
							if self.win.loopLatch==0:
								break;
						self.edgePixels.extend(curExtend)
						curRun=curExtend
						if len(curExtend) == 0:
							break;
					try:
						pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
						self.img.setPixmap(pmap)
						self.checkImageMemory(0)
						self.curCanvasData=pmap
					except:
						pass;
					QtGui.QApplication.processEvents()
					self.win.loopLatch=0
					if imgLoaded==0:
							self.win.statusBarUpdate(" -- Growing Edge Completed -- ", 5000, 1)
				else:
					self.extendShrinkEdge=0
					self.win.loopLatch=1
					curRun=self.edgePixelsBase
					for e in range(0,abs(edgeGrowth)):
						self.win.statusBarUpdate("( Press 'Escape' to Cancel ) -- Shrinking Edge - "+str(e+1)+" of "+str(abs(edgeGrowth)), 0, 0)
						QtGui.QApplication.processEvents()
						edgeGrowthCheck=int(self.win.edgeGrowthSlider.value)
						if edgeGrowthInit != edgeGrowthCheck:
							self.win.loopLatch=0
						if self.win.loopLatch==0:
							break;
						if e == 0:
							curGrowArr=[[0,0]]
						else:
							curGrowArr=growArr
						refreshRunner=0
						refreshDraw=200
						curShrink=[]
						for xy in curRun:
							for g in curGrowArr:
								refreshRunner+=1
								cur=map(sum,zip(xy,g))
								if cur in self.reachPixels:# and cur not in self.customPixels['add']:
									self.reachPixels.remove(cur)
									img.setPixel(cur[0],cur[1],QtGui.QColor(255,150,0,255).rgb())
									curShrink.append(cur)
								if refreshRunner == refreshDraw:
									pmap=QtGui.QPixmap.fromImage(img)
									refreshDraw+=refreshItter
									pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
									self.img.setPixmap(pmap)
									self.checkImageMemory(0,0)
									QtGui.QApplication.processEvents()
									edgeGrowthCheck=int(self.win.edgeGrowthSlider.value)
									if edgeGrowthInit != edgeGrowthCheck:
										self.win.loopLatch=0
									if self.win.loopLatch==0:
										break;
							if self.win.loopLatch==0:
								break;
						self.edgePixels.extend(curShrink)
						curRun=curShrink
					try:
						pmap=self.drawReachMask(1,1)
						self.img.setPixmap(pmap)
						self.checkImageMemory(0)
						self.curCanvasData=pmap
					except:
						pass;
					self.win.loopLatch=0
					self.updateEdges=1
					if imgLoaded==0:
						self.win.statusBarUpdate(" -- Shrinking Edge Completed -- ", 5000, 1)
			else:
				self.extendShrinkEdge=-1
				
			self.rebuildReachPixels(self.reachPixels,1)
			if imgLoaded==0:
				self.scanRange=tempScanRange
				alphaPadding=self.win.sliderAlphaReach.value
				self.scanRange[0]=max(tempScanRange[0]-alphaPadding, 0) if tempScanRange[0] != self.scanRange[0] else self.scanRange[0]
				self.scanRange[1]=max(tempScanRange[1]-alphaPadding, 0) if tempScanRange[1] != self.scanRange[1] else self.scanRange[1]
				self.scanRange[2]=min(tempScanRange[2]+alphaPadding, self.cWOrig) if tempScanRange[2] != self.scanRange[2] else self.scanRange[2]
				self.scanRange[3]=min(tempScanRange[3]+alphaPadding, self.cHOrig) if tempScanRange[3] != self.scanRange[3] else self.scanRange[3]
				
				self.drawReachMask()
		return img,tempScanRange