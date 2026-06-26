"""Comprehensive settings page with categorized configuration panels."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSlider,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton

if TYPE_CHECKING:
    from jarvis.core.config import AppConfig
    from jarvis.core.events import EventBus
    from jarvis.ui.themes.theme_manager import ThemeManager


class SettingsPage(QWidget):
    """Full settings page with tabs for each category."""

    settings_changed = Signal()

    def __init__(
        self,
        config: AppConfig,
        theme_manager: ThemeManager,
        event_bus: EventBus,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._theme = theme_manager
        self._bus = event_bus

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Settings")
        header.setObjectName("titleLabel")
        layout.addWidget(header)

        tabs = QTabWidget()
        tabs.addTab(self._build_appearance_tab(), "Appearance")
        tabs.addTab(self._build_ai_tab(), "AI Provider")
        tabs.addTab(self._build_speech_tab(), "Speech")
        tabs.addTab(self._build_security_tab(), "Security")
        tabs.addTab(self._build_plugins_tab(), "Plugins")
        tabs.addTab(self._build_privacy_tab(), "Privacy")
        tabs.addTab(self._build_about_tab(), "About")
        layout.addWidget(tabs)

    def _build_appearance_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)

        # Theme
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout(theme_group)

        row = QHBoxLayout()
        row.addWidget(QLabel("Theme:"))
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(self._theme.available_themes)
        self._theme_combo.setCurrentText(self._theme.current_theme)
        row.addWidget(self._theme_combo)
        theme_layout.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Accent Color:"))
        self._accent_input = QLineEdit(self._config.ui.accent_color)
        self._accent_input.setMaximumWidth(150)
        row2.addWidget(self._accent_input)
        theme_layout.addLayout(row2)

        layout.addWidget(theme_group)

        # Animations
        anim_group = QGroupBox("Animations & Effects")
        anim_layout = QVBoxLayout(anim_group)

        self._animations_check = QCheckBox("Enable Animations")
        self._animations_check.setChecked(self._config.ui.animations_enabled)
        anim_layout.addWidget(self._animations_check)

        self._particles_check = QCheckBox("Particle Effects")
        self._particles_check.setChecked(self._config.ui.particle_effects)
        anim_layout.addWidget(self._particles_check)

        self._blur_check = QCheckBox("Blur Effects")
        self._blur_check.setChecked(self._config.ui.blur_enabled)
        anim_layout.addWidget(self._blur_check)

        self._glass_check = QCheckBox("Glassmorphism")
        self._glass_check.setChecked(self._config.ui.glassmorphism)
        anim_layout.addWidget(self._glass_check)

        layout.addWidget(anim_group)

        # Font
        font_group = QGroupBox("Font")
        font_layout = QHBoxLayout(font_group)
        font_layout.addWidget(QLabel("Font Size:"))
        self._font_spin = QSpinBox()
        self._font_spin.setRange(10, 24)
        self._font_spin.setValue(self._config.ui.font_size)
        font_layout.addWidget(self._font_spin)
        layout.addWidget(font_group)

        # Language
        lang_group = QGroupBox("Language")
        lang_layout = QHBoxLayout(lang_group)
        lang_layout.addWidget(QLabel("Language:"))
        self._lang_combo = QComboBox()
        self._lang_combo.addItems(["en", "de", "fr", "es", "ja", "zh"])
        self._lang_combo.setCurrentText(self._config.ui.language)
        lang_layout.addWidget(self._lang_combo)
        layout.addWidget(lang_group)

        # Apply button
        apply_btn = AnimatedButton("Apply Changes", primary=True)
        apply_btn.clicked.connect(self._apply_appearance)
        layout.addWidget(apply_btn)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def _build_ai_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)

        provider_group = QGroupBox("AI Provider")
        pl = QVBoxLayout(provider_group)

        row = QHBoxLayout()
        row.addWidget(QLabel("Provider:"))
        self._provider_combo = QComboBox()
        self._provider_combo.addItems(["openai", "ollama", "lmstudio"])
        self._provider_combo.setCurrentText(self._config.ai.name)
        row.addWidget(self._provider_combo)
        pl.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("API Key:"))
        self._api_key_input = QLineEdit(self._config.ai.api_key)
        self._api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        row2.addWidget(self._api_key_input)
        pl.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Base URL:"))
        self._base_url_input = QLineEdit(self._config.ai.base_url)
        row3.addWidget(self._base_url_input)
        pl.addLayout(row3)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Model:"))
        self._model_input = QLineEdit(self._config.ai.model)
        row4.addWidget(self._model_input)
        pl.addLayout(row4)

        row5 = QHBoxLayout()
        row5.addWidget(QLabel("Temperature:"))
        self._temp_slider = QSlider(Qt.Orientation.Horizontal)
        self._temp_slider.setRange(0, 100)
        self._temp_slider.setValue(int(self._config.ai.temperature * 100))
        row5.addWidget(self._temp_slider)
        self._temp_label = QLabel(f"{self._config.ai.temperature:.2f}")
        self._temp_slider.valueChanged.connect(lambda v: self._temp_label.setText(f"{v / 100:.2f}"))
        row5.addWidget(self._temp_label)
        pl.addLayout(row5)

        self._streaming_check = QCheckBox("Enable Streaming")
        self._streaming_check.setChecked(self._config.ai.streaming)
        pl.addWidget(self._streaming_check)

        layout.addWidget(provider_group)

        save_btn = AnimatedButton("Save AI Settings", primary=True)
        layout.addWidget(save_btn)
        layout.addStretch()
        return container

    def _build_speech_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)

        speech_group = QGroupBox("Speech Settings")
        sl = QVBoxLayout(speech_group)

        self._speech_enabled = QCheckBox("Enable Speech")
        self._speech_enabled.setChecked(self._config.speech.enabled)
        sl.addWidget(self._speech_enabled)

        row = QHBoxLayout()
        row.addWidget(QLabel("Wake Word:"))
        self._wake_word_input = QLineEdit(self._config.speech.wake_word)
        row.addWidget(self._wake_word_input)
        sl.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("TTS Rate:"))
        self._tts_rate = QSlider(Qt.Orientation.Horizontal)
        self._tts_rate.setRange(100, 300)
        self._tts_rate.setValue(self._config.speech.tts_rate)
        row2.addWidget(self._tts_rate)
        sl.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Volume:"))
        self._tts_volume = QSlider(Qt.Orientation.Horizontal)
        self._tts_volume.setRange(0, 100)
        self._tts_volume.setValue(int(self._config.speech.tts_volume * 100))
        row3.addWidget(self._tts_volume)
        sl.addLayout(row3)

        layout.addWidget(speech_group)
        layout.addStretch()
        return container

    def _build_security_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)

        sec_group = QGroupBox("Security")
        sl = QVBoxLayout(sec_group)

        self._encryption_check = QCheckBox("Enable Database Encryption")
        self._encryption_check.setChecked(self._config.security.encryption_enabled)
        sl.addWidget(self._encryption_check)

        self._face_check = QCheckBox("Face Recognition Login")
        self._face_check.setChecked(self._config.security.face_recognition_enabled)
        sl.addWidget(self._face_check)

        self._pin_check = QCheckBox("PIN Fallback")
        self._pin_check.setChecked(self._config.security.pin_fallback)
        sl.addWidget(self._pin_check)

        self._pwd_check = QCheckBox("Password Fallback")
        self._pwd_check.setChecked(self._config.security.password_fallback)
        sl.addWidget(self._pwd_check)

        self._audit_check = QCheckBox("Audit Logging")
        self._audit_check.setChecked(self._config.security.audit_logging)
        sl.addWidget(self._audit_check)

        layout.addWidget(sec_group)
        layout.addStretch()
        return container

    def _build_plugins_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)

        info = QLabel("Installed plugins will appear here.")
        info.setObjectName("subtitleLabel")
        layout.addWidget(info)

        layout.addStretch()
        return container

    def _build_privacy_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)

        privacy_group = QGroupBox("Privacy")
        pl = QVBoxLayout(privacy_group)
        pl.addWidget(QCheckBox("Allow anonymous usage analytics"))
        pl.addWidget(QCheckBox("Store conversation history"))
        pl.addWidget(QCheckBox("Allow camera access"))
        pl.addWidget(QCheckBox("Allow microphone access"))

        layout.addWidget(privacy_group)
        layout.addStretch()
        return container

    def _build_about_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("JARVIS AI")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        version = QLabel("Version 1.0.0")
        version.setObjectName("subtitleLabel")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        desc = QLabel("Ultimate Desktop Assistant\nBuilt with Python, PySide6, and modern AI.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #8892a8;")
        layout.addWidget(desc)

        layout.addStretch()
        return container

    def _apply_appearance(self) -> None:
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance()
        theme = self._theme_combo.currentText()
        accent = self._accent_input.text()
        if app and isinstance(app, QApplication):
            self._theme.set_accent_color(accent)
            self._theme.switch_theme(theme, app)
        self.settings_changed.emit()
