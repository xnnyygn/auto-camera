from fabric.api import run, cd
from fabric.operations import put, prompt

CODE_DIR = '~/camera-agent'
PHOTO_DIR = '~/photos'
CONFIG_PATH = '~/settings.ini'

def deploy():
  # TODO kill camera-agent process
  # delete directory 'camera-agent'
  run('rm -rf ' + CODE_DIR)
  # TODO copy raspberry-pi files to 'camera-agent'
  put('camera-agent', '~')
  # capture
  if prompt('capture now? (y)[y/n]: ', default = 'y') == 'y':
    capture()

def capture():
  with cd(CODE_DIR):
    run('python main.py -f ' + CONFIG_PATH)

def clear_photo():
  run('rm %s/*' % PHOTO_DIR)