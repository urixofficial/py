from loguru import logger
from PyQt5.QtWidgets import QWidget, QDialog, QTableWidget, QLineEdit, QLabel, QPushButton, QComboBox, QCheckBox, QHBoxLayout, QGridLayout, QHeaderView, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt, QRegExp

class CheckBox(QWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.checkBox = QCheckBox()
		layout = QHBoxLayout()
		layout.addWidget(self.checkBox)
		layout.setAlignment(Qt.AlignCenter)
		layout.setContentsMargins(0,0,0,0)
		self.setLayout(layout)


class EditTableDialog(QDialog):

	def __init__(self, dbPath, tableName, tableInfo):
		super().__init__()
		self.tableName = tableName
		self.tableInfo = tableInfo

		# количество столбцов
		self.cols = len(self.tableInfo)

		# 0 - порядковый номер
		# 1 - иня
		# 2 - тип данных
		# 5 - первичный ключ

		# self.primaryKey = -1
		self.initUI()

	def initUI(self):

		logger.info('Отрисовка интерфейса')

		# создание диалога, присвоение имени окна
		self.setWindowTitle(f'Редактирование таблицы')

		# создание элементов формы
		self.tableNameEdit = QLineEdit()
		self.tableNameEdit.setText(self.tableName)

		self.fieldsTable = QTableWidget()
		self.fieldsTable.setColumnCount(3)
		self.fieldsTable.setRowCount(0)
		self.fieldsTable.verticalHeader().setVisible(False)
		self.fieldsTable.setHorizontalHeaderLabels(['Поле', 'Тип данных', 'Главный ключ'])
		self.fieldsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.fieldsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
		self.fieldsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
		
		# заполнение таблицы данными
		self.fieldsTable.setRowCount(self.cols)

		for item in self.tableInfo:
			self.fieldsTable.setCellWidget(item[0], 0, QLineEdit(item[1]))
			self.fieldsTable.setCellWidget(item[0], 1, QLabel(item[2]))
			self.fieldsTable.cellWidget(item[0], 1).setAlignment(Qt.AlignCenter)
			self.fieldsTable.setCellWidget(item[0], 2, QLabel(str(item[5])))
			self.fieldsTable.cellWidget(item[0], 2).setAlignment(Qt.AlignCenter)

		# кнопки принятия или отклонения окна
		self.addOkBtn = QPushButton('ОК')
		self.addCanceldBtn = QPushButton('Отмена')

		# присоедниение функций к кнопкам
		self.addOkBtn.clicked.connect(self.validate)
		self.addCanceldBtn.clicked.connect(self.reject)

		info = QLabel('*имена не должны начинаться с цифр, содержать пробелы или спецсимволы\nобязателено наличие одного главного ключа')
		info.setAlignment(Qt.AlignCenter)

		# компоновка
		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(self.addOkBtn)
		ctrlLayout.addWidget(self.addCanceldBtn)

		layout = QGridLayout()
		layout.addWidget(QLabel('Имя таблицы:'), 0, 0)
		layout.addWidget(self.tableNameEdit, 0, 1)
		layout.addWidget(self.fieldsTable, 1, 0, 1, 2)
		layout.addWidget(info, 2, 0, 1, 2)
		layout.addLayout(ctrlLayout, 3, 0, 1, 2)
		self.setLayout(layout)


	def addField(self):

		logger.info('Добавление строки')

		rows = self.fieldsTable.rowCount()

		self.fieldsTable.setRowCount(rows+1)
		self.fieldsTable.setCellWidget(rows, 0, QLineEdit())
		self.fieldsTable.setCellWidget(rows, 1, QComboBox())
		self.fieldsTable.cellWidget(rows, 1).addItems(['INTEGER', 'REAL', 'BOOLEAN', 'DATE', 'TEXT'])
		self.fieldsTable.setCellWidget(rows, 2, CheckBox())
		if self.primaryKey > -1:
			self.fieldsTable.cellWidget(rows, 2).setEnabled(False)
		self.fieldsTable.cellWidget(rows, 2).checkBox.stateChanged.connect(lambda state: self.keyCheck(rows, state))

		# self.fieldsTable.resizeColumnsToContents()

	def delField(self):

		logger.info('Удаление строки')

		rows = self.fieldsTable.rowCount()
		self.fieldsTable.setRowCount(rows-1)

	def validate(self):

		valid = True
		regex = '[^0-9][A-Za-zА-Яа-я0-9_]+'
		rows = self.fieldsTable.rowCount()

		# название таблицы
		if QRegExp(regex).exactMatch(self.tableNameEdit.text()):
			self.tableNameEdit.setStyleSheet('background-color: rgb(140, 255, 140)')
		else:
			valid = False
			self.tableNameEdit.setStyleSheet('background-color: rgb(255, 140, 140)')

		# названия полей
		for row in range(rows):
			if QRegExp(regex).exactMatch(self.fieldsTable.cellWidget(row, 0).text()):
				self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(140, 255, 140)')
			else:
				valid = False
				self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(255, 140, 140)')

		# если проверка пройдена, то прочитать и сохранить значения, принять окно
		if valid:
			self.tableName = self.tableNameEdit.text()
			self.tableHeaders = [self.fieldsTable.cellWidget(row, 0).text() for row in range(rows)]
			self.accept()