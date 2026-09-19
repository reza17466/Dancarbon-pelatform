"""Shared styling for DanCarbon Tech platform."""
import streamlit as st


def apply_global_styles():
    """Apply professional styling across the entire app."""
    st.markdown("""
    <style>
        /* Hide Streamlit default menu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Reduce top padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        
        /* TYPOGRAPHY */
        h1 { color: #1B365D !important; font-weight: 800 !important; }
        h2 { color: #1B365D !important; font-weight: 700 !important; margin-top: 2rem !important; }
        h3 { color: #2E74B5 !important; font-weight: 600 !important; }
        
        /* HERO */
        .hero-container { padding: 3rem 0 2rem 0; }
        .hero-title {
            font-size: 3rem; font-weight: 800; color: #1B365D;
            line-height: 1.1; margin-bottom: 0.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem; color: #6B7280;
            margin-bottom: 1.5rem; line-height: 1.6;
        }
        
        /* BADGES */
        .badge {
            display: inline-block; background: #DEEAF6; color: #1B365D;
            padding: 0.4rem 0.9rem; border-radius: 999px;
            font-size: 0.85rem; font-weight: 600;
            margin-right: 0.5rem; margin-bottom: 0.5rem;
            border: 1px solid #B4C7E7;
        }
        
        /* FEATURE CARDS */
        .feature-card {
            background: #FFFFFF; padding: 1.5rem; border-radius: 12px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            height: 100%; transition: all 0.2s ease;
        }
        .feature-card:hover {
            border-color: #2E74B5;
            box-shadow: 0 4px 12px rgba(46, 116, 181, 0.12);
            transform: translateY(-2px);
        }
        .feature-card h3 {
            color: #1B365D; margin-top: 0;
            font-size: 1.1rem; margin-bottom: 0.75rem;
        }
        .feature-card p {
            font-size: 0.95rem; color: #4B5563;
            margin: 0; line-height: 1.5;
        }
        
        /* STAT CARDS */
        .stat-card {
            background: linear-gradient(135deg, #F5F7FA 0%, #DEEAF6 100%);
            padding: 1.25rem; border-radius: 10px;
            text-align: center; border: 1px solid #B4C7E7;
        }
        .stat-value {
            font-size: 1.75rem; font-weight: 800;
            color: #1B365D; line-height: 1.2;
        }
        .stat-label {
            font-size: 0.85rem; color: #6B7280; margin-top: 0.25rem;
        }
        
        /* CTA BOX */
        .cta-box {
            background: linear-gradient(135deg, #1B365D 0%, #2E74B5 100%);
            color: white; padding: 2.5rem; border-radius: 16px;
            text-align: center; margin: 2rem 0;
            box-shadow: 0 8px 24px rgba(27, 54, 93, 0.15);
        }
        .cta-box h2 { color: white !important; margin-top: 0 !important; }
        .cta-box p { color: #DEEAF6 !important; font-size: 1.05rem; }
        
        /* FOOTER */
        .custom-footer {
            text-align: center; color: #9CA3AF;
            font-size: 0.85rem; padding: 2rem 0 1rem 0;
            border-top: 1px solid #E5E7EB; margin-top: 3rem;
        }
        .custom-footer a { color: #2E74B5; text-decoration: none; }
        
        /* METRICS */
        [data-testid="stMetricValue"] { color: #1B365D; font-weight: 700; }
        [data-testid="stMetricLabel"] { color: #6B7280; font-size: 0.85rem; }
        
        hr { margin: 2rem 0 !important; border-color: #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)


def hero_section(title, subtitle, badges=None):
    html = '<div class="hero-container">'
    html += f'<div class="hero-title">{title}</div>'
    html += f'<div class="hero-subtitle">{subtitle}</div>'
    if badges:
        for b in badges:
            html += f'<span class="badge">{b}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def feature_card(icon, title, description):
    st.markdown(f"""
    <div class="feature-card">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


def stat_card(value, label):
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def custom_footer():
    st.markdown("""
    <div class="custom-footer">
        <strong>DanCarbon Tech ApS</strong> — Advanced CO₂ Separation Technologies<br>
        Copenhagen, Denmark · <a href="mailto:contact@dancarbon.tech">contact@dancarbon.tech</a><br>
        <small>© 2026 DanCarbon Tech. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)
