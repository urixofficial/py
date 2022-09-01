from PyQt5.QtWidgets import QHeaderView, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

class FilterHeader(QHeaderView):
	filterActivated = pyqtSignal()

	def __init__(self, parent):
		super().__init__(Qt.Horizontal, parent)
		self._editors = []
		self._padding = 4
		self.setStretchLastSection(True)
		self.setSectionResizeMode(QHeaderView.Stretch)
		self.setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.setSortIndicatorShown(False)
		self.setSectionsMovable(True)
		self.sectionResized.connect(self.adjustPositions)
		parent.horizontalScrollBar().valueChanged.connect(self.adjustPositions)

	def setFilterBoxes(self, count):
		while self._editors:
			editor = self._editors.pop()
			editor.deleteLater()
		for index in range(count):
			editor = QLineEdit(self.parent())
			editor.setAlignment(Qt.AlignCenter)
			editor.setObjectName('filter')
			editor.setPlaceholderText('Filter')
			editor.setClearButtonEnabled(True)
			editor.returnPressed.connect(self.filterActivated.emit)
			editor.show()
			self._editors.append(editor)
		self.adjustPositions()

	def sizeHint(self):
		size = super().sizeHint()
		if self._editors:
			height = self._editors[0].sizeHint().height()
			size.setHeight(size.height() + height + self._padding)
		return size

	def updateGeometries(self):
		if self._editors:
			height = self._editors[0].sizeHint().height()
			self.setViewportMargins(0, 0, 0, height + self._padding)
		else:
			self.setViewportMargins(0, 0, 0, 0)
		super().updateGeometries()
		self.adjustPositions()

	def adjustPositions(self):
		for index, editor in enumerate(self._editors):
			height = editor.sizeHint().height()
			editor.move(
				self.sectionPosition(index) - self.offset() + 2,
				height + (self._padding // 2))
			editor.resize(self.sectionSize(index), height)

	def filterText(self, index):
		if 0 <= index < len(self._editors):
			return self._editors[index].text()
		return ''

	def setFilterText(self, index, text):
		if 0 <= index < len(self._editors):
			self._editors[index].setText(text)

	def clearFilters(self):
		for editor in self._editors:
			editor.clear()   