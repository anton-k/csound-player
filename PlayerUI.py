import wx
import os.path
import config
from Player import Player, readFiles

def addStar(x):
    name = x.GetLabel()
    x.SetLabel("* " + name)

def rmStar(x):
    name = x.GetLabel()
    x.SetLabel(name[2:])

class PlayerUI:
    def __init__(self, sizer, mainSizer, panel, btn):
        self.sizer = sizer
        self.mainSizer = mainSizer
        self.panel = panel
        self.player = Player([])
        self.toggleButton = btn

    def toggle(self):
        if self.player.isOn():
            self.stop()
        else:
            self.play()

    def play(self):
        self.toggleButton.SetLabel(config.stopSign)
        self.player.play()


    def stop(self):
        self.toggleButton.SetLabel(config.playSign)
        self.player.stop()

    def next(self):
        self.unHighlightTrack()
        self.player.next()
        self.highlightTrack()

    def prev(self):
        self.unHighlightTrack()
        self.player.prev()
        self.highlightTrack()

    def goTo(self, n):
        self.unHighlightTrack()
        self.player.goTo(n)
        self.highlightTrack()

    def quit(self):
        self.player.quit()

    def loadFiles(self, wnd, directory):
        files = readFiles(directory)

        self.player.stop()
        self.player = Player(files)

        def onItemClick(i):
            def res(e):
                if not(i == self.player.currentTrack and self.isOn()):
                    self.unHighlightTrack()
                    self.player.goTo(i)
                    self.highlightTrack()
            return res

        def onItemDoubleClick(i):
            n = i
            def res(e):
                if i == self.player.currentTrack and self.isOn():
                    self.stop()
                else:
                    onItemClick(n)(e)
                    self.play()
            return res

        self.sizer.Clear(deleteWindows = True)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(config.fontSize)

        for ind, x in enumerate(files):
            item = wx.StaticText(self.panel, label = x.basename())
            item.Bind(wx.EVT_LEFT_DOWN, onItemClick(ind))
            item.Bind(wx.EVT_LEFT_DCLICK, onItemDoubleClick(ind))
            item.SetSize(wx.Size(200, 80))
            item.SetFont(font)
            self.sizer.Add(item, 0, wx.ALL|wx.EXPAND, 5)

        self.highlightTrack()
        self.updateLayout(wnd)

    def updateLayout(self, wnd):
        self.sizer.Layout()
        self.mainSizer.Layout()
        self.mainSizer.Fit(wnd)

    def unHighlightTrack(self):
        color = config.offColor
        n = self.player.getCurrentTrack()
        item = self.sizer.GetItem(n)
        if not(item is None) and item.IsWindow():
            item.GetWindow().SetForegroundColour(color)
            rmStar(item.GetWindow())
            item.GetWindow().SetWindowStyle(wx.ALIGN_LEFT)

    def highlightTrack(self):
        color = config.onColor
        n = self.player.getCurrentTrack()
        item = self.sizer.GetItem(n)
        if not(item is None) and item.IsWindow():
            item.GetWindow().SetForegroundColour(color)
            addStar(item.GetWindow())
            item.GetWindow().SetWindowStyle(wx.ALIGN_RIGHT)

    def isOn(self):
        return self.player.isOn()

    def isOff(self):
        return self.player.isOff()