import sys
import random
import string
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QClipboard


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Şifrə Yaradıcı v0.8')
        self.setFixedSize(400, 350)

        # v0.8 Dizayn (QSS)
        # Background: Tünddən daha açığa doğru (Slate 950 -> Slate 700)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #020617, 
                    stop:1 #334155);
                color: #f1f5f9;
            }
            QLabel {
                background: transparent;
                font-size: 13px;
                font-weight: bold;
                color: #94a3b8;
            }
            #PasswordInput {
                background-color: rgba(71, 85, 105, 0.4); /* Açıq arxa fon tonu */
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                color: #38bdf8;
            }
            QSpinBox {
                background-color: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 8px;
                color: #38bdf8;
            }
            /* Action Button Styles (Copy/Clear) */
            .ActionButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                font-weight: bold;
                min-width: 40px;
                padding: 8px;
            }
            .ActionButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            #MainBtn {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0ea5e9, 
                    stop:1 #7dd3fc);
                border-radius: 15px;
                color: #020617;
                font-size: 15px;
                font-weight: 800;
                padding: 15px;
                border-bottom: 4px solid #0369a1;
            }
            #MainBtn:hover {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #38bdf8, 
                    stop:1 #bae6fd);
            }
            #MainBtn:pressed {
                border-bottom: 1px solid transparent;
                margin-top: 3px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        layout.addWidget(QLabel('ŞİFRƏ UZUNLUĞU:'))

        self.length_spin = QSpinBox()
        self.length_spin.setRange(8, 128)
        self.length_spin.setValue(16)
        layout.addWidget(self.length_spin)

        # Şifrə hissəsi üçün Horizontal Layout
        pass_row = QHBoxLayout()

        self.result_input = QLineEdit()
        self.result_input.setObjectName("PasswordInput")
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("...")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pass_row.addWidget(self.result_input)

        # Copy Düyməsi
        self.copy_btn = QPushButton('📋')
        self.copy_btn.setProperty("class", "ActionButton")
        self.copy_btn.setToolTip("Kopyala")
        self.copy_btn.clicked.connect(self.copy_password)
        pass_row.addWidget(self.copy_btn)

        # Sil (X) Düyməsi
        self.clear_btn = QPushButton('X')
        self.clear_btn.setProperty("class", "ActionButton")
        self.clear_btn.setToolTip("Təmizlə")
        self.clear_btn.clicked.connect(self.clear_password)
        pass_row.addWidget(self.clear_btn)

        layout.addLayout(pass_row)

        self.btn = QPushButton('YENİ ŞİFRƏ YARAT ↻')
        self.btn.setObjectName("MainBtn")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spin.value()
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))
        self.result_input.setText(password)

    def copy_password(self):
        password = self.result_input.text()
        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)

    def clear_password(self):
        self.result_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec())