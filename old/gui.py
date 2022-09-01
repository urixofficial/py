import sys
from loguru import logger
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtCore import Qt, QRegExp, QSize
from new_table_dialog import *
from edit_table_dialog import *
from edit_row_dialog import *
from import_dialog import *

MIN_WIDTH = 640
MIN_HEIGHT = 320
DEFAULT_DB_PATH = 'cartridge.db'
MODELS = ('725/85A', '737/83A/X', '712/35A', '728/78A', '80A/X', 'Samsung')

class MainWindow(QWidget):
	def __init__(self):

		super().__init__()
		self.logging = True
		self.initUI()

	def initUI(self):

		logger.info('Отрисовка интерфейса')

		# ============================ Управление ==========================================

		self.tablesBox = QComboBox()
		self.tablesBox.currentIndexChanged.connect(lambda: self.showTable(DEFAULT_DB_PATH, self.tablesBox.currentText()))
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
		# self.dbTable.cellChanged.connect(self.savePage)

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

	# ========================================= Обновление формы ================================

	def updateForm(self, dbPath):

		logger.info('Обновление формы')

		# подключение к БД и создание курсора
		db = sqlite3.connect(dbPath)
		c = db.cursor()

		# запрос данных из базы
		c.execute('SELECT name FROM sqlite_master WHERE type="table";')
		tables = [table[0] for table in c.fetchall() if not table[0].startswith('sqlite_')]

		# закрытие подключения
		db.close()

		self.tablesBox.clear()
		self.tablesBox.addItems(tables)

	def getTableInfo(self, dbPath, tableName):

		# подключение к БД и создание курсора
		db = sqlite3.connect(dbPath)
		c = db.cursor()

		# получение информации о таблице
		c.execute(f'SELECT * FROM pragma_table_info("{tableName}")')
		tableInfo = c.fetchall()

		# закрытие подключения
		db.close()

		return tableInfo

	# =========================================== Вывод таблицы ==========================================

	def showTable(self, dbPath, tableName, sort=1):

		if tableName == '': return

		logger.info(f'Вывод таблицы {tableName}')

		# получение информации о таблице
		tableInfo = self.getTableInfo(dbPath, tableName)

		# количество столбцов
		cols = len(tableInfo)
		self.dbTable.setColumnCount(cols)

		self.headers = []
\
		for i in tableInfo:

			colIndex = i[0]
			colName = i[1]
			colPK = i[5]

			# проверка на первичный ключ
			if colPK:

				if colName == 'ID':
					self.dbTable.setColumnHidden(colIndex, True)
				else:
					self.dbTable.setColumnHidden(colIndex, False)

				self.dbTable.setHorizontalHeaderItem(colIndex, QTableWidgetItem(f'*{colName}'))
			else:
				self.dbTable.setHorizontalHeaderItem(colIndex, QTableWidgetItem(f'{colName}'))
			self.headers.append(colName)

		# подключение к БД и создание курсора
		con = sqlite3.connect(dbPath)
		cur = con.cursor()

		# получение данных
		cur.execute(f'SELECT * FROM {tableName} ORDER BY {sort}')
		items = cur.fetchall()

		# закрытие подключения
		con.close()

		# количество строк
		rows = len(items)
		self.dbTable.setRowCount(rows)
		self.statusBar.setText(f'Количество записей: {rows}')
		self.statusBar.setObjectName('statusBar')

		# внесение данных в таблицу
		for row in range(rows):
			for col in range(cols):
				self.dbTable.setItem(row, col, QTableWidgetItem(str(items[row][col])))
				self.dbTable.item(row, col).setTextAlignment(Qt.AlignCenter)
				self.dbTable.item(row, col).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

	# ========================================== Диалог создания таблицы ================================

	def addTable(self, dbPath):

		dialog = NewTableDialog()

		if dialog.exec_():

			logger.info(f'Добавление таблицы {dialog.tableName} со столбцами {dialog.tableHeaders}')

			# подключение к БД и создание курсора
			con = sqlite3.connect(dbPath)
			cur = con.cursor()

			# внесение изменений в БД
			cur.execute(f'CREATE TABLE IF NOT EXISTS {dialog.tableName} ({dialog.tableHeaders})')
			con.commit()

			# закрытие подключения
			con.close()

			# обновить форму
			self.updateForm(dbPath)

			# выбрать вновь созданную таблицу
			self.tablesBox.setCurrentText(dialog.tableName)

	# =========================================== Удаление таблицы ==========================================

	def delTable(self, dbPath, table):

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

			# подключение к БД и создание курсора
			con = sqlite3.connect(dbPath)
			cur = con.cursor()

			# внесение изменений в БД
			cur.execute(f'DROP TABLE {table}')
			con.commit()

			# закрытие подключения
			con.close()

			# обновить форму
			self.updateForm(dbPath)

	# ================================================= Редактирование таблицы =============================================

	def editTable(self, dbPath, tableName):

		tableInfo = self.getTableInfo(dbPath, tableName)

		dialog = EditTableDialog(dbPath, tableName, tableInfo)

		if dialog.exec_():

			logger.info(f'Изменение таблицы {tableName}')

			# подключение к БД и создание курсора
			con = sqlite3.connect(dbPath)
			cur = con.cursor()

			# изменение имени таблицы
			if tableName != dialog.tableName:

				logger.info(f'Изменение имени таблицы на {dialog.tableName}')

				cur.execute(f'ALTER TABLE {tableName} RENAME TO {dialog.tableName}')
				con.commit()
				tableName = dialog.tableName

				# обновить форму
				self.updateForm(dbPath)

				# выбрать вновь созданную таблицу
				self.tablesBox.setCurrentText(dialog.tableName)

			# изменение имен столбцов
			for i in tableInfo:
				index = i[0]
				oldHeader = i[1]
				newHeader = dialog.tableHeaders[index]
				if oldHeader != newHeader:
					logger.info(f'Изменение имени столбца {oldHeader} на {newHeader}')
					cur.execute(f'ALTER TABLE {dialog.tableName} RENAME COLUMN {oldHeader} TO {newHeader}')
					con.commit()
					self.showTable(dbPath, tableName)

			# закрытие подключения
			con.close()

	# ================================================= Добавление записи =============================================

	def addRow(self, dbPath, tableName):

		logger.info(f'Добавление записи')

		tableInfo = self.getTableInfo(dbPath, tableName)

		dialog = EditRowDialog(tableInfo)

		if dialog.exec_():

			logger.info(f'Внесение данных {dialog.values}')

			# подключение к БД и создание курсора
			con = sqlite3.connect(dbPath)
			cur = con.cursor()
			
			# формирование списков заголовков и данных
			headers = ', '.join([header for header in self.headers])
			values = ', '.join(f'{value}' for value in dialog.values)

			# внесение изменений в БД
			cur.execute(f'INSERT OR IGNORE INTO {tableName} ({headers}) VALUES ({values});')
			con.commit()

			# закрытие подключения
			con.close()

			# обновить таблицу
			self.showTable(dbPath, tableName)

	# =============================================== Удаление записи ===============================================

	def delRow(self, dbPath, tableName):

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
			tableInfo = self.getTableInfo(dbPath, tableName)

			for i in tableInfo:
				colPK = i[5]
				if colPK:
					pkColIndex = i[0]
					pkColName = i[1]

			pkColValue = self.dbTable.item(self.dbTable.currentRow(), pkColIndex).text()

			# подключение к БД и создание курсора
			con = sqlite3.connect(dbPath)
			cur = con.cursor()

			# внесение изменений в БД
			cur.execute(f'DELETE FROM {tableName} WHERE {pkColName}={pkColValue}')
			con.commit()

			# закрытие подключения
			con.close()

			# обновить таблицу
			self.showTable(dbPath, tableName)

	# =============================================== Редактирование записи ===============================================

	def editRow(self, dbPath, tableName):

		logger.info(f'Редактирование записи')

		row = self.dbTable.currentRow()

		tableInfo = self.getTableInfo(dbPath, tableName)
		cols = len(tableInfo)
		values = [self.dbTable.item(row, col).text() for col in range(cols)]

		dialog = EditRowDialog(tableInfo, values)

		if dialog.exec_():

			logger.info(f'Внесение данных {dialog.data}')

			# подключение к БД и создание курсора
			con = sqlite3.connect(dbPath)
			cur = con.cursor()
			
			# формирование списков заголовков и данных
			headers = ', '.join([header for header in self.headers])
			values = ', '.join(f'{item}' for item in dialog.values)

			# внесение изменений в БД
			cur.execute(f'UPDATE {tableName} SET ({headers}) = ({values});')
			con.commit()

			# закрытие подключения
			con.close()

			# обновить таблицу
			self.showTable(dbPath, tableName)

	# =========================================== Импорт из CSV ==========================================

	def importCSV(self, dbPath, table):

		logger.info('Импорт из CSV')

		# подключение к БД и создание курсора
		con = sqlite3.connect(dbPath)
		cur = con.cursor()

		# запрос данных из базы
		cur.execute(f'SELECT * FROM {table}')
		headers = [item[0] for item in cur.description]

		dialog = ImportCSV(headers)
		if dialog.exec_():
			logger.info(f'Импортирован файл {dialog.csvPath}')
			logger.info(f'Поля {dialog.headers}')

			headers = ", ".join(dialog.headers)
			placeHolders = ", ".join(["?" for i in range(len(dialog.headers))])

			try:
				cur.executemany(f'INSERT OR IGNORE INTO {table} ({headers}) VALUES ({placeHolders})', dialog.data)
				con.commit()
			except Exception as e:
				logger.exception(e)
			

		con.close()

		self.updateForm(dbPath)

	# =========================================== Экспорт в CSV ==========================================

	def exportCSV(self, dbPath, table):

		logger.info('Экспорт в CSV')
		
		# подключение к БД и создание курсора
		con = sqlite3.connect(dbPath)
		cur = con.cursor()

		# запрос данных из базы
		cur.execute(f'SELECT * FROM {table}')
		headers = [item[0] for item in cur.description]
		items = cur.fetchall()

		con.close()

		data = ','.join(headers) + '\n'

		for item in items:
			data += ','.join(str(item)) + '\n'

		with open(f'{table}.csv', 'w') as file:

			file.write(data)

	def closeEvent(self, event):

		logger.info('Закрытие окна')

		event.accept()




# запуск приложения
if __name__ == '__main__':

	app = QApplication(sys.argv)
	app.setStyleSheet(open('style.qss', 'r').read())

	ex = MainWindow()
	sys.exit(app.exec_())