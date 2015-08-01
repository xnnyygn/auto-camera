import time
import datetime
import os
import sys
import logging

import picamera

import agent_util

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
    logging.info('capture to %s', filepath)
    camera.capture(filepath)
    return filepath

def determine_photo_path(config):
  # use current time as filename to prevent duplicating files
  filename = datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.jpg')
  capture_dir = config.get('Default', 'CaptureDir')
  agent_util.ensure_directory(capture_dir)
  return os.path.join(capture_dir, filename)

def upload_photo(filename, config):
  if config.getboolean('Default', 'CountFace'):
    import face_detect

    face_count = face_detect.count_face(filename)
    if config.getboolean('Default', 'DeletePhotoWithoutFace') and face_count == 0:
      # no face in photo, just delete this photo
      logging.info('no face, delete photo %s', filename)
      os.remove(filename)
      return
    else:
      logging.info('%d face detected', face_count)

  logging.info('start uploading')

if __name__ == '__main__':
  # TODO separate config
  config = agent_util.load_config('settings.ini')
  loggingLevel = config.get('Default', 'LoggingLevel')
  logging.basicConfig(
    level = agent_util.determineLoggingLevel(loggingLevel),
    format='%(asctime)s %(levelname)s %(message)s'
  )
  filename = take_photo(config)
  upload_photo(filename, config)