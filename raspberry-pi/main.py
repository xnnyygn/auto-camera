import picamera
import time

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
    println 'capture to %s' % filename
    camera.capture(filename)

if __name__ == '__main__':
  take_photo()