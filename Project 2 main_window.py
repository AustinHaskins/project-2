from PyQt6.QtWidgets import QMainWindow, QStackedWidget


class MainWindow(QMainWindow):
    def __init__(self, input_page, result_page):
        super().__init__()
        self.input_page = input_page
        self.result_page = result_page

        self.setWindowTitle("Vacation Spot Finder")
        self.resize(1200, 820)
        self.setMinimumSize(980, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.stack.addWidget(self.input_page)
        self.stack.addWidget(self.result_page)

    def show_input_page(self):
        self.stack.setCurrentWidget(self.input_page)

    def show_result_page(self):
        self.stack.setCurrentWidget(self.result_page)
