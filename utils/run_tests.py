#!/usr/bin/python

"""Runs unit tests for application."""

import optparse
import os
import sys
import unittest2

USAGE = """%prog SDK_PATH

Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation. Default is /usr/local/google_appengine on Mac OS."""


def main(sdk_path):
  sys.path.insert(0, sdk_path)
  import dev_appserver
  dev_appserver.fix_sys_path()
  import google
  print dir(google)
  test_path = os.path.join(os.path.dirname(__file__), '..')
  suite = unittest2.loader.TestLoader().discover(test_path, pattern='*_test.py')
  unittest2.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  parser = optparse.OptionParser(USAGE)
  options, args = parser.parse_args()
  main(args[0])
