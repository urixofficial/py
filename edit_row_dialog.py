from loguru import logger

from PyQt5.QtWidgets import QDialog, QTableWidget, QLineEdit, QPushButton, QVBoxLayout, \
	QHeaderView, QDateEdit, QTableWidgetItem, QLabel
from PyQt5.QtCore import QDate, QRegExp

from sqlite_handler import *
from check_box import *
from config import *


class EditRowDialog(QDialog):

	def __init__(self, dbPath, tableName, values=[]):
		super().__init__()

		logger.info('Инициализация')
		
		# позволяет отслеживать нажатия клавиш в этом окне
		self.setFocusPolicy(Qt.StrongFocus)
		self.setFocus()

		self.dbPath = dbPath
		self.tableName = tableName
		self.tableInfo = getTableInfo(dbPath, tableName)
		self.values = values
		self.initUI()

	def initUI(self):

		logger.info('Отрисовка интерфейса')

		# создание диалога, присвоение имени окна
		self.setWindowTitle('Добавление записи')

		self.setMinimumWidth(EDIT_ROW_WIDTH)
		self.setMinimumHeight(EDIT_ROW_HEIGHT)

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

		# столбец в фокусе по умолчанию
		defaultFocusCol = 0

		# определение первичного ключа
		for i in self.tableInfo:
			if i[5]: 
				self.pkCol = i[0]
				self.pkName = i[1]
				if self.pkName == 'ID':
					self.table.setColumnHidden(i[0], True)
					defaultFocusCol = 1

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

		self.table.resizeColumnsToContents()

		# статусбар
		self.info = QLabel()
		self.info.setAlignment(Qt.AlignCenter)

		# кнопки принятия или отклонения окна
		self.okBtn = QPushButton('ОК')
		self.okBtn.setDefault(True)
		self.cancelBtn = QPushButton('Отмена')

		# присоединение функций к кнопкам
		self.okBtn.clicked.connect(self.validate)
		self.cancelBtn.clicked.connect(self.reject)

		# компоновка
		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(self.okBtn)
		ctrlLayout.addWidget(self.cancelBtn)

		layout = QVBoxLayout()
		layout.addWidget(self.table)
		layout.addWidget(self.info)
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

		logger.info('Проверка введенных данных')

		valid = True
		status = ''

		# Проверка на уникальность ID
		if self.pkName != 'ID':
			id = self.table.cellWidget(0, self.pkCol).text()
			sqlRequest = f'SELECT rowid FROM {self.tableName} WHERE rowid={id}'
			idCheck = str(sqlExec(self.dbPath, sqlRequest)[0][0])
			if idCheck == id:
				valid = False
				self.table.cellWidget(0, self.pkCol).setStyleSheet('background-color: rgb(255, 140, 140)')
				logger.warning('Значение ID не уникально')
				status += '\nЗначение ID не уникально'

		regex = '[A-Za-zА-Яа-я0-9_]+'

		# Проверка по типам данных
		for col in range(self.cols):
			if self.types[col] == 'NULL':
				pass
			elif self.types[col] == 'INTEGER':
				# если столбец является первичным ключом и в ячейке пустая строка, то все норм - номер назначится автоматически
				if col == self.pkCol:
					if self.table.cellWidget(0, col).text() == '':
						self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				# проверка на соответствие только цифрам
				elif QRegExp('[0-9]+').exactMatch(self.table.cellWidget(0, col).text()):
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				else:
					valid = False
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(255, 140, 140)')
					status += '\nПоле не должно быть пустым или содержать не цифры'
			elif self.types[col] == 'REAL':
				if QRegExp('[0-9\.]+').exactMatch(self.table.cellWidget(0, col).text()):
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(140, 255, 140)')
				else:
					valid = False
					self.table.cellWidget(0, col).setStyleSheet('background-color: rgb(255, 140, 140)')
					status += '\nПоле не должно быть пустым или содержать не цифры'
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
					status += '\nПоле не должно быть пустым или содержать спецсимволы'

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
					self.values.append(f'{value}')

			self.accept()
		else:
			self.info.setText(status)