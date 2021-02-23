from Psychoemotional_simulator.windows.emotion import Emotion
from Psychoemotional_simulator.windows.UI.ui_selectemotions import Ui_SelectEmotions


class SelectEmotions:
    def __init__(self, main_window):
        self.main_window = main_window
        self.simulator = Emotion(self.main_window)

    def select_emotions(self):
        self.main_window.ui = Ui_SelectEmotions()
        self.main_window.ui.setupUi(self.main_window)
        self.main_window.setWindowTitle("Выбор эмоции")
        self.main_window.ui.pushButton.clicked.connect(self.emotion1)
        self.main_window.ui.pushButton_2.clicked.connect(self.emotion2)
        self.main_window.ui.pushButton_3.clicked.connect(self.emotion3)
        self.main_window.ui.pushButton_4.clicked.connect(self.emotion4)
        self.main_window.ui.pushButton_5.clicked.connect(self.emotion5)
        self.main_window.ui.pushButton_6.clicked.connect(self.emotion6)
        self.main_window.ui.pushButton_7.clicked.connect(self.emotion7)

    def emotion1(self):
        self.simulator.emotion(1)

    def emotion2(self):
        self.simulator.emotion(2)

    def emotion3(self):
        self.simulator.emotion(3)

    def emotion4(self):
        self.simulator.emotion(4)

    def emotion5(self):
        self.simulator.emotion(5)

    def emotion6(self):
        self.simulator.emotion(6)

    def emotion7(self):
        self.simulator.emotion(7)
