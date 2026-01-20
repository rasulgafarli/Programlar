# Riyazi Məsələlərin Həlli Programı - v1.5 (20.01.2023)

import sys
from sympy import symbols, Symbol, Eq, solve, S, diff, integrate, limit, simplify, factor, expand, pretty, N, pi, E
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QSpinBox, QMessageBox, QGridLayout
)

# --------- Simvolik parsinq üçün quruluş (FUNKSİYALARA DƏYMƏDİK) ----------
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
SAFE = {'pi': pi, 'e': E, 'x': symbols('x'), 'y': symbols('y'), 'z': symbols('z'), 't': symbols('t')}

def parse_safe(expr_text: str):
    return parse_expr(expr_text, transformations=TRANSFORMS, local_dict=SAFE)

def as_symbol(name: str) -> Symbol:
    name = (name or 'x').strip()
    if ',' in name:
        raise ValueError("Bir dəyişən adı gözlənilirdi (məs: x).")
    if name not in SAFE:
        SAFE[name] = symbols(name)
    return SAFE[name]

def show_error(parent: QWidget, msg: str):
    QMessageBox.critical(parent, "Xəta", msg)
# ---------------------------------------------------------------------------


# ------------------------------- TABS (Eyni funksiya, UI dəyişib) ---------
class EvaluateTab(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        self.input = QTextEdit()
        self.input.setPlaceholderText("Məsələn: (2+3)^2/5 + sin(pi/2)")
        self.btn = QPushButton("Hesabla")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        v.addWidget(QLabel("İfadə"))
        v.addWidget(self.input)
        v.addWidget(self.btn)
        v.addWidget(QLabel("Nəticə"))
        v.addWidget(self.out)

        self.btn.clicked.connect(self.compute)

    def compute(self):
        txt = self.input.toPlainText().strip()
        if not txt:
            show_error(self, "İfadə boşdur.")
            return
        try:
            expr = parse_safe(txt)
            simp = simplify(expr)
            self.out.setPlainText(f"{pretty(simp)}\n\n≈ {N(simp)}")
        except Exception as e:
            show_error(self, str(e))


class SolveTab(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        self.expr = QLineEdit()
        self.expr.setPlaceholderText("Məs: x^2 - 5*x + 6 = 0  və ya  x^2 - 5*x + 6")
        self.var = QLineEdit("x")
        self.btn = QPushButton("Həll et")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        grid.addWidget(QLabel("Tənlik və ya ifadə"), 0, 0, 1, 2)
        grid.addWidget(self.expr, 1, 0, 1, 2)
        grid.addWidget(QLabel("Dəyişən"), 2, 0)
        grid.addWidget(self.var, 2, 1)
        grid.addWidget(self.btn, 3, 0, 1, 2)
        grid.addWidget(QLabel("Nəticə"), 4, 0, 1, 2)
        grid.addWidget(self.out, 5, 0, 1, 2)

        self.btn.clicked.connect(self.compute)

    def compute(self):
        text = self.expr.text().strip()
        var = as_symbol(self.var.text())
        if not text:
            show_error(self, "İfadə boşdur.")
            return
        try:
            if '=' in text:
                L, R = [s.strip() for s in text.split('=', 1)]
                eq = Eq(parse_safe(L), parse_safe(R))
                sol = solve(eq, var, dict=True)
            else:
                sol = solve(parse_safe(text), var, dict=True)
            self.out.setPlainText(pretty(sol) if sol else "Həll tapılmadı.")
        except Exception as e:
            show_error(self, str(e))


class SystemTab(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        self.eq = QTextEdit()
        self.eq.setPlaceholderText("Hər sətrə bir tənlik yazın:\n\nx + y = 3\nx - y = 1")
        h = QHBoxLayout()
        self.vars = QLineEdit("x,y")
        self.btn = QPushButton("Sistemi həll et")
        h.addWidget(QLabel("Dəyişənlər (vergüllə)"))
        h.addWidget(self.vars)
        h.addWidget(self.btn)
        self.out = QTextEdit(); self.out.setReadOnly(True)

        v.addWidget(QLabel("Tənliklər"))
        v.addWidget(self.eq)
        v.addLayout(h)
        v.addWidget(QLabel("Nəticə"))
        v.addWidget(self.out)

        self.btn.clicked.connect(self.compute)

    def compute(self):
        raw = [ln.strip() for ln in self.eq.toPlainText().splitlines() if ln.strip()]
        if not raw:
            show_error(self, "Tənlik yazılmayıb.")
            return
        try:
            varlist = []
            for n in [s.strip() for s in self.vars.text().split(',') if s.strip()]:
                varlist.append(as_symbol(n))
            if not varlist:
                show_error(self, "Dəyişənləri x,y şəklində yazın.")
                return

            eqs = []
            for line in raw:
                if '=' in line:
                    L, R = [s.strip() for s in line.split('=', 1)]
                    eqs.append(Eq(parse_safe(L), parse_safe(R)))
                else:
                    eqs.append(Eq(parse_safe(line), S.Zero))
            sol = solve(eqs, varlist, dict=True)
            self.out.setPlainText(pretty(sol) if sol else "Həll tapılmadı.")
        except Exception as e:
            show_error(self, str(e))


class DerivativeTab(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        self.expr = QLineEdit()
        self.expr.setPlaceholderText("Məs: sin(x)*exp(x)")
        self.var = QLineEdit("x")
        self.order = QSpinBox(); self.order.setRange(1, 10); self.order.setValue(1)
        self.btn = QPushButton("Törəmə al")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        grid.addWidget(QLabel("İfadə"), 0, 0, 1, 3)
        grid.addWidget(self.expr, 1, 0, 1, 3)
        grid.addWidget(QLabel("Dəyişən"), 2, 0)
        grid.addWidget(self.var, 2, 1)
        grid.addWidget(QLabel("Sıra"), 2, 2)
        grid.addWidget(self.order, 2, 3)
        grid.addWidget(self.btn, 3, 0, 1, 4)
        grid.addWidget(QLabel("Nəticə"), 4, 0, 1, 4)
        grid.addWidget(self.out, 5, 0, 1, 4)

        self.btn.clicked.connect(self.compute)

    def compute(self):
        if not self.expr.text().strip():
            show_error(self, "İfadə boşdur.")
            return
        try:
            var = as_symbol(self.var.text())
            res = diff(parse_safe(self.expr.text()), var, int(self.order.value()))
            self.out.setPlainText(pretty(res))
        except Exception as e:
            show_error(self, str(e))


class IntegralTab(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        self.expr = QLineEdit(); self.expr.setPlaceholderText("Məs: x^2")
        self.var = QLineEdit("x")
        self.bounds = QLineEdit(); self.bounds.setPlaceholderText("Sərhədlər: a,b (boş: qeyri-müəyyən)")
        self.btn = QPushButton("İntegral al")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        grid.addWidget(QLabel("İfadə"), 0, 0, 1, 3)
        grid.addWidget(self.expr, 1, 0, 1, 3)
        grid.addWidget(QLabel("Dəyişən"), 2, 0)
        grid.addWidget(self.var, 2, 1)
        grid.addWidget(self.bounds, 2, 2)
        grid.addWidget(self.btn, 3, 0, 1, 3)
        grid.addWidget(QLabel("Nəticə"), 4, 0, 1, 3)
        grid.addWidget(self.out, 5, 0, 1, 3)

        self.btn.clicked.connect(self.compute)

    def compute(self):
        t = self.expr.text().strip()
        if not t:
            show_error(self, "İfadə boşdur.")
            return
        try:
            var = as_symbol(self.var.text())
            btxt = self.bounds.text().strip()
            expr = parse_safe(t)
            if btxt:
                parts = [p.strip() for p in btxt.split(',')]
                if len(parts) != 2:
                    raise ValueError("Sərhədləri a,b şəklində yazın.")
                a = parse_safe(parts[0]); b = parse_safe(parts[1])
                res = integrate(expr, (var, a, b))
            else:
                res = integrate(expr, var)
            self.out.setPlainText(pretty(res))
        except Exception as e:
            show_error(self, str(e))


class LimitTab(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        self.expr = QLineEdit(); self.expr.setPlaceholderText("Məs: sin(x)/x")
        self.var = QLineEdit("x")
        self.point = QLineEdit(); self.point.setPlaceholderText("Nöqtə: 0 və ya x->0")
        self.btn = QPushButton("Limit al")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        grid.addWidget(QLabel("İfadə"), 0, 0, 1, 3)
        grid.addWidget(self.expr, 1, 0, 1, 3)
        grid.addWidget(QLabel("Dəyişən"), 2, 0)
        grid.addWidget(self.var, 2, 1)
        grid.addWidget(self.point, 2, 2)
        grid.addWidget(self.btn, 3, 0, 1, 3)
        grid.addWidget(QLabel("Nəticə"), 4, 0, 1, 3)
        grid.addWidget(self.out, 5, 0, 1, 3)

        self.btn.clicked.connect(self.compute)

    def compute(self):
        if not self.expr.text().strip():
            show_error(self, "İfadə boşdur.")
            return
        if not self.point.text().strip():
            show_error(self, "Limit nöqtəsini yazın.")
            return
        try:
            var = as_symbol(self.var.text())
            ptxt = self.point.text().strip()
            if '->' in ptxt:
                _, right = [s.strip() for s in ptxt.split('->', 1)]
                p = parse_safe(right)
            else:
                p = parse_safe(ptxt)
            res = limit(parse_safe(self.expr.text()), var, p)
            self.out.setPlainText(pretty(res))
        except Exception as e:
            show_error(self, str(e))


class AlgebraTab(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        self.expr = QLineEdit(); self.expr.setPlaceholderText("Məs: (x^2 - 1)/(x - 1)")
        self.btn_simplify = QPushButton("Sadələşdir")
        self.btn_factor = QPushButton("Çarpanlara ayır")
        self.btn_expand = QPushButton("Açıq forma")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        grid.addWidget(QLabel("İfadə"), 0, 0, 1, 3)
        grid.addWidget(self.expr, 1, 0, 1, 3)
        grid.addWidget(self.btn_simplify, 2, 0)
        grid.addWidget(self.btn_factor, 2, 1)
        grid.addWidget(self.btn_expand, 2, 2)
        grid.addWidget(QLabel("Nəticə"), 3, 0, 1, 3)
        grid.addWidget(self.out, 4, 0, 1, 3)

        self.btn_simplify.clicked.connect(self.do_simplify)
        self.btn_factor.clicked.connect(self.do_factor)
        self.btn_expand.clicked.connect(self.do_expand)

    def _compute(self, func):
        txt = self.expr.text().strip()
        if not txt:
            show_error(self, "İfadə boşdur.")
            return
        try:
            res = func(parse_safe(txt))
            self.out.setPlainText(pretty(res))
        except Exception as e:
            show_error(self, str(e))

    def do_simplify(self):
        self._compute(simplify)

    def do_factor(self):
        self._compute(factor)

    def do_expand(self):
        self._compute(expand)
# ---------------------------------------------------------------------------


# ------------------------------ ƏSAS PƏNCƏRƏ --------------------------------
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Riyaziyyat Həll Edici — PyQt6 + SymPy")
        self.resize(960, 680)

        tabs = QTabWidget()
        tabs.addTab(EvaluateTab(), "Hesablayıcı")
        tabs.addTab(SolveTab(), "Tənlik Həlli")
        tabs.addTab(SystemTab(), "Sistem Həlli")
        tabs.addTab(DerivativeTab(), "Törəmə")
        tabs.addTab(IntegralTab(), "İntegral")
        tabs.addTab(LimitTab(), "Limit")
        tabs.addTab(AlgebraTab(), "Alqebra")

        self.setCentralWidget(tabs)
        self.apply_styles()   # --- Arxa fon, oval xanalar, rəngli düymələr ---

    def apply_styles(self):
        # Arxa fon (gradient), oval girişlər və rəngli düymələr
        self.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364);
        }
        QTabWidget::pane {
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 18px;
            background: rgba(255,255,255,0.06);
            padding: 6px;
        }
        QTabBar::tab {
            color: #e8f0f4;
            background: rgba(255,255,255,0.10);
            padding: 8px 14px;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
            margin: 2px;
        }
        QTabBar::tab:selected {
            background: rgba(255,255,255,0.25);
            color: white;
        }
        QLabel {
            color: #e3eef5;
            font-weight: 600;
            margin: 4px 2px;
        }
        QLineEdit, QTextEdit, QSpinBox {
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(0,0,0,0.15);
            border-radius: 16px;            /* OVAL XANALAR */
            padding: 8px 10px;
            color: #0f1a20;
            selection-background-color: #004e92;
            selection-color: white;
        }
        QTextEdit {
            padding: 10px 12px;
        }
        QPushButton {
            border: none;
            border-radius: 18px;            /* OVAL DÜYMƏLƏR */
            padding: 10px 16px;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #4facfe, stop:1 #00f2fe);
            font-weight: 600;
        }
        QPushButton:hover {
            filter: brightness(110%);
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #5fb6ff, stop:1 #22f6ff);
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #2e9bff, stop:1 #00d6e4);
        }
        QScrollBar:vertical, QScrollBar:horizontal {
            background: transparent;
        }
        """)


def main():
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
