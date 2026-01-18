import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QTextEdit, \
    QMessageBox, QScrollBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SortingProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ədədlərin çeşidlənməsi programı - v2")

        # Main layout
        main_layout = QVBoxLayout()

        # Input field
        self.input_label = QLabel("Ədədləri daxil edin:")
        self.input_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Ədədləri daxil edin:")
        self.input_field.setFixedHeight(60)

        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid gray;
                border-radius: 15px;
                padding: 5px;
            }
        """)

        # Set vertical scrollbar policy
        self.input_field.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.input_field.setVerticalScrollBar(QScrollBar(self))
        self.input_field.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                background: #FFFFFF;
                width: 15px;
                border-radius: 15px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 15px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #CCCCCC;
                border: none;
                height: 15px;
                border-radius: 15px;
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
            QPushButton:pressed {
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
            QPushButton:pressed {
                background-color: lightcoral;
            }
        """)
        self.clear_button.clicked.connect(self.clear_input)

        # Sort by order button
        self.sort_order_button = QPushButton("Artan yaxud azalan sırayla çeşidlə")
        self.sort_order_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.sort_order_button.setStyleSheet("""
            QPushButton {
                background-color: #238723;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: lightgreen;
            }
        """)
        self.sort_order_button.clicked.connect(self.ask_sort_order)

        # Adjust layout
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.input_label, alignment=Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(self.input_field, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.sort_order_button)
        button_layout.addStretch()

        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #ff793f;")
        self.setGeometry(100, 100, 500, 300)

    def sort_numbers(self):
        input_text = self.input_field.toPlainText()
        if not input_text:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return
        try:
            numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))
        except ValueError:
            self.show_message("Zəhmət olmasa iki ədəd daxil edin")
            return

        if len(numbers) < 2:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return

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

    def ask_sort_order(self):
        input_text = self.input_field.toPlainText()
        if not input_text:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return
        try:
            numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))
        except ValueError:
            self.show_message("Zəhmət olmasa iki ədəd daxil edin")
            return

        if len(numbers) < 2:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return

        order_dialog = QDialog(self)
        order_dialog.setWindowTitle("Çeşidləmə növü")

        layout = QVBoxLayout()
        message = QLabel("Siz verilmiş ədədləri artan, yoxsa azalan sırayla çeşidləmək istəyirsiz?")
        message.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        layout.addWidget(message)

        button_layout = QHBoxLayout()
        artan_button = QPushButton("Artan sırayla çeşidlə")
        artan_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        artan_button.setStyleSheet("""
            QPushButton {
                background-color: darkviolet;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: violet;
            }
        """)
        artan_button.clicked.connect(lambda: self.handle_sort_order(order_dialog, "Artan"))
        button_layout.addWidget(artan_button)

        azalan_button = QPushButton("Azalan sırayla çeşidlə")
        azalan_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        azalan_button.setStyleSheet("""
            QPushButton {
                background-color: darkviolet;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: violet;
            }
        """)
        azalan_button.clicked.connect(lambda: self.handle_sort_order(order_dialog, "Azalan"))
        button_layout.addWidget(azalan_button)

        layout.addLayout(button_layout)
        order_dialog.setLayout(layout)
        order_dialog.setStyleSheet("""
            QDialog {
                background-color: lightgreen;
                border-radius: 15px;
            }
        """)
        order_dialog.exec()

    def handle_sort_order(self, dialog, order):
        dialog.accept()
        self.sort_by_order(order)

    def sort_by_order(self, order):
        input_text = self.input_field.toPlainText()
        numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))

        if order == "Artan":
            sorted_numbers = sorted(numbers)
        else:
            sorted_numbers = sorted(numbers, reverse=True)

        result_text = ""
        positive_integers = [int(num) for num in sorted_numbers if num > 0 and num.is_integer()]
        negative_integers = [int(num) for num in sorted_numbers if num < 0 and num.is_integer()]
        positive_decimals = [num for num in sorted_numbers if num > 0 and not num.is_integer()]
        negative_decimals = [num for num in sorted_numbers if num < 0 and not num.is_integer()]

        if positive_integers:
            result_text += "Müsbət ədədlər: " + ", ".join(map(str, positive_integers)) + "\n"
        if negative_integers:
            result_text += "Mənfi ədədlər: " + ", ".join(map(str, negative_integers)) + "\n"
        if positive_decimals:
            result_text += "Müsbət onluq ədədlər: " + ", ".join(map(str, positive_decimals)) + "\n"
        if negative_decimals:
            result_text += "Mənfi onluq ədədlər: " + ", ".join(map(str, negative_decimals)) + "\n"

        self.show_result_window(result_text)

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
                border: 5px solid white;  # Change pink border to white
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

    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle("Xəbərdarlıq")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SortingProgram()
    ex.show()
    sys.exit(app.exec())
