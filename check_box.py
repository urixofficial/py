from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent

class CheckBox(QWidget):
    returnPressed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.checkBox = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.checkBox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
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