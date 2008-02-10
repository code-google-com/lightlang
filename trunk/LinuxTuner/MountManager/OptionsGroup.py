from PyQt4 import Qt
import Button
import Const

class OptionsGroup(Qt.QWidget):
	def __init__(self,popup_widget,parent = None):
		Qt.QWidget.__init__(self,parent)
		
		self.all_combo_boxes = []
		self.all_check_boxes = []
		self.all_spin_boxes = []
		self.all_labels = []
		self.all_lines = []
		
		self.popup_widget = popup_widget
		
		self.current_layout_row = 0
		self.layout = Qt.QGridLayout()
		self.setLayout(self.layout)
		
	def setColumnStretch(self,column):
		self.layout.setColumnStretch(column,1)
	
	def addComboBoxOption(self,default_value,possible_values,options,title,for_expert,doc_mark):
		### Add combo box option with possible values and title ###
		
		if len(options) != len(possible_values):
			print "Error: combo box option \"",title,"\" hasn't number of options, which must be"
			return
		
		combo_box = Qt.QComboBox()
		
		# Add items with options as data of item
		current_index = 0
		for possible_value in possible_values:
			combo_box.addItem(str(possible_value),Qt.QVariant(options[current_index]))
			current_index+=1
			
		# Set current index
		current_index = 0
		for possible_value in possible_values:
			if possible_value == default_value:
				combo_box.setCurrentIndex(current_index)
				break
			current_index+=1
			
		# Create label 
		label = Qt.QLabel(title)
			
		# Create info button
		button = None
		if doc_mark != None:
			button = Button.Button("info","",self.popup_widget,title,doc_mark)
		
		# Add row of widgets to layout
		if doc_mark != None:
			self.layout.addWidget(button,self.current_layout_row,0)
		self.layout.addWidget(label,self.current_layout_row,1)
		self.layout.addWidget(combo_box,self.current_layout_row,2)
	
		self.all_combo_boxes.append([combo_box,label,button,for_expert])
		self.current_layout_row+=1
	
	def addCheckBoxOption(self,title,options,for_expert,doc_mark):
		### Add check box option with possible values and title ###
		
		if len(options) > 2:
			print "Error: check box option \"",title,"\" have much options, as it's possible"
			return
			
		check_box = Qt.QCheckBox(title)
		
		# Create info button
		button = None
	 	if doc_mark != None:
			button = Button.Button("info","",self.popup_widget,title,doc_mark)
			
		# Add widget to layout
	 	if doc_mark != None:
			self.layout.addWidget(button,self.current_layout_row,0)
		self.layout.addWidget(check_box,self.current_layout_row,1,1,2)
		
		self.all_check_boxes.append([check_box,button,options,for_expert])
		self.current_layout_row+=1
		
	def addSpinBoxOption(self,mark,default_value,title,min_value,max_value,for_expert,doc_mark):
		### Add spin box option with possible values and title ###
		
		spin_box = Qt.QSpinBox()
		
		spin_box.setValue(int(default_value))
		spin_box.setMinimum(int(min_value))
		spin_box.setMaximum(int(max_value))
		
		# Create info button
		button = None
	 	if doc_mark != None:
			button = Button.Button("info","",self.popup_widget,title,doc_mark)
			
		# Create label
		label = Qt.QLabel(title)
			
		# Add widget to layout
	 	if doc_mark != None:
			self.layout.addWidget(button,self.current_layout_row,0)
		self.layout.addWidget(label,self.current_layout_row,1)
		self.layout.addWidget(spin_box,self.current_layout_row,2)
		
		self.all_spin_boxes.append([spin_box,label,button,mark,for_expert])
		self.current_layout_row+=1
		
	def addLineOption(self,mark,default_value,is_read_only,title,for_expert,doc_mark):
		
		line = Qt.QLineEdit()
		line.setText(str(default_value))
		line.setReadOnly(is_read_only)
		
		# Create info button
		button = None
	 	if doc_mark != None:
			button = Button.Button("info","",self.popup_widget,title,doc_mark)
			
		# Create label
		label = Qt.QLabel(title)
		
		
		# Add widget to layout
	 	if doc_mark != None:
			self.layout.addWidget(button,self.current_layout_row,0)
		self.layout.addWidget(label,self.current_layout_row,1)
		if mark == "mount_point":
			
			choose_button = Qt.QPushButton()
			choose_button.setIcon(Qt.QIcon(Const.Icons_path + "choose_mount_point.png"))
			
			dialog = Qt.QFileDialog()
			dialog.setFileMode(Qt.QFileDialog.DirectoryOnly)
			self.connect(choose_button,Qt.SIGNAL("clicked()"),dialog.exec_)
			
			temp_layout = Qt.QHBoxLayout()
			temp_layout.addWidget(line)
			temp_layout.addWidget(choose_button)
			self.layout.addLayout(temp_layout,self.current_layout_row,2)
		else:
			self.layout.addWidget(line,self.current_layout_row,2)
		
		self.all_lines.append([line,label,button,mark,for_expert])
		self.current_layout_row+=1
			
		
	def addLabelOption(self,title,value,for_expert,doc_mark):
		
		# Create info button
	 	if doc_mark != None:
			button = Button.Button("info","",self.popup_widget,title,doc_mark)
			self.layout.addWidget(button,self.current_layout_row,0)
		
		label = Qt.QLabel(title)
		label_value = Qt.QLabel(str(value))
		
		self.layout.addWidget(label,self.current_layout_row,1)
		self.layout.addWidget(label_value,self.current_layout_row,2)
		
		self.all_labels.append([label,label_value,for_expert])
		self.current_layout_row+=1
			
		
	def getAllOptionsAsText(self):
		
		text = ""
		
		for combo_box in self.all_combo_boxes:
			text += combo_box[0].itemData(combo_box[0].currentIndex()).toString() + ","
			
		for check_box in self.all_check_boxes:
			if len(check_box[2]) > 1:
				if check_box[0].isChecked():
					text += check_box[2][0]
				else:
					text += check_box[2][1]
			else:
				text += check_box[2]
		
		return text
			
	def getValueByMark(self,mark):
		
		for spin_box in self.all_spin_boxes:
			if mark == spin_box[3]:
				return spin_box[0].value()
			
		for line in self.all_lines:
			if mark == line[3]:
				return line[0].text()
			
		return None
		
	
	def setExpertMode(self,b):
		
		for combo_box in self.all_combo_boxes:
			if combo_box[3] != None and combo_box[3] == True:
				combo_box[0].setVisible(b)
				combo_box[1].setVisible(b)
				if combo_box[2] != None:
					combo_box[2].setVisible(b)
				
		for check_box in self.all_check_boxes:
			if check_box[3] != None and check_box[3] == True:
				check_box[0].setVisible(b)
				if check_box[1] != None:
					check_box[1].setVisible(b)
				
		for spin_box in self.all_spin_boxes:
			if spin_box[4] != None and spin_box[4] == True:
				spin_box[0].setVisible(b)
				spin_box[1].setVisible(b)
				if spin_box[2] != None:
					spin_box[2].setVisible(b)
				
		for line in self.all_lines:
			if line[4] != None and line[4] == True and line[3] != "mount_point":
				line[0].setReadOnly(not b)
		
		for label in self.all_labels:
			if label[2] != None and label[2] == True:
				label[0].setVisible(b)
				label[1].setVisible(b)
				
				