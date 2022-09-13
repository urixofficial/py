import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QApplication, QFileDialog

from edit_row_dialog import *
from edit_table_dialog import *
from header_filter import *
from import_dialog import *
from new_table_dialog import *
from sqlite_handler import *
from config import *

class MainWindow(QWidget):

	def __init__(self) -> None:

		super().__init__()
		self.initUI()

	def initUI(self) -> None:

		logger.info('Отрисовка интерфейса')

		# ============================ Управление ==========================================

		self.tablesBox = QComboBox()
		self.tablesBox.currentIndexChanged.connect(
			lambda: self.showTable(DEFAULT_DB_PATH, self.tablesBox.currentText()))
		addTableBtn = QPushButton()
		addTableBtn.setObjectName('control')
		addTableBtn.setToolTip('Добавить таблицу')
		addTableBtn.setIcon(QIcon('pic/add_table.png'))
		addTableBtn.setIconSize(QSize(32, 32))
		addTableBtn.clicked.connect(lambda: self.addTable(DEFAULT_DB_PATH))

		delTableBtn = QPushButton()
		delTableBtn.setObjectName('control')
		delTableBtn.setToolTip('Удалить таблицу')
		delTableBtn.setIcon(QIcon('pic/del_table.png'))
		delTableBtn.setIconSize(QSize(32, 32))
		delTableBtn.clicked.connect(lambda: self.delTable(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		editTableBtn = QPushButton()
		editTableBtn.setObjectName('control')
		editTableBtn.setToolTip('Редактировать таблицу')
		editTableBtn.setIcon(QIcon('pic/edit_table.png'))
		editTableBtn.setIconSize(QSize(32, 32))
		editTableBtn.clicked.connect(lambda: self.editTable(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		addRowBtn = QPushButton()
		addRowBtn.setObjectName('control')
		addRowBtn.setToolTip('Добавить запись')
		addRowBtn.setIcon(QIcon('pic/add_row.png'))
		addRowBtn.setIconSize(QSize(32, 32))
		addRowBtn.clicked.connect(lambda: self.addRow(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		delRowBtn = QPushButton()
		delRowBtn.setObjectName('control')
		delRowBtn.setToolTip('Удалить запись')
		delRowBtn.setIcon(QIcon('pic/del_row.png'))
		delRowBtn.setIconSize(QSize(32, 32))
		delRowBtn.clicked.connect(lambda: self.delRow(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		editRowBtn = QPushButton()
		editRowBtn.setObjectName('control')
		editRowBtn.setToolTip('Редактировать запись')
		editRowBtn.setIcon(QIcon('pic/edit_row.png'))
		editRowBtn.setIconSize(QSize(32, 32))
		editRowBtn.clicked.connect(lambda: self.editRow(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		importCSVBtn = QPushButton()
		importCSVBtn.setObjectName('control')
		importCSVBtn.setToolTip('Импорт из CSV')
		importCSVBtn.setIcon(QIcon('pic/import.png'))
		importCSVBtn.setIconSize(QSize(32, 32))
		importCSVBtn.clicked.connect(lambda: self.importCSV(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		exportCSVBtn = QPushButton()
		exportCSVBtn.setObjectName('control')
		exportCSVBtn.setToolTip('Экспорт в CSV')
		exportCSVBtn.setIcon(QIcon('pic/export.png'))
		exportCSVBtn.setIconSize(QSize(32, 32))
		exportCSVBtn.clicked.connect(lambda: self.exportCSV(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(self.tablesBox)
		ctrlLayout.addWidget(addTableBtn)
		ctrlLayout.addWidget(delTableBtn)
		ctrlLayout.addWidget(editTableBtn)
		ctrlLayout.addWidget(addRowBtn)
		ctrlLayout.addWidget(delRowBtn)
		ctrlLayout.addWidget(editRowBtn)
		ctrlLayout.addWidget(importCSVBtn)
		ctrlLayout.addWidget(exportCSVBtn)

		# ============================ Таблица =============================================

		self.dbTable = QTableWidget()
		self.dbTable.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.dbTable.verticalHeader().setVisible(False)
		# self.dbTable.horizontalHeader().setVisible(False)
		self.dbTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		# self.dbTable.horizontalHeader().sectionClicked.connect(self.showFilter)
		self.dbTable.doubleClicked.connect(lambda: self.editRow(DEFAULT_DB_PATH, self.tablesBox.currentText()))

		# создание заголовока
		horizontalHeader = FilterHeader(self.dbTable)

		horizontalHeader.filterActivated.connect(
			lambda: self.showTableContents(DEFAULT_DB_PATH, self.tablesBox.currentText()))
		self.dbTable.setHorizontalHeader(horizontalHeader)

		# ============================ Общая компоновка ====================================

		self.statusBar = QLabel()

		mainLayout = QVBoxLayout()
		mainLayout.addLayout(ctrlLayout)
		mainLayout.addWidget(self.dbTable)
		mainLayout.addWidget(self.statusBar)

		self.setLayout(mainLayout)

		self.resize(MIN_WIDTH, MIN_HEIGHT)

		self.updateForm(DEFAULT_DB_PATH)

		self.show()

	def updateForm(self, dbPath: str) -> None:

		logger.info('Обновление формы')

		sqlRequest = f'SELECT name FROM sqlite_master WHERE type="table";'
		items = sqlExec(dbPath, sqlRequest)
		tables = [table[0] for table in items if not table[0].startswith('sqlite_')]

		self.tablesBox.clear()
		self.tablesBox.addItems(tables)

	def showTable(self, dbPath: str, tableName: str) -> None:

		if tableName == '':
			return

		logger.info(f'Вывод заголовков таблицы {tableName}')

		# получение информации о таблице
		tableInfo = getTableInfo(dbPath, tableName)

		# количество столбцов
		self.cols = len(tableInfo)
		self.dbTable.setColumnCount(self.cols)

		self.headers = [col[1] for col in tableInfo]
		self.pkCol = [col[0] for col in tableInfo if col[5]][0]

		# заполнение
		for i in tableInfo:

			colIndex = i[0]
			colName = i[1]
			colPK = i[5]

			# проверка на первичный ключ
			if colPK:

				# скрыть столбец с именем ID
				if colName == 'ID':
					self.dbTable.setColumnHidden(colIndex, True)
				else:
					self.dbTable.setColumnHidden(colIndex, False)

				self.dbTable.setHorizontalHeaderItem(colIndex, QTableWidgetItem(f'*{colName}'))
			else:
				self.dbTable.setHorizontalHeaderItem(colIndex, QTableWidgetItem(f'{colName}'))

		self.dbTable.horizontalHeader().setFilterBoxes(self.cols)

		self.showTableContents(dbPath, tableName)
		self.dbTable.clearSelection()

	def showTableContents(self, dbPath: str, tableName: str, sort=1) -> None:

		logger.info(f'Вывод содержимого таблицы {tableName}')

		filtersText = [self.dbTable.horizontalHeader().filterText(col) for col in range(self.cols)]
		filterString = ' AND '.join(
			[f'{self.headers[col]} LIKE "%{filtersText[col]}%"' for col in range(self.cols) if filtersText[col]])

		sqlRequest = f'SELECT * FROM {tableName}'
		if filterString:
			sqlRequest += f' WHERE {filterString}'
		if sort:
			sqlRequest += f' ORDER BY {sort}'

		logger.info(sqlRequest)

		sqlAnswer = sqlExec(dbPath, sqlRequest)

		# количество строк
		self.rows = len(sqlAnswer)
		self.dbTable.setRowCount(self.rows)

		self.statusBar.setText(f'Количество записей: {self.rows}')
		self.statusBar.setObjectName('statusBar')

		# внесение данных в таблицу
		for row in range(self.rows):
			for col in range(self.cols):
				self.dbTable.setItem(row, col, QTableWidgetItem(str(sqlAnswer[row][col])))
				self.dbTable.item(row, col).setTextAlignment(Qt.AlignCenter)
				self.dbTable.item(row, col).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

	def addTable(self, dbPath: str) -> None:

		dialog = NewTableDialog()

		if dialog.exec_():
			logger.info(f'Добавление таблицы {dialog.tableName} со столбцами {dialog.tableHeaders}')

			sqlRequest = f'CREATE TABLE IF NOT EXISTS {dialog.tableName} ({dialog.tableHeaders})'
			sqlExec(dbPath, sqlRequest, True)

			self.updateForm(dbPath)
			self.tablesBox.setCurrentText(dialog.tableName)

	def delTable(self, dbPath: str, table: str) -> None:

		logger.info(f'Удаление таблицы {table}')

		# создание диалога, присвоение имени окна
		dialog = QDialog(self)
		dialog.setWindowTitle('Удаление таблицы')

		message = QLabel(f'Вы точно хотите удалить таблицу {table}?')
		okBtn = QPushButton('ОК')
		canceldBtn = QPushButton('Отмена')

		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(okBtn)
		ctrlLayout.addWidget(canceldBtn)

		okBtn.clicked.connect(dialog.accept)
		canceldBtn.clicked.connect(dialog.reject)

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(message)
		mainLayout.addLayout(ctrlLayout)

		dialog.setLayout(mainLayout)

		dialog.resize(dialog.sizeHint())

		if dialog.exec_() == dialog.Accepted:
			# внесение изменений в БД
			sqlRequest = f'DROP TABLE {table}'
			sqlExec(dbPath, sqlRequest, True)

			# обновить форму
			self.updateForm(dbPath)

	def editTable(self, dbPath: str, tableName: str) -> None:

		tableInfo = getTableInfo(dbPath, tableName)

		dialog = EditTableDialog(dbPath, tableName, tableInfo)

		if dialog.exec_():

			logger.info(f'Изменение таблицы {tableName}')

			# изменение имени таблицы
			if tableName != dialog.tableName:
				logger.info(f'Изменение имени таблицы на {dialog.tableName}')

				sqlRequest = f'ALTER TABLE {tableName} RENAME TO {dialog.tableName}'
				sqlExec(dbPath, sqlRequest, True)

				tableName = dialog.tableName
				self.updateForm(dbPath)

				# выбрать вновь созданную таблицу
				self.tablesBox.setCurrentText(tableName)

			# изменение имен столбцов
			for i in tableInfo:
				index = i[0]
				oldHeader = i[1]
				newHeader = dialog.tableHeaders[index]
				if oldHeader != newHeader:
					logger.info(f'Изменение имени столбца {oldHeader} на {newHeader}')

					sqlRequest = f'ALTER TABLE {dialog.tableName} RENAME COLUMN {oldHeader} TO {newHeader}'
					sqlExec(dbPath, sqlRequest, True)

					self.showTable(dbPath, tableName)

	def addRow(self, dbPath: str, tableName: str) -> None:

		logger.info(f'Добавление записи')

		dialog = EditRowDialog(dbPath, tableName)

		if dialog.exec_():
			logger.info(f'Внесение данных {dialog.values}')

			# формирование списков заголовков и данных
			headers = ', '.join([header for header in self.headers])
			values = ', '.join(f'{value}' for value in dialog.values)

			sqlRequest = f'INSERT OR IGNORE INTO {tableName} ({headers}) VALUES ({values});'
			sqlExec(dbPath, sqlRequest, True)

			# обновить таблицу
			self.showTable(dbPath, tableName)

	def delRow(self, dbPath: str, tableName: str) -> None:

		logger.info('Удаление записи ')

		if self.dbTable.rowCount() == 0:
			logger.info('Нет записей для удаления')
			return

		# создание диалога, присвоение имени окна
		dialog = QDialog(self)
		dialog.setWindowTitle('Удаление записи')

		message = QLabel(f'Вы точно хотите удалить выбранную запись?')
		okBtn = QPushButton('ОК')
		canceldBtn = QPushButton('Отмена')

		ctrlLayout = QHBoxLayout()
		ctrlLayout.addWidget(okBtn)
		ctrlLayout.addWidget(canceldBtn)

		okBtn.clicked.connect(dialog.accept)
		canceldBtn.clicked.connect(dialog.reject)

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(message)
		mainLayout.addLayout(ctrlLayout)

		dialog.setLayout(mainLayout)

		dialog.resize(dialog.sizeHint())

		if dialog.exec_() == dialog.Accepted:

			# получение информации о таблице
			tableInfo = getTableInfo(dbPath, tableName)

			for i in tableInfo:
				colPK = i[5]
				if colPK:
					pkColIndex = i[0]
					pkColName = i[1]

					pkColValue = self.dbTable.item(self.dbTable.currentRow(), pkColIndex).text()

					# внесение изменений в БД
					sqlRequest = f'DELETE FROM {tableName} WHERE {pkColName}={pkColValue}'
					sqlExec(dbPath, sqlRequest, True)

					# обновить таблицу
					self.showTable(dbPath, tableName)

	def editRow(self, dbPath: str, tableName: str) -> None:

		logger.info(f'Редактирование записи')

		row = self.dbTable.currentRow()

		tableInfo = getTableInfo(dbPath, tableName)
		cols = len(tableInfo)
		values = [self.dbTable.item(row, col).text() for col in range(cols)]

		dialog = EditRowDialog(dbPath, tableName, values)

		if dialog.exec_():
			logger.info(f'Внесение данных {dialog.values}')

			# формирование списков заголовков и данных
			headers = ', '.join([header for header in self.headers])
			values = ', '.join(f'{item}' for item in dialog.values)

			# внесение изменений в БД
			sqlRequest = f'UPDATE OR IGNORE {tableName} SET ({headers}) = ({values});'
			print(sqlRequest)
			sqlExec(dbPath, sqlRequest, True)

			# обновить таблицу
			self.showTable(dbPath, tableName)

	def importCSV(self, dbPath: str, tableName: str) -> None:

		logger.info('Импорт из CSV')

		tableInfo = getTableInfo(dbPath, tableName)
		headers = [col[1] for col in tableInfo]

		dialog = ImportCSV(headers)
		if dialog.exec_():
			logger.info(f'Импортирован файл {dialog.csvPath}')
			logger.info(f'Поля {dialog.headers}')

			headers = ", ".join(dialog.headers)
			placeHolders = ", ".join(["?" for i in range(len(dialog.headers))])

			try:
				sqlRequest = f'INSERT OR IGNORE INTO {tableName} ({headers}) VALUES ({placeHolders})'
				sqlExecMany(dbPath, sqlRequest, dialog.data, True)
			except Exception as e:
				logger.exception(e)

		self.updateForm(dbPath)

	def exportCSV(self, dbPath: str, tableName: str) -> None:

		logger.info('Экспорт в CSV')

		# формирование вывода
		tableInfo = getTableInfo(dbPath, tableName)
		headers = [col[1] for col in tableInfo]

		sqlRequest = f'SELECT * FROM {tableName}'
		items = sqlExec(dbPath, sqlRequest)

		data = ','.join(headers) + '\n'

		for item in items:
			data += ','.join(str(item)) + '\n'

		# диалог сохранения файла
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", f"{tableName}",
												  "Файлы CSV (*.csv);;Все файлы (*)", options=options)
		# сохранить файл
		if fileName:
			with open(f'{fileName}.csv', 'w') as file:
				file.write(data)

	def closeEvent(self, event) -> None:

		logger.info('Закрытие окна')

		event.accept()


# запуск приложения
if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(open('style.qss', 'r').read())
	win = MainWindow()
	sys.exit(app.exec_())
