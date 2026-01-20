import sys
import random
import string
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Program pəncərəsinin başlığı
        self.setWindowTitle('Şifrə Yaradıcı v0.2')
        self.setFixedSize(300, 200)

        # Layout (düzülüş) yaradılması
        layout = QVBoxLayout()

        # Etiket (Label)
        self.label = QLabel('Şifrə uzunluğunu seçin:')
        layout.addWidget(self.label)

        # Uzunluq seçimi üçün SpinBox
        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 32)
        self.length_spin.setValue(12)
        layout.addWidget(self.length_spin)

        # Nəticəni göstərmək üçün Input (Oxumaq üçün)
        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Şifrə burada görünəcək...")
        layout.addWidget(self.result_input)

        # Düymə (Button)
        self.btn = QPushButton('Şifrə Yarat')
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spin.value()
        # Sadə simvollar çoxluğu (hərflər və rəqəmlər)
        chars = string.ascii_letters + string.digits
        password = "".join(random.choice(chars) for _ in range(length))
        self.result_input.setText(password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec())