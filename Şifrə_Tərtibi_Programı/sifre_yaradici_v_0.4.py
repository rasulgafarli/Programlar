t, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Şifrə Yaradıcı v0.4')
        self.setFixedSize(350, 300)

        # Əsas Dizayn (QSS)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #0f172a);
                color: #f8fafc;
            }
            QLabel {
                background: transparent;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit, QSpinBox {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 8px;
                font-size: 14px;
                color: #60a5fa;
                selection-background-color: #3b82f6;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #3b82f6;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.8), 
                    stop:1 rgba(37, 99, 235, 0.9));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 18px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 12px;
                /* Şüşə effekti üçün kölgə simulyasiyası */
                border-bottom: 3px solid rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(96, 165, 250, 0.9), 
                    stop:1 rgba(59, 130, 246, 1));
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background: #1d4ed8;
                border-bottom: 1px solid transparent;
                margin-top: 2px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        self.label = QLabel('Şifrə uzunluğunu seçin:')
        layout.addWidget(self.label)

        self.length_spin = QSpinBox()
        self.length_spin.setRange(6, 64)
        self.length_spin.setValue(16)
        layout.addWidget(self.length_spin)

        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Şifrə burada görünəcək...")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_input)

        self.btn = QPushButton('Şifrə Yarat')
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spin.value()
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(chars) for _ in range(length))
        self.result_input.setText(password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec())