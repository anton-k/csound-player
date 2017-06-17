csound-player-curses
-------------------------------

## Install

To install clone the repo with git. cd to the `csound-player/curses` directory
and install with pip python package manager (version 2).
Navigate to ap/ap-learn-lsa and invoke pip to install:

~~~
pip2 install . --user --upgrade
~~~

pip2 -- forces the code to be compiled with Python 2.x
It installs ap-learn system-wide.

## Usage

usage: csound-player-curses [-h] [--multi] [--toggle] path

csound-player-curses - an utility to play csd files from the terminal

positional arguments:
  path        path to csd-files

optional arguments:
  -h, --help  show this help message and exit
  --multi     set multichoice
  --toggle    set toggle playback
