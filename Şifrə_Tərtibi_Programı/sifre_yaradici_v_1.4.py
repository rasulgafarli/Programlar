import sys
import random
import string
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QSpinBox, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Şifrə Yaradıcı')
        self.setFixedSize(450, 600)

        # Professional Master QSS Styling
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0f172a, 
                    stop:1 #334155);
                color: #f1f5f9;
            }
            QLabel {
                background: transparent;
                font-size: 11px;
                font-weight: 800;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            #PasswordInput {
                background-color: rgba(15, 23, 42, 0.9);
                border: 2px solid #38bdf8;
                border-radius: 20px;
                padding: 15px;
                font-size: 14px;
                font-family: 'Consolas', monospace;
                color: #7dd3fc;
            }
            QSpinBox {
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid #38bdf8;
                border-radius: 20px;
                padding: 8px 15px;
                color: #38bdf8;
                font-weight: bold;
                min-height: 40px;
            }
            QCheckBox {
                color: #e2e8f0;
                font-size: 13px;
                spacing: 12px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 12px;
                border: 2px solid #38bdf8;
                background: rgba(0, 0, 0, 0.2);
            }
            QCheckBox::indicator:checked {
                background-color: #38bdf8;
                border: 2px solid #ffffff;
                /* Note: We use a visual fill to signify "checked" clearly */
            }

            .ActionButton {
                background: rgba(56, 189, 248, 0.1);
                border: 1px solid #38bdf8;
                border-radius: 20px;
                color: #7dd3fc;
                font-weight: bold;
                padding: 10px 20px;
                border-bottom: 3px solid #0369a1;
            }
            .ActionButton:hover {
                background: rgba(56, 189, 248, 0.2);
            }
            .ActionButton:pressed {
                border-bottom: 1px solid transparent;
                margin-top: 2px;
            }

            #MainBtn {
                background: #38bdf8;
                border-radius: 25px;
                color: #020617; /* High contrast dark text */
                font-size: 16px;
                font-weight: 900;
                padding: 20px;
                border-bottom: 6px solid #0369a1;
            }
            #MainBtn:hover {
                background: #7dd3fc;
            }
            #MainBtn:pressed {
                border-bottom: 2px solid transparent;
                margin-top: 4px;
            }

            .StrengthBtn {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 8px;
                font-size: 11px;
                font-weight: bold;
                color: #94a3b8;
            }
            .StrengthBtn:hover { 
                background: rgba(56, 189, 248, 0.1); 
                color: #38bdf8;
            }
            #ActiveStrength { 
                border: 2px solid #38bdf8; 
                color: #38bdf8; 
                background: rgba(56, 189, 248, 0.2); 
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        # Title
        title_label = QLabel('Təhlükəsiz Şifrə Paneli')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; color: #38bdf8; font-weight: 900; letter-spacing: 2px;")
        layout.addWidget(title_label)

        # Length Input
        layout.addWidget(QLabel('Şifrə Uzunluğu:'))
        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 128)
        self.length_spin.setValue(16)
        layout.addWidget(self.length_spin)

        # Strength Presets
        layout.addWidget(QLabel('Hədəf Güc:'))
        strength_row = QHBoxLayout()
        self.btn_weak = QPushButton("Zəif")
        self.btn_medium = QPushButton("Orta")
        self.btn_strong = QPushButton("Güclü")

        for b in [self.btn_weak, self.btn_medium, self.btn_strong]:
            b.setProperty("class", "StrengthBtn")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            strength_row.addWidget(b)

        self.btn_weak.clicked.connect(lambda: self.apply_preset("weak"))
        self.btn_medium.clicked.connect(lambda: self.apply_preset("medium"))
        self.btn_strong.clicked.connect(lambda: self.apply_preset("strong"))
        layout.addLayout(strength_row)

        # Options
        self.check_nums = QCheckBox("Rəqəmlər (0-9)")
        self.check_nums.setChecked(True)
        self.check_syms = QCheckBox("Simvollar (!@#$...)")
        self.check_syms.setChecked(True)
        layout.addWidget(self.check_nums)
        layout.addWidget(self.check_syms)

        # Result Display
        self.result_input = QLineEdit()
        self.result_input.setObjectName("PasswordInput")
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Şifrə daxil edilməyib")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_input)

        # Utility Buttons
        btn_row = QHBoxLayout()
        self.copy_btn = QPushButton('Kopyala')
        self.copy_btn.setProperty("class", "ActionButton")
        self.copy_btn.clicked.connect(self.copy_password)
        btn_row.addWidget(self.copy_btn)

        self.clear_btn = QPushButton('Sil')
        self.clear_btn.setProperty("class", "ActionButton")
        self.clear_btn.clicked.connect(self.clear_password)
        btn_row.addWidget(self.clear_btn)
        layout.addLayout(btn_row)

        # Main Action Button
        self.btn = QPushButton('ŞİFRƏ TƏRTİB ET')
        self.btn.setObjectName("MainBtn")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def apply_preset(self, mode):
        # Reset visual IDs
        self.btn_weak.setObjectName("")
        self.btn_medium.setObjectName("")
        self.btn_strong.setObjectName("")

        if mode == "weak":
            self.length_spin.setValue(8)
            self.check_nums.setChecked(False)
            self.check_syms.setChecked(False)
            self.btn_weak.setObjectName("ActiveStrength")
        elif mode == "medium":
            self.length_spin.setValue(14)
            self.check_nums.setChecked(True)
            self.check_syms.setChecked(False)
            self.btn_medium.setObjectName("ActiveStrength")
        elif mode == "strong":
            self.length_spin.setValue(24)
            self.check_nums.setChecked(True)
            self.check_syms.setChecked(True)
            self.btn_strong.setObjectName("ActiveStrength")

        self.setStyle(self.style())

    def generate_password(self):
        length = self.length_spin.value()
        char_pool = string.ascii_letters
        if self.check_nums.isChecked(): char_pool += string.digits
        if self.check_syms.isChecked(): char_pool += string.punctuation

        password = "".join(random.choice(char_pool) for _ in range(length))
        self.result_input.setText(password)

    def copy_password(self):
        password = self.result_input.text()
        if password:
            QApplication.clipboard().setText(password)
            self.copy_btn.setText("Kopyalandı!")
            QTimer.singleShot(1500, lambda: self.copy_btn.setText("Kopyala"))

    def clear_password(self):
        self.result_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec())