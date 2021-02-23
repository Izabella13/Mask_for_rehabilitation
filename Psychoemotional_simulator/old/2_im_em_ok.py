# Импорт нужных библиотек
from time import sleep
import numpy as np
import csv
import cv2
import os
import dlib
import glob
import math


dat_path = '../windows/Data/'
dis_path = '../discript/'
dlib_face = 'dlib_face_recognition_resnet_model_v1.dat'
shape = 'shape_predictor_68_face_landmarks.dat'
# Расположение изображений
faces_folder_path = 'dataset/'
# Для каждой эмоции, устанавливаем свой id
face_id = input('\n введите номер эмоции и нажмите enter ==>  ')
Em_num = 'Em_' + face_id


# Функция, рассчитывающая два вида дискрипторов лица
def get_landmarks(image):
    # Функция выделяет лицо в прямоугольник
    detections = detector(image, 1)
    # Цикл по всем найденым на изображении лицам
    for k, d in enumerate(detections):
        # Рисуем лицевые ориентиры с помощью класса предиктора
        # (Возврат координат точек на лице)
        shape = predictor(image, d)
        # Получаем дискрипторы лица
        face_descriptor = facerec.compute_face_descriptor(image, shape)
        # Список для размещения координат точек лица по оси X
        xlist = []
        # Список для размещения координат точек лица по оси Y
        ylist = []
        # Сохраняем координаты X и Y в двух списках
        for i in range(0, 68):
            # Список для X
            xlist.append(float(shape.part(i).x))
            # Список для Y
            ylist.append(float(shape.part(i).y))
            # Берем 30 точку на носу как центральную на лице
        meannp = np.asarray((shape.part(30).x, shape.part(30).y))
        # Создаем список для записи дискрипторов1
        landmarks_vectorised = []
        # Расчитываем дискрипторы 1
        for w, z in zip(xlist, ylist):
            # Создаем масив из координат векторов расстояний
            coornp = np.asarray((z, w))
            # Рассчитываем расстояние от центральной точки до данной
            dist = np.linalg.norm(coornp - meannp)
            # Добавляем в список дискрипторы1
            landmarks_vectorised.append(dist)
            # Масштабируем параметры изображения
        landmarks_vectorised[:] = landmarks_vectorised[:] / landmarks_vectorised[27]
    # Добавляем значения переменных, если нет выделенных лиц на экране
    if len(detections) == 0:
        xlist = 0
        ylist = 0
        meannp = np.asarray((0, 0))
        landmarks_vectorised = 0
        face_descriptor = 0
    # Возвращаем дискрипторы1, количество выделенных лиц
    return xlist, ylist, meannp, landmarks_vectorised, face_descriptor
nn = 0
# Извлекаем 128 дискрипторов
facerec = dlib.face_recognition_model_v1(dat_path + dlib_face)
# Создаем объект который может выделять лица в прямоугольник
detector = dlib.get_frontal_face_detector()
# Загрузка данных для извлечения 68 точек лица
predictor = dlib.shape_predictor(dat_path + shape)
# Список для записи 68 дискрипторов
im_par = []
# Список для записи 128 дискрипторов
im_par1 = []
# Просмотр всего каталога,
# составление списка файлов в этом каталоге и начало его прохождения
for f in glob.glob(os.path.join(faces_folder_path + Em_num, "*.jpg")):
    img = dlib.load_rgb_image(f)
    l_mx, l_my, mn, l_mv, f_d = get_landmarks(img)
    if l_mx != 0:
        im_par.append(l_mv)
        im_par1.append(f_d)
        nn += 1
# Открываем текстовый файл 68 дискрипторов на запись
f = open(dis_path + Em_num + '.txt', 'w', newline='')
# Создаем объект который работает с csv файлами
writer = csv.writer(f, delimiter=',')
for it in im_par:
    # Запись каждого из 68 дискрипторов
    writer.writerow(it)
f.close()
# Открываем текстовый файл 128 дискрипторов на запись
f = open(dis_path + Em_num + '_128.txt', 'w', newline='')
# Создаем объект который работает с csv файлами
writer = csv.writer(f, delimiter=',')
for it in im_par1:
    # Запись каждого из 128 дискрипторов
    writer.writerow(it)
f.close()
print(nn)
