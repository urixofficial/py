from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout, QGroupBox, QComboBox, QSpinBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QLineEdit, QDateEdit, QPushButton, QCheckBox
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, Qt

class addRowDialog(QWidget):

	def __init__(self):

		super().__init__()
		self.logging = True
		self.initUI()

	def initUI(self):

		if self.logging: print('Отрисовка диалога')

		now = QDate.currentDate()

		self.dateEdit = QDateEdit()
		self.dateEdit.setDate(now)
		self.idEdit = QLineEdit()
		self.modelBox = QComboBox()
		self.modelBox.addItems(('725/85A', '737/83A/X', '712/35A', '728/78A', '80A/X', 'Samsung'))
		self.fillBox = QCheckBox()
		self.drumChangeBox = QCheckBox()
		self.magnetChangeBox = QCheckBox()
		self.statusBox = QComboBox()
		self.statusBox.addItems(('В работе', 'В резерве', 'Списан'))

		self.okBtn = QPushButton('OK')
		self.cancelBtn = QPushButton('Отмена')

		mainLayout = QGridLayout()
		mainLayout.addWidget(QLabel('Дата'),0,0)
		mainLayout.addWidget(self.dateEdit,1,0)
		mainLayout.addWidget(QLabel('Идентификатор'),0,1)
		mainLayout.addWidget(self.idEdit,1,1)
		mainLayout.addWidget(QLabel('Модель'),0,2)
		mainLayout.addWidget(self.modelBox,1,2)
		mainLayout.addWidget(QLabel('Заправка'),0,3)
		mainLayout.addWidget(self.fillBox,1,3)
		mainLayout.addWidget(QLabel('Замена\nфотобарабана'),0,4)
		mainLayout.addWidget(self.drumChangeBox,1,4)
		mainLayout.addWidget(QLabel('Замена\nмагнитного вала'),0,5)
		mainLayout.addWidget(self.magnetChangeBox,1,5)
		mainLayout.addWidget(QLabel('Статус'),0,6)
		mainLayout.addWidget(self.statusBox,1,6)
		mainLayout.addWidget(self.okBtn,2,5)
		mainLayout.addWidget(self.cancelBtn,2,6)

		self.setLayout(mainLayout)