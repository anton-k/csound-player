# csound-player
Desktop media player for Csound files

## Installation

To test just cd in the project and invoke `python`

````
> git clone https://github.com/anton-k/csound-player.git
> cd csound-player
> python main.py
```


Player requires `python-2.x`, `wxPython` and `python-csound` to be installed.
On Ubuntu/Debian it can be installed:

~~~
> sudo apt-get install python python-csound python-wxgtk2.8
~~~

## Usage

Right now player can do pretty basic stuff. It can load all csd or orc/sco files
in the given directory and play them on demand.

It's very basic but usefull. 

### Shorcuts

* Press arrow keys to step through the list of files. 

* Press `Space` to toggle play/stop.

* Press numbers to quickly switch between first ten tracks in the list.

### Designed for concerts

It's designed to be used on concerts, to create set of songs for performance. 
Also it can be used to create predefined synths for someone who doesn't know Csound.

Note that several instances can be launched at the same time.
You can use one playlist for midi instruments, another one for beats
and aybe another one for drones.

### todo

* add scrollers

* add preference items:

    * fonts
    
    * colors
    
* add resume playback. When one file stops continue to play the next one

* add installer (no need for python and friends to run)

-------------------------------------------------------

Happy Csounding!
Suggestions and patches are welcome!



