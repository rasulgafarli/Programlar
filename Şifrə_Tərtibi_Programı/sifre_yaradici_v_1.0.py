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
        self.setWindowTitle('Şifrə Yaradıcı v1.0 - Professional')
        self.setFixedSize(420, 480)

        # v1.0 Dizayn (QSS)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #020617, 
                    stop:1 #475569); /* Daha açıq alt hissə */
                color: #f1f5f9;
            }
            QLabel {
                background: transparent;
                font-size: 12px;
                font-weight: bold;
                color: #94a3b8;
                text-transform: uppercase;
            }
            #PasswordInput {
                background-color: rgba(15, 23, 42, 0.6);
                border: 2px solid rgba(56, 189, 248, 0.2);
                border-radius: 12px;
                padding: 12px;
                font-size: 18px;
                font-family: 'Consolas', monospace;
                color: #38bdf8;
            }
            QSpinBox, QCheckBox {
                background: transparent;
                color: #cbd5e1;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #38bdf8;
                background: rgba(255, 255, 255, 0.05);
            }
            QCheckBox::indicator:checked {
                background: #0ea5e9;
            }

            #StrengthLabel {
                font-size: 14px;
                padding: 5px;
                border-radius: 6px;
                background: rgba(0,0,0,0.2);
            }

            .ActionButton {
                background: rgba(56, 189, 248, 0.1);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 10px;
                color: #7dd3fc;
                font-weight: bold;
                padding: 8px 12px;
            }
            .ActionButton:hover {
                background: rgba(56, 189, 248, 0.25);
            }

            #MainBtn {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0284c7, 
                    stop:1 #38bdf8);
                border-radius: 18px;
                color: #020617;
                font-size: 16px;
                font-weight: 900;
                padding: 18px;
                border-bottom: 5px solid #0369a1;
            }
            #MainBtn:hover {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0ea5e9, 
                    stop:1 #7dd3fc);
            }
            #MainBtn:pressed {
                border-bottom: 1px solid transparent;
                margin-top: 4px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(18)

        # Uzunluq seçimi
        layout.addWidget(QLabel('ŞİFRƏ UZUNLUĞU:'))
        self.length_spin = QSpinBox()
        self.length_spin.setRange(6, 128)
        self.length_spin.setValue(16)
        layout.addWidget(self.length_spin)

        # Seçimlər (Checkbox-lar)
        self.check_nums = QCheckBox("Rəqəmlər olsun (0-9)")
        self.check_nums.setChecked(True)
        self.check_syms = QCheckBox("Simvollar olsun (!@#$...)")
        self.check_syms.setChecked(True)
        layout.addWidget(self.check_nums)
        layout.addWidget(self.check_syms)

        # Nəticə xanası
        self.result_input = QLineEdit()
        self.result_input.setObjectName("PasswordInput")
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Şifrəni yaradın...")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_input)

        # Güc indikatoru
        self.strength_label = QLabel('Güc: -')
        self.strength_label.setObjectName("StrengthLabel")
        self.strength_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.strength_label)

        # Düymələr sırası
        btn_row = QHBoxLayout()

        self.copy_btn = QPushButton('Copy')
        self.copy_btn.setProperty("class", "ActionButton")
        self.copy_btn.clicked.connect(self.copy_password)
        btn_row.addWidget(self.copy_btn)

        self.clear_btn = QPushButton('Sil (X)')
        self.clear_btn.setProperty("class", "ActionButton")
        self.clear_btn.clicked.connect(self.clear_password)
        btn_row.addWidget(self.clear_btn)

        layout.addLayout(btn_row)

        self.btn = QPushButton('ŞİFRƏNİ TƏRTİB ET ↻')
        self.btn.setObjectName("MainBtn")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spin.value()
        char_pool = string.ascii_letters
        if self.check_nums.isChecked():
            char_pool += string.digits
        if self.check_syms.isChecked():
            char_pool += string.punctuation

        password = "".join(random.choice(char_pool) for _ in range(length))
        self.result_input.setText(password)
        self.update_strength(password)

    def update_strength(self, pwd):
        length = len(pwd)
        has_num = any(c.isdigit() for c in pwd)
        has_sym = any(not c.isalnum() for c in pwd)

        score = length
        if has_num: score += 5
        if has_sym: score += 7

        if score < 15:
            text, color = "Zəif", "#ef4444"
        elif score < 25:
            text, color = "Orta", "#f59e0b"
        else:
            text, color = "Güclü", "#10b981"

        self.strength_label.setText(f"GÜC: {text}")
        self.strength_label.setStyleSheet(f"color: {color}; font-weight: bold; background: rgba(0,0,0,0.3);")

    def copy_password(self):
        password = self.result_input.text()
        if password:
            QApplication.clipboard().setText(password)
            self.copy_btn.setText("Kopyalandı!")
            self.copy_btn.setStyleSheet("color: #10b981; border-color: #10b981;")
            QTimer.singleShot(2000, self.reset_copy_text)

    def reset_copy_text(self):
        self.copy_btn.setText("Copy")
        self.copy_btn.setStyleSheet("")

    def clear_password(self):
        self.result_input.clear()
        self.strength_label.setText("Güc: -")
        self.strength_label.setStyleSheet("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec())