"""ROI Calculator — estimate savings and CO₂ reduction."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="ROI Calculator — DanCarbon Tech",
                   page_icon="💰", layout="wide")

st.title("💰 ROI & Savings Calculator")
st.markdown(
    "Estimate your potential savings with DanCarbon Tech's "
    "AI-optimized separation platform."
)

st.markdown("---")

# ==================================================================
# INPUTS
# ==================================================================
st.markdown("### 1. Your Plant Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    gas_flow = st.number_input(
        "Biogas flow rate (Nm³/h)",
        min_value=50.0, max_value=5000.0, value=500.0, step=50.0,
        help="Typical Danish biogas plant: 200–1500 Nm³/h"
    )

with col2:
    current_energy = st.number_input(
        "Current energy consumption (kWh/Nm³)",
        min_value=0.05, max_value=1.0, value=0.25, step=0.01,
        help="Typical amine scrubbing: 0.20–0.35 kWh/Nm³"
    )

with col3:
    energy_price = st.number_input(
        "Energy price (DKK/kWh)",
        min_value=0.5, max_value=5.0, value=1.20, step=0.10,
        help="Danish industrial electricity: ~1.0–1.5 DKK/kWh"
    )

col4, col5 = st.columns(2)

with col4:
    operating_hours = st.number_input(
        "Operating hours per year",
        min_value=1000, max_value=8760, value=8000, step=100,
        help="Typical: 7,500–8,500 hours/year"
    )

with col5:
    optimization_level = st.select_slider(
        "Optimization level",
        options=["Conservative", "Moderate", "Aggressive"],
        value="Moderate",
        help="Based on pilot data and industry benchmarks"
    )

st.markdown("---")

# ==================================================================
# CALCULATIONS
# ==================================================================
# Optimization percentages
opt_map = {
    "Conservative": {"energy": 0.05, "co2": 0.03},
    "Moderate": {"energy": 0.10, "co2": 0.05},
    "Aggressive": {"energy": 0.18, "co2": 0.08},
}
opt = opt_map[optimization_level]

# Annual figures
annual_gas = gas_flow * operating_hours  # Nm³/year
current_annual_energy = annual_gas * current_energy  # kWh/year
current_annual_cost = current_annual_energy * energy_price  # DKK/year

# Savings
energy_saved_kwh = current_annual_energy * opt["energy"]
energy_saved_dkk = energy_saved_kwh * energy_price

# CO₂ impact
# Assume ~1.5 kg CO₂ per Nm³ biogas processed
co2_processed_tonnes = annual_gas * 1.5 / 1000
co2_reduced_tonnes = co2_processed_tonnes * opt["co2"]

# DanCarbon platform cost (SaaS Professional)
platform_cost = 30000  # DKK/year
net_savings = energy_saved_dkk - platform_cost
roi_months = (platform_cost / energy_saved_dkk * 12) if energy_saved_dkk > 0 else 0

# 5-year projection
five_year_savings = net_savings * 5

# ==================================================================
# RESULTS
# ==================================================================
st.markdown("### 2. Estimated Results")

col_r1, col_r2, col_r3, col_r4 = st.columns(4)

with col_r1:
    st.metric(
        "Energy saved / year",
        f"{energy_saved_kwh:,.0f} kWh",
        delta=f"{opt['energy']*100:.0f}% reduction"
    )

with col_r2:
    st.metric(
        "Cost savings / year",
        f"{energy_saved_dkk:,.0f} DKK",
        delta=f"Net: {net_savings:,.0f} DKK"
    )

with col_r3:
    st.metric(
        "CO₂ reduced / year",
        f"{co2_reduced_tonnes:,.1f} tonnes",
        delta=f"{opt['co2']*100:.0f}% efficiency gain"
    )

with col_r4:
    if roi_months > 0:
        st.metric(
            "ROI period",
            f"{roi_months:.1f} months",
            delta="payback achieved"
        )
    else:
        st.metric("ROI period", "Immediate")

st.markdown("---")

# ==================================================================
# 5-YEAR PROJECTION CHART
# ==================================================================
st.markdown("### 3. Five-Year Savings Projection")

years = list(range(1, 6))
cumulative = [net_savings * y for y in years]
annual = [net_savings] * 5

fig = go.Figure()
fig.add_trace(go.Bar(
    x=years, y=annual,
    name='Annual savings',
    marker_color='#2E74B5',
))
fig.add_trace(go.Scatter(
    x=years, y=cumulative,
    name='Cumulative savings',
    line=dict(color='#1B365D', width=3),
    mode='lines+markers'
))
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Savings (DKK)",
    height=400,
    legend=dict(orientation='h', y=1.1),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridcolor='#E5E7EB')
st.plotly_chart(fig, use_container_width=True)

# ==================================================================
# SUMMARY TABLE
# ==================================================================
st.markdown("### 4. Summary Table")

summary_data = {
    "Metric": [
        "Annual gas processed",
        "Current annual energy",
        "Current annual energy cost",
        "Energy savings (kWh/year)",
        "Energy cost savings (DKK/year)",
        "DanCarbon platform cost (DKK/year)",
        "Net annual savings (DKK)",
        "CO₂ emissions reduced (tonnes/year)",
        "5-year net savings (DKK)",
    ],
    "Value": [
        f"{annual_gas:,.0f} Nm³",
        f"{current_annual_energy:,.0f} kWh",
        f"{current_annual_cost:,.0f} DKK",
        f"{energy_saved_kwh:,.0f} kWh",
        f"{energy_saved_dkk:,.0f} DKK",
        f"-{platform_cost:,.0f} DKK",
        f"{net_savings:,.0f} DKK",
        f"{co2_reduced_tonnes:,.1f} tonnes",
        f"{five_year_savings:,.0f} DKK",
    ]
}
st.dataframe(
    pd.DataFrame(summary_data),
    use_container_width=True,
    hide_index=True
)

# ==================================================================
# DOWNLOAD
# ==================================================================
st.markdown("---")
result_df = pd.DataFrame([{
    'Gas_flow_Nm3_per_h': gas_flow,
    'Energy_consumption_kWh_per_Nm3': current_energy,
    'Energy_price_DKK_per_kWh': energy_price,
    'Operating_hours': operating_hours,
    'Optimization_level': optimization_level,
    'Energy_saved_kWh_per_year': round(energy_saved_kwh, 0),
    'Cost_saved_DKK_per_year': round(energy_saved_dkk, 0),
    'Net_savings_DKK_per_year': round(net_savings, 0),
    'CO2_reduced_tonnes_per_year': round(co2_reduced_tonnes, 2),
    'ROI_months': round(roi_months, 1),
    'Five_year_savings_DKK': round(five_year_savings, 0),
}])

st.download_button(
    "📥 Download Your ROI Report (CSV)",
    result_df.to_csv(index=False),
    file_name="DanCarbon_ROI_Estimate.csv",
    mime="text/csv",
    type="primary"
)

# ==================================================================
# CTA
# ==================================================================
st.markdown("---")
st.markdown("""
### 💡 Want to validate these numbers?

Our **Process Audit (Gold)** service validates these estimates against
your actual plant data and provides a detailed optimization roadmap.

[📩 Request a Free Consultation](pages/9_📩_Request_Quote.py)
""")

st.caption(
    "⚠️ These are estimates based on pilot data and industry benchmarks. "
    "Actual results depend on plant configuration, feedstock, and operating conditions."
)
