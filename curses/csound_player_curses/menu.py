import glob, sys, os, atexit, signal
from cursesmenu import *
from cursesmenu.items import *
import curses

from csound_player_curses.player import CsdPlayer

class TogglePlayer:
  def __init__(self):
    self.toggles = {}
    self.player = get_csd_player()

  def play(self, file_name):
    if file_name in self.toggles:
      self.toggles[file_name] = not(self.toggles[file_name])
    else:
      self.toggles[file_name] = True

    if self.toggles[file_name]:
      self.player.add(file_name, file_name)
    else:
      self.player.stop(file_name)

class MultiPlayer:
  def __init__(self):
    self.player = get_csd_player()

  def play(self, file_name):
    self.player.add(file_name, file_name)

class SinglePlayer:
  def __init__(self):
    self.player = get_csd_player()

  def play(self, file_name):
    self.player.add('csd', file_name)

def get_player(config):
  if config.is_multi:
    if config.is_toggle:
      return TogglePlayer()
    else:
      return MultiPlayer()
  else:
    return SinglePlayer()

def get_track_names(path):
  return glob.glob(os.path.join(path, '*.csd'))

def strip_name(file_name):
  return os.path.splitext(os.path.basename(file_name))[0]

def to_menu(player, file_name):
  return FunctionItem(strip_name(file_name),
    lambda x: player.play(x),
    [file_name])

def get_track_menu(player, path):
  title = os.path.basename(path)
  submenu = CursesMenu('csound-player', title)
  for file_name in get_track_names(path):
    submenu.append_item(to_menu(player, file_name))
  return submenu

def get_csd_player():
  player = CsdPlayer()

  def on_exit():
    player.close()

  def sigint_handler(signal, frame):
    player.close()

  atexit.register(on_exit)
  signal.signal(signal.SIGINT, sigint_handler)
  return player

def get_args():
  return sys.argv[1]

def main(config):
  player = get_player(config)
  menu = get_track_menu(player, config.path)
  stdscr = curses.initscr()
  curses.start_color()
  curses.use_default_colors()
  menu.show()
