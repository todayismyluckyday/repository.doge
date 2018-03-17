# -*- coding: utf-8 -*-

import xbmcgui

class DialogInfo:

    def __init__(self):
        self.dlg = xbmcgui.Dialog()
        self.head = 'Cerebro IPTV (Sports Devil)'

    def show(self, message):

        #self.dlg.close()
        dp = xbmcgui.DialogProgress()
        dp.create("[COLOR=gold][B]Cerebro IPTV Hunter[/COLOR][/B]","This can take 2-45 seconds.(based on host & your device/speed)","It may look like its frozen its not, it's opening the stream... ","Please Wait!!!!")
        if dp: dp.close()
        self.dlg.ok(self.head, "Stream Down")