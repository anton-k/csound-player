import unicodedata
import os.path
import csnd6
from glob import glob


def stripExt(x):
    return (os.path.splitext(x))[0]

class CsdFile:
    def __init__(self, x):
        if isinstance(x, basestring):
            self.csd = x
            self.isCsd = True
        elif isinstance(x, tuple):
            self.orc = x[0]
            self.sco = x[1]
            self.isCsd = False
        else:
            pass

    def loadToEngine(self, engine):
        if self.isCsd:
            engine.Compile(unicode2string(self.csd))
            engine.Start()
        else:
            engine.SetOption("-odac")
            engine.SetOption("-d")
            orc = open(self.orc, 'r')
            sco = open(self.sco, 'r')
            engine.CompileOrc(orc.read())
            engine.ReadScore(sco.read())
            orc.close()
            sco.close()
            engine.Start()

    def __str__(self):
        if self.isCsd:
            return self.csd
        else:
            return self.orc + "/sco"

    def __repr__(self):
        return str(self)

    def basename(self):
        def nameOf(x):
            return os.path.basename(stripExt(x))

        if self.isCsd:
            return nameOf(self.csd)
        else:
            return nameOf(self.orc)

def unicode2string(x):
    return unicodedata.normalize('NFKD', x).encode('ascii','ignore')

def readFiles(directory):
    def byExt(d, ext):
        return sorted(glob(d + "/*." + ext))

    def groupOrcAndSco(x, y):
        x1 = map(stripExt, x)
        x2 = map(stripExt, y)
        common = list(set(x1).intersection(x2))
        return map(lambda a: CsdFile((a + ".orc", a + ".sco")), common)

    csds = byExt(directory, "csd")
    orcs = byExt(directory, "orc")
    scos = byExt(directory, "sco")

    return map(CsdFile, csds) + groupOrcAndSco(orcs, scos)

class Player:
    def __init__(self, files):
        self.files = files
        self.currentTrack = 0
        self.length = len(files)
        self.on = False
        self.engine = csnd6.Csound()

    def skipOnEmpty(fn):
        def res(*args):
            if (args[0].length == 0):
                return
            fn(*args)
        return res

    @skipOnEmpty
    def play(self):
        if not(self.on):
            self.on = True
            print ("Play " + str(self.currentTrack))
            self.files[self.currentTrack].loadToEngine(self.engine)
            try:
                self.audioThread = csnd6.CsoundPerformanceThread(self.engine)
                self.audioThread.Play()
            except:
                self.stop()


    @skipOnEmpty
    def stop(self):
        if (self.on):
            self.on = False
            print ("Stop " + str(self.currentTrack))
            self.audioThread.Stop()
            self.audioThread.Join()
            self.engine.Cleanup()
            self.engine.Reset()

    def quit(self):
        if (self.on):
            self.stop()

    def next(self):
        self.nextBy(1)

    def prev(self):
        self.nextBy(-1)

    def nextBy(self, n):
        self.goTo(self.currentTrack + n)

    @skipOnEmpty
    def goTo(self, n):
        def nextTrackId():
            self.currentTrack = (n) % self.length

        if (self.on):
            self.stop()
            nextTrackId()
            self.play()
        else:
            nextTrackId()

    def getCurrentTrack(self):
        return self.currentTrack

    def isOn(self):
        return self.on

    def isOff(self):
        return not(self.on)
