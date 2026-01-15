# DC-DC Converter Designer

Interactive **Power Electronics** design tool built with **Streamlit** + **Plotly**.

## Features

- **Topology Calculator**: Buck & Boost converters
- **Magnetic Design**: Turns (N), air gap, flux density gauge, saturation check
- **Transient Simulation**: Inductor current, output current, voltages (Vds/Vgs/Vin/Vout)
- **Real-time**: Change specs → see waveforms + metrics update instantly

## Quick Start

pip install streamlit numpy plotly
streamlit run app.py

Usage
Design Specs: Set Vin, Vout, power, frequency, ripple targets

Core Selection: Pick material or custom parameters

View Results: Electrical + magnetic design parameters

Simulate: Toggle waveforms to see transient behavior

Educational Value
Perfect for power electronics classes:

Visualize inductor current ripple vs saturation

See flux density vs core limits

Understand Buck vs Boost waveforms

Real-time design iteration

Tech Stack
Python + Streamlit

Plotly for interactive charts

NumPy for calculations

License
MIT License - see LICENSE © 2026
