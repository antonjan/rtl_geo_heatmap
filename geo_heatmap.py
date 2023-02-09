#!/usr/bin/env python
"""
Hello World, but with more meat.
"""

import wx
import wx.html

class MainFrame(wx.Frame):
    """
    Main frame
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Heatmap Recording!")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)
        
        # adding html viewer
        html = wx.html.HtmlWindow(self) 
        if "gtk2" in wx.PlatformInfo: 
            html.SetStandardFonts()
        
        # Alternatively render raw HTML with the SetPage method
        # html.SetPage("<h4>Hello World</h4>") 
        # Render a local HTML file
        html.LoadPage("folium_map.html") 

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)
        
        newItem = fileMenu.Append(-1, "&New...\tCtrl-N", "Creating a New recording file")
        saveItem = fileMenu.Append(-1, "&Save...\tCtrl-S","Saving recorded file")
        openItem = fileMenu.Append(-1, "&Open...\tCtrl-O", "Open exsiting recording")       
        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnNew, newItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample","About Hello World 2", wx.OK|wx.ICON_INFORMATION)
        
    def OnNew(self, event):
        """New file dialog box."""
        wx.MessageBox("New file dialog box")
      
    def OnSave(self, event):
        """Save file dialog box."""
        wx.MessageBox("Save file dialog box")
        
    def OnOpen(self, event):
        """Open file dialog box."""
        wx.MessageBox("Open file dialog box")
        
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='Geo Heatmap recorder')
#    frm = MyHtmlFrame(None, "Simple HTML File Viewer")  
    frm.Show()
    app.MainLoop()
