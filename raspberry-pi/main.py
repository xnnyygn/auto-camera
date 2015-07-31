import picamera
import time
import datetime
import cv2

def take_photo():
  '''take photo by pi camera'''
  # code recipe from
  # https://picamera.readthedocs.org/en/release-0.7/recipes1.html
  with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    # use current time as filename to prevent duplicating files
    filename = datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.jpg')
    print 'capture to %s' % filename
    camera.capture(filename)
    return filename

def count_face(filename):
  '''count face by opencv'''
  # https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

  img = cv2.imread(filename)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  return len(faces)

if __name__ == '__main__':
  filename = take_photo()
  print 'face in photo, %d' % count_face(filename)
