import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QTextEdit, \
    QMessageBox, QScrollBar, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SortingProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.history = []

    def initUI(self):
        self.setWindowTitle("Ədədlərin çeşidlənməsi programı - v3")

        # Main layout
        main_layout = QVBoxLayout()

        # Top layout for history button
        top_layout = QHBoxLayout()
        self.history_button = QPushButton("Tarixçə")
        self.history_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.history_button.setStyleSheet("""
            QPushButton {
                background-color: #DF1288;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #C2185B;
            }
        """)
        self.history_button.clicked.connect(self.show_history)
        top_layout.addStretch()
        top_layout.addWidget(self.history_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Input label
        self.input_label = QLabel("Ədədləri daxil edin:")
        self.input_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_label.setStyleSheet("color: black;")

        # Input field
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

        # Delete single character button
        self.delete_button = QPushButton("X")
        self.delete_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #686466;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: gray;
            }
        """)
        self.delete_button.setFixedSize(40, 40)
        self.delete_button.clicked.connect(self.delete_single_character)

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

        # Sort by both order button
        self.sort_both_order_button = QPushButton("Artan və azalanı bir sırada çeşidləyin")
        self.sort_both_order_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.sort_both_order_button.setStyleSheet("""
            QPushButton {
                background-color: #891B0A;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #A62E1C;
            }
        """)
        self.sort_both_order_button.clicked.connect(self.show_both_order_page)

        # Adjust layout
        main_layout.addLayout(top_layout)

        # Add spacer to push the input field to the upper part of the window
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addWidget(self.input_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.input_field, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.sort_order_button)
        main_layout.addLayout(button_layout)

        both_order_button_layout = QHBoxLayout()
        both_order_button_layout.addStretch()
        both_order_button_layout.addWidget(self.sort_both_order_button)
        both_order_button_layout.addStretch()
        main_layout.addLayout(both_order_button_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #ff793f;")
        self.setGeometry(100, 100, 600, 400)

    def sort_numbers(self):
        input_text = self.input_field.toPlainText()
        if not input_text:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return
        try:
            numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))
        except ValueError:
            self.show_message("Zəhmət olmasa ən azı 2 ədəd daxil edin")
            return

        if len(numbers) < 2:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return

        result_text = "Çeşidlənən ədədlər:\n"
        positive_integers = [int(num) for num in numbers if num > 0 and num.is_integer()]
        negative_integers = [int(num) for num in numbers if num < 0 and num.is_integer()]
        positive_decimals = [num for num in numbers if num > 0 and not num.is_integer()]
        negative_decimals = [num for num in numbers if num < 0 and not num.is_integer()]

        if negative_decimals:
            result_text += "Mənfi onluq ədədlər: " + ", ".join(map(str, negative_decimals)) + "\n"
        if negative_integers:
            result_text += "Mənfi ədədlər: " + ", ".join(map(str, negative_integers)) + "\n"
        if positive_decimals:
            result_text += "Müsbət onluq ədədlər: " + ", ".join(map(str, positive_decimals)) + "\n"
        if positive_integers:
            result_text += "Müsbət ədədlər: " + ", ".join(map(str, positive_integers)) + "\n"

        self.history.append(result_text)
        self.show_result_window(result_text)

    def clear_input(self):
        if not self.input_field.toPlainText().strip():
            self.show_message("Silmək üçün bir ədəd yoxdur.")
        else:
            self.input_field.clear()

    def delete_single_character(self):
        cursor = self.input_field.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.deletePreviousChar()

    def ask_sort_order(self):
        input_text = self.input_field.toPlainText()
        if not input_text:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return
        try:
            numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))
        except ValueError:
            self.show_message("Zəhmət olmasa ən azı 2 ədəd daxil edin")
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
                background-color: #7B7671;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: #B5DA09;
            }
        """)
        artan_button.clicked.connect(lambda: self.handle_sort_order(order_dialog, "Artan"))
        button_layout.addWidget(artan_button)

        azalan_button = QPushButton("Azalan sırayla çeşidlə")
        azalan_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        azalan_button.setStyleSheet("""
            QPushButton {
                background-color: #7B7671;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: #B5DA09;
            }
        """)
        azalan_button.clicked.connect(lambda: self.handle_sort_order(order_dialog, "Azalan"))
        button_layout.addWidget(azalan_button)

        # Back button
        back_button = QPushButton("Geri")
        back_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3A5582;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: #2E4372;
            }
        """)
        back_button.clicked.connect(order_dialog.reject)
        button_layout.addWidget(back_button)

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

        result_text = "Çeşidlənən ədədlər:\n"
        negative_decimals = [num for num in sorted_numbers if num < 0 and not num.is_integer()]
        negative_integers = [int(num) for num in sorted_numbers if num < 0 and num.is_integer()]
        positive_decimals = [num for num in sorted_numbers if num > 0 and not num.is_integer()]
        positive_integers = [int(num) for num in sorted_numbers if num > 0 and num.is_integer()]

        if negative_decimals:
            result_text += "Mənfi onluq ədədlər: " + ", ".join(map(str, negative_decimals)) + "\n"
        if negative_integers:
            result_text += "Mənfi ədədlər: " + ", ".join(map(str, negative_integers)) + "\n"
        if positive_decimals:
            result_text += "Müsbət onluq ədədlər: " + ", ".join(map(str, positive_decimals)) + "\n"
        if positive_integers:
            result_text += "Müsbət ədədlər: " + ", ".join(map(str, positive_integers)) + "\n"

        self.history.append(result_text)
        self.show_result_window(result_text)

    def show_history(self):
        history_window = QDialog(self)
        history_window.setWindowTitle("Tarixçə")

        layout = QVBoxLayout()
        history_display = QTextEdit()
        history_display.setFont(QFont("Arial", 12))
        history_display.setReadOnly(True)
        history_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid gray;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        history_content = "\n\n".join(reversed(self.history))
        history_display.setText(history_content)

        close_button = QPushButton("Bağla")
        close_button.setFont(QFont("Arial", 12))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: lightgray;
            }
        """)
        close_button.clicked.connect(history_window.accept)

        back_button = QPushButton("Geri")
        back_button.setFont(QFont("Arial", 12))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3A5582;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #2E4372;
            }
        """)
        back_button.clicked.connect(history_window.reject)

        layout.addWidget(history_display)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        history_window.setLayout(layout)
        history_window.setStyleSheet("""
            QDialog {
                background-color: lightgreen;
                border-radius: 15px;
            }
        """)
        history_window.setFixedSize(400, 500)
        history_window.exec()

    def show_result_window(self, result_text):
        result_window = QDialog(self)
        result_window.setWindowTitle("Nəticələr")

        layout = QVBoxLayout()

        result_display = QLabel(result_text)
        result_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_display.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        result_display.setStyleSheet("color: white;")
        result_display.setWordWrap(True)  # Enable word wrap to prevent text overflow

        back_button = QPushButton("Geri")
        back_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3A5582;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:pressed {
                background-color: #2E4372;
            }
        """)
        back_button.clicked.connect(result_window.reject)

        layout.addWidget(result_display)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def show_both_order_page(self):
        input_text = self.input_field.toPlainText()
        if not input_text:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return
        try:
            numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))
        except ValueError:
            self.show_message("Zəhmət olmasa ən azı 2 ədəd daxil edin")
            return

        if len(numbers) < 2:
            self.show_message("Xahiş edirik ən azı 2 ədəd daxil edin")
            return

        both_order_dialog = QDialog(self)
        both_order_dialog.setWindowTitle("Artan və Azalan Çeşidləmə")

        layout = QVBoxLayout()
        message = QLabel("Siz verilmiş ədədləri artan, yoxsa azalan sırayla çeşidləmək istəyirsiz?")
        message.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                background-color: #DAA2C1;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        layout.addWidget(message)

        button_layout = QHBoxLayout()
        artan_button = QPushButton("Artan sırayla çeşidlə")
        artan_button.setFont(QFont("Arial", 10))
        artan_button.setStyleSheet("""
            QPushButton {
                background-color: #7B7671;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: #B5DA09;
            }
        """)
        artan_button.clicked.connect(lambda: self.handle_both_order_sort(both_order_dialog, "Artan"))
        button_layout.addWidget(artan_button)

        azalan_button = QPushButton("Azalan sırayla çeşidlə")
        azalan_button.setFont(QFont("Arial", 10))
        azalan_button.setStyleSheet("""
            QPushButton {
                background-color: #7B7671;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: #B5DA09;
            }
        """)
        azalan_button.clicked.connect(lambda: self.handle_both_order_sort(both_order_dialog, "Azalan"))
        button_layout.addWidget(azalan_button)

        # Back button
        back_button = QPushButton("Geri")
        back_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3A5582;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:pressed {
                background-color: #2E4372;
            }
        """)
        back_button.clicked.connect(both_order_dialog.reject)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        both_order_dialog.setLayout(layout)
        both_order_dialog.setStyleSheet("""
            QDialog {
                background-color: #E3077F;
                border-radius: 15px;
            }
        """)
        both_order_dialog.exec()

    def handle_both_order_sort(self, dialog, order):
        dialog.accept()
        self.sort_by_both_order(order)

    def sort_by_both_order(self, order):
        input_text = self.input_field.toPlainText()
        numbers = list(dict.fromkeys([float(num) for num in input_text.split(',') if num.strip()]))

        if order == "Artan":
            sorted_numbers = sorted(numbers)
        else:
            sorted_numbers = sorted(numbers, reverse=True)

        negative_decimals = [num for num in sorted_numbers if num < 0 and not num.is_integer()]
        negative_integers = [int(num) for num in sorted_numbers if num < 0 and num.is_integer()]
        positive_decimals = [num for num in sorted_numbers if num > 0 and not num.is_integer()]
        positive_integers = [int(num) for num in sorted_numbers if num > 0 and num.is_integer()]

        result_text = "Çeşidlənən ədədlər:\n"
        if order == "Artan":
            if negative_decimals:
                result_text += ", ".join(map(str, negative_decimals)) + "\n"
            if negative_integers:
                result_text += ", ".join(map(str, negative_integers)) + "\n"
            result_text += "0\n"
            if positive_integers:
                result_text += ", ".join(map(str, positive_integers)) + "\n"
            if positive_decimals:
                result_text += ", ".join(map(str, positive_decimals)) + "\n"
        else:
            if positive_decimals:
                result_text += ", ".join(map(str, positive_decimals)) + "\n"
            if positive_integers:
                result_text += ", ".join(map(str, positive_integers)) + "\n"
            result_text += "0\n"
            if negative_integers:
                result_text += ", ".join(map(str, negative_integers)) + "\n"
            if negative_decimals:
                result_text += ", ".join(map(str, negative_decimals)) + "\n"

        self.history.append(result_text)
        self.show_result_window(result_text)

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
