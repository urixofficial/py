from PyQt5.QtWidgets import QDialog, QTableWidget, QLineEdit, QLabel, QPushButton, QComboBox, QHBoxLayout, QGridLayout, QHeaderView
from PyQt5.QtCore import QRegExp

class AddTableDialog(QDialog):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.initUI()

	def initUI(self):

		# создание диалога, присвоение имени окна
		self.setWindowTitle('Добавление таблицы')

		self.fieldsTable = QTableWidget()
		self.fieldsTable.setColumnCount(2)
		self.fieldsTable.setRowCount(0)
		self.fieldsTable.verticalHeader().setVisible(False)
		self.fieldsTable.setHorizontalHeaderLabels(['Поле', 'Тип данных'])
		self.fieldsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		# создание элементов формы
		self.tableNameEdit = QLineEdit()
		# dialog.tableNameEdit.setValidator(QRegExpValidator(QRegExp('\\w+')))

		# кнопки принятия или отклонения окна
		self.addFieldBtn = QPushButton('+')
		self.delFieldBtn = QPushButton('-')
		self.addOkBtn = QPushButton('ОК')
		self.addCanceldBtn = QPushButton('Отмена')

		# присоедниение функций к кнопкам
		self.addFieldBtn.clicked.connect(self.addField)
		self.delFieldBtn.clicked.connect(self.delField)
		self.addOkBtn.clicked.connect(self.validate)
		self.addCanceldBtn.clicked.connect(self.reject)

		# компоновка
		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(self.addFieldBtn)
		ctrlLayout.addWidget(self.delFieldBtn)
		ctrlLayout.addWidget(self.addOkBtn)
		ctrlLayout.addWidget(self.addCanceldBtn)

		layout = QGridLayout()
		layout.addWidget(QLabel('Имя таблицы:'), 0, 0)
		layout.addWidget(self.tableNameEdit, 0, 1)
		layout.addWidget(self.fieldsTable, 1, 0, 1, 2)
		layout.addWidget(QLabel('*имена не должны начинаться с цифр, содержать пробелы или спецсимволы'), 2, 0, 1, 2)
		layout.addLayout(ctrlLayout, 3, 0, 1, 2)
		self.setLayout(layout)

		self.resize(self.sizeHint())


	def addField(self):
		row = self.fieldsTable.rowCount()
		self.fieldsTable.setRowCount(row+1)
		self.fieldsTable.setCellWidget(row, 0, QLineEdit())
		self.fieldsTable.setCellWidget(row, 1, QComboBox())
		self.fieldsTable.cellWidget(row, 1).addItems(['INTEGER', 'REAL', 'TEXT'])

	def delField(self):
		row = self.fieldsTable.currentRow()
		self.fieldsTable.removeRow(row)

	def validate(self):

		valid = True
		regex = '[^0-9][A-Za-zА-Яа-я0-9_]+'

		if QRegExp(regex).exactMatch(self.tableNameEdit.text()):
			self.tableNameEdit.setStyleSheet('background-color: rgb(140, 255, 140)')
		else:
			valid = False
			self.tableNameEdit.setStyleSheet('background-color: rgb(255, 140, 140)')

		for row in range(self.fieldsTable.rowCount()):
			if QRegExp(regex).exactMatch(self.fieldsTable.cellWidget(row, 0).text()):
				self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(140, 255, 140)')
			else:
				valid = False
				self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(255, 140, 140)')

		if valid:

			self.table = self.tableNameEdit.text()

			fields = []
			for row in range(self.fieldsTable.rowCount()):
				fieldName = self.fieldsTable.cellWidget(row,0).text()
				fieldType = self.fieldsTable.cellWidget(row,1).currentText()
				fields.append(' '.join([fieldName, fieldType]))
			self.fields = ', '.join(fields)

			self.accept()