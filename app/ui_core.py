import sys
import time
import webbrowser

import engine
import settings
import ui
from console import log
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal


class UpdateConsole(QThread):
    log = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        QThread.__init__(self, parent)

    def run(self):
        with open("session_log", "r") as file:
            while True:
                file.seek(0)
                self.log.emit("".join(file.readlines()))
                time.sleep(0.5)


class MainWindowCore(ui.Ui_MainWindow):
    def __init__(self) -> None:
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        super().setupUi(self.MainWindow)

        self.github_button.clicked.connect(self.open_github)
        self.releases_button.clicked.connect(self.open_releases)
        self.engine_command.setText(settings.get_value("engine_command"))
        self.engine_command.textChanged.connect(self.update_engine_command)
        self.engine_browse_button.clicked.connect(self.browse_engine)

        engine_depth = settings.get_value("engine_depth")

        self.depth_slider.setValue(engine_depth)
        self.depth_value.setText(str(engine_depth))
        self.depth_slider.valueChanged.connect(self.update_depth)

        self.timeout_value.setText(str(settings.get_value("engine_timeout")))
        self.timeout_value.textChanged.connect(self.update_timeout)

        self.max_think_time_value.setText(
            str(settings.get_value("engine_max_thinking_time")))
        self.max_think_time_value.textChanged.connect(
            self.update_max_think_time)

        self.thread = UpdateConsole()
        self.thread.log.connect(self.add_log)
        self.thread.start()

        self.MainWindow.show()
        app.exec_()

        self.thread.terminate()
        self.thread.exit(0)
        try:
            engine.chess_engine.quit()
        except:
            pass
        

    def update_max_think_time(self):
        value = self.max_think_time_value.text()
        if value != "":
            settings.set_value("engine_max_thinking_time", int(value))

    def update_timeout(self):
        value = self.timeout_value.text()
        if value != "":
            settings.set_value("engine_timeout", int(value))

    def browse_engine(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.MainWindow, 'Single File', QtCore.QDir.rootPath(), '*.exe')
        self.engine_command.setText(str(fileName))
        try:
            log("Restarting engine...")
            engine.restart_engine()
        except Exception:
            log(
                "Engine crashed, edit engine command and restart program")
        else:
            log("Engine restartd")

    def open_github(self):
        webbrowser.open("https://github.com/ScriptingPath/ChessBot")

    def open_releases(self):
        webbrowser.open("https://github.com/ScriptingPath/ChessBot/releases/")

    def update_engine_command(self):
        settings.set_value(key="engine_command",
                           value=self.engine_command.text())
        try:
            log("Restarting engine...")
            engine.restart_engine()
        except Exception:
            log(
                "Engine crashed, edit engine command and restart program")
        else:
            log("Engine restartd")

    def update_depth(self):
        value = self.depth_slider.value()
        self.depth_value.setText(str(value))
        settings.set_value(key="engine_depth", value=int(value))

    def add_log(self, data):
        if self.console.toPlainText() != data:
            self.console.setText(data)


def start():
    MainWindowCore()


if __name__ == '__main__':
    start()
