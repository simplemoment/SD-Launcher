import json
import sys, os
from mylibos.functions import *
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox
)

class SDLauncher(QWidget):
    def __init__(self):
        super().__init__()

        self.sd_arguments_file = ""
        self.sd_user_batch = "webui-user.bat"
        self.sd_batch_executable_process = None

        self.setWindowTitle("SD Launcher")
        self.setWindowIcon(QIcon('icon.ico'))

        # Title Label
        self.title_label = QLabel()
        self.title_label.setPixmap(QPixmap(resource_load('sd.png')))

        # Options Layout
        self.options_layout = QVBoxLayout()

        # Autolaunch Checkbox
        self.autolaunch_checkbox = QCheckBox("Autolaunch")
        self.options_layout.addWidget(self.autolaunch_checkbox)

        # Xformers Checkbox
        self.xformers_checkbox = QCheckBox("Xformers")
        self.options_layout.addWidget(self.xformers_checkbox)

        # Dark Theme Checkbox
        self.dark_theme_checkbox = QCheckBox("Dark theme")
        self.options_layout.addWidget(self.dark_theme_checkbox)

        # Use API Checkbox
        self.use_api_checkbox = QCheckBox("Use API")
        self.options_layout.addWidget(self.use_api_checkbox)

        # Use CPU Combobox
        self.use_cpu_combobox = QComboBox()
        self.use_cpu_combobox.addItems(get_cpu_param_list())
        self.options_layout.addWidget(self.use_cpu_combobox)

        # Access via LAN Checkbox
        self.access_via_lan_checkbox = QCheckBox("Access via LAN")
        self.options_layout.addWidget(self.access_via_lan_checkbox)

        # Use MEDRAM Checkbox
        self.use_medram_checkbox = QCheckBox("Use MEDRAM")
        self.options_layout.addWidget(self.use_medram_checkbox)

        # Button Layout
        self.button_layout = QHBoxLayout()

        # Stop Button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_sd_batch)
        self.button_layout.addWidget(self.stop_button)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.button_layout.addWidget(self.save_button)

        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.run_sd_batch)
        self.button_layout.addWidget(self.start_button)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.options_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.load_settings_from_json()

    def run_sd_batch(self):
        "This function runs saved batch file"
        try:
            self.sd_batch_executable_process = subprocess_bat(self.sd_user_batch, False)
        except Exception as exc: raise exc
    def stop_sd_batch(self):
        "This, stops already executing batch"
        try:
            terminate_process_by_pid(self.sd_batch_executable_process)
        except Exception as exc: raise exc
    def save_settings(self):
        "Saves changed settings in the batch file 'webui-user.bat'"
        # '--autolaunch', '--xformers', '--theme=dark', '--api', '--use-cpu ', '--medvram', '--listen'
        arguments = []
        if self.sd_arguments_file != "":
            settings = {
                "--autolaunch ": self.autolaunch_checkbox.isChecked(),
                "--xformers ": self.xformers_checkbox.isChecked(),
                "--theme=dark ": self.dark_theme_checkbox.isChecked(),
                "--api ": self.use_api_checkbox.isChecked(),
                "--use-cpu=": self.use_cpu_combobox.currentText(),
                "--listen ": self.access_via_lan_checkbox.isChecked(),
                "--medvram ": self.use_medram_checkbox.isChecked(),
            }
            with open("./sd_args.txt", "w") as f:
                f.write(str(settings))
                f.close()
        else:
            settings = eval(self.sd_arguments_file)
        for key, value in settings.items():
            if value:
                if not key in arguments and not key == "--use-cpu=":
                    arguments.append(key)
                if key == "--use-cpu=":
                    arguments.append(f"{key}{value}")

        str_arguments = ""
        for arg in arguments:
            str_arguments += arg

        print(str_arguments)

        with open(self.sd_user_batch, "w") as f:
            f.write(get_webui_batch_file_res(str_arguments))
            f.close()

    def load_settings_from_json(self):
        "Loads already saved settings for all forms"
        if os.path.exists("./sd_args.txt"):
            with open("./sd_args.txt", "r") as f:
                self.sd_arguments_file = str(f.readline())
                f.close()
            for key, value in eval(self.sd_arguments_file).items():
                settings_custom = [
                    "--autolaunch ",
                    "--xformers ",
                    "--theme=dark ",
                    "--api ",
                    "--use-cpu=",
                    "--listen ",
                    "--medvram "
                ]
                if value and key != settings_custom[4]:
                    if key == settings_custom[0]:
                        self.autolaunch_checkbox.setChecked(True)
                    if key == settings_custom[1]:
                        self.xformers_checkbox.setChecked(True)
                    if key == settings_custom[2]:
                        self.dark_theme_checkbox.setChecked(True)
                    if key == settings_custom[3]:
                        self.use_api_checkbox.setChecked(True)
                    if key == settings_custom[5]:
                        self.access_via_lan_checkbox.setChecked(True)
                    if key == settings_custom[6]:
                        self.use_medram_checkbox.setChecked(True)
                elif value and key == settings_custom[4]:
                    self.use_cpu_combobox.setCurrentText(value)

        else:
            self.sd_arguments_file = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SDLauncher()
    window.show()
    sys.exit(app.exec())
