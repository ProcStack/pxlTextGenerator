### Might be good to keep internal to main window class
### But needed elsewhere and easy to find here
def ClearLayout(layout):
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
			
######
### Added late in the game
### I'll convert over all other slider groups to this in the future
### Will take some time is all
### Leaving them be for now
######
### SliderGroup(self,"Random Seed", [0,200,0],"float","%")
class SliderGroup(QtGui.QWidget):	
	def __init__(self, win,title,minMaxVal,padding,type,suffix,function=None):
		QtGui.QWidget.__init__(self)
		self.win=win
		self.title=title
		self.text=''
		self.suffix=suffix
		self.type=type
		self.min=minMaxVal[0]
		self.max=minMaxVal[1]
		if self.type == "float":
			self.max=minMaxVal[1]*100
		self.value=minMaxVal[2]
		self.function=function
		self.editTextMode=0
		self.runEvents=0
	
		sliderBlock=QtGui.QHBoxLayout()
		sliderBlock.setSpacing(0)
		sliderBlock.setMargin(0) 
		sliderTitle=QtGui.QLabel()
		sliderTitle.setText(self.title)
		sliderTitle.setStyleSheet("QLabel {margin:"+str(padding)+"px;}")
		sliderBlock.addWidget(sliderTitle)
		###
		self.slider=QtGui.QSlider()
		self.slider.setOrientation(QtCore.Qt.Horizontal)
		self.slider.setMinimum(self.min)
		self.slider.setMaximum(self.max)
		self.slider.setValue(self.value)
		self.slider.valueChanged.connect(self.sliderChange)
		sliderBlock.addWidget(self.slider)
		###
		self.sliderValueTextBlock=QtGui.QHBoxLayout()
		self.sliderValueText=QtGui.QLabel()
		self.sliderValueText.setFixedWidth(80)
		self.sliderValueText.setAlignment(QtCore.Qt.AlignCenter)
		self.setValueText()
		self.sliderValueText.mousePressEvent=self.valueTextPress
		self.sliderValueTextBlock.addWidget(self.sliderValueText)
		sliderBlock.addLayout(self.sliderValueTextBlock)
		self.runEvents=1
		self.setLayout(sliderBlock)
	def valueTextPress(self, e):
		if self.editTextMode==0:
			ClearLayout(self.sliderValueTextBlock)
			self.sliderValueTextEdit=QtGui.QLineEdit()
			self.sliderValueTextEdit.setFixedWidth(80)
			self.sliderValueTextEdit.setAlignment(QtCore.Qt.AlignCenter)
			text=self.value
			if self.type == "float":
				text=self.value/100.0
			text=str(text)
			self.sliderValueTextEdit.setText(text)
			self.sliderValueTextEdit.setStyleSheet("QLineEdit {selection-color:#ffffff;selection-background-color:#454545;background-color:#909090;}")
			self.sliderValueTextEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
			
			self.sliderValueTextEdit.editingFinished.connect(self.valueTextDone)
			self.sliderValueTextBlock.addWidget(self.sliderValueTextEdit)
			self.sliderValueTextEdit.setFocus()
			self.sliderValueTextEdit.selectAll()
			self.editTextMode=1
	def valueTextDone(self):
		self.sliderValueTextEdit.editingFinished.disconnect(self.valueTextDone)
		val=self.sliderValueTextEdit.text()
		if self.type == "float":
			if "." in val:
				varr=map(str, val.split("."))
				varr[1]=varr[1][0:2].ljust(2,"0")
				val=int(varr[0]+varr[1])
			else:
				val=int(val)*100
		else:
			val=int(val)
		self.value=val
		ClearLayout(self.sliderValueTextBlock)
		self.sliderValueText=QtGui.QLabel()
		self.sliderValueText.setFixedWidth(80)
		self.sliderValueText.setAlignment(QtCore.Qt.AlignCenter)
		self.sliderValueText.mousePressEvent=self.valueTextPress
		self.sliderValueTextBlock.addWidget(self.sliderValueText)
		self.slider.setValue(-1)
		self.editTextMode=0
		self.slider.setValue(val)
	def sliderChange(self):
		self.setValueText()
		if self.function != None:
			eval("self.win."+self.function)
	def setValueText(self,val=None):
		if val == None:
			val=self.slider.value()
		self.value=val
		if self.type == "float":
			valText=str(float(val)/100.0)+self.suffix
			self.sliderValueText.setText(valText)
			self.text=valText
		if self.type == "int":
			valText=str(val)+self.suffix
			self.sliderValueText.setText(valText)
			self.text=valText
			
class HorizontalBar(QtGui.QFrame):	
	def __init__(self):
		QtGui.QFrame.__init__(self)
		self.setFrameShape(QtGui.QFrame.HLine)
		self.setFrameShadow(QtGui.QFrame.Sunken)
		#self.setLineWidth(thickness)
		
class HorizontalBarCustom(QtGui.QWidget):	
	def __init__(self,offset,size):
		QtGui.QWidget.__init__(self)
		if type == "float":
			self.max=minMaxVal[1]*100
		self.value=minMaxVal[2]
	
		hBarBlock=QtGui.QHBoxLayout()
		hBarBlock.setSpacing(0)
		hBarBlock.setMargin(0)
		#self.setFrameShape(QtGui.QFrame.HLine)
		#self.setFrameShadow(QtGui.QFrame.Sunken)
		#hBarBlock.addWidget(self.hBar)
		self.setLayout(hBarBlock)