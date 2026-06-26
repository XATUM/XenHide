import os
import subprocess
import shutil
import platform
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QTextEdit, QPushButton,
                             QFileDialog, QStackedWidget, QFrame, QMessageBox,
                             QRadioButton, QButtonGroup)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

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
    
    full_path = os.path.normpath(os.path.join(base, relative_path))
    
    
    if not os.path.exists(full_path):
        flat_path = relative_path.replace("../", "").replace("..\\", "")
        full_path = os.path.normpath(os.path.join(base, flat_path))
        
    return full_path


#UI COLORS & STYLING
BG = "#F6F6F6"  # Light gray
FG = "#202020"  # Dark gray 
WHITE = "#FFFFFF"


NAV_BTN_STYLE = f"""
    QPushButton {{
        background: {WHITE};
        color: {FG};
        border: 1px solid #CCC;
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 13px;
    }}
    QPushButton:hover {{
        background: #EAEAEA;
        border: 1px solid #BBB;
    }}
    QPushButton:disabled {{
        color: #999;
        background: #F0F0F0;
    }}
"""


ACTION_BTN_STYLE = f"""
    QPushButton {{
        background: #3584E4; 
        color: {WHITE};
        border: 1px solid #1A5FB4;
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 13px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background: #1C71D8;
    }}
    QPushButton:disabled {{
        background: #999;
        border: 1px solid #777;
    }}
"""




def _system_name():
    return platform.system().lower()


def _desktop_name():
    return os.environ.get("XDG_CURRENT_DESKTOP", "").upper()


def _run_dialog_command(command, *args):
    result = subprocess.run(
        [command, *args], check=False, capture_output=True, text=True
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
            "zenity", "--file-selection", "--title", title,
            "--filename", f"{start_dir}/", "--file-filter", image_filter
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
            "zenity", "--file-selection", "--save", "--confirm-overwrite",
            "--title", title, "--filename", start_path, "--file-filter", image_filter
        )
    return _native_save_dialog(title, start_path, image_filter)


class HomeScreen(QWidget):
    def __init__(self, on_encrypt, on_decrypt):
        super().__init__()
        self.on_encrypt = on_encrypt
        self.on_decrypt = on_decrypt

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 20)

        # Top Logo Area
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("../Assets/logo.png"))
        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Fallback if image path is wrong
            self.logo_label.setText("🔒")
            self.logo_label.setFont(QFont("Arial", 72))

        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.logo_label)
        logo_layout.addSpacing(20)

        title = QLabel("Select Action")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(title)

        layout.addLayout(logo_layout)
        layout.addSpacing(40)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.radio_group = QButtonGroup(self)

        self.radio_enc = QRadioButton("Encrypt: Hide a secret message inside an image")
        self.radio_enc.setFont(QFont("Arial", 11))
        self.radio_enc.setChecked(True)  # Default selection
        self.radio_group.addButton(self.radio_enc)

        self.radio_dec = QRadioButton("Decrypt: Extract hidden message from an image")
        self.radio_dec.setFont(QFont("Arial", 11))
        self.radio_group.addButton(self.radio_dec)

        center_layout.addWidget(self.radio_enc)
        center_layout.addSpacing(10)
        center_layout.addWidget(self.radio_dec)

        layout.addLayout(center_layout)
        layout.addStretch()

        # Bottom Navigation Bar
        bottom_bar = QHBoxLayout()

        btn_about = QPushButton("About")
        btn_about.setStyleSheet(NAV_BTN_STYLE)
        btn_about.clicked.connect(self.show_about)

        btn_next = QPushButton("Next")
        btn_next.setStyleSheet(ACTION_BTN_STYLE)
        btn_next.clicked.connect(self.handle_next)

        bottom_bar.addWidget(btn_about)
        bottom_bar.addStretch()
        bottom_bar.addWidget(btn_next)

        layout.addLayout(bottom_bar)

    def handle_next(self):
        if self.radio_enc.isChecked():
            self.on_encrypt()
        else:
            self.on_decrypt()

    def show_about(self):
        QMessageBox.about(self, "About XenHide",
                          "XenHide v1.0\nMade by YMAZE\n\nA steganography tool to hide and extract secret messages from images.")


class EncryptScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.image_path = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 20)

        title = QLabel("Encrypt Image")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)

        # Upload Button
        self.upload_btn = QPushButton("Select Image Source (.png, .bmp)")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{ background: {WHITE}; color: {FG}; border: 1px solid #CCC;
                border-radius: 6px; padding: 20px; font-size: 13px; }}
            QPushButton:hover {{ background: #EAEAEA; }}
        """)
        self.upload_btn.clicked.connect(self.choose_image)
        layout.addWidget(self.upload_btn)
        layout.addSpacing(20)

        # Secret Message Input
        msg_label = QLabel("Enter Secret Message:")
        msg_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(msg_label)

        self.msg_input = QTextEdit()
        self.msg_input.setPlaceholderText("Type the message you want to hide...")
        self.msg_input.setStyleSheet(f"background: {WHITE}; border: 1px solid #CCC; border-radius: 4px; padding: 8px;")
        layout.addWidget(self.msg_input)
        layout.addStretch()

        # Bottom Navigation Bar
        bottom_bar = QHBoxLayout()

        btn_back = QPushButton("Back")
        btn_back.setStyleSheet(NAV_BTN_STYLE)
        btn_back.clicked.connect(on_back)

        self.btn_run = QPushButton("Encrypt & Save")
        self.btn_run.setStyleSheet(ACTION_BTN_STYLE)
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self.run)

        bottom_bar.addWidget(btn_back)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.btn_run)

        layout.addLayout(bottom_bar)

    def choose_image(self):
        path = pick_open_path("Select Image", os.path.expanduser("~"), "Images (*.png *.bmp)")
        if path:
            self.image_path = path
            self.upload_btn.setText(f"✓  {os.path.basename(path)}")
            self.btn_run.setEnabled(True)

    def run(self):
        msg = self.msg_input.toPlainText().strip()
        if not msg:
            QMessageBox.warning(self, "Input Required", "Please enter a secret message.")
            return
        out = pick_save_path("Save Output Image", os.path.join(os.path.expanduser("~"), "hidden.png"), "PNG (*.png)")
        if out:
            encode_image(self.image_path, msg, out)
            QMessageBox.information(self, "Success", f"Message hidden successfully!\nSaved to:\n{out}")


class DecryptScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.image_path = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 20)

        title = QLabel("Decrypt Image")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)

        # Upload Button
        self.upload_btn = QPushButton("Select Stego Image (.png, .bmp)")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{ background: {WHITE}; color: {FG}; border: 1px solid #CCC;
                border-radius: 6px; padding: 20px; font-size: 13px; }}
            QPushButton:hover {{ background: #EAEAEA; }}
        """)
        self.upload_btn.clicked.connect(self.choose_image)
        layout.addWidget(self.upload_btn)
        layout.addSpacing(20)

        # Result display
        self.result_frame = QFrame()
        self.result_frame.setStyleSheet(
            f"background: {WHITE}; border: 1px solid #CCC; border-radius: 6px; padding: 12px;")
        self.result_frame.setVisible(False)
        result_layout = QVBoxLayout(self.result_frame)

        result_label = QLabel("Hidden Message Found:")
        result_label.setFont(QFont("Arial", 10, QFont.Bold))

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("border: none; background: transparent; color: #333;")

        result_layout.addWidget(result_label)
        result_layout.addWidget(self.result_text)
        layout.addWidget(self.result_frame)

        layout.addStretch()

        # Bottom Navigation Bar
        bottom_bar = QHBoxLayout()

        btn_back = QPushButton("Back")
        btn_back.setStyleSheet(NAV_BTN_STYLE)
        btn_back.clicked.connect(on_back)

        self.btn_run = QPushButton("Extract")
        self.btn_run.setStyleSheet(ACTION_BTN_STYLE)
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self.run)

        bottom_bar.addWidget(btn_back)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.btn_run)

        layout.addLayout(bottom_bar)

    def choose_image(self):
        path = pick_open_path("Select Stego Image", os.path.expanduser("~"), "Images (*.png *.bmp)")
        if path:
            self.image_path = path
            self.upload_btn.setText(f"✓  {os.path.basename(path)}")
            self.btn_run.setEnabled(True)
            self.result_frame.setVisible(False)

    def run(self):
        msg = decode_image(self.image_path)
        if msg:
            self.result_text.setPlainText(msg)
            self.result_frame.setVisible(True)
        else:
            QMessageBox.information(self, "Not Found", "No hidden message found in this image.")


class XenHideGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XenHide")
        self.setGeometry(100, 100, 700, 500)
        self.setWindowIcon(QIcon(resource_path("../Assets/logo.png")))
        self.setStyleSheet(f"QMainWindow {{ background-color: {BG}; }}")

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

    app.setStyleSheet(f"""
        QWidget {{
            background-color: {BG};
            color: {FG};
            font-family: Arial, sans-serif;
        }}
        QRadioButton {{
            spacing: 10px;
        }}
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
        }}
        QMessageBox {{
            background-color: {BG};
        }}
    """)

    window = XenHideGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
