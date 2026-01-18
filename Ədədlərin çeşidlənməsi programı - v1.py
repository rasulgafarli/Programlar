import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SortingProgram(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ədədlərin çeşidlənməsi programı - v1")

        # Main layout
        main_layout = QVBoxLayout()

        # Input field
        self.input_label = QLabel("Ədədləri daxil edin:")
        self.input_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ədədləri daxil edin:")

        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid gray;
                border-radius: 15px;
                padding: 5px;
            }
        """)

        # Sort button
        self.sort_button = QPushButton("Çeşidlə")
        self.sort_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.sort_button.setStyleSheet("""
            QPushButton {
                background-color: darkblue;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.sort_button.clicked.connect(self.sort_numbers)

        # Clear button
        self.clear_button = QPushButton("Sil")
        self.clear_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        self.clear_button.clicked.connect(self.clear_input)

        # Adjust layout
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.input_label, alignment=Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(self.input_field, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #ff793f;")
        self.setGeometry(100, 100, 400, 200)

    def sort_numbers(self):
        input_text = self.input_field.text()
        numbers = [float(num) for num in input_text.split(',')]

        positive_integers = sorted([int(num) for num in numbers if num > 0 and num.is_integer()])
        negative_integers = sorted([int(num) for num in numbers if num < 0 and num.is_integer()])
        positive_decimals = sorted([num for num in numbers if num > 0 and not num.is_integer()])
        negative_decimals = sorted([num for num in numbers if num < 0 and not num.is_integer()])

        result_text = ""
        if positive_integers:
            result_text += "Müsbət ədədlər: " + ", ".join(map(str, positive_integers)) + "\n"
        if negative_integers:
            result_text += "Mənfi ədədlər: " + ", ".join(map(str, negative_integers)) + "\n"
        if positive_decimals:
            result_text += "Müsbət onluq ədədlər: " + ", ".join(map(str, positive_decimals)) + "\n"
        if negative_decimals:
            result_text += "Mənfi onluq ədədlər: " + ", ".join(map(str, negative_decimals)) + "\n"

        self.show_result_window(result_text)

    def clear_input(self):
        self.input_field.clear()

    def show_result_window(self, result_text):
        result_window = QDialog(self)
        result_window.setWindowTitle("Nəticələr")

        layout = QVBoxLayout()

        result_display = QLabel(result_text)
        result_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_display.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        result_display.setStyleSheet("color: white;")
        result_display.setWordWrap(True)  # Enable word wrap to prevent text overflow

        layout.addWidget(result_display)

        result_window.setStyleSheet("""
            QDialog {
                background-color: #ff69b4;
                border: 5px solid brown;
                padding: 10px;
            }
            QDialog::content {
                border: 3px solid white;
                background-color: darkcyan;
                border-radius: 15px;
            }
        """)

        result_window.setLayout(layout)
        result_window.setFixedSize(300, 400)
        result_window.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SortingProgram()
    ex.show()
    sys.exit(app.exec())
