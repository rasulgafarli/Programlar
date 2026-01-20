# --- Söz və Hərf Sayğacı Proqramı (Kursor Fokusu ilə) ---

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QGridLayout,
                             QGraphicsDropShadowEffect, QStyle)
from PyQt6.QtGui import QFont, QColor, QFontMetrics, QIcon
from PyQt6.QtCore import Qt, QTimer


# ==============================================================================
# NƏTİCƏ PƏNCƏRƏLƏRİ (Dəyişiklik yoxdur)
# ==============================================================================
class ThickThinVowelResultsWindow(QDialog):
    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Qalın və İncə Saitlərin Sayı")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog { background-color: #FEF9E7; }
            QLabel {
                color: #AF601A; background-color: #FDEBD0;
                border: 3px solid #F39C12; border-radius: 12px; padding: 15px;
            }
            QPushButton {
                font: bold 12px; color: white; padding: 8px 15px;
                border-radius: 16px; border: none; background-color: #E74C3C;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        thick_vowels = "aıou"
        thin_vowels = "eəiöü"
        thick_count, thin_count = 0, 0
        for char in sentence_to_analyze:
            if char.isalpha():
                if char.lower() in thick_vowels:
                    thick_count += 1
                elif char.lower() in thin_vowels:
                    thin_count += 1
        self.result_label = QLabel(f"Qalın sait sayı: {thick_count}\nİncə sait sayı: {thin_count}")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shadow = QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 80))
        self.result_label.setGraphicsEffect(shadow)
        self.close_button = QPushButton("Bağla")
        self.close_button.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(self.close_button)


class OpenClosedVowelResultsWindow(QDialog):
    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Açıq və Qapalı Saitlərin Sayı")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog { background-color: #E8F8F5; }
            QLabel {
                color: #0E6655; background-color: #D1F2EB;
                border: 3px solid #16A085; border-radius: 12px; padding: 15px;
            }
            QPushButton {
                font: bold 12px; color: white; padding: 8px 15px;
                border-radius: 16px; border: none; background-color: #E74C3C;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        open_vowels = "aeəoö"
        closed_vowels = "ıiuü"
        open_count, closed_count = 0, 0
        for char in sentence_to_analyze:
            if char.isalpha():
                if char.lower() in open_vowels:
                    open_count += 1
                elif char.lower() in closed_vowels:
                    closed_count += 1
        self.result_label = QLabel(f"Açıq sait sayı: {open_count}\nQapalı sait sayı: {closed_count}")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shadow = QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 80))
        self.result_label.setGraphicsEffect(shadow)
        self.close_button = QPushButton("Bağla")
        self.close_button.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(self.close_button)


class VowelConsonantResultsWindow(QDialog):
    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sait və Samit Sayı")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog { background-color: #F2F2FE; }
            QLabel#vowelConsonantLabel {
                color: #154360; background-color: #D6EAF8;
                border: 3px solid #3498DB; border-radius: 12px; padding: 15px;
            }
            QPushButton { font: bold 12px; color: white; padding: 8px 15px; border-radius: 16px; border: none; }
            QPushButton#closeButton { background-color: #E74C3C; }
            QPushButton#closeButton:hover { background-color: #C0392B; }
        """)
        vowels_az = "aıoueəiöü"
        vowel_count, consonant_count = 0, 0
        for char in sentence_to_analyze:
            if char.isalpha():
                if char.lower() in vowels_az:
                    vowel_count += 1
                else:
                    consonant_count += 1
        self.result_label = QLabel(f"Sait sayı: {vowel_count}\nSamit sayı: {consonant_count}")
        self.result_label.setObjectName("vowelConsonantLabel")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shadow = QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 80))
        self.result_label.setGraphicsEffect(shadow)
        self.close_button = QPushButton("Bağla")
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(self.close_button)


class ResultsWindow(QDialog):
    def __init__(self, sentence_to_analyze, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hesablama Nəticəsi")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog { background-color: #E9F7EF; }
            QLabel#resultLabel {
                color: #145A32; background-color: #D4EFDF;
                border: 3px solid #27AE60; border-radius: 12px; padding: 15px;
            }
            QPushButton { font: bold 12px; color: white; padding: 8px 15px; border-radius: 16px; border: none; }
            QPushButton#closeButton { background-color: #E74C3C; }
            QPushButton#closeButton:hover { background-color: #C0392B; }
        """)
        words = sentence_to_analyze.strip().split()
        word_count = len(words)
        letter_count = sum(c.isalpha() for c in sentence_to_analyze)
        char_count_no_spaces = len(sentence_to_analyze.replace(' ', '').replace('\n', ''))
        self.result_label = QLabel(
            f"Söz sayı: {word_count}\nHərf sayı: {letter_count}\nSimvol sayı (boşluqsuz): {char_count_no_spaces}")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setObjectName("resultLabel")
        shadow = QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 80))
        self.result_label.setGraphicsEffect(shadow)
        self.close_button = QPushButton("Bağla")
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addWidget(self.close_button)


# ==============================================================================
# ƏSAS PƏNCƏRƏ
# ==============================================================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cümlə Təhlili")
        self.sentence_to_pass = ""

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Təhlil etmək üçün mətninizi bura yazın...")
        self.input_box.setMinimumWidth(400)

        self.clear_button = QPushButton()
        self.clear_button.setObjectName("clearButton")
        close_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton)
        self.clear_button.setIcon(close_icon)

        self.text_edit_container = QWidget()
        self.text_edit_container.setObjectName("textEditContainer")
        container_shadow = QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=2, color=QColor(0, 0, 0, 60))
        self.text_edit_container.setGraphicsEffect(container_shadow)

        grid_layout = QGridLayout(self.text_edit_container)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)
        grid_layout.addWidget(self.input_box, 0, 0)
        grid_layout.addWidget(self.clear_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        font_metrics = QFontMetrics(self.input_box.font())
        line_height = font_metrics.height()
        self.min_height = line_height * 3 + 15
        self.max_height = line_height * 8 + 15
        self.input_box.setMinimumHeight(self.min_height)

        self.input_box.textChanged.connect(self.on_text_changed)
        self.clear_button.clicked.connect(self.reset_ui_to_initial_state)

        self.error_label = QLabel("İcazə verilməyən simvol daxil edildi!")
        self.error_label.setObjectName("errorLabel")
        self.error_label.hide()
        self.calculate_button = QPushButton("Hesabla")
        self.close_button = QPushButton("Bağla")
        self.close_button.setObjectName("closeButton")

        self.vowel_consonant_button = QPushButton("Sait/Samit")
        self.results_button = QPushButton("Söz/hərf sayı")
        self.thick_thin_button = QPushButton("Qalın/İncə")
        self.open_closed_button = QPushButton("Açıq/Qapalı")

        self.result_buttons = [
            self.vowel_consonant_button, self.results_button,
            self.thick_thin_button, self.open_closed_button
        ]
        for button in self.result_buttons:
            button.hide()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.text_edit_container)
        main_layout.addWidget(self.error_label)

        button_layout_row1 = QHBoxLayout()
        button_layout_row1.addWidget(self.result_buttons[0])
        button_layout_row1.addWidget(self.result_buttons[1])

        button_layout_row2 = QHBoxLayout()
        button_layout_row2.addWidget(self.result_buttons[2])
        button_layout_row2.addWidget(self.result_buttons[3])

        self.shadow_effects = [
            QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=4, color=QColor(0, 0, 0, 100)) for _ in
            range(6)]
        self.calculate_button.setGraphicsEffect(self.shadow_effects[0])
        self.results_button.setGraphicsEffect(self.shadow_effects[1])
        self.close_button.setGraphicsEffect(self.shadow_effects[2])
        self.vowel_consonant_button.setGraphicsEffect(self.shadow_effects[3])
        self.thick_thin_button.setGraphicsEffect(self.shadow_effects[4])
        self.open_closed_button.setGraphicsEffect(self.shadow_effects[5])

        main_layout.addWidget(self.calculate_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(button_layout_row1)
        main_layout.addLayout(button_layout_row2)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.calculate_button.clicked.connect(self.validate_and_proceed)
        self.close_button.clicked.connect(self.close)
        self.results_button.clicked.connect(self.open_results_window)
        self.vowel_consonant_button.clicked.connect(self.open_vowel_consonant_window)
        self.thick_thin_button.clicked.connect(self.open_thick_thin_window)
        self.open_closed_button.clicked.connect(self.open_open_closed_window)

        self.apply_styles()
        self.on_text_changed()

    def reset_ui_to_initial_state(self):
        self.input_box.clear()
        for button in self.result_buttons:
            button.hide()
        self.error_label.hide()
        self.text_edit_container.setProperty("hasError", False)
        self.text_edit_container.style().polish(self.text_edit_container)
        self.adjustSize()
        # YENİ: Kursoru mətn qutusuna qaytarırıq
        self.input_box.setFocus()

    def open_thick_thin_window(self):
        dialog = ThickThinVowelResultsWindow(self.sentence_to_pass, self)
        dialog.exec()

    def open_open_closed_window(self):
        dialog = OpenClosedVowelResultsWindow(self.sentence_to_pass, self)
        dialog.exec()

    def on_text_changed(self):
        self.clear_button.setVisible(bool(self.input_box.toPlainText()))
        doc_height = self.input_box.document().size().toSize().height()
        frame_height = self.input_box.frameWidth() * 2
        final_doc_height = doc_height + frame_height + 5
        new_height = max(self.min_height, min(final_doc_height, self.max_height))
        self.input_box.setFixedHeight(new_height)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F2F2FE; color: #4A235A; }
            QWidget#textEditContainer {
                background-color: white; border: 2px solid #D2B4DE; border-radius: 18px;
            }
            QWidget#textEditContainer[hasError="true"] { border: 2px solid #E74C3C; }
            QTextEdit {
                background-color: transparent; border: none; padding: 8px 35px 8px 10px; font-size: 16px;
            }
            QPushButton#clearButton {
                min-width: 24px; max-width: 24px; min-height: 24px; max-height: 24px;
                background-color: transparent; border-radius: 12px; border: none;
                margin-top: 8px; margin-right: 8px;
            }
            QPushButton#clearButton:hover { background-color: #EAECEE; }
            QPushButton {
                color: white; font-size: 13px; font-weight: bold;
                padding: 8px 15px; border-radius: 16px; border: none; min-width: 120px;
            }
            QPushButton#hesablaButton { background-color: #9B59B6; }
            QPushButton#hesablaButton:hover { background-color: #8E44AD; }
            QPushButton#vowelButton { background-color: #3498DB; }
            QPushButton#vowelButton:hover { background-color: #2980B9; }
            QPushButton#resultsButton { background-color: #2ECC71; }
            QPushButton#resultsButton:hover { background-color: #27AE60; }
            QPushButton#thickThinButton { background-color: #F39C12; }
            QPushButton#thickThinButton:hover { background-color: #D68910; }
            QPushButton#openClosedButton { background-color: #1ABC9C; }
            QPushButton#openClosedButton:hover { background-color: #16A085; }
            QPushButton#closeButton { background-color: #E74C3C; }
            QPushButton#closeButton:hover { background-color: #C0392B; }
            QPushButton:pressed { background-color: #5B2C6F; }
            QLabel#errorLabel { color: #E74C3C; padding-left: 10px; }
        """)
        self.vowel_consonant_button.setObjectName("vowelButton")
        self.results_button.setObjectName("resultsButton")
        self.calculate_button.setObjectName("hesablaButton")
        self.thick_thin_button.setObjectName("thickThinButton")
        self.open_closed_button.setObjectName("openClosedButton")

    def open_vowel_consonant_window(self):
        dialog = VowelConsonantResultsWindow(self.sentence_to_pass, self)
        dialog.exec()

    def open_results_window(self):
        dialog = ResultsWindow(self.sentence_to_pass, self)
        dialog.exec()

    def is_valid_sentence(self, text):
        if not text: return True
        allowed_chars = "abcdefghijklmnopqrstuvwxyzəöüıçşğABCDEFGHIJKLMNOPQRSTUVWXYZƏÖÜIÇŞĞ0123456789 .,:-\n"
        forbidden_start_chars = {'.', ',', ':', '-'}
        trimmed_text = text.lstrip()
        if trimmed_text and trimmed_text[0] in forbidden_start_chars: return False
        for char in text:
            if char not in allowed_chars: return False
        return True

    def show_buttons_sequentially(self, index=0):
        if index >= len(self.result_buttons):
            return
        button_to_show = self.result_buttons[index]
        button_to_show.show()
        self.adjustSize()
        QTimer.singleShot(100, lambda: self.show_buttons_sequentially(index + 1))

    def validate_and_proceed(self):
        text = self.input_box.toPlainText()
        self.on_text_changed()

        for button in self.result_buttons:
            button.hide()

        if not text.strip():
            self.sentence_to_pass = ""
            self.error_label.setText("Xahiş edirik, təhlil etmək üçün bir cümlə daxil edin!")
            self.error_label.show()
            self.text_edit_container.setProperty("hasError", True)

        elif not self.is_valid_sentence(text):
            self.sentence_to_pass = ""
            self.error_label.setText("İcazə verilməyən simvol daxil edildi!")
            self.error_label.show()
            self.text_edit_container.setProperty("hasError", True)

        else:
            self.sentence_to_pass = text
            self.error_label.hide()
            self.text_edit_container.setProperty("hasError", False)
            self.show_buttons_sequentially()

        self.text_edit_container.style().polish(self.text_edit_container)
        self.adjustSize()
        # YENİ: Kursoru hər zaman mətn qutusuna qaytarırıq
        self.input_box.setFocus()


# --- Proqramı Başladan Hissə ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())