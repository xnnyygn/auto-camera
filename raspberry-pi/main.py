import picamera
import time
import datetime
import cv

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

def count_face():
  '''count face by opencv'''
  # https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
  face_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

  img = cv.imread('20150731-13-51-57.jpg')
  gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  return len(faces)

if __name__ == '__main__':
  print count_face()