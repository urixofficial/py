from loguru import logger
from PyQt5.QtWidgets import QDialog, QFileDialog, QPushButton, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem, QComboBox

# добавить непосредственно импорт

class ImportCSV(QDialog):

	def __init__(self, fields, *args, **kwargs):
		
		super().__init__(*args, **kwargs)
		self.fields = fields
		self.initUI()

	def initUI(self):

		logger.info('Отрисовка интерфейса')

		# создание диалога, присвоение имени окна
		self.setWindowTitle('Импорт из CSV')

		# таблица предпросмотра
		self.previewTable = QTableWidget()
		self.previewTable.setColumnCount(0)
		self.previewTable.setRowCount(0)
		self.previewTable.verticalHeader().setVisible(False)
		self.previewTable.horizontalHeader().setVisible(False)

		# кнопки
		self.getPathBtn = QPushButton('Выбрать файл')
		self.addOkBtn = QPushButton('ОК')
		self.addCanceldBtn = QPushButton('Отмена')

		# присоедниение функций к кнопкам
		self.getPathBtn.clicked.connect(self.openFile)
		self.addOkBtn.clicked.connect(self.validate)
		self.addCanceldBtn.clicked.connect(self.reject)

		# компоновка
		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(self.addOkBtn)
		ctrlLayout.addWidget(self.addCanceldBtn)

		layout = QGridLayout()
		layout.addWidget(self.getPathBtn, 0, 0)
		layout.addWidget(self.previewTable, 1, 0)
		layout.addLayout(ctrlLayout, 2, 0)
		self.setLayout(layout)

	def openFile(self):

		logger.info('Открытие файла')

		self.csvPath = QFileDialog.getOpenFileName(self, 'Open file', '', 'CSV (*.csv)')[0]

		try:
			with open(self.csvPath, 'r', encoding='1251') as file:
				data = []
				for i in range(5):
					line = file.readline()
					if line != '' or line != '\n':
						data.append(line.rstrip('\n').split(';'))
		except Exception as e:
			print(e)
			return

		rows, cols = len(data), len(data[0])

		self.previewTable.setRowCount(rows)
		self.previewTable.setColumnCount(cols)

		for col in range(cols):
			self.previewTable.setCellWidget(0, col, QComboBox())
			self.previewTable.cellWidget(0, col).addItem('Не импортировать')
			self.previewTable.cellWidget(0, col).addItems(self.fields)

		for row in range(1, rows):
			for col in range(cols):
				self.previewTable.setItem(row, col, QTableWidgetItem(data[row][col]))

		self.previewTable.resizeColumnsToContents()
		self.resize(self.sizeHint())

	def validate(self):

		logger.info('Валидация')

		rows, cols = self.previewTable.rowCount(), self.previewTable.columnCount()

		for field in self.fields:
			matchList = []
			for col in range(cols):
				if self.previewTable.cellWidget(0, col).currentText() == field:
					matchList.append(col)
			if len(matchList) > 1:
				for col in matchList:
					self.previewTable.cellWidget(0, col).setStyleSheet('background: red;')
				return

		# self.headers = [self.previewTable.cellWidget(0, col).currentText() for col in range(cols) if self.previewTable.cellWidget(0, col).currentIndex() != 0]
		
		colsToImport = [col for col in range(cols) if self.previewTable.cellWidget(0, col).currentIndex() != 0]
		self.headers = [self.previewTable.cellWidget(0, col).currentText() for col in colsToImport]
		self.data = []

		with open(self.csvPath, 'r', encoding='1251') as file:
			lines = file.read().splitlines()
			for line in lines:
				filteredLine = [line.split(';')[i] for i in colsToImport]
				self.data.append(filteredLine)

		self.accept()
				
			

