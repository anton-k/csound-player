#!/usr/bin/python
import config
import wx
from wx.lib.scrolledpanel import ScrolledPanel
import glob

from PlayerUI import PlayerUI

class St:
    def __init__(self):
        self.cfg = wx.Config('myconfig')

    def setPlayer(self, sizer, mainSizer, panel, btn):
        self.player = PlayerUI(sizer, mainSizer, panel, btn)

    def getPlayer(self):
        return self.player

    def getLastDir(self):
        return unicode(self.cfg.Read('last_dir', ''))
        
    def setLastDir(self, path):
        self.cfg.Write('last_dir', str(path))


def menuItem(wnd, menu, id, title, msg, action, font):
    item = wx.MenuItem(menu, id, title, msg)
    item.SetFont(font)
    menu.AppendItem(item)
    wnd.Bind(wx.EVT_MENU, action, item)

def boxSizer(orient, xs):
    b = wx.BoxSizer(orient)
    for x in xs:
        b.Add(x, 1, wx.EXPAND)
    return b

def horSizer(xs):
    return boxSizer(wx.HORIZONTAL, xs)

def verSizer(xs):
    return boxSizer(wx.VERTICAL, xs)

def setAccelerators(wnd, st):
    def onLeftUp(e):
        st.getPlayer().prev()

    def onRightDown(e):
        st.getPlayer().next()

    def onToggle(e):
        st.getPlayer().toggle()

    def onNum(i):
        def res(e):            
            st.getPlayer().goTo(i)
        return res

    leftUpId = wx.NewId()
    rightDownId = wx.NewId()
    togglePlayId = wx.NewId()

    wnd.Bind(wx.EVT_MENU, onLeftUp,     id = leftUpId)
    wnd.Bind(wx.EVT_MENU, onRightDown,  id = rightDownId)
    wnd.Bind(wx.EVT_MENU, onToggle,     id = togglePlayId)

    goId = []
    for i in range(10):
        goId.append(wx.NewId())
        wnd.Bind(wx.EVT_MENU, onNum(i),     id = goId[i])

    def key(code, idx):
        return (wx.ACCEL_NORMAL, code, idx)

    numKeys = []
    for i in range(10):
        numKeys.append(key(ord(str((i+1) % 10)), goId[i]))

    accelTbl = wx.AcceleratorTable(
        [ key(wx.WXK_LEFT,  leftUpId)
        , key(wx.WXK_UP,    leftUpId)
        , key(wx.WXK_RIGHT, rightDownId)
        , key(wx.WXK_DOWN,  rightDownId)
        , key(wx.WXK_SPACE, togglePlayId)] + numKeys)

    wnd.SetAcceleratorTable(accelTbl)

def initMenu(wnd, st):
    def onQuit(e):
        wnd.Close()

    def onLoad(e):
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON, defaultPath = st.getLastDir())
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath() 
            st.setLastDir(path)
            st.getPlayer().loadFiles(wnd, path)
        dialog.Destroy()

    def onPreferences(e):
        pass

    def onAbout(e):    
        description = """Csound Player is a simple player for Csound files.
It can play csd and sco/orc files. It loads all files in the given directory
and creates a playlist out of csound files.
"""

        licence = """Csound Player is free software; you can redistribute 
it and/or modify it under the terms of the BSD License."""

        info = wx.AboutDialogInfo()

        info.SetName('Csound Player')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2015 Anton Kholomiov')
        info.SetWebSite('http://github.com/anton-k')
        info.SetLicence(licence)
        info.AddDeveloper('Anton Kholomiov')
        info.AddDocWriter('Anton Kholomiov')
        info.AddArtist('The Math Art')
        info.AddTranslator('Anton Kholomiov')

        wx.AboutBox(info)


    font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
    font.SetPointSize(config.fontSize)

    menubar = wx.MenuBar()
    loadMenu = wx.Menu()
    menubar.SetFont(font)
    menubar.Append(loadMenu, '&File')
    wnd.SetMenuBar(menubar)

    menuItem(wnd, loadMenu, wx.ID_ANY, '&Load', 'Load files', onLoad, font)    
    menuItem(wnd, loadMenu, wx.ID_ANY, '&Preferences', 'Settings', onPreferences, font)        
    menuItem(wnd, loadMenu, wx.ID_EXIT, '&Quit', 'Quit application', onQuit, font)   

    aboutMenu = wx.Menu()
    menubar.Append(aboutMenu, '&Help') 
    menuItem(wnd, aboutMenu, wx.ID_ANY, '&About', 'About', onAbout, font)   

    setAccelerators(wnd, st)
    
def initButtons(wnd, st):
    font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
    font.SetPointSize(config.fontSize)

    def button(x):
        name = x[0]
        clbk = x[1]
        btn = wx.Button(wnd, label = name)
        btn.Bind(wx.EVT_BUTTON, clbk)
        btn.SetForegroundColour(config.onColor)       
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        btn.SetFont(font)
        return btn

    def onPlay(e):
        st.getPlayer().toggle()

    def onPrev(e):
        st.getPlayer().prev()

    def onNext(e):
        st.getPlayer().next()

    box = horSizer(map(button, [(config.playSign, onPlay), (config.prevSign, onPrev), (config.nextSign, onNext)]))    
    return box

def initItems(wnd, st):        
    return verSizer([])        

def initMainSizer(wnd, st, btns, items):
    sizer = wx.BoxSizer(wx.VERTICAL)    
    sizer.Add(btns, 0, wx.EXPAND)
    sizer.AddSpacer(10)

    panel = wx.Panel(wnd, -1)     
    panel.SetBackgroundColour(config.bkgColor)
    panel.SetSizer(items)

    setShortCuts(panel, st)

    sizer.Add(panel, 0, wx.EXPAND)  
    toggleButton = btns.GetItem(0).GetWindow()  
    st.setPlayer(items, sizer, panel, toggleButton)
    wnd.SetSizer(sizer)

def initContent(wnd, st):
    initMainSizer(wnd, st,
        initButtons(wnd, st),
        initItems(wnd, st))

def initExit(wnd, st):
    def onExit(e):
        st.getPlayer().quit()
        wnd.Destroy()        

    wnd.Bind(wx.EVT_CLOSE, onExit) 

def initUI(wnd, st):    
    initMenu(wnd, st)
    initContent(wnd, st)   
    initExit(wnd, st)
    

def keyNum(keycode, st):
    if keycode == ord('1'):
        st.getPlayer().goTo(0)
    elif keycode == ord('2'):
        st.getPlayer().goTo(1)
    elif keycode == ord('3'):
        st.getPlayer().goTo(2)
    elif keycode == ord('4'):
        st.getPlayer().goTo(3)
    elif keycode == ord('5'):
        st.getPlayer().goTo(4)
    elif keycode == ord('6'):
        st.getPlayer().goTo(5)
    elif keycode == ord('7'):
        st.getPlayer().goTo(6)
    elif keycode == ord('8'):
        st.getPlayer().goTo(7)
    elif keycode == ord('9'):
        st.getPlayer().goTo(8)
    elif keycode == ord('0'):
        st.getPlayer().goTo(9)
    else:
        pass

def setShortCuts(wnd, st):
    def onKeyPress(event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_LEFT or keycode == wx.WXK_UP:
            st.getPlayer().prev()
        elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_DOWN:
            st.getPlayer().next()
        elif keycode == wx.WXK_SPACE:
            st.getPlayer().toggle()
        else:            
            keyNum(keycode, st)

    wnd.Bind(wx.EVT_KEY_DOWN, onKeyPress)
    wnd.SetFocus()


def main():
    app = wx.App()
    wnd = wx.Frame(None, wx.ID_ANY, "Csound Player", size=(450, 90), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
    st = St()
    initUI(wnd, st)

    lastDir = st.getLastDir()
    if lastDir != '':
        st.getPlayer().loadFiles(wnd, lastDir)

    wnd.Centre()
    wnd.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()