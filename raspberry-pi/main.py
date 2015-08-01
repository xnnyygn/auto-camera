import time
import datetime
import os
import sys
import ConfigParser

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
    # TODO use capture dir setting
    camera.capture(filename)
    return filename

def upload_photo(filename, config):
  if config.getboolean('Default', 'DeletePhotoWithoutFace'):
    face_count = face_detect.count_face(filename)
    if face_count == 0:
      # no face in photo, just delete this photo
      # TODO use log
      print 'no face, delete photo %s' % filename
      os.remove(filename)
      return
    else:
      print '%d face detected, keep going' % face_count

  print 'start uploading'
  

def load_config(config_filename):
  # https://wiki.python.org/moin/ConfigParserExamples
  config = ConfigParser.ConfigParser()
  fp = open(config_filename)
  config.readfp(fp)
  fp.close
  return config

if __name__ == '__main__':
  # TODO separate config
  config = load_config('settings.ini')
  filename = take_photo()
  upload_photo(filename, config)