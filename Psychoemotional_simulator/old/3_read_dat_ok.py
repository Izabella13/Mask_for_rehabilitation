from sklearn import svm
from sklearn.utils import shuffle
import csv
import pickle


dis_path = '../discript/'
dat_path = '../windows/Data/'
# Список, содержащий дискрипторы
dat = []
# Список, содержащий номера эмоций
emotion_number = []
# Список, содержащий документы c параметрами каждой эмоции в формате cvs
file_names = ['Em_1_128.txt', 'Em_2_128.txt', 'Em_3_128.txt',
              'Em_4_128.txt', 'Em_5_128.txt', 'Em_6_128.txt',
              'Em_7_128.txt']
# Запуск цикла, пробегающегося по списку file_names,
# доставая и его индекс i, и то, что в нем находится
for i, file_name in enumerate(file_names):
    # открываем каждый из этих файлов с разрешением на чтение
    f = open(dis_path + file_name, 'r')
    # Считываем параметры в формате CVS
    reader = csv.reader(f)
    # Пробегаемся по считанным данным
    for row in reader:
        # Добавляем в список считанные данные
        dat.append(row)
        # Добавляем в список номера всех эмоций
        emotion_number.append(i + 1)
    # Закрываем файлы
    f.close
# Индекс в списке, соответствующий 80-ти процентам
# (0.8 - доля от общей выборки на обучаение)
pp = int(len(dat) * 0.8)
# Смешивает полученные данные одинаковым способ,
# сохраняя соответствие номера эмоций и их параметров
dat, emotion_number = shuffle(dat, emotion_number, random_state=0)
# Обучаящая выборка
learning_dat, learning_emotion_number = dat[:pp], emotion_number[:pp]
# Тестирующая выборка
test_dat, test_emotion_number = dat[pp+1:], emotion_number[pp+1:]
# Задаем параметры для метода обучения Support Vector Machine
clf = svm.SVC(C=2.0, gamma=2.0, kernel='poly', degree=3)
# Запускаем метод обучения Support Vector Machine
clf.fit(learning_dat, learning_emotion_number)
# Доля правильно определенных эмоций на фотографиях из базы
succesfull_prediction = clf.score(test_dat, test_emotion_number)
# Выводим полученную долю в консоль
print (succesfull_prediction)
# Сохроняем полученные данные в файл svm_dat
f = open(dat_path + 'svm_dat.dat', 'wb')
# Запись на диск
pickle.dump(clf, f)
f.close

