import sys

from gui import MyWidget
from PySide2.QtWidgets import (
    QApplication,
)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
