# ⚡ DC-DC Converter Designer

Design, simulate, and validate **power converters** without the headache of manual spreadsheet iterations. This interactive tool bridges the gap between theoretical circuit design and real-world hardware validation — so you can focus on insights, not formulas.

Made with ⚙️ by **Raymond Borres™**

---

## 🌟 Why I Built This

Let’s be honest — calculating inductor ripple, checking core saturation, and verifying switching stresses usually means juggling multiple datasheets, obscure calculator tabs, and that overgrown Excel file from last semester.

I built this app to **centralize** that entire workflow. You can adjust converter parameters on the fly and instantly visualize the impact on magnetic flux density (\(B_{max}\)), inductor current, switching waveforms, and output regulation. It's designed to make **power converter design intuitive and visual** — the way it should be.

---

## 🚀 Key Features

* **⚙️ Dual Topology Support**
  * Fully interactive design environments for both **Buck** and **Boost** converters.

* **🧲 Magnetic Design Suite**
  * Compute required turns (\(N\)) and air gap lengths automatically.
  * Built-in **saturation check** evaluates \(B_{max}\) in real time to ensure your core stays within the linear region.

* **📊 Interactive Simulation**
  * **High-resolution Plotly charts** visualize:
    * Inductor Current (\(I_L\))
    * Output Voltage (\(V_{out}\))
    * Switching Node Waveforms (\(V_{ds}\), \(V_{gs}\))
  * See parameter sensitivity instantly — adjust switching frequency or load via sliders and watch the waveform evolve in real time.

* **🔄 Real-Time Feedback**
  * No need to rerun code manually. Every parameter update recalculates flux, current, voltage, and ripple values on the spot.

---

## 🛠️ Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.x** | Core computation and interface logic |
| **Streamlit** | Interactive and reactive web front-end |
| **Plotly** | Beautiful, dynamic power electronics graphs |
| **NumPy** | Fast numerical simulation and waveform math |

---

## 📥 Quick Start

### 1️⃣ Install Dependencies
  Run this in your terminal to set up your environment:
    ```bash
    pip install streamlit numpy plotly
### 2️⃣ Launch the App
    Navigate to the project directory and start your local Streamlit server:
    ```bash
    streamlit run app.py

## 📖 How to Use It
  1. Set Your Targets:
  In the sidebar, enter V_in, V_out, Power, and switching frequency (f_sw).

  2. Pick Your Core:
  Choose from the material library or input your own custom core parameters: 
  A_e, L_e, μ_r.

  3. Validate:
  Check the “Saturation Check” indicator — if your B_max exceeds the core’s linear range, the tool will advise you to increase L or select a different core.

  4. Analyze:
  Explore interactive plots for waveforms, ripple characteristics, and transient behaviour across different load and switching conditions.

## 🎓 Educational Value
Perfect for students, researchers, and engineers learning or teaching Power Electronics.

### Use it to explore:

1. The inverse relationship between Inductance (L) and ripple current.

2. How switching frequency (f_sw) alters converter efficiency and current stress.

3. The trade-off between core size and energy storage.

4. The distinct waveform behaviors across Buck vs. Boost topologies.

## 📜 License
Distributed under the MIT License.
See the LICENSE file for details.

Built with ⚡ and passion by Raymond Borres™
