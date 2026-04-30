from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class ResultPage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.apply_styles()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 18, 24, 18)
        root.setSpacing(14)

        top_row = QHBoxLayout()
        self.back_button = QPushButton("Back to Input")
        self.back_button.setFixedWidth(180)
        top_row.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        top_row.addStretch()
        root.addLayout(top_row)

        result_card = QFrame()
        result_card.setObjectName("card")
        result_layout = QVBoxLayout(result_card)
        result_layout.setContentsMargins(34, 28, 34, 28)
        result_layout.setSpacing(18)

        result_title = QLabel("Your Vacation Review")
        title_font = QFont()
        title_font.setPointSize(21)
        title_font.setBold(True)
        result_title.setFont(title_font)
        result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.review_label = QLabel("")
        self.review_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.review_label.setWordWrap(True)
        self.review_label.setObjectName("review")

        self.match_title = QLabel("Best Matched Location")
        self.match_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.match_title.setObjectName("matchTitle")

        self.location_label = QLabel("")
        self.location_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.location_label.setWordWrap(True)
        self.location_label.setObjectName("location")

        self.description_label = QLabel("")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setObjectName("description")

        result_layout.addWidget(result_title)
        result_layout.addWidget(self.review_label)
        result_layout.addSpacing(10)
        result_layout.addWidget(self.match_title)
        result_layout.addWidget(self.location_label)
        result_layout.addWidget(self.description_label)
        result_layout.addStretch()

        root.addWidget(result_card, stretch=1)

    def show_result(self, review_text, location_text, description_text):
        self.review_label.setText(review_text)
        self.location_label.setText(location_text)
        self.description_label.setText(description_text)

    def apply_styles(self):
        self.setStyleSheet(
            """
            QWidget {
                background: #f3f4f6;
                color: #1f2937;
                font-size: 14px;
            }
            QLabel {
                background: transparent;
            }
            QFrame#card {
                background: white;
                border: 1px solid #d4dae3;
                border-radius: 18px;
            }
            QComboBox, QPushButton {
                min-height: 42px;
                border-radius: 10px;
                border: 1px solid #c7d2de;
                padding: 6px 10px;
                background: white;
            }
            QPushButton {
                background: #246bce;
                color: white;
                font-weight: 600;
                min-width: 150px;
                padding: 10px 18px;
            }
            QPushButton:hover {
                background: #1e5fb8;
            }
            QLabel#review {
                font-size: 15px;
                color: #334e68;
                line-height: 1.5;
            }
            QLabel#matchTitle {
                font-size: 18px;
                font-weight: 700;
                color: #1f2937;
            }
            QLabel#location {
                font-size: 20px;
                font-weight: 700;
                color: #153e75;
            }
            QLabel#description {
                font-size: 15px;
                color: #334e68;
            }
            """
        )
