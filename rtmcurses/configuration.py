# Copyright (c) 2010 Manuel Vonthron <manuel.vonthron@acadis.org>
#
# Redistribution of this file is permitted under
# the terms of the BSD license

from os.path import join, isfile
from os import environ
from sys import stderr
from re import compile
from ConfigParser import ConfigParser, RawConfigParser

configuration_parser = ConfigParser(allow_no_value = True)
configuration_parser.add_section('Display')
configuration_parser.set('Display', 'history_size', '20')
configuration_parser.set('Display', 'max_view_height', '480')

configuration_parser.add_section('Keys')
configuration_parser.set('Keys', 'rtm_api_key', None)
configuration_parser.set('Keys', 'rtm_shared_secret', None)
configuration_parser.set('Keys', 'rtm_token', None)

if 'HOME' in environ:
  HOME = environ['HOME']
elif 'USERPROFILE' in environ:
  HOME = environ['USERPROFILE']
else:
  print >>stderr, 'Unable to determine home directory; setting defaults'

configuration_file = join(HOME, '.config', 'rtmcurses.conf')
if isfile(configuration_file):
  with open(configuration_file, 'rU') as f:
    configuration_parser.readfp(f)
else:
  print >>stderr, 'No such file: %s Setting defaults' % configuration_file


for key, value in configuration_parser.items('Display'):
  globals()[key] = int(value)
for key, value in configuration_parser.items('Keys'):
  globals()[key] = value
