import sys
import random
import string
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QSpinBox, QCheckBox, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Şifrə Yaradıcı v1.2 - Master')
        self.setFixedSize(450, 550)

        # v1.2 Dizayn (QSS)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #020617, 
                    stop:1 #64748b); /* Daha da açıq alt hissə */
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
                background-color: rgba(15, 23, 42, 0.7);
                border: 2px solid rgba(56, 189, 248, 0.3);
                border-radius: 15px;
                padding: 15px;
                font-size: 20px;
                font-family: 'Consolas', 'Courier New', monospace;
                color: #38bdf8;
            }
            QSpinBox {
                background: rgba(15, 23, 42, 0.5);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 18px; /* Oval forma */
                padding: 8px 15px;
                color: #38bdf8;
                font-weight: bold;
                min-height: 35px;
            }
            QCheckBox {
                color: #cbd5e1;
                font-size: 13px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 1px solid #0ea5e9;
                background: rgba(0, 0, 0, 0.2);
            }
            QCheckBox::indicator:checked {
                background: #0ea5e9;
                image: url(check.png); /* Note: Placeholder for actual image */
            }

            /* Oval Scrollbar Styling */
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(56, 189, 248, 0.4);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            .ActionButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(56, 189, 248, 0.2), 
                    stop:1 rgba(56, 189, 248, 0.1));
                border: 1px solid rgba(56, 189, 248, 0.4);
                border-radius: 15px; /* Oval */
                color: #7dd3fc;
                font-weight: bold;
                padding: 10px 20px;
                border-bottom: 3px solid rgba(0, 0, 0, 0.3); /* Kölgə effekti */
            }
            .ActionButton:hover {
                background: rgba(56, 189, 248, 0.3);
                border: 1px solid #38bdf8;
            }
            .ActionButton:pressed {
                border-bottom: 1px solid transparent;
                margin-top: 2px;
            }

            #MainBtn {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0284c7, 
                    stop:1 #7dd3fc);
                border-radius: 22px; /* Tam oval */
                color: #020617;
                font-size: 16px;
                font-weight: 900;
                padding: 20px;
                border-bottom: 6px solid #0369a1;
                margin-top: 10px;
            }
            #MainBtn:hover {
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0, 
                    stop:0 #0ea5e9, 
                    stop:1 #bae6fd);
            }
            #MainBtn:pressed {
                border-bottom: 2px solid transparent;
                margin-top: 14px;
            }

            .StrengthBtn {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 5px;
                font-size: 10px;
                color: #94a3b8;
            }
            .StrengthBtn:hover { background: rgba(255, 255, 255, 0.1); }
            .ActiveStrength { border: 1px solid #38bdf8; color: #38bdf8; background: rgba(56, 189, 248, 0.1); }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Başlıq
        title = QLabel('V 1.2 MASTER SECURITY')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Uzunluq seçimi
        layout.addWidget(QLabel('ŞİFRƏ UZUNLUĞU:'))
        self.length_spin = QSpinBox()
        self.length_spin.setRange(6, 128)
        self.length_spin.setValue(16)
        layout.addWidget(self.length_spin)

        # Güc Seçimi (Presetlər)
        layout.addWidget(QLabel('HƏDƏF GÜC:'))
        strength_row = QHBoxLayout()
        self.btn_weak = QPushButton("Zəif")
        self.btn_medium = QPushButton("Orta")
        self.btn_strong = QPushButton("Güclü")
        for b in [self.btn_weak, self.btn_medium, self.btn_strong]:
            b.setProperty("class", "StrengthBtn")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            strength_row.addWidget(b)

        self.btn_weak.clicked.connect(lambda: self.set_preset("weak"))
        self.btn_medium.clicked.connect(lambda: self.set_preset("medium"))
        self.btn_strong.clicked.connect(lambda: self.set_preset("strong"))
        layout.addLayout(strength_row)

        # Seçimlər
        self.check_nums = QCheckBox("Rəqəmlər (0-9)")
        self.check_nums.setChecked(True)
        self.check_syms = QCheckBox("Simvollar (!@#$...)")
        self.check_syms.setChecked(True)
        layout.addWidget(self.check_nums)
        layout.addWidget(self.check_syms)

        # Nəticə xanası
        self.result_input = QLineEdit()
        self.result_input.setObjectName("PasswordInput")
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Generate...")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_input)

        # Düymələr sırası
        btn_row = QHBoxLayout()

        self.copy_btn = QPushButton('Kopyala')
        self.copy_btn.setProperty("class", "ActionButton")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_password)
        btn_row.addWidget(self.copy_btn)

        self.clear_btn = QPushButton('Sil')
        self.clear_btn.setProperty("class", "ActionButton")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_password)
        btn_row.addWidget(self.clear_btn)

        layout.addLayout(btn_row)

        self.btn = QPushButton('ŞİFRƏNİ TƏRTİB ET ↻')
        self.btn.setObjectName("MainBtn")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.generate_password)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def set_preset(self, level):
        if level == "weak":
            self.length_spin.setValue(8)
            self.check_nums.setChecked(False)
            self.check_syms.setChecked(False)
        elif level == "medium":
            self.length_spin.setValue(14)
            self.check_nums.setChecked(True)
            self.check_syms.setChecked(False)
        elif level == "strong":
            self.length_spin.setValue(24)
            self.check_nums.setChecked(True)
            self.check_syms.setChecked(True)

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