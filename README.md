**⚡ DC-DC Converter Designer**

Design, simulate, and validate power converters without the headache of manual spreadsheet iterations. This tool is built to bridge the gap between theoretical power electronics and practical hardware design.

🌟 Why I Built This

Let’s be honest: calculating inductor ripple, checking core saturation, and verifying switching stresses usually involves jumping between three different datasheets and a messy Excel file.

I built this tool to centralize that workflow. It lets you tweak your specs on the fly and immediately see how your choices impact the magnetic flux density ($B_{max}$) and the electrical waveforms.

🚀 Key Features

Dual Topology Support: Fully interactive calculators for both Buck and Boost converters.

Magnetic Design Suite:

Calculate necessary Turns ($N$) and air gap lengths.

Saturation Check: Automatic flux density gauging to ensure your core remains in the linear region.

Interactive Simulation:

High-resolution Plotly waveforms for Inductor Current ($I_L$) and Output Voltage ($V_{out}$).

Switching node analysis including $V_{ds}$ and $V_{gs}$ visualization.

Real-time Updates: Adjust a slider for switching frequency or load and watch the waveforms update instantly.

🛠️ Tech Stack

Python 3.x

Streamlit: For the interactive, reactive web interface.

Plotly: For zoomable, high-fidelity power electronics charts.

NumPy: Powering the underlying physics and transient calculations.

📥 Quick Start

1. Install Dependencies

Run this in your terminal to get the environment ready:

pip install streamlit numpy plotly


2. Launch the App

Navigate to the project folder and start the local server:

streamlit run app.py


📖 How to Use It

Set Your Targets: Use the sidebar to input $V_{in}$, $V_{out}$, Power, and your desired switching frequency ($f_{sw}$).

Pick Your Core: Choose from a library of materials or enter custom parameters ($A_e, L_e, \mu_r$).

Validate: Keep an eye on the "Saturation Check" indicator. If your $B_{max}$ exceeds your core's limits, the tool will warn you to increase $L$ or pick a larger core.

Analyze: Scroll through the simulation results to inspect the transient behavior and steady-state ripple.

🎓 Educational Value

This is a great tool for Power Electronics students to visualize:

How Inductance ($L$) and Switching Frequency ($f_{sw}$) inversely affect current ripple.

The direct relationship between physical core size and energy storage.

The difference in switching stress between different converter topologies.

📜 License

Distributed under the MIT License.

Built with ⚡ by Raymond Borres :)
