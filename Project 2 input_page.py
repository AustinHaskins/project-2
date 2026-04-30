from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSlider,
    QStyle,
    QStyleOptionSlider,
    QToolTip,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

SLIDER_MIN = 169
SLIDER_MAX = 938


class InputPage(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.build_ui()
        self.apply_styles()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 18, 24, 18)
        root.setSpacing(14)

        subtitle = QLabel(
            "Vacation Spot Finder\n"
            "Please fill out the inputs so we can find the best match for your trip."
        )
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")

        root.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")
        form_layout = QGridLayout(card)
        form_layout.setContentsMargins(34, 28, 34, 28)
        form_layout.setHorizontalSpacing(26)
        form_layout.setVerticalSpacing(22)
        form_layout.setColumnStretch(0, 1)
        form_layout.setColumnStretch(1, 1)

        self.season_combo = QComboBox()
        self.season_combo.addItems([s.title() for s in self.config["seasons"]])

        self.primary_combo = QComboBox()
        self.primary_combo.addItem("Select primary activity")
        self.primary_combo.addItems([self.pretty_label(a) for a in self.config["primary_activities"]])

        self.secondary_combo_1 = QComboBox()
        self.secondary_combo_1.addItem("No preference")
        self.secondary_combo_1.addItems([self.pretty_label(a) for a in self.config["secondary_activities"]])

        self.secondary_combo_2 = QComboBox()
        self.secondary_combo_2.addItem("No preference")
        self.secondary_combo_2.addItems([self.pretty_label(a) for a in self.config["secondary_activities"]])

        form_layout.addWidget(self.make_center_label("Trip season"), 0, 0)
        form_layout.addWidget(self.season_combo, 0, 1)
        form_layout.addWidget(self.make_center_label("Primary activity"), 1, 0)
        form_layout.addWidget(self.primary_combo, 1, 1)
        form_layout.addWidget(self.make_center_label("Secondary Activity #1"), 2, 0)
        form_layout.addWidget(self.secondary_combo_1, 2, 1)
        form_layout.addWidget(self.make_center_label("Secondary Activity #2"), 3, 0)
        form_layout.addWidget(self.secondary_combo_2, 3, 1)

        region_group_box = QGroupBox("Trip region")
        region_group_box.setObjectName("pillGroup")
        region_layout = QHBoxLayout(region_group_box)
        region_layout.setContentsMargins(18, 18, 16, 14)
        region_layout.setSpacing(24)
        region_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.region_group = QButtonGroup(self)
        self.us_radio = QRadioButton("U.S.")
        self.intl_radio = QRadioButton("International")
        self.region_group.addButton(self.us_radio, 0)
        self.region_group.addButton(self.intl_radio, 1)
        region_layout.addWidget(self.us_radio)
        region_layout.addWidget(self.intl_radio)
        form_layout.addWidget(region_group_box, 4, 0, 1, 2)

        temp_group_box = QGroupBox("Preferred average temperature")
        temp_group_box.setObjectName("pillGroup")
        temp_group_box.setMinimumWidth(700)
        temp_group_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        temp_layout = QVBoxLayout(temp_group_box)
        temp_layout.setContentsMargins(18, 6, 18, 16)
        temp_layout.setSpacing(6)

        self.temp_value = QLabel()
        self.temp_value.setObjectName("tempValue")
        self.temp_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.temp_slider.setMinimum(SLIDER_MIN)
        self.temp_slider.setMaximum(SLIDER_MAX)
        self.temp_slider.setValue((SLIDER_MIN + SLIDER_MAX) // 2)
        self.temp_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.temp_slider.valueChanged.connect(self.update_temp_label)
        self.temp_slider.sliderMoved.connect(self.show_slider_tooltip)
        self.temp_slider.sliderPressed.connect(self.show_current_slider_tooltip)

        range_row = QHBoxLayout()
        range_row.setContentsMargins(0, 0, 0, 0)
        range_row.addWidget(QLabel("16.9°F"))
        range_row.addStretch()
        range_row.addWidget(QLabel("93.8°F"))

        temp_layout.addWidget(self.temp_value)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addLayout(range_row)
        form_layout.addWidget(temp_group_box, 5, 0, 1, 2)

        button_row = QHBoxLayout()
        button_row.addStretch()
        self.continue_button = QPushButton("Find a Location!")
        self.continue_button.setFixedWidth(220)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.continue_button)
        button_row.addStretch()

        form_layout.addLayout(button_row, 6, 0, 1, 2)

        root.addWidget(card, stretch=1)
        root.addStretch()

        self.update_temp_label(self.temp_slider.value())

    def make_center_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def pretty_label(self, raw: str) -> str:
        return raw.replace("_", " ").title()

    def selected_region(self) -> str:
        if self.us_radio.isChecked():
            return "U.S."
        if self.intl_radio.isChecked():
            return "International"
        return "Not selected"

    def slider_temp(self) -> float:
        return self.temp_slider.value() / 10.0

    def update_temp_label(self, value: int):
        self.temp_value.setText(f"{value / 10.0:.1f}°F")
        if self.temp_slider.isSliderDown():
            self.show_slider_tooltip(value)

    def show_current_slider_tooltip(self):
        self.show_slider_tooltip(self.temp_slider.value())

    def show_slider_tooltip(self, value: int):
        option = QStyleOptionSlider()
        self.temp_slider.initStyleOption(option)
        handle_rect = self.temp_slider.style().subControlRect(
            QStyle.ComplexControl.CC_Slider,
            option,
            QStyle.SubControl.SC_SliderHandle,
            self.temp_slider,
        )
        center = handle_rect.center()
        global_pos = self.temp_slider.mapToGlobal(QPoint(center.x(), handle_rect.top() - 18))
        QToolTip.showText(global_pos, f"{value / 10.0:.1f}°F", self.temp_slider, handle_rect)

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
            QLabel#subtitle {
                color: white;
                font-size: 15px;
            }
            QGroupBox#pillGroup {
                background: #f7f7f8;
                border: 1px solid #cfd5dd;
                border-radius: 18px;
                margin-top: 16px;
                padding-top: 10px;
                font-weight: 600;
                color: #1f2937;
            }
            QGroupBox#pillGroup::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 8px;
                background: #f3f4f6;
            }
            QComboBox, QPushButton {
                min-height: 42px;
                border-radius: 10px;
                border: 1px solid #c7d2de;
                padding: 6px 10px;
                background: white;
            }
            QComboBox:hover, QPushButton:hover {
                border-color: #7aa7d9;
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
            QLabel#tempValue {
                font-size: 17px;
                font-weight: 700;
                color: #243b53;
            }
            QRadioButton {
                spacing: 8px;
                color: #243b53;
                background: transparent;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #9aa5b1;
                border-radius: 9px;
                background: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #246bce;
                border-radius: 9px;
                background: #246bce;
            }
            QSlider {
                background: transparent;
                min-height: 26px;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 8px;
                background: #d6dbe3;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #246bce;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #d6dbe3;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: 2px solid #246bce;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
            QToolTip {
                background: #1f2937;
                color: white;
                border: 1px solid #111827;
                padding: 6px 10px;
                border-radius: 8px;
                font-size: 12px;
            }
            """
        )
