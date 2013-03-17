#!/usr/bin/python
# -*- coding: utf-8 -*-

#search-desktop.py

import wx
class Display(wx.Frame):
    def __init__(self, parent, title):
        super(Display, self).__init__(parent, title=title, size=(450, 450))
        
        self.InitUI()
        self.Show()
    
    def InitUI(self):
        
        menubar = wx.MenuBar()
        # set File menu, Quit item here.
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        # set Help menu, About item here.
        helpMenu = wx.Menu()
        hitem = helpMenu.Append(wx.ID_ABOUT, 'About', 'About Information')
        menubar.Append(helpMenu, '&About')
        self.Bind(wx.EVT_MENU, self.OnHelp, hitem)
        
        self.SetMenuBar(menubar)    #add menubar to frame.
        
        panel = wx.Panel(self)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # query fields selection.
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, label='KeyWords')
        cb1.SetFont(font)
        cb1.SetValue(True)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, label='Author Name')
        cb2.SetFont(font)
        hbox4.Add(cb2, flag=wx.LEFT, border=15)
        cb3 = wx.CheckBox(panel, label='Journal Name')
        cb3.SetFont(font)
        hbox4.Add(cb3, flag=wx.LEFT, border=15)
        vbox.Add(hbox4, flag=wx.LEFT|wx.TOP, border=8)
        vbox.Add((-1, 10))          
        
        # source selection
        srcSelect = wx.BoxSizer(wx.HORIZONTAL)
        srcText = wx.StaticText(panel, label='Source ')
        srcText.SetFont(font)
        srcSelect.Add(srcText, flag=wx.RIGHT, border=28)
        srcPath = wx.ComboBox(panel)
        srcSelect.Add(srcPath, proportion=1)
        srcFile = wx.Button(panel, label="Browse...")
        srcSelect.Add(srcFile, proportion=0.5)
        vbox.Add(srcSelect, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)
#        vbox.Add((-1, 10))
        
        # destination selection
        destSelect = wx.BoxSizer(wx.HORIZONTAL)
        destText = wx.StaticText(panel, label='Destination ')
        destText.SetFont(font)
        destSelect.Add(destText, flag=wx.RIGHT, border=0)
        destPath = wx.ComboBox(panel)
        destSelect.Add(destPath, proportion=1)
        destFile = wx.Button(panel, label="Browse...")
        destSelect.Add(destFile, proportion=0.5)
        vbox.Add(destSelect, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)        
        vbox.Add((-1, 10))    
        
        # manual input query terms.
        manual_query = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Manual Query:')
        st2.SetFont(font)
        manual_query.Add(st2)
        vbox.Add(manual_query, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add((-1, 10))
        
        # input textual area.
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
            border=10)
        vbox.Add((-1, 25))
        
        # OK and Close button.
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 25))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 25))
        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)
        
        
    def OnQuit(self):
        self.close()
        
    def OnHelp(self):
        print "Kylin Search"
        
if __name__ == '__main__':
  
    app = wx.App()
    Display(None, title="Kylin Search")
    app.MainLoop()