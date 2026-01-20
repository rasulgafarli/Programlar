# --- Söz və Hərf Sayğacı Proqramı (Canlı Bənövşəyi Dizayn ilə) ---

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QDialog, QGraphicsDropShadowEffect)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt


# ==============================================================================
# NƏTİCƏ PƏNCƏRƏSİ (Dizaynı yenilənmiş)
# ==============================================================================
class ResultsWindow(QDialog):
    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hesablama Nəticəsi")
        self.setFixedSize(350, 250)

        # DƏYİŞİKLİK: Yeni, canlı bənövşəyi rəng palitrası
        self.setStyleSheet("""
            QDialog {
                background-color: #F2F2FE; /* Çox açıq, sakit bənövşəyi fon */
            }
            QLabel#resultLabel {
                color: #341F4E; /* Mətn üçün tünd bənövşəyi */
                background-color: #E8E6F8; /* Açıq bənövşəyi fon */
                border: 2px solid #8E44AD; /* Canlı bənövşəyi çərçivə */
                border-radius: 12px;
                padding: 15px;
            }
            QPushButton {
                font: bold 12px;
                color: white;
                background-color: #9B59B6; /* Açıq bənövşəyi düymə */
                padding: 8px 15px;
                border-radius: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #8E44AD; /* Hover üçün bir az tünd */
            }
            QPushButton:pressed {
                background-color: #5B2C6F; /* Basıldıqda daha tünd */
            }
        """)

        # --- Hesablama Məntiqi (Dəyişməz qalıb) ---
        words = sentence_to_analyze.strip().split()
        word_count = len(words)
        letter_count = sum(c.isalpha() for c in sentence_to_analyze)
        char_count_no_spaces = len(sentence_to_analyze.replace(' ', ''))

        # --- Nəticələrin Göstərilməsi ---
        self.result_label = QLabel(
            f"Söz sayı: {word_count}\n"
            f"Hərf sayı: {letter_count}\n"
            f"Simvol sayı (boşluqsuz): {char_count_no_spaces}"
        )
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setObjectName("resultLabel")

        # --- "Bağla" Düyməsi ---
        self.close_button = QPushButton("Bağla")
        self.close_button.clicked.connect(self.close)

        # --- Pəncərənin Quruluşu (Layout) ---
        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(self.close_button)
        self.setLayout(layout)


# ==============================================================================
# ƏSAS PƏNCƏRƏ (Dizaynı yenilənmiş)
# ==============================================================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cümlə Təhlili")
        self.setGeometry(200, 200, 200, 200)
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
        self.close_button = QPushButton("Bağla")
        self.close_button.setObjectName("closeButton")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.error_label)

        shadow1 = QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 80))
        self.calculate_button.setGraphicsEffect(shadow1)
        shadow2 = QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 80))
        self.results_button.setGraphicsEffect(shadow2)
        shadow3 = QGraphicsDropShadowEffect(blurRadius=15, xOffset=2, yOffset=2, color=QColor(0, 0, 0, 80))
        self.close_button.setGraphicsEffect(shadow3)

        main_layout.addWidget(self.calculate_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.results_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        self.calculate_button.clicked.connect(self.validate_and_proceed)
        self.results_button.clicked.connect(self.open_results_window)
        self.close_button.clicked.connect(self.close)

        # DƏYİŞİKLİK: Yeni, canlı bənövşəyi rəng palitrası
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { 
                background-color: #F2F2FE; /* Əsas fon çox açıq bənövşəyi */
                color: #4A235A; /* Mətn üçün standart tünd bənövşəyi */
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #D2B4DE;
                padding: 10px 15px; font-size: 16px;
                border-radius: 22px; min-height: 24px;
            }
            QLineEdit:focus {
                border: 2px solid #8E44AD; /* Fokusda ana bənövşəyi rəng */
            }
            QLineEdit[hasError="true"] { border: 2px solid #E74C3C; }

            QPushButton {
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 15px; 
                border-radius: 16px;
                border: none;
            }
            /* Əsas düymə ("Hesabla") */
            QPushButton#hesablaButton, QPushButton {
                background-color: #9B59B6; /* Canlı, açıq bənövşəyi */
            }
            QPushButton#hesablaButton:hover, QPushButton:hover {
                background-color: #8E44AD; /* Hover üçün ana rəng */
            }

            /* Nəticə düyməsi */
            QPushButton#resultsButton {
                background-color: #3498DB; /* Fərqlənməsi üçün mavi */
            }
            QPushButton#resultsButton:hover {
                background-color: #2980B9;
            }

            /* Bağla düyməsi */
            QPushButton#closeButton {
                background-color: #B2BABB; /* Neytral boz */
            }
            QPushButton#closeButton:hover {
                background-color: #99A3A4;
            }

            QPushButton:pressed { background-color: #5B2C6F; }
            QLabel#errorLabel { color: #E74C3C; padding-left: 10px; }
        """)
        self.calculate_button.setObjectName("hesablaButton")

    def is_valid_sentence(self, text):
        if not text: return True
        allowed_chars = "abcdefghijklmnopqrstuvwxyzəöüıçşğABCDEFGHIJKLMNOPQRSTUVWXYZƏÖÜIÇŞĞ0123456789 .,:-"
        forbidden_start_chars = {'.', ',', ':', '-'}
        trimmed_text = text.lstrip()
        if trimmed_text and trimmed_text[0] in forbidden_start_chars: return False
        for char in text:
            if char not in allowed_chars: return False
        return True

    def validate_and_proceed(self):
        text = self.input_box.text()
        if self.is_valid_sentence(text) and text.strip():
            self.sentence_to_pass = text
            self.error_label.hide()
            self.results_button.show()
            self.input_box.setProperty("hasError", False)
        else:
            self.results_button.hide()
            if text.strip():
                self.error_label.show()
                self.input_box.setProperty("hasError", True)
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