import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QSize
from WeatherDisplayUI import WeatherDisplayUI
from WeatherData import WeatherData
from styles import style_sheet


class SearchLocationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_data = WeatherData()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 500, 125)
        self.setWindowTitle("Weather Application")
        self.setUpLocationUI()
        self.setObjectName("SearchLocationUIWidget")
        self.setStyleSheet("background-color: white;")
        self.show()

    def setUpLocationUI(self):
        aspect = Qt.AspectRatioMode.KeepAspectRatioByExpanding
        transform = Qt.TransformationMode.SmoothTransformation

        main_h_box = QHBoxLayout()
        main_h_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        search_img = self.loadImage(r"images\search.png")
        btn_icon = QIcon(search_img)

        search_btn = QPushButton()
        search_btn.setObjectName("SearchButton")
        search_btn.setStyleSheet("border-radius: 25px; background-color: #dff6ff")
        search_btn.setIcon(btn_icon)
        search_btn.setIconSize(QSize(50, 50))
        search_btn.setFixedSize(QSize(50, 50))
        search_btn.clicked.connect(self.isClicked)

        loc_label = QLabel()
        loc_img = self.loadImage(r"images\location.png")
        loc_label.setPixmap(loc_img.scaled(loc_label.size(), aspect, transform))
        loc_label.setScaledContents(True)
        loc_label.setFixedSize(50, 50)

        # search_img = self.loadImage(r"images\search.png")
        # search_img.setScaledContents(True)
        # search_img.setFixedSize(50, 50)

        self.enter_loc_edit = QLineEdit()
        self.enter_loc_edit.setStyleSheet("border: none;")
        self.enter_loc_edit.setClearButtonEnabled(True)
        self.enter_loc_edit.setFont(QFont("Open Sans", 16))
        self.enter_loc_edit.setMinimumHeight(25)
        self.enter_loc_edit.setPlaceholderText("Enter Your Location")
        self.enter_loc_edit.setTextMargins(25, 5, 25, 5)

        main_h_box.addWidget(loc_label)
        main_h_box.addWidget(self.enter_loc_edit)
        main_h_box.addWidget(search_btn)

        self.setLayout(main_h_box)

    def isClicked(self):
        self.close()

        self.weatherDisplayUI = WeatherDisplayUI(cityName=self.enter_loc_edit.text())
        self.weatherDisplayUI.show()

    def loadFont(self, font_path):
        try:
            with open(font_path):
                return font_path
        except FileNotFoundError as err:
            print(f"File not found: Error {err}")

    def loadImage(self, image_path) -> QPixmap:
        try:
            # aspect = Qt.AspectRatioMode.KeepAspectRatioByExpanding
            # transform = Qt.TransformationMode.SmoothTransformation
            # image = QLabel(self)
            pixmap = QPixmap(image_path)
            # image.setPixmap(pixmap.scaled(image.size(), aspect, transform))

            return pixmap
        except FileNotFoundError as err:
            print(f"Image not found. Error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchLocationUI()

    sys.exit(app.exec())
