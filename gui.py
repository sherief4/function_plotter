from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import numpy as np
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from read import convert_func

Y_RANGE = (-1000, 1000)  # the minimum and the maximum values of y-axis


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter Application")
        self.setStyleSheet("background-color: grey")

        #  create widgets
        self.view = FigureCanvasQTAgg(Figure(figsize=(9, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self)
        # Minimum and Maximum values of x
        self.mn = QDoubleSpinBox()
        self.mn.setStyleSheet("background-color: white")
        self.mx = QDoubleSpinBox()
        self.mx.setStyleSheet("background-color: white")
        self.mn.setPrefix("Min x : ")
        self.mx.setPrefix("Max x : ")
        self.mn.setRange(*Y_RANGE)
        self.mx.setRange(*Y_RANGE)
        self.mn.setValue(-25)  # set min x to -10
        self.mx.setValue(25)  # set max x to 10
        self.function = QLineEdit()
        self.function.setStyleSheet("background-color: white")
        self.function.setText("")
        self.func_label = QLabel(text="F(x):")
        self.submit = QPushButton(text="Plot F(x)")
        self.submit.setStyleSheet("background-color: white")
        #  Create layout
        input_layout1 = QHBoxLayout()
        input_layout1.addWidget(self.func_label)
        input_layout1.addWidget(self.function)
        input_layout1.addWidget(self.mn)
        input_layout1.addWidget(self.mx)
        input_layout2 = QHBoxLayout()
        input_layout2.addWidget(self.submit)

        v_layout = QVBoxLayout()
        v_layout.addLayout(input_layout1)
        v_layout.addLayout(input_layout2)
        v_layout.addWidget(self.toolbar)
        self.setLayout(v_layout)
        v_layout.addWidget(self.view)
        self.error_dialog = QMessageBox()

        # connect inputs with on_change method
        self.mn.valueChanged.connect(lambda _: self.on_change(1))
        self.mx.valueChanged.connect(lambda _: self.on_change(2))
        self.submit.clicked.connect(lambda _: self.on_change(3))
        self.on_change(0)

    # User Input error handling
    @Slot()
    def on_change(self, idx):  # idx is used to notify the program that the values are changing
        mn = self.mn.value()
        mx = self.mx.value()
        # warning: min x can't be greater than or equal to max x
        if idx == 1 and mn >= mx:
            self.mn.setValue(mx - 1)
            self.error_dialog.setWindowTitle("Limits error")
            self.error_dialog.setText("Min x can\'t be greater than Max x")
            self.error_dialog.show()
            return

        # warning: max x can't be less than or equal to min x
        if idx == 2 and mx <= mn:
            self.mx.setValue(mn + 1)
            self.error_dialog.setWindowTitle("x limits Error!")
            self.error_dialog.setText("Max x can't be greater than 'min x'.")
            self.error_dialog.show()
            return
        x = np.arange(mn, mx +1, 0.4)
        try:
            y = convert_func(self.function.text())(x)
        except ValueError as e:
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText(str(e))
            self.error_dialog.show()
            return

        self.axes.clear()
        self.axes.plot(x, y)
        self.view.draw()
