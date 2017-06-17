from setuptools import setup, find_packages

setup(name='csound-player-curses',
      version='0.1',
      description='Csound player in the terminal',
      url='https://github.com/anton-k/csound-player/curses',
      author='Anton Kholomiov',
      author_email='anton.kholomiov@gmail.com',
      license='BSD3',
      install_requires=[
          'curses-menu', 'argparse'
      ],
      entry_points = {
        'console_scripts': ['csound-player-curses=csound_player_curses.main:main'],
        },
      packages=find_packages(),
      zip_safe=False)
