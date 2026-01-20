# --- Söz və Hərf Sayğacı Proqramı (Yeni Düymə Stili ilə) ---

import sys
# DƏYİŞİKLİK: Kölgə üçün yeni importlar əlavə edildi
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QDialog, QGraphicsDropShadowEffect)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt


# ==============================================================================
# NƏTİCƏ PƏNCƏRƏSİ
# ==============================================================================
class ResultsWindow(QDialog):
    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hesablama Nəticəsi")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #F0F3F4;")
        words = sentence_to_analyze.strip().split()
        word_count = len(words)
        char_count = len(sentence_to_analyze)
        self.result_label = QLabel(f"Söz sayı: {word_count}\nSimvol sayı: {char_count}")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        self.setLayout(layout)


# ==============================================================================
# ƏSAS PƏNCƏRƏ
# ==============================================================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Söz Təhlili")
        self.setGeometry(300, 300, 500, 250)

        self.sentence_to_pass = ""

        self.info_label = QLabel("Təhlil etmək üçün aşağıdakı xanaya bir cümlə yazın:")
        self.info_label.setFont(QFont("Arial", 12))

        self.input_box = QLineEdit()

        self.error_label = QLabel("İcazə verilməyən simvol daxil edildi!")
        self.error_label.setObjectName("errorLabel")
        self.error_label.hide()

        self.calculate_button = QPushButton("Hesabla")

        self.results_button = QPushButton("Söz/hərf sayı")
        self.results_button.setObjectName("resultsButton")
        self.results_button.hide()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.error_label)

        # DƏYİŞİKLİK: Düymələri loop ilə yaratmasaq da, hər birinə kölgəni ayrıca əlavə edirik
        # Hesabla düyməsi üçün kölgə
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(15)
        shadow1.setXOffset(2)
        shadow1.setYOffset(2)
        shadow1.setColor(QColor(0, 0, 0, 80))
        self.calculate_button.setGraphicsEffect(shadow1)

        # Söz/hərf sayı düyməsi üçün kölgə
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setXOffset(2)
        shadow2.setYOffset(2)
        shadow2.setColor(QColor(0, 0, 0, 80))
        self.results_button.setGraphicsEffect(shadow2)

        main_layout.addWidget(self.calculate_button)
        main_layout.addWidget(self.results_button)

        self.setLayout(main_layout)

        self.calculate_button.clicked.connect(self.validate_and_proceed)
        self.results_button.clicked.connect(self.open_results_window)

        self.apply_styles()

    def apply_styles(self):
        """Proqramın bütün vizual stilini təyin edən QSS kodu."""
        self.setStyleSheet("""
            QWidget { background-color: #F0F3F4; }
            QLineEdit {
                background-color: white; border: 1px solid #bdc3c7;
                padding: 10px 15px; font-size: 16px;
                border-radius: 22px; min-height: 24px;
            }
            QLineEdit[hasError="true"] { border: 2px solid #E74C3C; }

            /* DƏYİŞİKLİK: Düymə stilləri yeniləndi */
            QPushButton {
                color: white;
                font-size: 13px; /* Şrifti bir az kiçiltdik */
                font-weight: bold;
                padding: 8px; /* Daxili boşluğu azaldaraq düyməni kiçiltdik */
                border-radius: 16px; /* Hündürlüyə uyğun radius */
                border: none; /* Kölgənin daha yaxşı görünməsi üçün çərçivəni ləğv etdik */
                /* Yeni yüksək kontrastlı gradient */
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #85C1E9, stop:1 #1B4F72);
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #AED6F1, stop:1 #21618C);
            }
            QPushButton:pressed {
                background-color: #1B4F72; /* Tünd rəng */
            }

            /* Yaşıl düymə üçün də yüksək kontrastlı gradient */
            QPushButton#resultsButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #7DCEA0, stop:1 #145A32);
            }
            QPushButton#resultsButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #A9DFBF, stop:1 #196F3D);
            }
            QPushButton#resultsButton:pressed {
                background-color: #145A32;
            }
            QLabel#errorLabel { color: #E74C3C; padding-left: 10px; }
        """)

    def is_valid_sentence(self, text):
        if not text:
            return True
        allowed_chars = "abcdefghijklmnopqrstuvwxyzəöüıçşğABCDEFGHIJKLMNOPQRSTUVWXYZƏÖÜIÇŞĞ0123456789 .,:-"
        forbidden_start_chars = {'.', ',', ':', '-'}
        trimmed_text = text.lstrip()
        if trimmed_text and trimmed_text[0] in forbidden_start_chars:
            return False
        for char in text:
            if char not in allowed_chars:
                return False
        return True

    def validate_and_proceed(self):
        text = self.input_box.text()
        if self.is_valid_sentence(text) and text.strip():
            self.sentence_to_pass = text
            self.error_label.hide()
            self.results_button.show()
            self.input_box.setProperty("hasError", False)
            self.input_box.style().polish(self.input_box)
        else:
            self.results_button.hide()
            if text.strip():
                self.error_label.show()
                self.input_box.setProperty("hasError", True)
                self.input_box.style().polish(self.input_box)
            else:
                self.error_label.hide()
                self.input_box.setProperty("hasError", False)
                self.input_box.style().polish(self.input_box)

    def open_results_window(self):
        dialog = ResultsWindow(self.sentence_to_pass, self)
        dialog.exec()


# --- Proqramı Başladan Hissə ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())