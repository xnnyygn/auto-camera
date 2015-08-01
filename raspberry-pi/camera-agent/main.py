import time
import datetime
import os
import sys
import ConfigParser

import picamera

import face_detect

def take_photo(config):
  '''take photo by pi camera'''
  # code recipe from
  # https://picamera.readthedocs.org/en/release-0.7/recipes1.html
  with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    filepath = determine_photo_path(config)
    # TODO use log
    print 'capture to %s' % filepath
    camera.capture(filepath)
    return filepath

def determine_photo_path(config):
  # use current time as filename to prevent duplicating files
  filename = datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.jpg')
  capture_dir = config.get('Default', 'CaptureDir')
  ensure_directory(capture_dir)
  return os.path.join(capture_dir, filename)

# TODO can be a utility method
def ensure_directory(path):
  if not os.path.isdir(path):
    print 'directory [%s] not exist, create it' % path
    os.mkdirs(path)

def upload_photo(filename, config):
  if config.getboolean('Default', 'CountFace'):
    face_count = face_detect.count_face(filename)
    if config.getboolean('Default', 'DeletePhotoWithoutFace') and face_count == 0:
      # no face in photo, just delete this photo
      # TODO use log
      print 'no face, delete photo %s' % filename
      os.remove(filename)
      return
    else:
      print '%d face detected' % face_count

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
  filename = take_photo(config)
  upload_photo(filename, config)