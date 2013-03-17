#!/usr/bin/python
# -*- coding: utf-8 -*-

# newclass.py

import wx

class Example(wx.Frame):

    def __init__(self, parent, title):    
        super(Example, self).__init__(parent, title=title, 
            size=(650, 450))

        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
      
        panel = wx.Panel(self)
        
        # vertical space and horizon space settings.
        sizer = wx.GridBagSizer(5, 5)
        # product trade logo.
        product_logo = wx.StaticText(panel, label="Welcome to Kylin Search\n")
        sizer.Add(product_logo, pos=(0, 0), span=(1,5),  flag=wx.TOP|wx.LEFT, border=10)
        # for segment line
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5), flag=wx.EXPAND|wx.BOTTOM, border=5)    #with GBSpan 1,5

        # for source file selection.
        src_text = wx.StaticText(panel, label="Source:")
        sizer.Add(src_text, pos=(2, 0), flag=wx.LEFT, border=10)

        src_select = wx.ComboBox(panel)
        sizer.Add(src_select, pos=(2, 1), span=(1, 3), 
                    flag=wx.EXPAND, border=0)        

        src_file = wx.Button(panel, label="Browse...")
        sizer.Add(src_file, pos=(2, 4), flag=wx.RIGHT, border=5)

        # for destination selection.
        dest_text = wx.StaticText(panel, label="Destination:")
        sizer.Add(dest_text, pos=(3, 0), flag=wx.LEFT, border=10)

        dest_select = wx.ComboBox(panel)
        sizer.Add(dest_select, pos=(3, 1), span=(1, 3), flag=wx.EXPAND, border=0)

        dest_file = wx.Button(panel, label="Browse...")
        sizer.Add(dest_file, pos=(3, 4), flag=wx.RIGHT, border=5)

        # query fields select.
        sb = wx.StaticBox(panel, label="Query Fields")

        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        
        # set default keywords search.
        keywords_cb = wx.CheckBox(panel, label="Keywords")
        boxsizer.Add(keywords_cb,
            flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=26)
        keywords_cb.SetValue(True)
        
        boxsizer.Add(wx.CheckBox(panel, label="Author Name"),
            flag=wx.CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, border=26)
        boxsizer.Add(wx.CheckBox(panel, label="Journal Name"),
            flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=26)
        sizer.Add(boxsizer, pos=(4, 1), span=(1, 3), 
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        # set growable space for column 3
        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)


if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="Create Java Class")
    app.MainLoop()