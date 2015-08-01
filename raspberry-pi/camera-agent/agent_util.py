import logging
import ConfigParser
import os

LOGGING_LEVEL_MAP = {
  'DEBUG': logging.DEBUG,
  'INFO': logging.INFO,
  'WARNING': logging.WARNING,
  'ERROR': logging.ERROR
}

def determineLoggingLevel(levelStr):
  '''determine logging level, default is warning'''
  if levelStr in LOGGING_LEVEL_MAP:
    return LOGGING_LEVEL_MAP[levelStr]
  else:
    return logging.WARNING

def load_config(filename):
  '''load config'''
  # https://wiki.python.org/moin/ConfigParserExamples
  config = ConfigParser.ConfigParser()
  fp = open(filename)
  config.readfp(fp)
  fp.close
  return config

def ensure_directory(path):
  '''ensure directory exist, create if not exist'''
  if not os.path.isdir(path):
    logging.info('directory [%s] not exist, create it', path)
    os.makedirs(path)