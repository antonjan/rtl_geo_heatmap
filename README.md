# rtl_geo_heatmap
This repository will have the code of an rf signal strenth mapping tool (using an RTL dongle and a GPS for recording.
The code is writin in Python3
# Project Status.
The project just started 8 Feb 2023
Not all the fucktionality is working yet.
# Screenshot![Alt text](images/gio_map.jpg?raw=true "Geo Heatmap")<br>

# Description of what this Application will do.
If you use and RTL-SDR donge and a USB GPS you can then connect this to a laptop with an external mobile antenna and the application will map the RF signel strenth of a transmitter on a map.
The Map will have hotspot overys of the signal strenth of the transmitter that you recored with this aplication.
The aplication logs the signal strent while you driving and will then overy the details on a map.
# Dependincy libraeries
    wxWidgets
    pandas
    folium
    pylab
    numpy
    rtlsdr
    sys
    
 # Environment
 Needs python 3.12<br>
    
    sudo apt install rtl-sdr librtlsdr-dev
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
    python3 -m venv geo/
    source geo/bin/activate
    pip install pyrtlsdr
    pip install setuptools==80.9.0


