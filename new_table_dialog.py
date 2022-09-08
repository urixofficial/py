from loguru import logger
from PyQt5.QtWidgets import QWidget, QDialog, QTableWidget, QLineEdit, QLabel, QPushButton, QComboBox, QCheckBox, \
    QHBoxLayout, QGridLayout, QHeaderView, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt, QRegExp
from check_box import *
from config import *

class NewTableDialog(QDialog):

    def __init__(self, tableInfo=[]):
        super().__init__()

        logger.info('Инициализация')

        # позволяет отслеживать нажатия клавиш в этом окне
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.primaryKey = -1
        self.initUI()

    def initUI(self) -> None:

        logger.info('Отрисовка интерфейса')

        # создание диалога, присвоение имени окна
        self.setWindowTitle('Добавление таблицы')

        self.setMinimumWidth(EDIT_TABLE_WIDTH)
        self.setMinimumHeight(EDIT_TABLE_HEIGHT)

        self.fieldsTable = QTableWidget()
        self.fieldsTable.setColumnCount(3)
        self.fieldsTable.setRowCount(0)
        self.fieldsTable.verticalHeader().setVisible(False)
        self.fieldsTable.setHorizontalHeaderLabels(['Поле', 'Тип данных', 'Первичный ключ'])
        self.fieldsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.fieldsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.fieldsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.fieldsTable.resizeColumnsToContents()
        self.dynAdd()

        # создание элементов формы
        self.tableNameEdit = QLineEdit()

        # кнопки принятия или отклонения окна
        self.addOkBtn = QPushButton('ОК')
        self.addCanceldBtn = QPushButton('Отмена')

        # присоедниение функций к кнопкам
        self.addOkBtn.clicked.connect(self.validate)
        self.addCanceldBtn.clicked.connect(self.reject)

        self.info = QLabel()
        self.info.setAlignment(Qt.AlignCenter)

        # компоновка
        ctrlLayout = QHBoxLayout()
        ctrlLayout.addWidget(self.addOkBtn)
        ctrlLayout.addWidget(self.addCanceldBtn)

        layout = QGridLayout()
        layout.addWidget(QLabel('Имя таблицы:'), 0, 0)
        layout.addWidget(self.tableNameEdit, 0, 1)
        layout.addWidget(self.fieldsTable, 1, 0, 1, 2)
        layout.addWidget(self.info, 2, 0, 1, 2)
        layout.addLayout(ctrlLayout, 3, 0, 1, 2)
        self.setLayout(layout)

    def dynAdd(self) -> None:

        logger.info('Динамическое добавление строки')

        rows = self.fieldsTable.rowCount()

        # если строки отстутствуют, то добавить одну и присоединить эту функцию к изменению текста
        if rows < 1:
            self.addField()
            self.fieldsTable.cellWidget(0, 0).textChanged.connect(self.dynAdd)

        # если строки присутствуют
        else:

            # текст в последней строке
            lastText = self.fieldsTable.cellWidget(rows - 1, 0).text()

            # если текст в последней строке не пустой, то добавить новую строку
            if lastText != '':
                self.fieldsTable.cellWidget(rows - 1, 0).textChanged.disconnect(self.dynAdd)
                self.fieldsTable.cellWidget(rows - 1, 0).textChanged.connect(self.dynDel)
                self.addField()
                self.fieldsTable.cellWidget(rows, 0).textChanged.connect(self.dynAdd)

    def dynDel(self) -> None:

        logger.info('Динамическое удаление строки')

        rows = self.fieldsTable.rowCount()

        # если строк больше одной
        if rows > 1:

            # текст предпоследней строки
            preLastText = self.fieldsTable.cellWidget(rows - 2, 0).text()

            # если предпоследняя строка пуста
            if preLastText == '':
                self.fieldsTable.cellWidget(rows - 2, 0).textChanged.disconnect(self.dynDel)
                self.fieldsTable.cellWidget(rows - 2, 0).textChanged.connect(self.dynAdd)
                self.delField()

                # если строк больше двух
                if rows > 2:
                    self.fieldsTable.cellWidget(rows - 3, 0).textChanged.connect(self.dynDel)

    def addField(self) -> None:

        logger.info('Добавление строки')

        rows = self.fieldsTable.rowCount()

        self.fieldsTable.setRowCount(rows + 1)
        self.fieldsTable.setCellWidget(rows, 0, QLineEdit())
        self.fieldsTable.setCellWidget(rows, 1, QComboBox())
        self.fieldsTable.cellWidget(rows, 1).addItems(['INTEGER', 'REAL', 'BOOLEAN', 'DATE', 'TEXT'])
        self.fieldsTable.setCellWidget(rows, 2, CheckBox())
        if self.primaryKey > -1:
            self.fieldsTable.cellWidget(rows, 2).setEnabled(False)
        self.fieldsTable.cellWidget(rows, 2).checkBox.stateChanged.connect(lambda state: self.keyCheck(rows, state))

    def delField(self) -> None:

        logger.info('Удаление строки')

        rows = self.fieldsTable.rowCount()
        self.fieldsTable.setRowCount(rows - 1)

    def keyCheck(self, currentRow: int, state: bool) -> None:

        logger.info('Проверка первичного ключа')

        if state:
            self.primaryKey = currentRow
        else:
            self.primaryKey = -1

        rows = self.fieldsTable.rowCount()

        if state:
            for row in range(rows):
                if row == self.primaryKey:
                    self.fieldsTable.cellWidget(row, 2).checkBox.setObjectName('enabled')
                    self.fieldsTable.cellWidget(row, 2).setEnabled(True)
                else:
                    self.fieldsTable.cellWidget(row, 2).checkBox.setObjectName('disabled')
                    self.fieldsTable.cellWidget(row, 2).setEnabled(False)
        else:
            for row in range(rows):
                self.fieldsTable.cellWidget(row, 2).checkBox.setObjectName('enabled')
                self.fieldsTable.cellWidget(row, 2).setEnabled(True)

    def validate(self) -> None:

        logger.info('Проверка введенных данных')

        valid = True
        status = ''
        regex = '[^0-9][A-Za-zА-Яа-я0-9_]+'
        rows = self.fieldsTable.rowCount()

        # название таблицы
        if QRegExp(regex).exactMatch(self.tableNameEdit.text()):
            self.tableNameEdit.setStyleSheet('background-color: rgb(140, 255, 140)')
        else:
            valid = False
            self.tableNameEdit.setStyleSheet('background-color: rgb(255, 140, 140)')
            status += '\nИмя таблицы не должно быть пустым, начинаться с цифр,\nсодержать пробелы или спецсимволы'

        # названия полей и наличие главного ключа
        pk = 0

        for row in range(rows - 1):

            # проверка на соответствие маске
            text = self.fieldsTable.cellWidget(row, 0).text()
            if QRegExp(regex).exactMatch(text):
                self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(140, 255, 140)')
            else:
                valid = False
                self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(255, 140, 140)')
                logger.info('Значение не соответствует маске')
                status += '\nИмена столбцов не должны начинаться с цифр,\nсодержать пробелы или спецсимволы'

            # проверка на совпадение имен
            values = [self.fieldsTable.cellWidget(i, 0).text() for i in range(row)]
            for index, value in enumerate(values):
                if text == value:
                    valid = False
                    self.fieldsTable.cellWidget(index, 0).setStyleSheet('background-color: rgb(255, 140, 140)')
                    self.fieldsTable.cellWidget(row, 0).setStyleSheet('background-color: rgb(255, 140, 140)')
                    logger.warning('Совпадение имен')
                    status += '\nИмена столбцов не должны совпадать'

            # проверка на первичный ключ
            if self.fieldsTable.cellWidget(row, 2).checkBox.isChecked():
                pk += 1

        if pk == 1:
            for row in range(rows - 1):
                self.fieldsTable.cellWidget(row, 2).setStyleSheet('background-color: rgb(140, 255, 140)')
        else:
            valid = False
            for row in range(rows - 1):
                self.fieldsTable.cellWidget(row, 2).setStyleSheet('background-color: rgb(255, 140, 140)')
            logger.warning('Не указан первичный ключ')
            status += '\nУкажите первичный ключ'

        if valid:

            self.tableName = self.tableNameEdit.text()

            tableHeaders = []

            for row in range(rows - 1):
                headerName = self.fieldsTable.cellWidget(row, 0).text()
                headerType = self.fieldsTable.cellWidget(row, 1).currentText()
                primaryKey = self.fieldsTable.cellWidget(row, 2).checkBox.isChecked()
                # autoIncrement = self.fieldsTable.cellWidget(row, 3).checkBox.isChecked()
                header = [headerName, headerType]
                if primaryKey: header.append('PRIMARY KEY')
                tableHeaders.append(' '.join(header))
            self.tableHeaders = ', '.join(tableHeaders)

            self.accept()
        else:
            self.info.setText(status)
