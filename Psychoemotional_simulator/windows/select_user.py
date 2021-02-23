import os

import cv2
import dlib
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage
from scipy.spatial import distance

from Psychoemotional_simulator.windows import utils
from Psychoemotional_simulator.windows.UI.ui_selectuser import Ui_SelectUser


class SelectUser:
    def __init__(self, main_window):
        self.main_window = main_window
        self.cap = cv2.VideoCapture(0)
        self.image = None
        self.data_path = os.path.join(os.path.dirname(__file__), 'Data')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(os.path.join(self.data_path, 'shape_predictor_68_face_landmarks.dat'))
        self.face_rec = dlib.face_recognition_model_v1(os.path.join(self.data_path, 'dlib_face_recognition_resnet_model_v1.dat'))
        self.names = ['Даня', 'Никита', 'Белла', 'Вадимчик']
        self.fdi = []
        self.ind_d = 0
        self.ind_u = 0
        self.ind_p = 0
        self.j = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.view_cam)
        self.shape = None

    def select_user(self):
        self.main_window.ui = Ui_SelectUser()
        self.main_window.ui.setupUi(self.main_window)
        self.main_window.ui.pushButton.clicked.connect(self.next_window)
        self.main_window.setWindowTitle('Обнаружение пользователя')
        self.timer.start(20)

    def view_cam(self):
        ret, self.image = self.cap.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        height, width, channel = self.image.shape
        step = channel * width
        self.rectangle_face()
        q_img = QImage(self.image.data, width, height, step, QImage.Format_RGB888)
        self.main_window.ui.label.setPixmap(QPixmap.fromImage(q_img))

    def rectangle_face(self):
        detection = self.detector(self.image, 1)
        face_descriptor_frame = 0
        if len(detection) == 0 and self.ind_d == 0:
            self.main_window.ui.label_2.setText('Нет никого в кадре')
            self.ind_d, self.ind_p, self.ind_u = 1, 0, 0
        for k, d in enumerate(detection):
            if self.j % 3 == 0:
                self.shape = self.predictor(self.image, d)
                face_descriptor_frame = self.face_rec.compute_face_descriptor(self.image, self.shape)
            utils.rectangle_face(self.image, detection, self.shape)
            if self.j % 3 == 0:
                if not self.ind_p:
                    for c, fd in enumerate(self.fdi):
                        q = distance.euclidean(fd, face_descriptor_frame)
                        if q < 0.6:
                            self.main_window.ui.label_2.setText(f'Привет {self.names[c]}!')
                            self.ind_p = 1
                            self.ind_d = 0
                            self.ind_u = 1

                if not self.ind_u:
                    self.main_window.ui.label_2.setText('Пользователь не определен')
                    self.ind_u = 1
                    self.ind_d = 0
        cv2.waitKey(5)
        self.j += 1

    def next_window(self):
        self.timer.stop()
        self.main_window.main_window.main_window()
