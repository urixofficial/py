from loguru import logger
from PyQt5.QtWidgets import QWidget, QDialog, QTableWidget, QLineEdit, QLabel, QPushButton, QComboBox, QCheckBox, QHBoxLayout, QVBoxLayout, QHeaderView, QDateEdit, QTableWidgetItem
from PyQt5.QtCore import Qt, QRegExp, QDate, QEvent, pyqtSignal
from PyQt5.QtGui import QKeyEvent

class CheckBox(QWidget):

	returnPressed = pyqtSignal()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.checkBox = QCheckBox()
		layout = QHBoxLayout()
		layout.addWidget(self.checkBox)
		layout.setAlignment(Qt.AlignCenter)
		layout.setContentsMargins(0,0,0,0)
		self.setLayout(layout)
		self.setObjectName('checkBox')
		self.setFocusPolicy(Qt.StrongFocus)

	def keyPressEvent(self, event: QKeyEvent) -> None:

		key = event.key()

		if key == Qt.Key_Space:
			if self.checkBox.isChecked() == False:
				self.checkBox.setChecked(True)
			else:
				self.checkBox.setChecked(False)

		elif key == Qt.Key_Return or key == Qt.Key_Enter:
			self.returnPressed.emit()

			# super().keyPressEvent(event)

class EditRowDialog(QDialog):

	def __init__(self, tableInfo, values=[]):
		super().__init__()
		
		# позволяет отслеживать нажатия клавиш в этом окне
		self.setFocusPolicy(Qt.StrongFocus)
		self.setFocus()

		self.tableInfo = tableInfo
		self.values = values
		self.initUI()

	def initUI(self):

		# создание диалога, присвоение имени окна
		self.setWindowTitle('Добавление записи')

		# количество столбцов
		self.cols = len(self.tableInfo)

		# создание таблицы
		self.table = QTableWidget()
		self.table.setColumnCount(self.cols)
		self.table.setRowCount(1)
		self.table.verticalHeader().setVisible(False)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		
		# присвоение заголовков и чтение типов данных
		self.types = []

		# определение первичного ключа
		for i in self.tableInfo:
			if i[5]: 
				self.pkCol = i[0]
				self.pkName = i[1]
				if self.pkName == 'ID':
					self.table.setColumnHidden(i[0], True)
					defaultFocusCol = 1
				else:
					self.table.setColumnHidden(i[0], False)
					defaultFocusCol = 0
				self.table.setHorizontalHeaderItem(i[0], QTableWidgetItem(f'*{i[1]}\n{i[2]}'))
			else:
				self.table.setHorizontalHeaderItem(i[0], QTableWidgetItem(f'{i[1]}\n{i[2]}'))

			self.types.append(i[2])

		# заполнение таблицы в зависимости от типа данных
		for col in range(self.cols):
			if self.types[col] == 'NULL':
				pass
			elif self.types[col] == 'INTEGER':
				self.table.setCellWidget(0, col, QLineEdit())
				self.table.cellWidget(0, col).returnPressed.connect(self.validate)
				if self.values:
					self.table.cellWidget(0, col).setText(self.values[col])

			elif self.types[col] == 'REAL':
				self.table.setCellWidget(0, col, QLineEdit())
				self.table.cellWidget(0, col).returnPressed.connect(self.validate)
				if self.values:
					self.table.cellWidget(0, col).setText(self.values[col])

			elif self.types[col] == 'BOOLEAN':
				self.table.setCellWidget(0, col, CheckBox())
				self.table.cellWidget(0, col).returnPressed.connect(self.validate)
				if self.values:
					value = True if self.values[col] == '1' else False
					self.table.cellWidget(0, col).checkBox.setChecked(value)

			elif self.types[col] == 'DATE':
				if self.values:
					self.table.setCellWidget(0, col, QDateEdit(QDate().fromString(self.values[col], 'yyyy-MM-dd')))
				else:
					self.table.setCellWidget(0, col, QDateEdit(QDate().currentDate()))
				self.table.cellWidget(0, col).setCalendarPopup(True)
				self.table.cellWidget(0, col).setFrame(False)
				# self.table.cellWidget(0, col).returnPressed.connect(self.validate)

			elif self.types[col] == 'BLOB':
				pass
			elif self.types[col] == 'TEXT':
				self.table.setCellWidget(0, col, QLineEdit())
				self.table.cellWidget(0, col).returnPressed.connect(self.validate)
				if self.values:
					self.table.cellWidget(0, col).setText(self.values[col])
				
				# значение по умолчанию
				headerName = self.tableInfo[col][1]
				if headerName == 'Статус':
					self.table.cellWidget(0, col).setText('В работе')


		# self.table.resizeColumnsToContents()
		self.setMinimumWidth(640)

		# кнопки принятия или отклонения окна
		self.okBtn = QPushButton('ОК')
		self.okBtn.setDefault(True)
		self.cancelBtn = QPushButton('Отмена')

		# присоедниение функций к кнопкам
		self.okBtn.clicked.connect(self.validate)
		self.cancelBtn.clicked.connect(self.reject)

		# компоновка
		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(self.okBtn)
		ctrlLayout.addWidget(self.cancelBtn)

		layout = QVBoxLayout()
		layout.addWidget(self.table)
		layout.addLayout(ctrlLayout)
		self.setLayout(layout)

		self.table.cellWidget(0, defaultFocusCol).setFocus()

	def keyPressEvent(self, event: QKeyEvent):

		QDialog.keyPressEvent(self, event)

		if event.key() == Qt.Key_Return:
			self.validate()

		if event.key() == Qt.Key_Escape:
			self.reject()

	def validate(self):

		valid = True
		regex = '[A-Za-zА-Яа-я0-9_]+'

		for col in range(self.cols):
			if self.types[col] == 'NULL':
				pass
			elif self.types[col] == 'INTEGER':
				# если столбец является первычным ключом и в ячейке пустая строка, то все норм - номер назначится автоматически
				if col == self.pkCol and self.table.cellWidget(0, col).text() == '':
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				# проверка на соответствие только цифрам
				elif QRegExp('[0-9]+').exactMatch(self.table.cellWidget(0, col).text()):
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				else:
					valid = False
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(255, 140, 140)')
			elif self.types[col] == 'REAL':
				if QRegExp('[0-9\.]+').exactMatch(self.table.cellWidget(0, col).text()):
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				else:
					valid = False
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(255, 140, 140)')
			elif self.types[col] == 'BOOLEAN':
				pass
			elif self.types[col] == 'DATE':
				pass
			elif self.types[col] == 'BLOB':
				pass
			elif self.types[col] == 'TEXT':
				if QRegExp('[\w\s]+').exactMatch(self.table.cellWidget(0, col).text()):
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				else:
					valid = False
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(255, 140, 140)')

		if valid:

			self.values = []

			for col in range(self.cols):

				widget = self.table.cellWidget(0, col)

				if isinstance(widget, QLineEdit):
					value = widget.text()
					if col == self.pkCol and value == '': value = 'NULL'
					if self.types[col] =='TEXT': value = f'\'{value}\''
					self.values.append(value)
				elif isinstance(widget, CheckBox):
					value = 1 if widget.checkBox.isChecked() else 0
					self.values.append(value)
				elif isinstance(widget, QDateEdit):
					value = widget.date().toString('yyyy-MM-dd')
					self.values.append(f'\'{value}\'')

			self.accept()