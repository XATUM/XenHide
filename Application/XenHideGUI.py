import os
import subprocess
import shutil
import platform
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QTextEdit, QPushButton,
                              QFileDialog, QStackedWidget, QFrame, QMessageBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from xencrypt import encode_image
from xendcrypt import decode_image


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)

BG = "#F5F0E8"
FG = "#1A1A1A"
WHITE = "#FFFFFF"


def _system_name():
    return platform.system().lower()


def _desktop_name():
    return os.environ.get("XDG_CURRENT_DESKTOP", "").upper()


def _run_dialog_command(command, *args):
    result = subprocess.run(
        [command, *args],
        check=False,
        capture_output=True,
        text=True,
    )
    path = result.stdout.strip()
    return path if result.returncode == 0 and path else ""


def _native_open_dialog(title, start_dir, image_filter):
    dialog = QFileDialog(None, title)
    dialog.setFileMode(QFileDialog.ExistingFile)
    dialog.setNameFilter(image_filter)
    dialog.setOption(QFileDialog.DontUseNativeDialog, False)
    dialog.setDirectory(start_dir)
    if dialog.exec_():
        selected = dialog.selectedFiles()
        return selected[0] if selected else ""
    return ""


def _native_save_dialog(title, start_path, image_filter):
    dialog = QFileDialog(None, title)
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    dialog.setNameFilter(image_filter)
    dialog.setDefaultSuffix("png")
    dialog.setOption(QFileDialog.DontUseNativeDialog, False)
    dialog.selectFile(start_path)
    if dialog.exec_():
        selected = dialog.selectedFiles()
        return selected[0] if selected else ""
    return ""


def pick_open_path(title, start_dir, image_filter):
    system_name = _system_name()

    if system_name in {"windows", "darwin"}:
        return _native_open_dialog(title, start_dir, image_filter)

    desktop_name = _desktop_name()

    if "KDE" in desktop_name and shutil.which("kdialog"):
        return _run_dialog_command("kdialog", "--getopenfilename", start_dir, image_filter, "--title", title)

    if any(name in desktop_name for name in ("GNOME", "UNITY", "XFCE", "MATE", "CINNAMON")) and shutil.which("zenity"):
        return _run_dialog_command(
            "zenity",
            "--file-selection",
            "--title",
            title,
            "--filename",
            f"{start_dir}/",
            "--file-filter",
            image_filter,
        )

    return _native_open_dialog(title, start_dir, image_filter)


def pick_save_path(title, start_path, image_filter):
    system_name = _system_name()

    if system_name in {"windows", "darwin"}:
        return _native_save_dialog(title, start_path, image_filter)

    desktop_name = _desktop_name()

    if "KDE" in desktop_name and shutil.which("kdialog"):
        return _run_dialog_command("kdialog", "--getsavefilename", start_path, image_filter, "--title", title)

    if any(name in desktop_name for name in ("GNOME", "UNITY", "XFCE", "MATE", "CINNAMON")) and shutil.which("zenity"):
        return _run_dialog_command(
            "zenity",
            "--file-selection",
            "--save",
            "--confirm-overwrite",
            "--title",
            title,
            "--filename",
            start_path,
            "--file-filter",
            image_filter,
        )

    return _native_save_dialog(title, start_path, image_filter)



CARD_STYLE = f"""
    QPushButton {{
        background: {WHITE}; color: {FG};
        border: 2px solid {FG}; border-radius: 8px;
        padding: 20px; text-align: left; font-size: 13px;
    }}
    QPushButton:hover {{ background: {FG}; color: {BG}; }}
"""
RUN_STYLE = f"""
    QPushButton {{
        background: {FG}; color: {BG};
        border: none; border-radius: 6px;
        padding: 13px; font-size: 13px; font-weight: bold; letter-spacing: 2px;
    }}
    QPushButton:hover {{ background: #333; }}
    QPushButton:disabled {{ background: #aaa; }}
"""
BACK_STYLE = f"""
    QPushButton {{
        background: none; color: {FG};
        border: 1.5px solid {FG}; border-radius: 6px;
        padding: 5px 12px; font-size: 12px;
    }}
    QPushButton:hover {{ background: {FG}; color: {BG}; }}
"""


class HomeScreen(QWidget):
    def __init__(self, on_encrypt, on_decrypt):
        super().__init__()
        self.setStyleSheet(f"background: {BG};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(16)

        title = QLabel("Welcome to XenHide")
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {FG}; font-style: italic; border-bottom: 2px dotted {FG}; padding-bottom: 16px;")
        layout.addWidget(title)

        sub = QLabel("Made by Xenon Akro")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #888; font-size: 11px; letter-spacing: 3px;")
        layout.addWidget(sub)

        row = QHBoxLayout()
        enc_btn = QPushButton("ENCRYPT (A -> *)\nHide a secret message inside an image")
        enc_btn.setStyleSheet(CARD_STYLE)
        enc_btn.setFixedHeight(90)
        enc_btn.clicked.connect(on_encrypt)

        dec_btn = QPushButton("DECRYPT (*->A)\nExtract hidden message from an image")
        dec_btn.setStyleSheet(CARD_STYLE)
        dec_btn.setFixedHeight(90)
        dec_btn.clicked.connect(on_decrypt)

        row.addWidget(enc_btn)
        row.addWidget(dec_btn)
        layout.addLayout(row)
        layout.addStretch()

        footer = QLabel("XENON AKRO · XENHIDE v1.0")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(f"color: #aaa; font-size: 10px; letter-spacing: 2px; border-top: 1px dotted {FG}; padding-top: 12px;")
        layout.addWidget(footer)


class EncryptScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.image_path = None
        self.setStyleSheet(f"background: {BG};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(12)

        hdr = QHBoxLayout()
        back = QPushButton("← BACK")
        back.setStyleSheet(BACK_STYLE)
        back.setFixedWidth(80)
        back.clicked.connect(on_back)
        title = QLabel("ENCRYPT")
        title.setStyleSheet(f"color: {FG}; font-size: 14px; font-weight: bold; letter-spacing: 2px;")
        hdr.addWidget(back)
        hdr.addWidget(title)
        hdr.addStretch()
        layout.addLayout(hdr)

        self.upload_btn = QPushButton("  Click to upload the image (PNG/BMP)")
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{ background: {WHITE}; color: #888; border: 2px dashed {FG};
                border-radius: 8px; padding: 28px; font-size: 13px; text-align: center; }}
            QPushButton:hover {{ background: #eee8dc; }}
        """)
        self.upload_btn.clicked.connect(self.choose_image)
        layout.addWidget(self.upload_btn)

        msg_label = QLabel("SECRET MESSAGE")
        msg_label.setStyleSheet("color: #888; font-size: 11px; letter-spacing: 2px;")
        layout.addWidget(msg_label)

        self.msg_input = QTextEdit()
        self.msg_input.setPlaceholderText("Type the message you want to hide...")
        self.msg_input.setStyleSheet(f"background: {WHITE}; border: 1.5px solid {FG}; border-radius: 6px; padding: 8px; font-size: 13px;")
        self.msg_input.setFixedHeight(90)
        layout.addWidget(self.msg_input)

        self.run_btn = QPushButton("ENCRYPT & SAVE IMAGE")
        self.run_btn.setStyleSheet(RUN_STYLE)
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.run)
        layout.addWidget(self.run_btn)
        layout.addStretch()

    def choose_image(self):
        path = pick_open_path("Select Image", os.path.expanduser("~"), "Images (*.png *.bmp)")
        if path:
            self.image_path = path
            self.upload_btn.setText(f"✓  {path.split('/')[-1]}")
            self.run_btn.setEnabled(True)

    def run(self):
        msg = self.msg_input.toPlainText().strip()
        if not msg:
            QMessageBox.warning(self, "XenHide", "Please enter a secret message.")
            return
        out = pick_save_path("Save Output Image", os.path.join(os.path.expanduser("~"), "hidden.png"), "PNG (*.png)")
        if out:
            encode_image(self.image_path, msg, out)
            QMessageBox.information(self, "XenHide", f"✓ Message hidden successfully!\nSaved to: {out}")


class DecryptScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.image_path = None
        self.setStyleSheet(f"background: {BG};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(12)

        hdr = QHBoxLayout()
        back = QPushButton("← BACK")
        back.setStyleSheet(BACK_STYLE)
        back.setFixedWidth(80)
        back.clicked.connect(on_back)
        title = QLabel("DECRYPT")
        title.setStyleSheet(f"color: {FG}; font-size: 14px; font-weight: bold; letter-spacing: 2px;")
        hdr.addWidget(back)
        hdr.addWidget(title)
        hdr.addStretch()
        layout.addLayout(hdr)

        self.upload_btn = QPushButton(" Click to upload the  image (PNG/BMP)")
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{ background: {WHITE}; color: #888; border: 2px dashed {FG};
                border-radius: 8px; padding: 28px; font-size: 13px; text-align: center; }}
            QPushButton:hover {{ background: #eee8dc; }}
        """)
        self.upload_btn.clicked.connect(self.choose_image)
        layout.addWidget(self.upload_btn)

        self.run_btn = QPushButton("EXTRACT MESSAGE")
        self.run_btn.setStyleSheet(RUN_STYLE)
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.run)
        layout.addWidget(self.run_btn)

        self.result_frame = QFrame()
        self.result_frame.setStyleSheet(f"background: {WHITE}; border: 1.5px solid {FG}; border-radius: 8px; padding: 12px;")
        self.result_frame.setVisible(False)
        result_layout = QVBoxLayout(self.result_frame)
        result_label = QLabel("HIDDEN MESSAGE FOUND")
        result_label.setStyleSheet("color: #888; font-size: 11px; letter-spacing: 2px;")
        self.result_text = QLabel()
        self.result_text.setStyleSheet(f"color: {FG}; font-size: 14px; font-style: italic;")
        self.result_text.setWordWrap(True)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.result_text)
        layout.addWidget(self.result_frame)
        layout.addStretch()

    def choose_image(self):
        path = pick_open_path("Select Stego Image", os.path.expanduser("~"), "Images (*.png *.bmp)")
        if path:
            self.image_path = path
            self.upload_btn.setText(f"✓  {path.split('/')[-1]}")
            self.run_btn.setEnabled(True)

    def run(self):
        msg = decode_image(self.image_path)
        if msg:
            self.result_text.setText(msg)
            self.result_frame.setVisible(True)
        else:
            QMessageBox.information(self, "XenHide", "No hidden message found in this image.")


class XenHideGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XENHIDE")
        self.setGeometry(60, 60, 750, 580)
        self.setWindowIcon(QIcon(resource_path("../Assets/logo.png")))

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = HomeScreen(self.go_encrypt, self.go_decrypt)
        self.encrypt = EncryptScreen(self.go_home)
        self.decrypt = DecryptScreen(self.go_home)

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.encrypt)
        self.stack.addWidget(self.decrypt)

    def go_home(self): self.stack.setCurrentWidget(self.home)
    def go_encrypt(self): self.stack.setCurrentWidget(self.encrypt)
    def go_decrypt(self): self.stack.setCurrentWidget(self.decrypt)


def main():
    app = QApplication(sys.argv)
    palette = app.palette()
    from PyQt5.QtGui import QPalette, QColor
    palette.setColor(QPalette.Window, QColor("#F5F0E8"))
    palette.setColor(QPalette.WindowText, QColor("#1A1A1A"))
    palette.setColor(QPalette.Base, QColor("#FFFFFF"))
    palette.setColor(QPalette.Text, QColor("#1A1A1A"))
    palette.setColor(QPalette.Button, QColor("#F5F0E8"))
    palette.setColor(QPalette.ButtonText, QColor("#1A1A1A"))
    app.setPalette(palette)
    window = XenHideGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()