#!/usr/bin/env python3
"""
Geo Heatmap Recorder - Python 3.12 compatible
"""

import serial
import wx
import webbrowser
import csv
import threading
from threading import Thread, Event
from queue import Queue
from time import sleep
import numpy as np
from rtlsdr import RtlSdr


# =========================
# Main GUI Frame
# =========================

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        pnl = wx.Panel(self)

        st = wx.StaticText(pnl, label="")
        font = st.GetFont()
        font.PointSize += 3
        font = font.Bold()
        st.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 50))
        pnl.SetSizer(sizer)

        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Geo Heatmap Recorder Ready")

    # =========================

    def makeMenuBar(self):

        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        newItem = fileMenu.Append(-1, "&New...\tCtrl-N")
        saveItem = fileMenu.Append(-1, "&Save...\tCtrl-S")
        openItem = fileMenu.Append(-1, "&Open...\tCtrl-O")

        startMenu = wx.Menu()
        startItem = startMenu.Append(-1, "&Start")
        stopItem = startMenu.Append(-1, "&Stop")

        mapMenu = wx.Menu()
        mapItem = mapMenu.Append(-1, "&Show Map")

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(startMenu, "Start/Stop")
        menuBar.Append(mapMenu, "Heatmap")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        # Bindings
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnNew, newItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnStart, startItem)
        self.Bind(wx.EVT_MENU, self.OnStop, stopItem)
        self.Bind(wx.EVT_MENU, self.OnMap, mapItem)

    # =========================

    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox("Hello from wxPython")

    def OnAbout(self, event):
        wx.MessageBox(
            "Geo Heatmap Recorder",
            "About",
            wx.OK | wx.ICON_INFORMATION,
        )

    def OnNew(self, event):
        wx.MessageBox("New file dialog")

    def OnSave(self, event):
        wx.MessageBox("Save file dialog")

    def OnOpen(self, event):
        wx.MessageBox("Open file dialog")

    def OnStart(self, event):
        self.worker = WorkerStreaming()
        self.worker.start()
        wx.MessageBox("Recording started")

    def OnStop(self, event):
        if hasattr(self, "worker"):
            self.worker.stop()
        wx.MessageBox("Recording stopped")

    def OnMap(self, event):
        webbrowser.open("folium_map.html", new=2)
        wx.MessageBox("Opened map in browser")


# =========================
# Worker Thread
# =========================

class WorkerStreaming(Thread):

    def __init__(self):
        super().__init__()
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    @staticmethod
    def get_rf_signal():
        try:
            sdr = RtlSdr()
            sdr.sample_rate = 2.048e6
            sdr.center_freq = 70e6
            sdr.freq_correction = 60
            sdr.gain = 'auto'

            samples = sdr.read_samples(256 * 1024)
            sdr.close()

            return 10 * np.log10(np.var(samples))

        except Exception:
            print("RTL-SDR not available")
            return None

    @staticmethod
    def decode(coord):
        head, tail = coord.split(".")
        deg = head[:-2]
        minutes = head[-2:]
        return f"{deg} deg {minutes}.{tail} min"

    def run(self):

        print("Starting GPS read")
        port = "/dev/ttyACM0"

        try:
            ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        except Exception:
            print("GPS not available")
            return

        loop = 0
        interval = 10

        while not self._stop_event.is_set():

            data = ser.readline()

            if data.startswith(b"$GPRMC"):

                parts = data.decode("utf-8").split(",")

                if parts[2] == "V":
                    print("No satellite data")
                    continue

                time_str = f"{parts[1][0:2]}:{parts[1][2:4]}:{parts[1][4:6]}"
                lat = self.decode(parts[3])
                dirLat = parts[4]
                lon = self.decode(parts[5])
                dirLon = parts[6]
                speed = parts[7]
                trCourse = parts[8]
                date = f"{parts[9][0:2]}/{parts[9][2:4]}/{parts[9][4:6]}"

                if loop >= interval:

                    rfPower = self.get_rf_signal()

                    try:
                        with open("geo_rf.csv", "a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow([
                                time_str, lat, dirLat,
                                lon, dirLon, speed,
                                trCourse, date, rfPower
                            ])
                    except Exception:
                        print("Cannot write to file")

                    print("Logged RF power:", rfPower)
                    loop = 0

                loop += 1

        ser.close()


# =========================
# Main Entry
# =========================

if __name__ == "__main__":

    app = wx.App()
    frm = MainFrame(None, title="Geo Heatmap Recorder")
    frm.Show()
    app.MainLoop()

