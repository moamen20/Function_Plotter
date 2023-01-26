# import needed libraries
import numpy as np
import sys
import re
# GUI libraries
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
# Plotting libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from PySide2.QtGui import QColor,QFont

# define default constant
DEFAULT_FUNCTION = "x"
X_RANGE = (-100, 100)
DEFAULT_RANGE = (-10, 10)
DEFAULT_font = QFont("Times", 12)
BOLD_font = QFont("Helvetica", 12, QFont.Bold)

# list of allowed words to be entered by the user
allowed_elements = ['+', '-', '*', 'x', 'sin', 'cos', 'exp', '/', '^', ]

# for converting from string to mathematical expression
replacement_func = {'sin': 'np.sin', 'cos': 'np.cos', 'exp': 'np.exp', '^': '**'}

# define a function take an expression and check its Validity then evaluates the string expression and returns its value
def eval_function(func):
    #check if expression valid or not
    for item in re.findall('[a-zA-Z_]+', func):
        if item not in allowed_elements:
            raise ValueError(
                f" '{item}' is not a valid element to use, expression must be function of x .\n Please use valid elements from the following list {', '.join(allowed_elements)}.\n then write the expression in a right way, ex: 5*x^3 + 2/x\n")

    for old, new in replacement_func.items():
        func = func.replace(old, new)

    # to deal with constant functions e.g., y = 1
    if "x" not in func:
        func = f"{func}+0*x"

    def funeval(x):
        return eval(func)

    return funeval


#************************************ GUI *******************************

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        # main window
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Function Plotter")
        self.setStyleSheet("color: 	darkblue;"
                        "background-color:turquoise;"
                        "selection-color: black;"
                        "selection-background-color: red;")
        self.sc = MplCanvas(self, width=10, height=8, dpi=100)

        # build DoubleSpinBox for min x & max x values
        self.mn = QDoubleSpinBox()
        self.mn.setStyleSheet("background-color:white;")
        self.mx = QDoubleSpinBox()
        self.mx.setStyleSheet("background-color:white;")
        self.mn.setPrefix("min x: ")
        self.mx.setPrefix("max x: ")
        self.mn.setRange(*X_RANGE)
        self.mx.setRange(*X_RANGE)
        self.mn.setValue(DEFAULT_RANGE[0])
        self.mx.setValue(DEFAULT_RANGE[1])
        self.mn.setFont(DEFAULT_font)
        self.mx.setFont(DEFAULT_font)
        # connect the min & max values of x with change method
        self.mn.valueChanged.connect(lambda _: self.change_axes())
        self.mx.valueChanged.connect(lambda _: self.change_axes())
        # building layout of x values
        xrange_layout = QHBoxLayout()
        xrange_layout.addWidget(self.mn)
        xrange_layout.addWidget(self.mx)

        # build a text box for function
        self.func_label = QLabel(text="Function: ")
        self.func_label.setFont(BOLD_font)
        self.function = QLineEdit()
        self.function.setStyleSheet("background-color:white;")
        self.function.setText(DEFAULT_FUNCTION)
        self.function.setFont(DEFAULT_font)
        self.submit = QPushButton(text="Plot")
        self.submit.setStyleSheet("background-color:white;")
        self.submit.setFont(BOLD_font)
        self.submit.clicked.connect(lambda _: self.plot_signal())
        # function layout
        func_layout = QHBoxLayout()
        func_layout.addWidget(self.func_label)
        func_layout.addWidget(self.function)
        func_layout.addWidget(self.submit)

        # Create toolbar, passing canvas as first parameter, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        # building the main layout to add our components
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        layout.addLayout(xrange_layout)
        layout.addLayout(func_layout)

        # define error dialog
        self.error_dialog = QMessageBox()
        self.error_dialog.setFont(DEFAULT_font)

        # Create a placeholder widget to hold our toolbar and canvas.

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def change_axes(self):
        """ Update the signal plotting with the new values """
        mn = self.mn.value()
        mx = self.mx.value()
        # if min x greater than or equal to max x show error message
        if mn >= mx:
            self.error_dialog.setWindowTitle("x limits Error!")
            self.error_dialog.setText("'min x' should be less than 'max x'.")
            self.error_dialog.show()
            return
        #if min x is smaller than max x plot the signal
        else:
            self.plot_signal()

    # define a function to plot the signal
    def plot_signal(self):
        mn = self.mn.value()
        mx = self.mx.value()
        x = np.linspace(mn, mx)
        try:
            y = eval_function(self.function.text())(x)
        #in case of function expression is not valid, show error message
        except ValueError as e:
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText(str(e))
            self.error_dialog.show()
            return

        self.sc.axes.clear()
        self.sc.axes.plot(x, y)


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()
