#!/usr/bin/python
# -*- coding: utf-8 -*-

#search-desktop.py

import os
import wx
import xlwt
from searcher import Search

class Display(wx.Frame):
    
    def __init__(self, parent, title):
        super(Display, self).__init__(parent, title=title, size=(450, 450))
        
        self.FromFile = False
        # setting some global variables.
        self.srcPath = ''
        self.destPath = ''
        
        self.terms = ''
        self.srcPathComb = ''
        self.destPathComb = ''
        
        self.InitUI()
        self.Show()
    
    def InitUI(self):
        """ initialize the UI display of the main frame"""
        
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
        
        #query fields selection.
        sb = wx.StaticBox(panel, label="Query Fields")
        sb.SetFont(font)
        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        
        # set default keywords search.
        keywords_cb = wx.CheckBox(panel, label="Keywords")
        boxsizer.Add(keywords_cb, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=26)
        keywords_cb.SetValue(True)
        boxsizer.Add(wx.CheckBox(panel, label="Author Name"), flag=wx.CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, border=26)
        boxsizer.Add(wx.CheckBox(panel, label="Journal Name"), flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=26)        
        vbox.Add(boxsizer, flag=wx.LEFT|wx.TOP|wx.EXPAND, border=8)
        vbox.Add((-1, 10))
        
        # source selection
        srcSelect = wx.BoxSizer(wx.HORIZONTAL)
        srcText = wx.StaticText(panel, label='Source ')
        srcText.SetFont(font)
        srcSelect.Add(srcText, flag=wx.RIGHT, border=28)
        self.srcPathComb = wx.ComboBox(panel)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus, self.srcPathComb)
        srcSelect.Add(self.srcPathComb, proportion=1)
        srcFile = wx.Button(panel, label="Browse...")
        #bind the event should before the Boxsizer.
        self.Bind(wx.EVT_BUTTON, self.OnSrcFile, srcFile)
        srcSelect.Add(srcFile, proportion=0.5)
        vbox.Add(srcSelect, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=3)
        
        # destination selection
        destSelect = wx.BoxSizer(wx.HORIZONTAL)
        destText = wx.StaticText(panel, label='Destination ')
        destText.SetFont(font)
        destSelect.Add(destText, flag=wx.RIGHT, border=0)
        self.destPathComb = wx.ComboBox(panel)
        destSelect.Add(self.destPathComb, proportion=1)
        destFile = wx.Button(panel, label="Browse...")
        self.Bind(wx.EVT_BUTTON, self.OnDestFile, destFile)
        destSelect.Add(destFile, proportion=0.5)
        vbox.Add(destSelect, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=3)        
        vbox.Add((-1, 10))    
        
        # manual input query terms.
        manual_query = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Manual Query:')
        st2.SetFont(font)
        manual_query.Add(st2)
        vbox.Add(manual_query, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add((-1, 10))
        
        # input textual area.
        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.terms = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(self.terms, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
            border=10)
        vbox.Add((-1, 25))
        
        # OK and Close button.
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        search = wx.Button(panel, label='Search', size=(70, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSearch, search)
        hbox5.Add(search)
        
        close = wx.Button(panel, label='Close', size=(70, 25))
        self.Bind(wx.EVT_BUTTON, self.OnQuit, close)
        hbox5.Add(close, flag=wx.LEFT|wx.BOTTOM, border=5)
        
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)
        
        
        
    def OnSrcFile(self, e):
        """ select source file terms to query """
        
        # setting the select from file flag to true.
        
        self.FromFile = True
        self.srcdirname = ''
        dlg = wx.FileDialog(self, "Choose Source Terms File", self.srcdirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.srcfilename = dlg.GetFilename()
            self.srcdirname = dlg.GetDirectory() + '/'
            self.srcPath = os.path.join(unicode(self.srcdirname), unicode(self.srcfilename))
            f = open(self.srcPath, 'r')
            self.terms.SetValue(f.read())
            self.srcPathComb.SetValue(self.srcPath)
            f.close()
        dlg.Destroy()
        
        
    def OnDestFile(self, e):
        """ select destination file to store the results"""
        
        self.destdirname = ''
        dlg = wx.FileDialog(self, "Choose Destination Path", self.destdirname, "", "*.*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.destfilename = dlg.GetFilename()
            self.destdirname = dlg.GetDirectory() + '/'
            self.destPath = os.path.join(self.destdirname, self.destfilename)
#            f = open(self.destPath, 'w')
#            f.write("Hello, I'am the query results")
            self.destPathComb.SetValue(self.destPath)
        dlg.Destroy()
        
    def OnSearch(self, e):
        """ main Whoosh search interface for search module """
        
        if not self.FromFile:
            try:
                f = open(self.srcPathComb.GetValue(), 'r')
                self.terms.SetValue(f.read())
            except IOError as e:
                dlg = wx.MessageDialog(self, e.strerror, "Source Path Error", wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return
                
        src_dir = self.srcPathComb.GetValue()
        dest_dir = self.destPathComb.GetValue()
        text = self.terms.GetValue()
        
        print "Now, invoke the search Module"
        
        # validation check for the src, dest and query terms.
        if not src_dir.strip() or not dest_dir.strip():
            dlg = wx.MessageDialog(self, "Please validate the source, destination not empty!", "Validation Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if text.strip():
            queries = text.splitlines()
            search = Search()
            
            # recursive create directory.
            destpath = self.destPathComb.GetValue()
            destdir = os.path.dirname(destpath)
            if not os.path.exists(destdir):
                os.makedirs(destdir)
                
#            f = open(destpath, 'w')
            # write the results to sheets.
            book = xlwt.Workbook()
            sh = book.add_sheet("Sorted Frequency") 
            ezxf = xlwt.easyxf
            heading_xf = ezxf('align: wrap on, vert centre, horiz center')            
            
            column = 0
            for query in queries:
                hits = search.search(query)
                kw_freq = search.fre_rank(hits)
                # write to the heading.
                sh.write(0, column, query, heading_xf)
                sh.write(0, column+1, str(len(kw_freq)), heading_xf)
                
                self.xls_write(sh, kw_freq, column)
                column += 2
            book.save(destpath)
                # text file write modular
#                for word, freq in kw_freq:
#                   f.write(word.encode("gbk") + "\t" + str(freq) + "\n")
#                f.write("------------------------------------------\n")
#                    
#            f.close()
            
        
    def xls_write(self, sh, kw_freq, column):
        """ write the list in column of excel """
        
        # setting the cell style, font, alignment etc.
        ezxf = xlwt.easyxf
        heading_xf = ezxf('align: wrap on, vert centre, horiz center')
        row = 1
        for word, freq in kw_freq:
            sh.write(row, column, word, heading_xf)
            sh.write(row, column+1, str(freq), heading_xf)
            row += 1
    
    def OnFocus(self, e):
        self.FromFile = False
        
    def OnQuit(self, e):
        self.Close(True)
        
    def OnHelp(self, e):
        """Show the help and version information about Kylin Search"""
                
        dlg = wx.MessageDialog(self, " Version 0.1 By Joseph Heng\n lengerfulluse@gmail.com\n Any feedback please let me know\n", "About Kylin Search", wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
if __name__ == '__main__':
  
    app = wx.App()
    Display(None, title="Kylin Search")
    app.MainLoop()