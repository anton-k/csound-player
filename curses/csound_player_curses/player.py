import  subprocess, os

_FNULL = open(os.devnull, 'w')

class Proc:
  def __init__(self, args):
    self.proc = subprocess.Popen(args, stdout=_FNULL, stderr=subprocess.STDOUT)

  def stop(self):
    self.proc.kill()

class Player:
  def __init__(self):
    self.procs = {}

  def add(self, name, cmd):
    self.stop(name)
    self.procs[name] = Proc(cmd)

  def stop(self, name):
    if name in self.procs:
      p_old = self.procs[name]
      p_old.stop()
      del self.procs[name]

  def close(self):
    for name in self.procs.keys():
      self.stop(name)

class CsdPlayer:
  def __init__(self):
    self.player = Player()

  def add(self, name, file_name):
    self.player.add(name, ['csound', file_name])

  def stop(self, name):
    self.player.stop(name)

  def close(self):
    self.player.close()
