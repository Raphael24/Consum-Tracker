import sys
from PyQt5 import QtWidgets, uic




class ConsumUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("Consum.ui", self)


app = QtWidgets.QApplication(sys.argv)
dialog = ConsumUI()
dialog.show()
sys.exit(app.exec_())
