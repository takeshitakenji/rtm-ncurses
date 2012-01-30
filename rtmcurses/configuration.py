# Copyright (c) 2010 Manuel Vonthron <manuel.vonthron@acadis.org>
#
# Redistribution of this file is permitted under
# the terms of the BSD license

from os.path import join, isfile
from os import environ
from sys import stderr
from re import compile

supported_vars = frozenset([
  'history_size',
  'max_view_height',
  'rtm_api_key',
  'rtm_shared_secret',
  'rtm_token',
])

history_size=20
max_view_height=200

rtm_api_key = None
rtm_shared_secret = None
rtm_token = None

if 'HOME' in environ:
  HOME = environ['HOME']
elif 'USERPROFILE' in environ:
  HOME = environ['USERPROFILE']
else:
  print >>stderr, 'Unable to determine home directory; setting defaults'

configuration_file = join(HOME, '.rtmcurses.conf')
conf_regex = compile(r'^\s*(\S+)\s*=\s*(.*?)$')
if isfile(configuration_file):
  with open(configuration_file, 'rU') as f:
    for line in f:
      line = line.rstrip()
      if line and not line.startswith('#'):
        m = conf_regex.search(line)
        if m:
          if m.group(1) in supported_vars:
            value = m.group(2)
            if not value:
              value = None
            elif value.isdigit():
              value = int(value)
            globals()[m.group(1)] = value
        else:
          print >>stderr, 'Invalid syntax:', line
else:
  print >>stderr, 'No such file: %s Setting defaults' % configuration_file
