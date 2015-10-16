import wx
import random

colors = ['#159594', '#1A8CAB', '#8B1C55', '#FF1900', '#ED6639', wx.BLUE, '#005A31', '#DF3D82']
mainColor = random.choice(colors)

onColor = mainColor #'#FF9009'
offColor = wx.BLACK # '#118C4E'
bkgColor = wx.WHITE
fontSize = 12

playSign = "On"
stopSign = "||"
nextSign = ">>"
prevSign = "<<"
