#!/usr/bin/env python
"""
Hello World, but with more meat.
"""

import wx
import wx.html
import webbrowser
from rtlsdr import *
from numpy import *
import time
from pylab import *

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
        st = wx.StaticText(pnl, label="")
        font = st.GetFont()
        font.PointSize += 3
        font = font.Bold()
        st.SetFont(font)
        
        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 50))
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
        
        # Strat and Stop recording meny
        startMenu = wx.Menu()
        startstopMenu = wx.Menu()
        startItem = startMenu.Append(-1, "&Start...\tCtrl-N", "Start Recording RF signal strenth")
        stopItem = startMenu.Append(-1, "&Stop...\tCtrl-N", "Stop Recording RF signal strenth")
        
        #Map menu
        mapMenu = wx.Menu()
        mapItem = mapMenu.Append(-1, "&Show Map...\tCtrl-N", "Display the Heatmap")     
        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(startMenu,"Start/Stop")
        menuBar.Append(mapMenu,"Heatmap")
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
        self.Bind(wx.EVT_MENU, self.OnStart, startItem)
        self.Bind(wx.EVT_MENU, self.OnStop, stopItem)
        self.Bind(wx.EVT_MENU, self.OnMap, mapItem)

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
        
    def OnStart(self, event):
        """Start recording rtl power measurmrnts."""
#       sdr.read_samples_async(power_meter_callback)
        sdr = RtlSdr()

        # configure device
        sdr.sample_rate = 2.048e6  # Hz
        sdr.center_freq = 70e6     # Hz
        sdr.freq_correction = 60   # PPM
        sdr.gain = 'auto'
        samples = sdr.read_samples(256*1024)
        self.lblname = wx.StaticText(self, label='relative power: %0.1f dB' % (10*log10(var(samples))), pos=(20,60))
#        self.editname = wx.TextCtrl(self, value="Enter here your name", pos=(150, 60), size=(140,-1))
        sdr.close()

        # use matplotlib to estimate and plot the PSD
#        psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
#        xlabel('Frequency (MHz)')
#        ylabel('Relative power (dB)')
#
#        show()

        print(samples)
        print ('relative power: %0.1f dB' % (10*log10(var(samples))))
        
    def OnStop(self, event):
        """Stop recording rtl power measurmrnts."""
        sdr.read_samples_async()
#       wx.MessageBox("Stop recording rtl Power Measurements")            
        
    def OnMap(self, event):
        """Open Map in browser."""
        new = 2 # open in a new tab, if possible

        # open a public URL, in this case, the webbrowser docs
        #url = "http://docs.python.org/library/webbrowser.html"
        #webbrowser.open(url,new=new)

        # open an HTML file on my own (Windows) computer
        #url = "file:///home/anton/rtl_geo_heatmap/folium_map.html"
        #webbrowser.open(url,new=new)

        # open an HTML file on my own (Windows) computer
        url = "folium_map.html"
        webbrowser.open(url,new=new)

        wx.MessageBox("Open Map in Browser")
        
         
        
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='Geo Heatmap recorder')
#    frm = MyHtmlFrame(None, "Simple HTML File Viewer")  
    frm.Show()
#    @limit_calls(9)
#    def power_meter_callback(samples, sdr):
#        print ('relative power: %0.1f dB' % (10*log10(var(samples))))
#        time.sleep(3)
#        wx.MessageBox("Start recording rtl Power Measurements")
   
#    sdr = RtlSdr()
#   sdr.sample_rate = 1.2e6
#    sdr.center_freq = 145.950e6
#    sdr.gain = 63
#    sdr.freq_correction = 60
    #sdr.gain = 'auto'
    #set_bandwidth
    #set_direct_sampling()
    #samples = sdr.read_samples(256*1024)
    #sdr.close()
    #set_direct_sampling
    
    app.MainLoop()
