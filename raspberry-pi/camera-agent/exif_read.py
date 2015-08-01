import sys

import exifread

def read_exif(filename):
  fp = open(filename, 'rb')
  tags = exifread.process_file(fp)
  fp.close()
  return tags

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print 'usage <filename>'
  else:
    filename = sys.argv[1]
    tags = read_exif(filename)
    for tag in tags.keys():
      if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
          print "Key: %s, value %s" % (tag, tags[tag])