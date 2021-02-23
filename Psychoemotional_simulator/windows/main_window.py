from PySide6.QtWidgets import QApplication, QMainWindow

from Psychoemotional_simulator.windows.select_emotions import SelectEmotions
from Psychoemotional_simulator.windows.select_user import SelectUser
from Psychoemotional_simulator.windows.UI.ui_mainwindow import Ui_MainWindow
from Psychoemotional_simulator.windows.UI.ui_mainwindow1 import Ui_MainWindow as Ui_MainWindow1
from Psychoemotional_simulator.windows.simulator import Simulator


import sys


class MainWindow1(QMainWindow):
    def __init__(self):
        super(MainWindow1, self).__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.ui.pushButton.setText("Распознать пользователя")
        self.ui.pushButton.clicked.connect(self.select_user_window)
        self.ui.pushButton_2.clicked.connect(self.main__window)
        self.main_window = MainWindow(self)
        self.selectUser = SelectUser(self)
        self.setWindowTitle('Главное меню')

    def select_user_window(self):
        self.selectUser.select_user()

    def main__window(self):
        self.main_window.main_window()


class MainWindow:
    def __init__(self, main_window: MainWindow1):
        self.__main_window = main_window
        self.select_emotions = SelectEmotions(self.__main_window)
        self.simulator = Simulator(self.__main_window)

    def main_window(self):
        self.__main_window.ui = Ui_MainWindow()
        self.__main_window.ui.setupUi(self.__main_window)
        self.__main_window.setWindowTitle("Главный экран")
        self.__main_window.ui.pushButton.clicked.connect(self.select_emotions_window)
        self.__main_window.ui.pushButton_2.clicked.connect(self.simulator_window)

    def select_emotions_window(self):
        self.select_emotions.select_emotions()

    def simulator_window(self):
        self.simulator.emotion()


def main():
    app = QApplication(sys.argv)
    w = MainWindow1()
    w.show()
    sys.exit(app.exec_())
