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
//
Usage
1. Design Specs: Set Vin, Vout, power, frequency, ripple targets

2. Core Selection: Pick material or custom parameters

3. View Results: Electrical + magnetic design parameters

4. Simulate: Toggle waveforms to see transient behavior
//
Educational Value
1. Perfect for power electronics classes:
Visualize inductor current ripple vs saturation
See flux density vs core limits
Understand Buck vs Boost waveforms
Real-time design iteration
//
Tech Stack
1. Python + Streamlit

2. Plotly for interactive charts

3. NumPy for calculations

License
MIT License - see LICENSE © 2026
