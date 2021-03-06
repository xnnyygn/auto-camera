import time
import datetime
import os
import sys
import logging
import argparse

import agent_util
import photo_uploader

def take_photo(config):
  if config.getboolean('Mock', 'Status'):
    filename = config.get('Mock', 'PhotoPath')
    logging.debug('Mock On, use mock photo at %s', filename)
    return filename
  else:
    return __take_photo_by_picamera(config)

def __take_photo_by_picamera(config):
  '''take photo by pi camera'''
  import picamera

  # code recipe from
  # https://picamera.readthedocs.org/en/release-0.7/recipes1.html
  with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    filepath = determine_photo_path(config)
    logging.info('Capture to %s', filepath)
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
      logging.info('No face, delete photo %s', filename)
      os.remove(filename)
      return
    else:
      logging.info('%d face detected', face_count)

  logging.info('Start uploading')
  resp = photo_uploader.upload(filename, config)
  status_code = resp.status_code
  # TODO more appropriate checking method
  if status_code == 201: # created
    logging.info('Upload %s successfully, AWS key %s', filename, resp.json()['aws_key'])
  else:
    logging.warn('Failed to upload %s, status code %d', filename, status_code)

def __parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--config')
  args = parser.parse_args()
  return vars(args)

def __load_config(args):
  config_path = args['config'] or 'settings.ini'
  print 'Load config from ' + os.path.realpath(config_path)
  return agent_util.load_config(config_path)

def __init(config):
  loggingLevel = config.get('Default', 'LoggingLevel')
  logging.basicConfig(
    level = agent_util.determineLoggingLevel(loggingLevel),
    format='%(asctime)s %(levelname)s %(message)s'
  )

if __name__ == '__main__':
  config = __load_config(__parse_args())
  __init(config)
  filename = take_photo(config)
  upload_photo(filename, config)