# --- Söz və Hərf Sayğacı Proqramı (Son Dəyişikliklərlə Tam Versiya) ---

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# ==============================================================================
# NƏTİCƏ PƏNCƏRƏSİ ÜÇÜN SİNİF
# ==============================================================================
class ResultsWindow(QDialog):
    """
    Bu sinif, söz və hərf sayının göstəriləcəyi yeni, kiçik pəncərəni
    (dialoqu) təmsil edir.
    """

    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hesablama Nəticəsi")
        self.setFixedSize(300, 150)

        # Nəticə pəncərəsinin də arxa fon rəngini əsas pəncərə ilə eyni edirik
        self.setStyleSheet("background-color: #F0F3F4;")

        # Hesablama məntiqi
        words = sentence_to_analyze.strip().split()
        word_count = len(words)

        char_count = len(sentence_to_analyze)

        # Nəticələrin göstərilməsi
        self.result_label = QLabel(f"Söz sayı: {word_count}\nSimvol sayı: {char_count}")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        self.setLayout(layout)


# ==============================================================================
# ƏSAS PROQRAM PƏNCƏRƏSİ ÜÇÜN SİNİF
# ==============================================================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Söz Təhlili")
        self.setGeometry(300, 300, 500, 220)

        self.sentence_to_pass = ""

        # --- Elementlərin yaradılması ---
        self.info_label = QLabel("Təhlil etmək üçün aşağıdakı xanaya bir cümlə yazın:")
        self.info_label.setFont(QFont("Arial", 12))

        self.input_box = QLineEdit()

        self.calculate_button = QPushButton("Hesabla")

        self.results_button = QPushButton("Söz/hərf sayı")
        # Düyməyə QSS-də müraciət etmək üçün unikal ad veririk
        self.results_button.setObjectName("resultsButton")
        self.results_button.hide()

        # --- Layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.calculate_button)
        main_layout.addWidget(self.results_button)
        self.setLayout(main_layout)

        # --- Siqnalların bağlanması ---
        self.calculate_button.clicked.connect(self.show_results_button)
        self.results_button.clicked.connect(self.open_results_window)

        # Bütün stilləri tətbiq edirik
        self.apply_styles()

    def apply_styles(self):
        """Proqramın bütün vizual stilini təyin edən QSS kodu."""
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F3F4;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                padding: 8px;
                font-size: 14px;
                border-radius: 18px;
            }

            /* BÜTÜN düymələr üçün ümumi stil (göy rəng) */
            QPushButton {
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 18px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #3498DB, stop:1 #2980B9);
            }

            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #5DADE2, stop:1 #3498DB);
            }

            QPushButton:pressed {
                background-color: #2980B9;
            }

            /* Yalnız adı "resultsButton" olan düymə üçün xüsusi stil (yaşıl rəng) */
            QPushButton#resultsButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #2ECC71, stop:1 #27AE60);
            }

            QPushButton#resultsButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #58D68D, stop:1 #2ECC71);
            }

            QPushButton#resultsButton:pressed {
                background-color: #27AE60;
            }
        """)

    def show_results_button(self):
        text = self.input_box.text()
        if text.strip():
            self.sentence_to_pass = text
            self.results_button.show()
        else:
            self.results_button.hide()

    def open_results_window(self):
        dialog = ResultsWindow(self.sentence_to_pass, self)
        dialog.exec()


# --- Proqramı Başladan Hissə ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())