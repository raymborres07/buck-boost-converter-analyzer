import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Power Electronics Designer", page_icon="⚡", layout="wide")

st.title("⚡ DC-DC Converter Designer (Power Electronics Class)")
st.markdown("""
**Complete Design Suite:** Topology Calculation, Magnetic Core Design ($N$, Gap, Saturation), and Transient Simulation.
""")

# --- SIDEBAR: INPUT PARAMETERS ---
st.sidebar.header("1. Design Specs")

converter_type = st.sidebar.selectbox("Converter Topology", ["Buck (Step-Down)", "Boost (Step-Up)"])

# Voltage & Current
v_in = st.sidebar.number_input("Input Voltage (Vin)", value=12.0, min_value=1.0)
v_out = st.sidebar.number_input(
    "Target Output Voltage (Vo)",
    value=5.0 if converter_type == "Buck (Step-Down)" else 24.0,
    min_value=0.1,
)
p_target = st.sidebar.number_input(
    "Target Output Power (Po) [W]",
    value=20.0 if converter_type == "Buck (Step-Down)" else 5.0,
    min_value=0.1,
)

# Switching Specs
f_sw_khz = st.sidebar.slider("Switching Frequency (kHz)", 10, 500, 10)
f_sw = f_sw_khz * 1000

ripple_percent = st.sidebar.slider("Inductor Ripple (%)", 10, 50, 20)  # slightly smaller default
dv_percent = st.sidebar.slider("Output Voltage Ripple (%)", 0.1, 5.0, 0.5)
efficiency = st.sidebar.number_input(
    "Target Efficiency (%)", value=100.0, min_value=1.0, max_value=100.0
)
eta = efficiency / 100.0

# --- MAGNETIC CORE INPUTS ---
st.sidebar.markdown("---")
st.sidebar.header("2. Core Design")

# Core Database: Name -> {AL (nH), Bsat (T), Ae (mm^2)}
core_db = {
    "TDK PC40 (Datasheet)": {"AL": 1950.0, "Bsat": 0.39, "Ae": 120.0},
    "Generic Ferrite": {"AL": 1000.0, "Bsat": 0.35, "Ae": 80.0},
    "Kool Mu 60u": {"AL": 61.0, "Bsat": 1.05, "Ae": 100.0},
    "Custom": {"AL": 2000.0, "Bsat": 0.3, "Ae": 50.0},
}

selected_core = st.sidebar.selectbox("Select Core Material", list(core_db.keys()))
defaults = core_db[selected_core]

# Inputs with defaults based on selection
al_val_nh = st.sidebar.number_input("Core AL Value (nH/N²)", value=defaults["AL"])
b_sat_limit = st.sidebar.number_input("Core Saturation Flux (Bsat) [T]", value=defaults["Bsat"])
ae_val_mm2 = st.sidebar.number_input("Effective Area (Ae) [mm²]", value=defaults["Ae"])

# Simulation Limits
st.sidebar.markdown("---")
st.sidebar.header("3. Hardware Limits")
i_hard_sat = st.sidebar.number_input(
    "Inductor Saturation Current (A)",
    value=10.0,  # default ~10 A so IL ripple is visible
    help="Current clamps at this value in simulation.",
)
v_gate_drive = st.sidebar.number_input("Gate Drive Voltage (Vgs)", value=10.0)

# --- CALCULATIONS ---
valid_design = True
duty_cycle = 0.0
L_val = 0.0
C_val = 0.0
i_load = p_target / v_out

# Power Math
p_out = p_target
p_in = p_out / eta
p_loss = p_in - p_out

if converter_type == "Buck (Step-Down)":
    if v_out >= v_in:
        st.error("Error: For Buck, V_out must be < V_in.")
        valid_design = False
    else:
        duty_cycle = v_out / v_in
        i_L_avg = i_load
        delta_i_L = i_L_avg * (ripple_percent / 100.0)
        L_val = ((v_in - v_out) * duty_cycle) / (delta_i_L * f_sw)
        delta_v_out = v_out * (dv_percent / 100.0)
        C_val = delta_i_L / (8 * f_sw * delta_v_out)

elif converter_type == "Boost (Step-Up)":
    if v_out <= v_in:
        st.error("Error: For Boost, V_out must be > V_in.")
        valid_design = False
    else:
        duty_cycle = (v_out - v_in) / v_out
        i_in = p_in / v_in
        i_L_avg = i_in
        delta_i_L = i_L_avg * (ripple_percent / 100.0)
        L_val = (v_in * duty_cycle) / (delta_i_L * f_sw)
        delta_v_out = v_out * (dv_percent / 100.0)
        C_val = (i_load * duty_cycle) / (f_sw * delta_v_out)

# --- MAGNETIC MATH ---
if valid_design:
    # 1. Peak Current
    i_peak = i_L_avg + (delta_i_L / 2)

    # 2. Number of Turns: N = SQRT( L_nH / AL )
    L_nh = L_val * 1e9
    n_turns_calc = np.sqrt(L_nh / al_val_nh)
    n_turns = np.ceil(n_turns_calc)

    # 3. Energy: E = 0.5 * L * Ipk^2
    energy_stored = 0.5 * L_val * (i_peak**2)

    # 4. Air Gap (Derived from basic reluctance eq): lg = (mu_0 * N^2 * Ae) / L
    mu_0 = 4 * np.pi * 1e-7
    ae_m2 = ae_val_mm2 * 1e-6
    gap_meters = (mu_0 * (n_turns**2) * ae_m2) / L_val
    gap_mm = gap_meters * 1000

    # 5. Actual Flux Density: B = (L * Ipk) / (N * Ae)
    b_actual = (L_val * i_peak) / (n_turns * ae_m2)

# --- DISPLAY RESULTS ---
if valid_design:

    # ROW 1: Electrical Specs
    st.header("1. Electrical Design")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Inductance (L)", f"{L_val*1e6:.1f} µH")
    c2.metric("Output Cap (Co)", f"{C_val*1e6:.1f} µF")
    c3.metric("Duty Cycle", f"{duty_cycle:.2f}")
    c4.metric("Peak Current (Ipk)", f"{i_peak:.2f} A")

    # ROW 2: Magnetic Specs
    st.markdown("---")
    st.header("2. Magnetic Design")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Required Turns (N)", f"{int(n_turns)}")
    m2.metric("Stored Energy", f"{energy_stored*1000:.3f} mJ")
    m3.metric("Air Gap (lg)", f"{gap_mm:.3f} mm")
    m4.metric(
        "Flux Density (B)",
        f"{b_actual:.3f} T",
        delta=f"Limit: {b_sat_limit} T",
        delta_color="normal",
    )

    # Use 80% of Bsat as “safe” limit
    b_safe = 0.8 * b_sat_limit

    # Flux Gauge
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=b_actual,
            title={"text": "Core Flux Saturation (Tesla)"},
            gauge={
                "axis": {"range": [0, b_sat_limit * 1.5]},
                "bar": {"color": "red" if b_actual > b_safe else "#00CC96"},
                "steps": [
                    {"range": [0, b_safe], "color": "rgba(0,200,0,0.1)"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": b_safe,
                },
            },
        )
    )
    fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    if b_actual > b_sat_limit:
        st.error(f"⚠️ CORE SATURATION WARNING! Flux {b_actual:.2f}T > Limit {b_sat_limit}T")

    # ROW 3: Simulation
    st.markdown("---")
    st.header("3. Transient Simulation")

    # Toggles
    st.caption("Toggle Waveforms:")
    col_t1, col_t2, col_t3, col_t4, col_t5, col_t6 = st.columns(6)
    show_vin = col_t1.checkbox("Input Voltage (Vin)", value=False)
    show_vout = col_t2.checkbox("Output Voltage (Vout)", value=False)
    show_vds = col_t3.checkbox("Switch Voltage (Vds)", value=False)
    show_vgs = col_t4.checkbox("Gate Voltage (Vgs)", value=False)
    show_il = col_t5.checkbox("Inductor Current (IL)", value=True)
    show_iout = col_t6.checkbox("Output Current (Iout)", value=True)

    # Calc Waveforms
    T = 1 / f_sw
    num_cycles = 3
    t = np.linspace(0, num_cycles * T, 1000)

    wave_IL = []
    wave_vin = []
    wave_vds = []
    wave_vgs = []
    wave_vout = []
    wave_iout = []

    # Current slopes
    if converter_type == "Buck (Step-Down)":
        slope_on = (v_in - v_out) / L_val
        slope_off = -v_out / L_val
        vds_high = v_in
    else:
        slope_on = v_in / L_val
        slope_off = (v_in - v_out) / L_val
        vds_high = v_out

    # Min/max current values
    i_min = i_L_avg - (delta_i_L / 2)
    i_max = i_L_avg + (delta_i_L / 2)

    v_out_ripple_amp = v_out * (dv_percent / 100.0)

    # Iout ripple amplitude (small compared to IL ripple)
    i_out_ripple = delta_i_L * 0.1

    for time_step in t:
        cycle_time = time_step % T
        t_on = duty_cycle * T
        t_off = T - t_on

        # --- Inductor Current (Triangular Waveform) ---
        if cycle_time < t_on:
            # ON period: current ramps up from i_min
            current_val = i_min + slope_on * cycle_time
            vgs_curr = v_gate_drive
            vds_curr = 0.0
        else:
            # OFF period: current ramps down from i_max
            current_val = i_max + slope_off * (cycle_time - t_on)
            vgs_curr = 0.0
            vds_curr = vds_high

        # Saturation Clamp
        clamped_i = min(current_val, i_hard_sat)
        wave_IL.append(clamped_i)

        # Voltages
        wave_vin.append(v_in)
        wave_vds.append(vds_curr)
        wave_vgs.append(vgs_curr)

        # Output Voltage (sine approximation of capacitor ripple)
        v_out_ripple_amp = v_out * (dv_percent / 100.0)
        wave_vout.append(
            v_out + v_out_ripple_amp * np.sin(2 * np.pi * f_sw * time_step)
        )


        # Output Current (DC load with small ripple)
        wave_iout.append(
            i_load + (i_out_ripple * 0.5 * np.sin(2 * np.pi * f_sw * time_step - np.pi / 2))
        )

    # --- PLOTTING (2 Charts) ---

    # CHART A: Currents (Inductor + Output + Saturation)
    fig_i = go.Figure()

    # IL trace (toggle)
    if show_il:
        fig_i.add_trace(
            go.Scatter(
                x=t * 1e6,
                y=wave_IL,
                mode="lines",
                name="Inductor Current (IL)",
                line=dict(color="#00CC96", width=3),
            )
        )

    # Iout trace (toggle)
    if show_iout:
        fig_i.add_trace(
            go.Scatter(
                x=t * 1e6,
                y=wave_iout,
                mode="lines",
                name="Output Current (Iout)",
                line=dict(color="#FFA15A", width=2, dash="dashdot"),
            )
        )

    # Saturation Limit
    fig_i.add_trace(
        go.Scatter(
            x=[0, num_cycles * T * 1e6],
            y=[i_hard_sat, i_hard_sat],
            mode="lines",
            name="Saturation Limit",
            line=dict(color="red", dash="dash"),
        )
    )

    fig_i.update_layout(
        title="Current Waveforms (IL vs Iout)",
        xaxis_title="Time (µs)",
        yaxis_title="Current (A)",
        template="plotly_dark",
        height=350,
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_i, use_container_width=True)

    # CHART B: System Voltages
    fig_v = go.Figure()
    if show_vin:
        fig_v.add_trace(
            go.Scatter(
                x=t * 1e6, y=wave_vin, mode="lines", name="Vin", line=dict(color="#636EFA")
            )
        )
    if show_vout:
        fig_v.add_trace(
            go.Scatter(
                x=t * 1e6, y=wave_vout, mode="lines", name="Vout", line=dict(color="#EF553B")
            )
        )
    if show_vds:
        fig_v.add_trace(
            go.Scatter(
                x=t * 1e6, y=wave_vds, mode="lines", name="Vds (Switch)", line=dict(color="#FFA500")
            )
        )
    if show_vgs:
        fig_v.add_trace(
            go.Scatter(
                x=t * 1e6, y=wave_vgs, mode="lines", name="Vgs (Gate)", line=dict(color="#AB63FA")
            )
        )

    fig_v.update_layout(
        title="Voltage Waveforms",
        xaxis_title="Time (µs)",
        yaxis_title="Voltage (V)",
        template="plotly_dark",
        height=350,
        legend=dict(orientation="h", y=1.1),
    )
    if any([show_vin, show_vout, show_vds, show_vgs]):
        st.plotly_chart(fig_v, use_container_width=True)
