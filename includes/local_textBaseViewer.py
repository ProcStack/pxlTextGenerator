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
		
		self.curCanvasData=None
		self.scanRange=[self.cW,self.cH,0,0]
		self.rect=[0,0,256,256]
		self.reachPixelsBase=[]
		self.reachPixels=[]
		self.edgePixelsBase=[]
		self.edgePixels=[]
		self.customPixels={}
		self.customPixels['add']=[]
		self.customPixels['rem']=[]
		self.extendShrinkEdge=-1
		self.mouseDown=0
		self.mousePressStart=[]
		self.scrollStart=[]
		self.mouseDrag=0
		self.brushSize=-1
		self.brushPixelData=[]
		self.brushEdgePixelData=[]
		self.curButton=-1
		
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

	def setDefaultScroll(self): ### Not running right now
		curScrollH=self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().maximum()
		curScrollV=self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().maximum()
		self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().setValue(curScrollH)
		self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().setValue(curScrollV)
	def resetScanRange(self):
		pmap=QtGui.QPixmap()
		pmap.load(self.imgPath)
		self.img.setPixmap(pmap)
		self.curCanvasData=pmap
		self.scanRange=[self.cW,self.cH,0,0]
		self.reachPixelsBase=[]
		self.reachPixels=[]
		self.edgePixelsBase=[]
		self.edgePixels=[]
		self.customPixels={}
		self.customPixels['add']=[]
		self.customPixels['rem']=[]
		self.setZoom(self.win.zoom)
	def mousePressEvent(self, event):
		pos=event.globalPos()
		self.mousePressStart=[pos.x(), pos.y()]
		self.mouseDown=1
		self.curButton=event.buttons()
		scrollH=self.curImgBlock.parent().parent().parent().parent().horizontalScrollBar().value()
		scrollV=self.curImgBlock.parent().parent().parent().parent().verticalScrollBar().value()
		self.scrollStart=[scrollH, scrollV]
	def mouseMoveEvent(self, event):
		self.curButton=event.buttons()
		if self.curButton == QtCore.Qt.NoButton:
			if self.win.textBaseToolMode in [1,2]:
				pos=event.pos()
				posX=int(pos.x()*(1.0/self.zoom))
				posY=int(pos.y()*(1.0/self.zoom))
				self.drawBrushRadius(self.win.textBaseToolMode, [posX,posY])
		elif self.curButton == QtCore.Qt.LeftButton:
			if self.win.textBaseToolMode==1 or self.win.textBaseToolMode==2:
				pos=event.pos()
				posX=int(pos.x()*(1.0/self.zoom))
				posY=int(pos.y()*(1.0/self.zoom))
				self.setCustomPixels( self.win.textBaseToolMode, [posX,posY], self.win.brushSizeSlider.value )
			elif self.win.selectColorMode==3 and self.win.selectColorMode>0:
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
			posX=int(pos.x()*(1.0/self.zoom))
			posY=int(pos.y()*(1.0/self.zoom))
			
			if self.win.textBaseToolMode==1 or self.win.textBaseToolMode==2:
				self.setCustomPixels( self.win.textBaseToolMode, [posX,posY], self.win.brushSizeSlider.value )
			elif self.win.textBaseToolMode==3 and self.win.selectColorMode>0:
				self.win.selectColorMode=0
				self.win.setNewThresholdColor([posX,posY])
				self.win.textBaseToolMode=0
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
							
							midRunFull=midRun.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
							pxmap=QtGui.QPixmap.fromImage(midRunFull)
							self.img.setPixmap(pxmap)
						if runner >= killCheck:
							print "Error - Runaway train"
							print "Ran too long without finding anything."
							latch=0
						else:
							xyPos=pixelQueue.pop(0)
							x=xyPos[0]
							y=xyPos[1]
							#curStr=str(x)+","+str(y)
							
							#############################################
							r,g,b,a=QtGui.QColor(img.pixel(x,y)).getRgb()
							
							val=(r+g+b)
							edgeHit=0
							if val<thresh:
								latch=1
							else:
								edgeHit=1
								
							if edgeHit==0:
								self.reachPixelsBase.append(xyPos)
							else:
								edgePos=[x,y]
								if edgePos not in self.edgePixelsBase:
									self.edgePixelsBase.append(edgePos)
								
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
								if ((latch == 1 and val<thresh) or latch==0) and edgeHit==0:
									midRun.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
									runner=0
									hit=0
									for xy in growArr:
										nextX=max(0, min(x+xy[0], self.cWOrig))
										nextY=max(0, min(y+xy[1], self.cHOrig))
										nextArr=[nextX,nextY]#str(nextX)+","+str(nextY)
										if nextArr not in self.reachPixelsBase:
											hit+=1
											self.reachPixelsBase.append(nextArr)
											pixelQueue.append(nextArr)
							if len(pixelQueue) == 0:
								latch=0
					for xy in self.reachPixelsBase:
						x=xy[0]
						y=xy[1]
						#img.setPixel(x,y,QtGui.QColor(0,255,0,255).rgb())
						
					self.reachPixels.extend(self.reachPixelsBase)
					
					newEdgeBuild=[]
					for p in self.edgePixelsBase:
						for a in growArr:
							xy=map(lambda x,c: x+c, p,a)
							xy[0]=min(self.cW-1, max(1, xy[0]))
							xy[1]=min(self.cH-1, max(1, xy[1]))
							if xy not in self.reachPixels:
								newEdgeBuild.append(p)
					self.edgePixelsBase=newEdgeBuild
					self.edgePixels=[]
					self.edgePixels.extend(self.edgePixelsBase)
					
					QtGui.QApplication.processEvents()
					
					img,tempScanRange=self.extendReachEdges(img,tempScanRange)
					
					if self.win.loopLatch==1:
						self.win.loopLatch=0
					# Update scanRange to display bounding box better
					alphaPadding=self.win.sliderAlphaReach.value()
					self.scanRange[0]=max(tempScanRange[0]-alphaPadding, 0) if tempScanRange[0] != self.scanRange[0] else self.scanRange[0]
					self.scanRange[1]=max(tempScanRange[1]-alphaPadding, 0) if tempScanRange[1] != self.scanRange[1] else self.scanRange[1]
					self.scanRange[2]=min(tempScanRange[2]+alphaPadding, self.cWOrig-1) if tempScanRange[2] != self.scanRange[2] else self.scanRange[2]
					self.scanRange[3]=min(tempScanRange[3]+alphaPadding, self.cHOrig-1) if tempScanRange[3] != self.scanRange[3] else self.scanRange[3]
										
					self.drawReachMask()
					self.win.statusBarUpdate(" -- Character Search Complete! --", 5000, 1)

		self.mouseDown=0
		self.mouseDrag=0
	def wheelEvent(self, event):
		val = event.delta() / abs(event.delta())
		targetZoom= self.zoom + val*.1
		self.setZoom(targetZoom)
	def setCustomPixels(self,mode,pos,brushSize):
		brushSize=float(brushSize)/2.0
		alphaPadding=self.win.sliderAlphaReach.value()
		origRangePixels=[[0,0]]
		if brushSize > 1:
			self.buildBrushPixels()
			origRangePixels=self.brushPixelData
			"""
			
			mmin=[int(max(0, pos[0]-brushSize)), int(max(0, pos[1]-brushSize))]
			mmax=[int(min(self.cW-1, pos[0]+brushSize)), int(min(self.cW-1, pos[1]+brushSize))]
			curmm=[self.scanRange[0],self.scanRange[1],self.scanRange[2],self.scanRange[3]]
						curmm[0]=min(curmm[0], x-alphaPadding )
						curmm[1]=min(curmm[1], y-alphaPadding )
						curmm[2]=max(curmm[2], x+alphaPadding )
						curmm[3]=max(curmm[3], y+alphaPadding )
						"""
		######
		#origRangePixels=map(lambda x: [x[0]+pos[0], x[1]+pos[1]], origRangePixels)
		origRangePixels=map(lambda x: [ max(0, min(self.cWOrig-1, x[0]+pos[0])), max(0, min(self.cHOrig-1, x[1]+pos[1])) ], origRangePixels)
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

		if mode == 1: # Add
			for xy in origRangePixels:
				self.scanRange[0]=max(min(xy[0], self.scanRange[0]), 0)
				self.scanRange[1]=max(min(xy[1], self.scanRange[1]), 0)
				self.scanRange[2]=min(max(xy[0], self.scanRange[2]), self.cWOrig-1)
				self.scanRange[3]=min(max(xy[1], self.scanRange[3]), self.cHOrig-1)
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
	def drawReachMask(self,bbox=1,ret=0):
		img=self.win.imgData[self.win.curImage]
		img=img.toImage()
		for xy in self.reachPixels:
			img.setPixel(xy[0],xy[1],QtGui.QColor(0,255,0,255).rgb())
		if self.extendShrinkEdge==1:
			for xy in self.edgePixelsBase:
				x=xy[0]
				y=xy[1]
				img.setPixel(x,y,QtGui.QColor(0,255,150,255).rgb())
		if bbox==1:
			img=self.drawBoundingBox(img)
		pmap=QtGui.QPixmap.fromImage(img)
		self.curCanvasData=pmap
		pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
		if ret == 1:
			return pmap
		else:
			self.img.setPixmap(pmap)
			return None
	def drawBoundingBox(self, img):
		# Build Bounding Box
		# Might be cool to make this interactive
		# Still don't know why I try to avoid QPainter so much
		# Something about QPainter bothers me, and can't put my finger on it....
		bboxRun=[]
		bboxRun.append( [[max(0, self.scanRange[0]-1), self.scanRange[0]], [ self.scanRange[1], self.scanRange[3]] ] )
		bboxRun.append( [[self.scanRange[2], min(self.cWOrig-1, self.scanRange[2]+1)], [ self.scanRange[1], self.scanRange[3]] ] )
		bboxRun.append( [[self.scanRange[0], self.scanRange[2]], [ max(0, self.scanRange[1]-1), self.scanRange[1]] ] )
		bboxRun.append( [[self.scanRange[0], self.scanRange[2]], [ self.scanRange[3], min(self.cHOrig-1, self.scanRange[3]+1)] ] )
		for xy in bboxRun:
			for x in range(xy[0][0],xy[0][1]):
				for y in range(xy[1][0],xy[1][1]):
					img.setPixel(x,y,QtGui.QColor(255,0,0,255).rgb())
		return img
	def setZoom(self, targetZoom):
		targetW=int(float(self.cWOrig)*targetZoom)
		targetH=int(float(self.cHOrig)*targetZoom)
		targetMax=max(targetW, targetH)
		if targetMax < 15000 and targetMax>0:
			self.cW=targetW
			self.cH=targetH
			self.zoom=targetZoom
			self.win.zoom=targetZoom
			self.drawReachMask()
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
	def drawBrushRadius(self, mode, xy):
		self.buildBrushPixels()
		if mode == 0:
			img=self.curCanvasData.toImage()
			img=img.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			pmap=QtGui.QPixmap.fromImage(img)
			self.img.setPixmap(pmap)
			return
		if len(self.brushEdgePixelData)>0:
			img=self.curCanvasData
			img=img.scaled(self.cWOrig,self.cHOrig, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
			img=img.toImage()
			curBrushPixels=self.brushEdgePixelData
			curBrushPixels=map(lambda x: [ max(0, min(self.cWOrig-1, x[0]+xy[0])), max(0, min(self.cHOrig-1, x[1]+xy[1])) ], curBrushPixels)
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
	def extendReachEdges(self,img=None, tempScanRange=None):
		edgeGrowth=int(self.win.edgeGrowthSlider.value)
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
					curRun=self.edgePixels
					self.win.loopLatch=1
					for e in range(1,edgeGrowth+1):
						self.win.statusBarUpdate("( Press 'Escape' to Cancel ) -- Extending Edge - "+str(e)+" of "+str(edgeGrowth)+" - - Total Edge Pixels - "+str(len(self.edgePixels)), 0, 0)
						QtGui.QApplication.processEvents()
						if self.win.loopLatch==0:
							break;
						curGrowArr=growArr
						refreshRunner=0
						refreshDraw=200
						curExtend=[]
						for xy in curRun:
							for g in curGrowArr:
								refreshRunner+=1
								cur=map(sum,zip(xy,g))
								if cur not in self.reachPixelsBase and cur not in self.edgePixels and cur not in curExtend:
									img.setPixel(cur[0],cur[1],QtGui.QColor(0,0,255,255).rgb())
									curExtend.append(cur)
									if imgLoaded==0:
										tempScanRange[0]=min(tempScanRange[0], cur[0])
										tempScanRange[1]=min(tempScanRange[1], cur[1])
										tempScanRange[2]=max(tempScanRange[2], cur[0])
										tempScanRange[3]=max(tempScanRange[3], cur[1])
								if refreshRunner == refreshDraw:
									refreshDraw+=refreshItter#+int(15*(refreshDraw/refreshItter))
									pmap=QtGui.QPixmap.fromImage(img)
									pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
									self.img.setPixmap(pmap)
									QtGui.QApplication.processEvents()
						self.edgePixels.extend(curExtend)
						curRun=curExtend
						if len(curExtend) == 0:
							break;
					try:
						pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
						self.img.setPixmap(pmap)
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
								if cur in self.reachPixels:
									self.reachPixels.remove(cur)
									img.setPixel(cur[0],cur[1],QtGui.QColor(255,150,0,255).rgb())
									curShrink.append(cur)
								if refreshRunner == refreshDraw:
									pmap=QtGui.QPixmap.fromImage(img)
									refreshDraw+=refreshItter#+int(15*(refreshDraw/refreshItter))
									pmap=pmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
									self.img.setPixmap(pmap)
									QtGui.QApplication.processEvents()
						self.edgePixels.extend(curShrink)
						curRun=curShrink
						
					try:
						pmap=self.drawReachMask(1,1)
						self.img.setPixmap(pmap)
						self.curCanvasData=pmap
					except:
						pass;
					self.win.loopLatch=0
					if imgLoaded==0:
						self.win.statusBarUpdate(" -- Shrinking Edge Completed -- ", 5000, 1)
			else:
				self.extendShrinkEdge=-1
				
			self.rebuildReachPixels(self.reachPixels,1)
			if imgLoaded==0:
				self.scanRange=tempScanRange
				alphaPadding=self.win.sliderAlphaReach.value()
				self.scanRange[0]=max(tempScanRange[0]-alphaPadding, 0) if tempScanRange[0] != self.scanRange[0] else self.scanRange[0]
				self.scanRange[1]=max(tempScanRange[1]-alphaPadding, 0) if tempScanRange[1] != self.scanRange[1] else self.scanRange[1]
				self.scanRange[2]=min(tempScanRange[2]+alphaPadding, self.cWOrig) if tempScanRange[2] != self.scanRange[2] else self.scanRange[2]
				self.scanRange[3]=min(tempScanRange[3]+alphaPadding, self.cHOrig) if tempScanRange[3] != self.scanRange[3] else self.scanRange[3]
				
				#img=self.drawBoundingBox(img)
				self.drawReachMask()
				
				"""pxmap=QtGui.QPixmap.fromImage(img)
				pxmap=pxmap.scaled(self.cW,self.cH, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
				self.img.setPixmap(pxmap)"""
		return img,tempScanRange