import requests

# config is an instance of ConfigParser
def upload(filename, config):
  return __upload(
    filename,
    config.get('Upload', 'ServerURI'),
    config.get('Upload', 'Location'),
    config.get('Default', 'CameraName')
  )

def __upload(filename, server_uri, location, camera_name):
  f = open(filename, 'rb')
  # https://requests.readthedocs.org/en/latest/user/quickstart/
  resp = requests.post(
    server_uri,
    files = {'photo_file': f},
    data = {
      'photo[location]': location, 
      'camera_name': camera_name
    }
  )
  f.close
  return resp

if __name__ == '__main__':
  import sys
  
  if len(sys.argv) < 5:
    print 'usage <filename> <server_uri> <location> <camera_name>'
  else:
    resp = __upload(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    status_code = resp.status_code
    if status_code != 201: # created
      print resp
    else:
      print resp.json()