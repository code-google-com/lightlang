from PyQt4 import Qt

class Menu(Qt.QMenu) :
	def __init__(self, icon = None, text = None, parent = None) :
		Qt.QMenu.__init__(self, parent)
		
		self.caption_action = Qt.QWidgetAction(self)
		self.caption_action.setEnabled(False)

		self.caption_action_frame = Qt.QFrame()
		try : # FIXME: Check Qt.QFrameStyledPanel in PyQt-4.2
				self.caption_action_frame.setFrameShape(Qt.QFrame.StyledPanel) # Liksys Fix for KDE4
		except :
				self.caption_action_frame.setFrameShape(Qt.QFrame.Box) # KDE4
		self.caption_action.setDefaultWidget(self.caption_action_frame)

		self.caption_action_frame_layout = Qt.QHBoxLayout()
		self.caption_action_frame_layout.setMargin(3)
		self.caption_action_frame_layout.setSpacing(3)
		self.caption_action_frame.setLayout(self.caption_action_frame_layout)

		self.caption_action_icon_label = Qt.QLabel()
		icon_size = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		if icon != None:
			self.caption_action_icon_label.setPixmap(icon.pixmap(Qt.QSize(icon_size, icon_size)))
		self.caption_action_frame_layout.insertWidget(-1, self.caption_action_icon_label, 0)

		self.caption_action_label = Qt.QLabel()
		if text != None:
			self.caption_action_label.setText(text)
		self.caption_action_frame_layout.insertWidget(-1, self.caption_action_label, 20)

		font = self.caption_action_label.font()
		font.setBold(True)
		self.caption_action_label.setFont(font)

		self.addAction(self.caption_action)
		 		    
        ### Public ###

	def setCaption(self,text) :
		self.caption_action_label.setText(text)