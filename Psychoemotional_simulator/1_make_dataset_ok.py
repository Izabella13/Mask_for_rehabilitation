import cv2
import time


haarcascade = 'Data/haarcascade_frontalface_default.xml'
directory = "dataset/EM_{}_{}.jpg"
# захватываем изображение
cam = cv2.VideoCapture(0)
# устанавливаем высоту кадра
cam.set(3, 800)
# устанавливаем ширину кадра
cam.set(4, 600)
# Установим классификатор лица, предоставляемый библиотекой OpenCV
face_detector = cv2.CascadeClassifier(haarcascade)
# Для каждой эмоции, устанавливаем свой id
face_id = input('\n введите номер эмоции и нажмите enter ==>  ')
print("\t [INFO] Инициализация лица. Смотрите в камеру и ждите...")
count = 0

while(True):
    ret, img = cam.read()
    # Переводим изображение в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Выделяем лицо в прямоугольную область
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Сохраняем захваченное изображение в папку dataset
        cv2.imwrite(directory.format(face_id, int(time.time() * 1e9)), gray[y:(y + h), x:(x + w)])
        cv2.imshow('image', img)
    if cv2.waitKey(70) & 0xff == 27:
        # Для завершения работы программы нажмите «ESC»
        break
    elif count >= 200:
        # Остановка программы после создания заданного количества кадров
        break
    print(count)

print("\n [INFO] Закрытие программы")
cam.release()
# Заканчиваем видеопоток и закрываем окна
cv2.destroyAllWindows()
