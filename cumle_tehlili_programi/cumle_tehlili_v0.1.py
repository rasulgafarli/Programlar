# --- Söz və Hərf Sayğacı Proqramı ---

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QDialog, QFontDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# ==============================================================================
# BU, YENİ AÇILACAQ NƏTİCƏ PƏNCƏRƏSİ ÜÇÜN SİNİFDİR (CLASS)
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

        # --- Hesablama məntiqi ---
        # Boşluqları nəzərə alaraq sözlərin sayını tapırıq
        words = sentence_to_analyze.strip().split()
        word_count = len(words)

        # Boşluqlar da daxil olmaqla bütün simvolların sayını tapırıq
        char_count = len(sentence_to_analyze)

        # --- Nəticələrin göstərilməsi ---
        self.result_label = QLabel(f"Söz sayı: {word_count}\nSimvol sayı: {char_count}")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        self.setLayout(layout)


# ==============================================================================
# BU, ƏSAS PROQRAM PƏNCƏRƏSİ ÜÇÜN SİNİFDİR
# ==============================================================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Söz Təhlili")
        self.setGeometry(300, 300, 500, 200)

        # Məlumatın saxlanacağı dəyişən
        self.sentence_to_pass = ""

        # --- Elementlərin yaradılması ---
        self.info_label = QLabel("Təhlil etmək üçün aşağıdakı xanaya bir cümlə yazın:")
        self.info_label.setFont(QFont("Arial", 12))

        self.input_box = QLineEdit()
        self.input_box.setFont(QFont("Arial", 14))

        self.calculate_button = QPushButton("Hesabla")
        self.calculate_button.setFont(QFont("Arial", 12))

        # Bu düymə başlanğıcda GİZLİ olacaq
        self.results_button = QPushButton("Söz/hərf sayı")
        self.results_button.setFont(QFont("Arial", 12))
        self.results_button.hide()  # <-- Başlanğıcda düyməni gizlədirik

        # --- Layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.calculate_button)
        main_layout.addWidget(self.results_button)
        self.setLayout(main_layout)

        # --- Siqnalların (hadisələrin) bağlanması ---
        self.calculate_button.clicked.connect(self.show_results_button)
        self.results_button.clicked.connect(self.open_results_window)

    def show_results_button(self):
        """
        'Hesabla' düyməsinə basıldıqda bu funksiya işə düşür.
        """
        text = self.input_box.text()
        if text.strip():  # Əgər xana boş deyilsə
            # Cümləni daha sonra istifadə etmək üçün yadda saxlayırıq
            self.sentence_to_pass = text
            # Nəticə düyməsini görünən edirik
            self.results_button.show()
        else:
            # Əgər xana boşdursa, nəticə düyməsini gizlədirik
            self.results_button.hide()

    def open_results_window(self):
        """
        'Söz/hərf sayı' düyməsinə basıldıqda bu funksiya işə düşür.
        """
        # Nəticə pəncərəsinin bir nüsxəsini yaradırıq və cümləni ona ötürürük
        dialog = ResultsWindow(self.sentence_to_pass, self)
        dialog.exec()  # Dialoq pəncərəsini açır və istifadəçi bağlayana qədər gözləyir


# --- Proqramı Başladan Hissə ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())