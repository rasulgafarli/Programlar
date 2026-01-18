import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


def text_to_binary(text):
    return ' '.join(format(ord(c), '08b') for c in text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cümlə İkilik Koda Çevirici")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Cümlə daxil edin:")
        self.layout.addWidget(self.label)

        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)

        self.convert_button = QPushButton("Çevir")
        self.convert_button.setStyleSheet(
            "background-color: green; color: white; font-weight: bold; border-radius: 15px; padding: 10px;")
        self.convert_button.setFont(QFont('Arial', 12))
        self.convert_button.clicked.connect(self.show_binary_window)
        self.layout.addWidget(self.convert_button)

        self.setStyleSheet("background-color: #f0f0f0;")

    def show_binary_window(self):
        text = self.text_input.text()
        binary_text = text_to_binary(text)

        self.binary_window = BinaryWindow(text, binary_text)
        self.binary_window.show()


class BinaryWindow(QMainWindow):
    def __init__(self, original_text, binary_text):
        super().__init__()
        self.setWindowTitle("Çevirilmiş Cümlə")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.original_label = QLabel("Əvvəlki Cümlə:")
        self.layout.addWidget(self.original_label)

        self.original_text = QTextEdit()
        self.original_text.setText(original_text)
        self.original_text.setReadOnly(True)
        self.layout.addWidget(self.original_text)

        self.binary_label = QLabel("İkilik Kod:")
        self.layout.addWidget(self.binary_label)

        self.binary_text = QTextEdit()
        self.binary_text.setText(binary_text)
        self.binary_text.setReadOnly(True)
        self.layout.addWidget(self.binary_text)

        self.setStyleSheet("background-color: #e0ffe0;")
        self.resize(600, 400)


app = QApplication(sys.argv)

main_window = MainWindow()
main_window.resize(400, 200)
main_window.show()

sys.exit(app.exec())
