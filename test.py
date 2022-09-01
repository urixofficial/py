	





import sys
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QWidget):

	def __init__(self):

		super().__init__()
		self.logging = True
		self.initUI()

	def initUI(self):

		db = QSqlDatabase.addDatabase('QSQLITE')
		db.setDatabaseName('test.db')

		if not db.open():
			print('Connetion to DB failed')

		query = QSqlQuery()
		query.exec(f'SELECT * FROM Картриджи')
		print(query.result())

		self.model = QSqlTableModel()
		delrow = -1
		self.initializeModel(self.model)

		view1 = self.createView("Table Model (View 1)", self.model)
		view1.clicked.connect(self.findrow)

		layout = QVBoxLayout()
		layout.addWidget(view1)

		button = QPushButton("Add a row")
		button.clicked.connect(self.addrow)
		layout.addWidget(button)

		btn1 = QPushButton("del a row")
		btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
		layout.addWidget(btn1)

		self.setLayout(layout)
		self.setWindowTitle("Database Demo")
		self.show()

	def initializeModel(self, model):
		self.model.setTable('sportsmen')
		self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
		self.model.select()
		self.model.setHeaderData(0, Qt.Horizontal, "ID")
		self.model.setHeaderData(1, Qt.Horizontal, "First name")
		self.model.setHeaderData(2, Qt.Horizontal, "Last name")

	def createView(self, title, model):
		view = QTableView()
		view.setModel(self.model)
		view.setWindowTitle(title)
		return view

	def addrow(self):
		print (self.model.rowCount())
		ret = self.model.insertRows(self.model.rowCount(), 1)
		print (ret)

	def findrow(self, i):
		delrow = i.row()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())