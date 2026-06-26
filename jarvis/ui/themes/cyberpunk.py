"""Cyberpunk theme — neon-heavy, high-contrast futuristic design."""

CYBERPUNK_PALETTE: dict[str, str] = {
    "window": "#0d0015",
    "window_text": "#f0e6ff",
    "base": "#120020",
    "alternate_base": "#1a0030",
    "text": "#f0e6ff",
    "button": "#1f0035",
    "button_text": "#f0e6ff",
    "highlight": "#ff00ff",
    "highlight_text": "#0d0015",
    "tooltip_base": "#1f0035",
    "tooltip_text": "#f0e6ff",
}

CYBERPUNK_QSS = """
/* ===== JARVIS AI — Cyberpunk Theme ===== */

* {
    font-family: 'Segoe UI', 'SF Pro Display', 'Inter', sans-serif;
}

QMainWindow {
    background-color: #0d0015;
}

QWidget {
    background-color: transparent;
    color: #f0e6ff;
}

QFrame#glassPanel {
    background-color: rgba(18, 0, 32, 200);
    border: 1px solid rgba(255, 0, 255, 0.2);
    border-radius: 16px;
}

QFrame#sidebar {
    background-color: rgba(13, 0, 21, 230);
    border-right: 1px solid rgba(255, 0, 255, 0.12);
}

QFrame#sidebar QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 12px;
    color: #9980b3;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
}

QFrame#sidebar QPushButton:hover {
    background-color: rgba(255, 0, 255, 0.08);
    color: #f0e6ff;
}

QFrame#sidebar QPushButton:checked {
    background-color: rgba(255, 0, 255, 0.12);
    color: {{ACCENT}};
    border-left: 3px solid {{ACCENT}};
}

QPushButton {
    background-color: rgba(31, 0, 53, 200);
    border: 1px solid rgba(255, 0, 255, 0.25);
    border-radius: 10px;
    color: #f0e6ff;
    padding: 8px 20px;
    font-weight: 500;
    min-height: 36px;
}

QPushButton:hover {
    background-color: rgba(255, 0, 255, 0.15);
    border-color: #ff00ff;
}

QPushButton#primaryButton {
    background-color: #ff00ff;
    color: #0d0015;
    border: none;
    font-weight: 600;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: rgba(18, 0, 32, 180);
    border: 1px solid rgba(255, 0, 255, 0.15);
    border-radius: 10px;
    color: #f0e6ff;
    padding: 10px 14px;
    selection-background-color: #ff00ff;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #ff00ff;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 0, 255, 0.25);
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QLabel#titleLabel {
    color: #ff00ff;
    font-size: 28px;
    font-weight: 700;
}

QLabel#statValue {
    color: #ff00ff;
    font-size: 24px;
    font-weight: 600;
}

QProgressBar {
    background-color: rgba(255, 0, 255, 0.08);
    border: none;
    border-radius: 6px;
    height: 8px;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ff00ff, stop:1 #00ffff);
    border-radius: 6px;
}

QComboBox {
    background-color: rgba(18, 0, 32, 180);
    border: 1px solid rgba(255, 0, 255, 0.2);
    border-radius: 10px;
    color: #f0e6ff;
    padding: 8px 14px;
}

QSlider::groove:horizontal {
    background: rgba(255, 0, 255, 0.1);
    height: 4px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #ff00ff;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QSlider::sub-page:horizontal {
    background: #ff00ff;
    border-radius: 2px;
}

QToolTip {
    background-color: #1f0035;
    border: 1px solid rgba(255, 0, 255, 0.25);
    border-radius: 8px;
    color: #f0e6ff;
    padding: 6px 10px;
}
"""
