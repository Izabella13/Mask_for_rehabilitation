import cv2


def rectangle_face(image, detection, shape):
    cv2.rectangle(image, (detection[0].left(), detection[0].top()),
                  (detection[0].right(), detection[0].bottom()), (0, 0, 255), 1)
    for j in range(0, 17):
        cv2.circle(image, (shape.part(j).x, shape.part(j).y), 1, (255, 0, 255), 1)
    for j in range(18, 26):
        cv2.circle(image, (shape.part(j).x, shape.part(j).y), 1, (255, 255, 255), 1)
    for j in range(27, 36):
        cv2.circle(image, (shape.part(j).x, shape.part(j).y), 1, (0, 255, 0), 1)
    for j in range(36, 48):
        cv2.circle(image, (shape.part(j).x, shape.part(j).y), 1, (255, 0, 0), 1)
    for j in range(49, 68):
        cv2.circle(image, (shape.part(j).x, shape.part(j).y), 1, (0, 0, 255), 1)
    cv2.circle(image, (shape.part(30).x, shape.part(30).y), 1, (0, 255, 255), 1)