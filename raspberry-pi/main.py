import time
import datetime
import os
import sys

import picamera

import face_detect

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
    # TODO use log
    print 'capture to %s' % filename
    camera.capture(filename)
    return filename

def upload_photo_if_face_detected(filename):
  face_count = face_detect.count_face(filename)
  if face_count == 0:
    # no face in photo, just delete this photo
    # TODO use log
    print 'no face, delete photo %s' % filename
    os.remove(filename)
  else:
    print '%d face detected, start uploading' % face_count

if __name__ == '__main__':
  filename = take_photo()
  upload_photo_if_face_detected(filename)