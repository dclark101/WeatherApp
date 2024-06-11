from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtGui import QPixmap, QIcon, QFontDatabase, QFont
from PyQt6.QtCore import Qt, QSize
from WeatherData import WeatherData


class WeatherDisplayUI(QWidget):
    def __init__(self, cityName):
        super().__init__()
        self.cityName = cityName
        print(self.cityName)
        self.weatherData = WeatherData()

        self.data = self.weatherData.getWeatherData(self.cityName)
        self.temp = self.data["main"]["temp"]
        self.f_temp = self.kelvinToFahrenheit()
        self.humidity = self.data["main"]["humidity"]
        self.wind_speed = self.data["wind"]["speed"]
        self.weatherInfo = self.data["weather"][0]["description"]
        self.mainWeatherInfo = self.data["weather"][0]["main"]

        self.aspect = Qt.AspectRatioMode.KeepAspectRatioByExpanding
        self.transform = Qt.TransformationMode.SmoothTransformation
        id = QFontDatabase.addApplicationFont(
            self.loadFont(r"fonts\static\OpenSans-Regular.ttf")
        )

        print(id)
        families = QFontDatabase.applicationFontFamilies(id)
        print(families[0])

        self.initalizeUI()

    def searchBarLayout(self) -> QHBoxLayout:

        main_h_box = QHBoxLayout()
        main_h_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        search_img = self.loadImage(r"images\search.png")

        btn_icon = QIcon(search_img)

        search_btn = QPushButton()
        search_btn.setStyleSheet("")
        search_btn.setIcon(btn_icon)
        search_btn.setIconSize(QSize(50, 50))
        search_btn.setFixedSize(QSize(50, 50))
        search_btn.clicked.connect(self.isClicked)

        loc_label = QLabel()
        loc_img = self.loadImage(r"images\location.png")
        loc_label.setPixmap(
            loc_img.scaled(loc_label.size(), self.aspect, self.transform)
        )
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

        return main_h_box

    def bottomWeatherInfoLayout(self) -> QHBoxLayout:
        humidity_widget = QWidget()
        wind_speed_widget = QWidget()

        humidity_img = self.loadImage(r"images\humidity.png")
        humidity_img_label = QLabel()
        humidity_img_label.setPixmap(
            humidity_img.scaled(humidity_img_label.size(), self.aspect, self.transform)
        )
        humidity_img_label.setScaledContents(True)
        humidity_img_label.setFixedSize(50, 50)
        self.humidity_desc_label = QLabel(f"{self.humidity}% Humidity")
        self.humidity_desc_label.setWordWrap(True)
        humidity_h_box = QHBoxLayout()
        humidity_h_box.addWidget(humidity_img_label)
        humidity_h_box.addWidget(self.humidity_desc_label)

        wind_speed_img = self.loadImage(r"images\wind.png")
        wind_speed_img_label = QLabel()
        wind_speed_img_label.setPixmap(
            wind_speed_img.scaled(
                wind_speed_img_label.size(), self.aspect, self.transform
            )
        )
        wind_speed_img_label.setScaledContents(True)
        wind_speed_img_label.setFixedSize(50, 50)
        self.wind_speed_desc_label = QLabel(f"{self.wind_speed}Km/h Wind Speed")
        self.wind_speed_desc_label.setWordWrap(True)
        wind_speed_h_box = QHBoxLayout()
        wind_speed_h_box.addWidget(wind_speed_img_label)
        wind_speed_h_box.addWidget(self.wind_speed_desc_label)

        humidity_widget.setLayout(humidity_h_box)
        wind_speed_widget.setLayout(wind_speed_h_box)
        humidity_widget.setFont(QFont("Open Sans", 12))
        wind_speed_widget.setFont(QFont("Open Sans", 12))

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(humidity_widget, 0, Qt.AlignmentFlag.AlignLeft)
        main_h_box.addWidget(wind_speed_widget, 0, Qt.AlignmentFlag.AlignRight)

        return main_h_box

    def initalizeUI(self):
        self.setWindowTitle("Weather Display")
        self.setGeometry(100, 100, 450, 650)
        self.setUpWeatherDisplayUI()
        self.setStyleSheet("background-color: white;")

    def setUpWeatherDisplayUI(self):

        main_v_box = QVBoxLayout()

        self.weather_img = (
            self.loadImageBasedOnWeather()
        )  # self.loadImage(r"images\icons\sunny.svg")

        self.weather_img_label = QLabel()
        self.weather_img_label.setPixmap(
            self.weather_img.scaled(
                self.weather_img_label.size(), self.aspect, self.transform
            )
        )
        self.weather_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_img_label.setFixedSize(400, 400)
        self.weather_img_label.setScaledContents(True)

        self.temperature = QLabel(f"{self.f_temp}")
        self.temperature.setObjectName("TempLabel")
        temp_font = QFont("Open Sans", 32)
        temp_font.setBold(True)
        self.temperature.setFont(temp_font)
        self.weather_desc = QLabel(self.weatherInfo)
        self.weather_desc.setFont(QFont("Open Sans", 14))

        main_v_box.addLayout(self.searchBarLayout())
        main_v_box.addWidget(self.weather_img_label, 0, Qt.AlignmentFlag.AlignCenter)
        main_v_box.addWidget(
            self.temperature,
            0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )
        main_v_box.addWidget(
            self.weather_desc,
            0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )
        main_v_box.addLayout(self.bottomWeatherInfoLayout(), 0)
        main_v_box.setContentsMargins(25, 25, 25, 25)
        self.setLayout(main_v_box)

    def isClicked(self):
        self.cityName = self.enter_loc_edit.text()
        self.data = self.weatherData.getWeatherData(self.cityName)

        self.temp = self.data["main"]["temp"]
        self.humidity = self.data["main"]["humidity"]
        self.wind_speed = self.data["wind"]["speed"]
        self.weatherInfo = self.data["weather"][0]["description"]
        self.mainWeatherInfo = self.data["weather"][0]["main"]
        self.weather_img = self.loadImageBasedOnWeather()

        self.temperature.setText(f"{self.kelvinToFahrenheit()}")
        self.weather_desc.setText(f"{self.weatherInfo}")
        self.humidity_desc_label.setText(f"{self.humidity}% Humidity")
        self.wind_speed_desc_label.setText(f"{self.wind_speed}Km/h Wind Speed")
        self.weather_img_label.setPixmap(
            self.weather_img.scaled(
                self.weather_img_label.size(), self.aspect, self.transform
            )
        )

    def kelvinToFahrenheit(self) -> float:
        """A function that converts kelvin to fahrenheit"""
        k = float(self.temp)
        f = ((k - 273.15) * (9 / 5)) + 32

        return round(f, 1)

    def loadImageBasedOnWeather(self):
        match self.mainWeatherInfo:
            case "Clouds":
                return self.loadImage(r"images\icons\cloudy.svg")
            case "Clear":
                return self.loadImage(r"images\icons\sunny.svg")
            case "Rain":
                return self.loadImage(r"images\icons\rain_cloud_drizzle.svg")
            case "Mist":
                return self.loadImage(r"images\icons\foggy.svg")
            case _:
                return self.loadImage(r"images\icons\unknown.svg")

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
