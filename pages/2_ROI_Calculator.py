"""ROI Calculator — real thermodynamic calculations with CoolProp."""
import streamlit as st
import pandas as pd
import numpy as np

try:
    import CoolProp.CoolProp as CP
    HAS_COOLPROP = True
except Exception:
    HAS_COOLPROP = False

st.set_page_config(page_title="ROI Calculator — DanCarbon Tech",
                   page_icon="💰", layout="wide")

st.title("💰 ROI Calculator")
st.markdown(
    "Real thermodynamic properties (CoolProp) + published energy "
    "benchmarks for biogas upgrading technologies."
)

if not HAS_COOLPROP:
    st.warning(
        "⚠️ CoolProp is not installed. Falling back to ideal-gas "
        "approximation. Add `CoolProp` to `requirements.txt` for full accuracy."
    )

st.markdown("---")

# ==================================================================
# SECTION 1: GAS FEED
# ==================================================================
st.markdown("## 1. Gas Feed Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    biogas_flow = st.number_input(
        "Biogas flow rate (Nm³/h)",
        min_value=50.0, max_value=5000.0, value=500.0, step=50.0,
        help="Normal conditions: 0°C, 1.013 bar"
    )
with col2:
    ch4_pct = st.slider("CH₄ content (mol%)", 50.0, 70.0, 63.0, 0.5)
with col3:
    co2_pct = 100.0 - ch4_pct
    st.metric("CO₂ content (mol%)", f"{co2_pct:.1f}")

with st.expander("Optional trace components"):
    col1, col2, col3 = st.columns(3)
    h2s_ppm = col1.number_input("H₂S (ppm)", 0, 5000, 200, 50)
    h2o_pct = col2.number_input("H₂O (mol%)", 0.0, 10.0, 2.0, 0.5)
    o2_pct = col3.number_input("O₂ (mol%)", 0.0, 5.0, 0.5, 0.1)

st.markdown("---")

# ==================================================================
# SECTION 2: OPERATING CONDITIONS
# ==================================================================
st.markdown("## 2. Operating Conditions")

col1, col2, col3 = st.columns(3)
with col1:
    T_operation = st.number_input(
        "Absorption temperature (K)", 280.0, 350.0, 297.0, 1.0
    )
with col2:
    P_operation = st.number_input(
        "Absorption pressure (bar)", 1.0, 30.0, 17.0, 0.5
    )
with col3:
    T_regen = st.number_input(
        "Regeneration temperature (K)", 320.0, 420.0, 373.0, 5.0,
        help="Amine: 393–403 K | Physical solvent: 350–380 K"
    )

st.markdown("---")

# ==================================================================
# SECTION 3: THERMODYNAMIC PROPERTIES
# ==================================================================
st.markdown("## 3. Thermodynamic Properties (Real Gas via CoolProp)")

total_frac = ch4_pct + co2_pct
ch4_frac = ch4_pct / total_frac
co2_frac = co2_pct / total_frac
P_pa = P_operation * 1e5

if HAS_COOLPROP:
    mixture_str = f"Methane[{ch4_frac:.4f}]&CarbonDioxide[{co2_frac:.4f}]"
    try:
        Z_factor = CP.PropsSI('Z', 'T', T_operation, 'P', P_pa, mixture_str)
        density = CP.PropsSI('Dmass', 'T', T_operation, 'P', P_pa, mixture_str)
        cp = CP.PropsSI('Cpmass', 'T', T_operation, 'P', P_pa, mixture_str)
        cv = CP.PropsSI('Cvmass', 'T', T_operation, 'P', P_pa, mixture_str)
        gamma = cp / cv
        enthalpy = CP.PropsSI('Hmass', 'T', T_operation, 'P', P_pa, mixture_str)
        entropy = CP.PropsSI('Smass', 'T', T_operation, 'P', P_pa, mixture_str)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Z-factor", f"{Z_factor:.4f}")
        col2.metric("Density", f"{density:.2f} kg/m³")
        col3.metric("Cp", f"{cp/1000:.3f} kJ/kg·K")
        col4.metric("γ = Cp/Cv", f"{gamma:.4f}")

        col1, col2 = st.columns(2)
        col1.metric("Enthalpy", f"{enthalpy/1e6:.3f} MJ/kg")
        col2.metric("Entropy", f"{entropy/1000:.4f} kJ/kg·K")

        st.caption(
            "Real-gas properties computed with CoolProp using the "
            "GERG-2008 equation of state for the CH₄/CO₂ mixture."
        )
    except Exception as e:
        st.error(f"CoolProp error: {e}")
        Z_factor, density, cp, gamma = 1.0, 1.2, 2000, 1.3
else:
    R = 8.314
    M_mix = (ch4_frac * 16.04 + co2_frac * 44.01) / 1000
    density = P_pa * M_mix / (R * T_operation)
    Z_factor, cp, gamma = 1.0, 2200, 1.3
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Z-factor (ideal)", f"{Z_factor:.4f}")
    col2.metric("Density (ideal)", f"{density:.2f} kg/m³")
    col3.metric("Cp (approx)", f"{cp/1000:.3f} kJ/kg·K")
    col4.metric("γ (approx)", f"{gamma:.4f}")

st.markdown("---")

# ==================================================================
# SECTION 4: ENERGY CALCULATIONS
# ==================================================================
st.markdown("## 4. Energy Calculations")

n_flow_kmol_h = biogas_flow / 22.414
n_flow_mol_s = n_flow_kmol_h * 1000 / 3600
co2_flow_kmol_h = n_flow_kmol_h * (co2_pct / 100)
co2_mass_kg_h = co2_flow_kmol_h * 44.01

st.markdown("### Select Current Technology")
current_tech = st.selectbox(
    "Upgrading technology",
    [
        "Amine scrubbing (MEA 30%)",
        "Water scrubbing",
        "Pressure swing adsorption (PSA)",
        "Polymeric membranes",
        "Organic physical scrubbing (Selexol-type)",
    ]
)

tech_energy = {
    "Amine scrubbing (MEA 30%)": {
        "regen_MJ_per_kg_CO2": 3.8,
        "elec_kWh_per_Nm3": 0.12,
        "source": "Rochelle (2009), Science 325, 1652",
    },
    "Water scrubbing": {
        "regen_MJ_per_kg_CO2": 0.0,
        "elec_kWh_per_Nm3": 0.28,
        "source": "Patterson et al. (2015), Appl. Energy 150, 117",
    },
    "Pressure swing adsorption (PSA)": {
        "regen_MJ_per_kg_CO2": 0.0,
        "elec_kWh_per_Nm3": 0.30,
        "source": "Grande (2012), ISRN Chem. Eng.",
    },
    "Polymeric membranes": {
        "regen_MJ_per_kg_CO2": 0.0,
        "elec_kWh_per_Nm3": 0.25,
        "source": "Scholz et al. (2013), J. Membr. Sci. 444, 359",
    },
    "Organic physical scrubbing (Selexol-type)": {
        "regen_MJ_per_kg_CO2": 1.8,
        "elec_kWh_per_Nm3": 0.15,
        "source": "Kohl & Nielsen (1997), Gas Purification, 5th ed.",
    },
}
tech = tech_energy[current_tech]

hours_per_year = st.number_input(
    "Operating hours per year", 1000, 8760, 8000, 100
)

elec_kWh_h = tech["elec_kWh_per_Nm3"] * biogas_flow
elec_kWh_year = elec_kWh_h * hours_per_year

thermal_MJ_h = tech["regen_MJ_per_kg_CO2"] * co2_mass_kg_h
thermal_kWh_h = thermal_MJ_h / 3.6
thermal_kWh_year = thermal_kWh_h * hours_per_year

total_kWh_year = elec_kWh_year + thermal_kWh_year

col1, col2, col3 = st.columns(3)
col1.metric("Electrical energy", f"{elec_kWh_year:,.0f} kWh/y")
col2.metric("Thermal energy", f"{thermal_kWh_year:,.0f} kWh/y")
col3.metric("Total energy", f"{total_kWh_year:,.0f} kWh/y")

st.caption(f"Source: {tech['source']}")

st.markdown("---")

# ==================================================================
# SECTION 5: DANCARBON OPTIMIZATION
# ==================================================================
st.markdown("## 5. DanCarbon Optimization Scenarios")

st.markdown("""
The DanCarbon platform identifies the optimal operating window using
the validated response-surface model (R² = 0.91). Savings come from
three sources:
1. Operating-window optimization at the discovered optimum
2. Solvent formulation tuning (physical vs chemical absorption)
3. Reduced methane slip (better CH₄/CO₂ selectivity)

The percentage scenarios below are **literature-based targets**, to be
**validated during the Danish pilot**.
""")

scenario = st.radio(
    "Optimization scenario",
    ["Conservative (5%)", "Moderate (10%)", "Aggressive (18%)"],
    index=1, horizontal=True,
)
saving_pct = {
    "Conservative (5%)": 0.05,
    "Moderate (10%)": 0.10,
    "Aggressive (18%)": 0.18,
}[scenario]

savings_kWh_year = total_kWh_year * saving_pct
new_total_kWh_year = total_kWh_year - savings_kWh_year

col1, col2, col3 = st.columns(3)
col1.metric("Current", f"{total_kWh_year:,.0f} kWh/y")
col2.metric("Savings", f"{savings_kWh_year:,.0f} kWh/y",
            delta=f"{saving_pct*100:.0f}%")
col3.metric("Optimized", f"{new_total_kWh_year:,.0f} kWh/y")

st.markdown("---")

# ==================================================================
# SECTION 6: CO2 IMPACT
# ==================================================================
st.markdown("## 6. CO₂ Impact")

co2_captured_tonnes = co2_mass_kg_h * hours_per_year / 1000
grid_ef = 0.11  # kg CO₂/kWh (Denmark 2024, Energinet)
co2_avoided_tonnes = savings_kWh_year * grid_ef / 1000

col1, col2, col3 = st.columns(3)
col1.metric("CO₂ captured (product)", f"{co2_captured_tonnes:,.0f} t/y")
col2.metric("CO₂ avoided (energy)", f"{co2_avoided_tonnes:,.1f} t/y")
col3.metric("Total CO₂ impact",
            f"{co2_captured_tonnes + co2_avoided_tonnes:,.0f} t/y")

st.caption("Grid factor: 0.11 kg CO₂/kWh (Denmark 2024, Energinet)")

st.markdown("---")

# ==================================================================
# SECTION 7: FINANCIAL
# ==================================================================
st.markdown("## 7. Financial Analysis")

col1, col2 = st.columns(2)
with col1:
    electricity_price = st.number_input(
        "Electricity price (DKK/kWh)", 0.5, 5.0, 1.20, 0.10
    )
with col2:
    heat_price = st.number_input(
        "Heat/steam price (DKK/kWh)", 0.1, 2.0, 0.40, 0.05
    )

current_elec_cost = elec_kWh_year * electricity_price
current_thermal_cost = thermal_kWh_year * heat_price
current_total_cost = current_elec_cost + current_thermal_cost

if total_kWh_year > 0:
    elec_frac = elec_kWh_year / total_kWh_year
    thermal_frac = thermal_kWh_year / total_kWh_year
else:
    elec_frac, thermal_frac = 0, 0

total_savings = (savings_kWh_year * elec_frac * electricity_price +
                 savings_kWh_year * thermal_frac * heat_price)

platform_cost = st.number_input(
    "DanCarbon platform subscription (DKK/year)",
    0, 1000000, 30000, 5000
)

net_savings = total_savings - platform_cost
roi_months = (platform_cost / total_savings * 12) if total_savings > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current cost", f"{current_total_cost:,.0f} DKK/y")
col2.metric("Savings", f"{total_savings:,.0f} DKK/y",
            delta=f"Net: {net_savings:,.0f} DKK")
col3.metric("Platform", f"-{platform_cost:,.0f} DKK/y")
col4.metric("Payback",
            f"{roi_months:.1f} months" if roi_months > 0 else "Immediate")

st.markdown("---")

# ==================================================================
# SECTION 8: 5-YEAR PROJECTION
# ==================================================================
st.markdown("## 8. Five-Year Projection")

years = [1, 2, 3, 4, 5]
cumulative = [net_savings * y for y in years]
chart_df = pd.DataFrame({
    "Year": years,
    "Cumulative savings (DKK)": cumulative,
}).set_index("Year")

st.line_chart(chart_df)
st.metric("5-year net savings", f"{net_savings * 5:,.0f} DKK")

st.markdown("---")

# ==================================================================
# SECTION 9: SUMMARY
# ==================================================================
st.markdown("## 9. Summary")

summary = pd.DataFrame({
    "Parameter": [
        "Biogas flow",
        "CH₄ / CO₂",
        "Absorption T / P",
        "Regeneration T",
        "Current technology",
        "Z-factor (real gas)",
        "Current electrical",
        "Current thermal",
        "Total current energy",
        "Optimization scenario",
        "Energy savings",
        "CO₂ captured (product)",
        "CO₂ avoided (energy)",
        "Total CO₂ impact",
        "Annual savings",
        "Platform cost",
        "Net annual savings",
        "Payback period",
        "5-year net savings",
    ],
    "Value": [
        f"{biogas_flow:,.0f} Nm³/h",
        f"{ch4_pct:.1f}% / {co2_pct:.1f}%",
        f"{T_operation:.1f} K / {P_operation:.2f} bar",
        f"{T_regen:.1f} K",
        current_tech,
        f"{Z_factor:.4f}",
        f"{elec_kWh_year:,.0f} kWh/y",
        f"{thermal_kWh_year:,.0f} kWh/y",
        f"{total_kWh_year:,.0f} kWh/y",
        scenario,
        f"{savings_kWh_year:,.0f} kWh/y ({saving_pct*100:.0f}%)",
        f"{co2_captured_tonnes:,.0f} t/y",
        f"{co2_avoided_tonnes:,.1f} t/y",
        f"{co2_captured_tonnes + co2_avoided_tonnes:,.0f} t/y",
        f"{total_savings:,.0f} DKK/y",
        f"-{platform_cost:,.0f} DKK/y",
        f"{net_savings:,.0f} DKK/y",
        f"{roi_months:.1f} months" if roi_months > 0 else "Immediate",
        f"{net_savings * 5:,.0f} DKK",
    ]
})
st.dataframe(summary, use_container_width=True, hide_index=True)

st.download_button(
    "📥 Download full calculation report (CSV)",
    summary.to_csv(index=False),
    file_name="DanCarbon_ROI_Report.csv",
    mime="text/csv",
    type="primary",
)

# ==================================================================
# REFERENCES
# ==================================================================
st.markdown("---")
st.markdown("## References")
st.markdown("""
1. **CoolProp** — Bell, I.H. et al. (2014). *Pure and Pseudo-pure Fluid Thermophysical Property Evaluation.* Ind. Eng. Chem. Res. 53(6), 2498–2508.

2. **Amine regeneration duty** — Rochelle, G.T. (2009). *Amine Scrubbing for CO₂ Capture.* Science 325, 1652–1654.

3. **Water scrubbing** — Patterson, T. et al. (2015). *An evaluation of the upgrading technologies for biogas.* Applied Energy 150, 117–126.

4. **PSA** — Grande, C.A. (2012). *Advances in Pressure Swing Adsorption for Gas Separation.* ISRN Chemical Engineering.

5. **Membranes** — Scholz, M. et al. (2013). *Pilot scale demonstration of a membrane-based process for CO₂ separation from biogas.* J. Membr. Sci. 444, 359–367.

6. **Physical solvent** — Kohl, A.L. & Nielsen, R.B. (1997). *Gas Purification*, 5th ed., Gulf Publishing.

7. **Danish grid emission factor** — Energinet (2024). *Miljødeklaration for el.*

8. **DanCarbon experimental model** — Reza Chash (2016), MSc thesis, Mahshahr University.
""")

st.caption(
    "⚠️ **Disclaimer:** Baseline energy values are from published "
    "literature. DanCarbon's optimization percentages are literature-"
    "based targets — **they will be replaced with pilot-validated data** "
    "after the Danish demonstration."
)
