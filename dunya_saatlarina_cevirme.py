import sys
import pytz
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dünya Saatları")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setMinimumSize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.az_time_label = QLabel("Azərbaycan saatı:")
        self.az_time_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.az_time_label)

        self.az_time_display = QLineEdit()
        self.az_time_display.setReadOnly(True)
        self.az_time_display.setFont(QFont('Arial', 14))
        self.az_time_display.setStyleSheet("border: 2px solid black; border-radius: 15px; padding: 10px;")
        self.layout.addWidget(self.az_time_display)

        self.country_label = QLabel("Ölkə adı seçin:")
        self.country_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.country_label)

        self.country_combo = QComboBox()
        self.countries = sorted(pytz.country_names.items(), key=lambda x: x[1])
        for country_code, country_name in self.countries:
            self.country_combo.addItem(country_name, country_code)
        self.country_combo.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.country_combo)

        self.convert_button = QPushButton("Çevir")
        self.convert_button.setStyleSheet(
            "background-color: green; color: white; font-weight: bold; border-radius: 15px; padding: 10px;")
        self.convert_button.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.convert_button.clicked.connect(self.show_converted_time)
        self.layout.addWidget(self.convert_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_az_time)
        self.timer.start(1000)

        self.update_az_time()

    def update_az_time(self):
        az_tz = pytz.timezone('Asia/Baku')
        az_time = datetime.now(az_tz)
        self.az_time_display.setText(az_time.strftime('%H:%M:%S'))

    def show_converted_time(self):
        country_code = self.country_combo.currentData()
        country_name = self.country_combo.currentText()
        country_tz = pytz.timezone(pytz.country_timezones[country_code][0])

        az_tz = pytz.timezone('Asia/Baku')
        az_time = datetime.now(az_tz)
        country_time = az_time.astimezone(country_tz)

        time_difference = (country_time.utcoffset() - az_time.utcoffset()).total_seconds() / 3600

        self.conversion_window = ConversionWindow(az_time, country_time, time_difference, country_tz, country_name)
        self.conversion_window.show()


class ConversionWindow(QMainWindow):
    def __init__(self, az_time, country_time, time_difference, country_tz, country_name):
        super().__init__()
        self.setWindowTitle("Çevrilmiş Saat")
        self.setStyleSheet("background-color: #e0ffe0;")
        self.setMinimumSize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.az_time_label = QLabel("Azərbaycan saatı:")
        self.az_time_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.az_time_label)

        self.az_time_display = QLineEdit()
        self.az_time_display.setReadOnly(True)
        self.az_time_display.setFont(QFont('Arial', 14))
        self.az_time_display.setStyleSheet("border: 2px solid black; border-radius: 15px; padding: 10px;")
        self.layout.addWidget(self.az_time_display)

        self.country_time_label = QLabel(f"{country_name} saatı:")
        self.country_time_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.country_time_label)

        self.country_time_display = QLineEdit()
        self.country_time_display.setReadOnly(True)
        self.country_time_display.setFont(QFont('Arial', 14))
        self.country_time_display.setStyleSheet("border: 2px solid black; border-radius: 15px; padding: 10px;")
        self.layout.addWidget(self.country_time_display)

        self.time_difference_label = QLabel("Zaman fərqi:")
        self.time_difference_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.time_difference_label)

        diff_hours = int(time_difference)
        diff_minutes = int((time_difference - diff_hours) * 60)
        diff_str = f"{abs(diff_hours)} saat, {abs(diff_minutes)} dəqiqə "
        if time_difference > 0:
            diff_str += "irəlidir"
        else:
            diff_str += "geridir"
        self.time_difference_display = QLabel(diff_str)
        self.time_difference_display.setFont(QFont('Arial', 14))
        self.layout.addWidget(self.time_difference_display)

        self.country_tz = country_tz

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_times)
        self.timer.start(1000)

        self.update_times()

    def update_times(self):
        az_tz = pytz.timezone('Asia/Baku')
        az_time = datetime.now(az_tz)
        self.az_time_display.setText(az_time.strftime('%H:%M:%S'))

        country_time = az_time.astimezone(self.country_tz)
        self.country_time_display.setText(country_time.strftime('%H:%M:%S'))


app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

sys.exit(app.exec())
