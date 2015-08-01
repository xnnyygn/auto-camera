import sys

import cv2

def detect_faces(filename):
  # https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
  # https://realpython.com/blog/python/face-recognition-with-python/
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
  img = cv2.imread(filename)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(
    gray, 
    scaleFactor = 1.1,
    minNeighbors = 5,
    minSize = (30, 30)
  )
  return (img, faces)

def highlight_faces(filename):
  img, faces = detect_faces(filename)
  for (x,y,w,h) in faces:
    # border color is blue
    # draw rectangle one by one
    img = cv2.rectangle(img, (x, y),(x + w, y + h), (255, 0, 0), 2)

  cv2.imshow('Face Detection',img)
  cv2.waitKey(0) # press any key to close window
  cv2.destroyAllWindows()

def count_face(filename):
  # second position is faces
  return len(detect_faces(filename)[1])

if __name__ == '__main__':
  argc = len(sys.argv) - 1
  if(argc < 1):
    print '''USAGE: <image> [<action>]
available action: highlight, count
default and fallback action is highlight'''
  else:
    # first(zero index) is script filename
    filename = sys.argv[1]
    if(argc > 1 and sys.argv[2] == 'count'):
      print '%d face(s) detected in image' % count_face(filename)
    else:
      highlight_faces(filename)