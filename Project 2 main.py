import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from model_vac import VacationModel
from input_page import InputPage
from result_page import ResultPage
from main_window import MainWindow
from controller_vac import AppController


def main():
    app = QApplication(sys.argv)

    data_file = Path(__file__).resolve().parent / "data" / "vacation_spots_complete.json"
    model = VacationModel(data_file)
    options = model.get_options()

    input_page = InputPage(options)
    result_page = ResultPage()
    window = MainWindow(input_page, result_page)

    AppController(model, window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
