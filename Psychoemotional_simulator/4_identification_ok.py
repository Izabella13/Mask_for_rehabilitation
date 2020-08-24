from scipy.spatial import distance
from pygame import mixer
import keyboard
from time import sleep
import glob, cv2, dlib
from PIL import ImageFont, ImageDraw, Image
import pickle
import numpy as np
import random

dat_path='Data/'
mp3_pic_path='mp3_pic/'

# Инициализация размера изображения, которое нужно изменить, и захват его размера
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    # Если ширина и высота ничему не равны, вернуть исходное изображение
    if width is None and height is None:
        return image
    # Проверяем, если высота ничему не равна
    if width is None:
        # Рассчитываем соотношение высоты и построить размеры
        r = height / float(h)
        dim = (int(w * r), height)
    #Условие, если высота чему-то равна
    else:
        # Рассчитываем соотношение высоты и построить размеры
        r = width / float(w)
        dim = (width, int(h * r))
    # Меняем размер изображения
    resized = cv2.resize(image, dim, interpolation = inter)
    # Возвращаем измененный размер изображения
    return resized
# Создаем объект, который выделяет лицо прямоугольником
detector = dlib.get_frontal_face_detector()
# Загрузка(шаблона) данных обучения для точек на лице
predictor = dlib.shape_predictor(dat_path+'shape_predictor_68_face_landmarks.dat')
# Загрузка данных обучения нейросети resnet
facerec = dlib.face_recognition_model_v1(dat_path+'dlib_face_recognition_resnet_model_v1.dat')
# Подключение камеры
video_capture = cv2.VideoCapture(0)
# Задаем размеры кадра камеры   160x120
video_capture.set(3, 360)
# 360x240
video_capture.set(4, 240)
img_path = ['p_D.jpg','p_N.jpg','p_I.jpg','p_V.jpg']
fdi = [] 
audio = ['u_D.mp3','u_N.mp3','u_I.mp3','u_V.mp3','u_U.mp3']
names = ['Даня','Никита','Белла','Вадимчик']
ind_u=0
mixer.init()

for im in img_path:
    img = cv2.imread(mp3_pic_path+im)
    # Ф-ция выделяет лицо в прямоугольник
    detections = detector(img, 1)
    # Цикл по всем найденным на изображении лицам
    for k,d in enumerate(detections):
        # Возвращает координаты точек на лице
        shape = predictor(img, d)
        # Получаем 128 дискрипторов лица
        face_descriptor_img = facerec.compute_face_descriptor(img, shape)
        fdi.append(face_descriptor_img)
ind_d,ind_u,ind_p,j=0,0,0,0

# Цикл обработки nn кадров
while(1):
    # Запуск камеры
    ret, frame = video_capture.read()
    # Ф-ция выделяет лицо в прямоугольник
    detections = detector(frame, 1)
    face_descriptor_frame =0
    if len(detections) == 0:
        if not ind_d:
            print('нет никого в кадре')
            ind_d,ind_p,ind_u=1,0,0
    # Цикл по всем найденным на изображении лицам
    for k,d in enumerate(detections):
        if j%3==0:
            # Возвращает координаты точек на лице
            shape = predictor(frame, d)
            # Получаем 128 дискрипторов лица
            face_descriptor_frame = facerec.compute_face_descriptor(frame, shape)
            # Рисуем прямоугольник вокруг лица
        cv2.rectangle(frame, (detections[0].left(), detections[0].top()),
                      (detections[0].right(), detections[0].bottom()), (0, 0, 255), 1)
        for k in range(0,17): 
            cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (255,0,255), 1)
        for k in range(18,26):
            cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (255,255,255), 1)
        for k in range(27,36): 
            cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (0,255,0), 1)
        for k in range(36,48):  
            cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (255,0,0), 1)
        for k in range(49,68):
            cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (0,0,255), 1)
        cv2.circle(frame, (shape.part(30).x, shape.part(30).y), 1, (0,255,255), 1)
        if j%3==0:
            if not ind_p:
                for c,fd in enumerate(fdi):
                    q = distance.euclidean(fd,face_descriptor_frame)
                    if q<0.6:
                        # Загрузка звуковой дорожки,
                        # содержащихся в списке sound,
                        # с последующим ее проигрыванием
                        mixer.music.load(mp3_pic_path+audio[c])
                        mixer.music.play()
                        print('Привет {}!'.format(names[c]))
                        ind_p,ind_d,ind_u=1,0,1    
            if not ind_u:
                print('Пользователь не распознан')
                # Загрузка звуковой дорожки, содержащихся в списке sound,
                # с последующим ее проигрыванием
                mixer.music.load(mp3_pic_path+audio[4])
                mixer.music.play()
                ind_u,ind_d=1,0
    # Выводим картинку с камеры
    cv2.imshow('camera', image_resize(frame, height = 300))
    cv2.moveWindow('camera', 600,400)
    # Задержка изображений
    cv2.waitKey(10)
    if keyboard.is_pressed('q'):
        print('вы нажали q. Подождите пожалуйста')
        print('Выберите сценарий обучения:')
        print('1) Случайный порядок')
        print('2) Изначально заданная последовательность')
        choice = int(input())
        break 
    j+=1
cv2.destroyAllWindows()

# Кол-во кадров для обработки для определения эмоций
nn=20
# Уровень подтвержения эмоций(если выше P_em, то переходим  к следующей эмоции)
P_em=0.5
# Функция отвечающая за вывод окна с картинками
# Создаем объект, который выделяет лицо прямоугольником
detector = dlib.get_frontal_face_detector()
# Загрузка(шаблона) данных обучения для точек на лице
predictor = dlib.shape_predictor(dat_path+'shape_predictor_68_face_landmarks.dat')
# Загрузка данных обучения нейросети resnet
facerec = dlib.face_recognition_model_v1(dat_path+'dlib_face_recognition_resnet_model_v1.dat')
# добавляем файл шрифта ttf с поддержкой кирилицы
font= ImageFont.truetype("DejaVuSans.ttf", 18)
# Список эмоций, которые будут выводиться в консоль
emotions=['Радость', 'Удивление', 'Грусть', 'Злость', 'Отвращение', 'Презрение', 'Страх']
# Звуковые дорожки, содержащие обращение к каждой из эмоций
sound=['1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3', '6.mp3', '7.mp3']
# Звуковые дорожки, содержащие обращение к подсказке по каждой из эмоций
sound1 = ['1_h.mp3', '2_h.mp3', '3_h.mp3', '4_h.mp3', '5_h.mp3', '6_h.mp3', '7_h.mp3']
# Изображения, содержащие подсказки к каждой из эмоций
pictures=['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg']
# Открываем файл svm_dat.dat для чтения как двоичный
f=open(dat_path+'svm_dat.dat','rb')
# Загружаем обученный метод svm
clf=pickle.load(f) 
# Закрываем файл
f.close
# Инициализация mixer из pygame
mixer.init()

if choice == 1:
    i=0

    while i<7:
        rand = random.randint(0,6)
        emotions[i], emotions[rand] = emotions[rand], emotions[i]
        pictures[i], pictures[rand] = pictures[rand], pictures[i]
        sound[i], sound[rand] = sound[rand], sound[i]
        sound1[i], sound1[rand] = sound1[rand], sound1[i]
        i+=1

# Начало цикла, проходящему по всему списку emotions,
# содержащий и индекс i, и его содержание
for i, em in enumerate(emotions):
    # Переменная, которая считает кол-во попыток изображения каждой эмоции
    tries = 0
    # Переменная, содержащия в себе процент того,
    # насколько оператор показывает похожую эмоцию
    emotion_result=0
    # Начало цикла, который будет просить показать эмоцию, попробовать еще раз
    # или перейти к следующей в зависимости от схожести с примером

    while emotion_result<P_em:
        tries += 1
        img =cv2.imread(mp3_pic_path+pictures[i])
        # Задержка изображений
        cv2.waitKey(10)
        # Выводим картинку с камеры
        cv2.imshow('example', img)
        cv2.moveWindow('example', 150,150)
        # Загрузка звуковой дорожки, содержащихся в списке sound,
        # с последующим ее проигрыванием
        mixer.music.load(mp3_pic_path+sound[i])
        mixer.music.play()
        # Выводит в консоль просьбу показать эмоцию из списка emotions
        print("Покажите нам "+ em)
        # Цикл обработки nn кадров
        for j in range(nn):
            # Запуск камеры
            ret, frame = video_capture.read()
            # Ф-ция выделяет лицо в прямоугольник
            detections = detector(frame, 1)
            # Добавляем значения переменных, если нет выделенных лиц лиц на экране
            if len(detections) == 0:
                    em_n=0
                    print(em_n)
            # Цикл по всем найденным на изображении лицам
            for k, d in enumerate(detections):
                if j%1==0:
                    # Возвращает координаты точек на лице
                    shape = predictor(frame, d)
                    # Получаем 128 дискрипторов лица
                    face_descriptor = facerec.compute_face_descriptor(frame, shape)
                    # Создаем список для дискрипторов
                    dat=[]
                    # Записываем 128 дискрипторов для каждого лица
                    dat.append(face_descriptor)
                    em_n=clf.predict(dat)
                # Рисуем прямоугольник вокруг лица
                cv2.rectangle(frame, (detections[0].left(),
                                      detections[0].top()),
                              (detections[0].right(),
                               detections[0].bottom()),
                               (0, 0, 255), 1)
                for k in range(0,17):
                    cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (255,0,255), 1)
                for k in range(18,26):
                    cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (255,255,255), 1)
                for k in range(27,36):
                    cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (0,255,0), 1)
                for k in range(36,48):
                    cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (255,0,0), 1)
                for k in range(49,68):
                    cv2.circle(frame, (shape.part(k).x, shape.part(k).y), 1, (0,0,255), 1)
                cv2.circle(frame, (shape.part(30).x, shape.part(30).y), 1, (0,255,255), 1)    
                print(em_n)
                # если эмоция показана верна, то переходим к другой эмоции
                if em_n==i+1:
                    emotion_result+=1
                    # передаем изображение для обработки в библиотеку pillow
                    img_pil = Image.fromarray(frame)
                    # создаем объект, содержащий изображение
                    draw = ImageDraw.Draw(img_pil)
                    # выводим текст кирилицей
                    draw.text( (detections[0].left(), detections[0].top()-20),
                             emotions[int(em_n)-1], font=font, fill=(0,255,0))
                    frame = np.array(img_pil)
                else:
                    # передаем изображение для обработки в библиотеку pillow
                    img_pil = Image.fromarray(frame)
                    # создаем объект, содержащий изображение
                    draw = ImageDraw.Draw(img_pil)
                    # выводим текст кирилицей
                    draw.text( (detections[0].left(), detections[0].top()-20),  emotions[int(em_n)-1], font=font, fill=(0,0,255))
                    # возвращаем изображение с названием эмоции
                    frame = np.array(img_pil)
            # задержка изображений
            cv2.waitKey(10)
            # выводим картинку с камеры
            cv2.imshow('camera', image_resize(frame, height = 600))
            cv2.moveWindow('camera', 600,150)
        # считаем долю правильно воспроизведенных эмоций
        emotion_result=emotion_result/nn
        # Условие, если проецнт совпадения с эмоцией оператора больше или равен P_em процентам
        if emotion_result>=P_em:
            # Запускает звуковую дорожку, содержащую в себе похвалу оператора
            mixer.music.load(mp3_pic_path+'8.mp3')
            mixer.music.play()
            # Выводит в консоль "Молодец"
            print("Молодец  "+"{0:.2f}".format(emotion_result*100)+'%')
            sleep(2)
        else:
            # Запускает звуковую дорожку, содержащую в себе прозьбу оператора попробовать еще
            mixer.music.load(mp3_pic_path+'9.mp3')
            mixer.music.play()
            # Выводит в консоль "Попробуй еще"
            print("Попробуте еще " +"{0:.2f}".format(emotion_result*100)+'%')
            sleep(2)
            if tries % 3 == 2:
                mixer.music.load(mp3_pic_path + sound1[i])
                mixer.music.play()
                # Делает паузу в исполнении скрипта, чтобы дорожка полностью проигралась
                sleep(6)

# закрываем камеру
video_capture.release()
# закрываем все окна, открытые во время работы программы
cv2.destroyAllWindows()
