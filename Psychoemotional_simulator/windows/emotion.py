import functools

import dlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage

import os
import cv2

from Psychoemotional_simulator.windows import utils
from Psychoemotional_simulator.windows.UI.ui_simulator import Ui_Simulator
import pickle


class Emotion:
    def __init__(self, main_window):
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.view_cam)
        self.cap = cv2.VideoCapture(0)
        self.data_path = os.path.join(os.path.dirname(__file__), 'Data')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(os.path.join(self.data_path, 'shape_predictor_68_face_landmarks.dat'))
        self.face_rec = dlib.face_recognition_model_v1(os.path.join(self.data_path, 'dlib_face_recognition_resnet_model_v1.dat'))
        self.emotions = ['Радость', 'Удивление', 'Грусть', 'Злость', 'Отвращение', 'Презрение', 'Страх']
        self.fdi = []
        self.ind_d = 0
        self.ind_u = 0
        self.ind_p = 0
        self.image = None
        self.P_em = 0.5
        self.f = open(os.path.join(self.data_path, 'svm_dat.dat'), 'rb')
        self.clf = pickle.load(self.f)
        self.emotion_result = 0
        self.nn = 20
        self.e = None
        self.label = None
        self.font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'pictures', 'DejaVuSans.ttf'), 18)
        self.shape = None
        self.i = 0
        self.step = 0
        self.width = 0
        self.height = 0
        self.em_n = 0

    def view_cam(self):
        ret, self.image = self.cap.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.height, self.width, channel = self.image.shape
        self.step = channel * self.width
        self.rectangle_face()
        q_img = QImage(self.image.data, self.width, self.height, self.step, QImage.Format_RGB888)
        self.main_window.ui.label_3.setPixmap(QPixmap.fromImage(q_img))

    def start(self, e):
        self.e = e
        self.main_window.ui = Ui_Simulator()
        self.main_window.ui.setupUi(self.main_window)
        callback = functools.partial(self.emotion, e=e, cmd='stop')
        self.main_window.ui.pushButton.clicked.connect(callback)
        self.main_window.ui.label.setPixmap(
            QPixmap(os.path.join(os.path.dirname(__file__), 'pictures', f'{str(e)}.jpg')))
        self.main_window.setWindowTitle('Тренажер')
        self.timer.start(30)

    def emotion(self, e: int, cmd='sim'):
        if cmd == 'sim':
            self.start(e)
        elif cmd == 'stop':
            self.timer.stop()
            self.main_window.main_window.select_emotions_window()

    def rectangle_face(self):
        detection = self.detector(self.image, 1)
        if len(detection) == 0:
            self.main_window.ui.label_2.setText('Нет никого в кадре')
            self.em_n = 0
        for k, d in enumerate(detection):
            if self.i % 3 == 0:
                self.shape = self.predictor(self.image, d)
                face_description = self.face_rec.compute_face_descriptor(self.image, self.shape)
                dat = [face_description]
                self.em_n = self.clf.predict(dat)
            utils.rectangle_face(self.image, detection, self.shape)
            img_pil = Image.fromarray(self.image)
            draw = ImageDraw.Draw(img_pil)
            if self.em_n == self.e:
                self.emotion_result += 1
                draw.text((detection[0].left(), detection[0].top() - 20), self.emotions[int(self.em_n) - 1],
                          font=self.font, fill=(0, 255, 0))
            else:
                draw.text((detection[0].left(), detection[0].top() - 20), self.emotions[int(self.em_n) - 1],
                          font=self.font, fill=(255, 0, 0))
            self.image = np.array(img_pil)
        cv2.waitKey(10)
        if self.i == self.nn:
            self.emotion_result = self.emotion_result / self.nn
            if self.emotion_result >= self.P_em:
                self.main_window.ui.label_2.setText("Молодец:  " + "{0:.2f}".format(self.emotion_result * 100) + '%')
                self.emotion(self.e, 'stop')
            else:
                self.main_window.ui.label_2.setText(
                    "Попробуй ещё:  " + "{0:.2f}".format(self.emotion_result * 100) + '%')
            self.i = 0
        else:
            self.i += 1
