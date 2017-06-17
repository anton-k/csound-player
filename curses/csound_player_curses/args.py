import argparse, sys, os

class Config:
  def __init__(self, path, is_multi, is_toggle):
    self.path = path
    self.is_multi = is_multi
    self.is_toggle = is_toggle

class HelperArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def fail_with(error_message):
    print('ERROR: ' + error_message)
    sys.exit(1)

def check_dir(path):
  if not(os.path.isdir(path)):
    fail_with("No directory at %s" % path)

def get_config():
  parser = HelperArgumentParser(description =
    'csound-player-curses - an utility to play csd files from the terminal')

  parser.add_argument("path", help="path to csd-files", type=str)
  parser.add_argument("--multi", help="set multichoice", action="store_true")
  parser.add_argument("--toggle", help="set toggle playback", action="store_true")
  args = parser.parse_args()
  check_dir(args.path)
  return Config(args.path, args.multi, args.toggle)
