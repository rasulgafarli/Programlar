import sys
import random
import string
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Şifrə Yaradıcı v0.6')
        self.setFixedSize(350, 320)

        # v0.6 Yeni Dizayn (QSS)
        # Background: Tünddən açığa, Yuxarıdan Aşağıya
        # Button: Tünddən açığa, Aşağıdan Yuxarıya
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #020617, 
                    stop:1 #1e293b);
                color: #f1f5f9;
            }
            QLabel {
                background: transparent;
                font-size: 13px;
                font-weight: 600;
                color: #94a3b8;
                margin-bottom: 2px;
            }
            QLineEdit, QSpinBox {
                background-color: rgba(30, 41, 59, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 14px;
                padding: 10px;
                font-size: 14px;
                color: #38bdf8;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #0ea5e9;
                background-color: rgba(30, 41, 59, 0.9);
            }
            QPushButton {
                /* Button Gradient: Aşağıdan Yuxarıya (x1:0, y1:1 to x2:0, y2:0) */
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0369a1, 
                    stop:1 #38bdf8);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 14px;
                border-bottom: 4px solid #075985;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0ea5e9, 
                    stop:1 #7dd3fc);
            }
            QPushButton:pressed {
                background: #0284c7;
                border-bottom: 1px solid transparent;
                margin-top: 3px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        self.label = QLabel('ŞİFRƏ UZUNLUĞU')
        layout.addWidget(self.label)

        self.length_spin = QSpinBox()
        self.length_spin.setRange(8, 128)
        self.length_spin.setValue(20)
        layout.addWidget(self.length_spin)

        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Şifrəni yaratmaq üçün basın...")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_input)

        # Ox ilə Yenilə işarəsi (↻)
        self.btn = QPushButton('Şifrəni Yenilə ↻')
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spin.value()
        # Daha güclü simvollar seti
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))
        self.result_input.setText(password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec())