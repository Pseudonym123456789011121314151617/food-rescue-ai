"""Dark Futuristic theme — Iron Man JARVIS meets Windows 12."""

DARK_FUTURISTIC_PALETTE: dict[str, str] = {
    "window": "#0a0e17",
    "window_text": "#e0e6f0",
    "base": "#0f1420",
    "alternate_base": "#141a2a",
    "text": "#e0e6f0",
    "button": "#1a2235",
    "button_text": "#e0e6f0",
    "highlight": "#00d4ff",
    "highlight_text": "#0a0e17",
    "tooltip_base": "#1a2235",
    "tooltip_text": "#e0e6f0",
}

DARK_FUTURISTIC_QSS = """
/* ===== JARVIS AI — Dark Futuristic Theme ===== */

* {
    font-family: 'Segoe UI', 'SF Pro Display', 'Inter', sans-serif;
}

QMainWindow {
    background-color: #0a0e17;
}

QWidget {
    background-color: transparent;
    color: #e0e6f0;
}

/* --- Glass Panels --- */
QFrame#glassPanel {
    background-color: rgba(15, 20, 32, 200);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px;
}

/* --- Sidebar --- */
QFrame#sidebar {
    background-color: rgba(10, 14, 23, 230);
    border-right: 1px solid rgba(0, 212, 255, 0.1);
}

QFrame#sidebar QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 12px;
    color: #8892a8;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
}

QFrame#sidebar QPushButton:hover {
    background-color: rgba(0, 212, 255, 0.08);
    color: #e0e6f0;
}

QFrame#sidebar QPushButton:checked,
QFrame#sidebar QPushButton[active="true"] {
    background-color: rgba(0, 212, 255, 0.12);
    color: {{ACCENT}};
    border-left: 3px solid {{ACCENT}};
}

/* --- Dock --- */
QFrame#dock {
    background-color: rgba(15, 20, 32, 220);
    border-top: 1px solid rgba(0, 212, 255, 0.08);
    border-radius: 0px;
}

/* --- Buttons --- */
QPushButton {
    background-color: rgba(26, 34, 53, 200);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px;
    color: #e0e6f0;
    padding: 8px 20px;
    font-weight: 500;
    min-height: 36px;
}

QPushButton:hover {
    background-color: rgba(0, 212, 255, 0.15);
    border-color: {{ACCENT}};
}

QPushButton:pressed {
    background-color: rgba(0, 212, 255, 0.25);
}

QPushButton#primaryButton {
    background-color: {{ACCENT}};
    color: #0a0e17;
    border: none;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #33ddff;
}

QPushButton#dangerButton {
    background-color: rgba(255, 59, 48, 0.15);
    border-color: rgba(255, 59, 48, 0.3);
    color: #ff3b30;
}

/* --- Input Fields --- */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: rgba(15, 20, 32, 180);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 10px;
    color: #e0e6f0;
    padding: 10px 14px;
    selection-background-color: {{ACCENT}};
    selection-color: #0a0e17;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: {{ACCENT}};
}

/* --- Scroll Bars --- */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: rgba(0, 212, 255, 0.2);
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(0, 212, 255, 0.4);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: rgba(0, 212, 255, 0.2);
    border-radius: 4px;
    min-width: 30px;
}

/* --- Labels --- */
QLabel#titleLabel {
    color: {{ACCENT}};
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 2px;
}

QLabel#subtitleLabel {
    color: #8892a8;
    font-size: 14px;
    font-weight: 400;
}

QLabel#statValue {
    color: {{ACCENT}};
    font-size: 24px;
    font-weight: 600;
}

QLabel#statLabel {
    color: #8892a8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* --- Tab Widget --- */
QTabWidget::pane {
    background-color: rgba(15, 20, 32, 180);
    border: 1px solid rgba(0, 212, 255, 0.1);
    border-radius: 12px;
    padding: 8px;
}

QTabBar::tab {
    background-color: transparent;
    color: #8892a8;
    padding: 10px 20px;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
}

QTabBar::tab:selected {
    color: {{ACCENT}};
    border-bottom-color: {{ACCENT}};
}

QTabBar::tab:hover {
    color: #e0e6f0;
}

/* --- Combo Box --- */
QComboBox {
    background-color: rgba(15, 20, 32, 180);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 10px;
    color: #e0e6f0;
    padding: 8px 14px;
    min-height: 36px;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #141a2a;
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 8px;
    selection-background-color: rgba(0, 212, 255, 0.15);
    color: #e0e6f0;
}

/* --- Sliders --- */
QSlider::groove:horizontal {
    background: rgba(0, 212, 255, 0.1);
    height: 4px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: {{ACCENT}};
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: {{ACCENT}};
    border-radius: 2px;
}

/* --- Progress Bar --- */
QProgressBar {
    background-color: rgba(0, 212, 255, 0.08);
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {{ACCENT}}, stop:1 #00ff88);
    border-radius: 6px;
}

/* --- Check Box --- */
QCheckBox {
    spacing: 8px;
    color: #e0e6f0;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid rgba(0, 212, 255, 0.3);
    background-color: transparent;
}

QCheckBox::indicator:checked {
    background-color: {{ACCENT}};
    border-color: {{ACCENT}};
}

/* --- Tool Tips --- */
QToolTip {
    background-color: #1a2235;
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 8px;
    color: #e0e6f0;
    padding: 6px 10px;
}

/* --- Menu --- */
QMenuBar {
    background-color: transparent;
    color: #8892a8;
}

QMenu {
    background-color: #141a2a;
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 10px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 6px;
}

QMenu::item:selected {
    background-color: rgba(0, 212, 255, 0.12);
    color: {{ACCENT}};
}

/* --- Splitter --- */
QSplitter::handle {
    background: rgba(0, 212, 255, 0.08);
    width: 2px;
}

/* --- Status Bar --- */
QStatusBar {
    background-color: rgba(10, 14, 23, 230);
    border-top: 1px solid rgba(0, 212, 255, 0.08);
    color: #8892a8;
}

/* --- Group Box --- */
QGroupBox {
    background-color: rgba(15, 20, 32, 150);
    border: 1px solid rgba(0, 212, 255, 0.1);
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 20px;
    font-weight: 600;
}

QGroupBox::title {
    color: {{ACCENT}};
    subcontrol-origin: margin;
    padding: 0 10px;
}
"""
