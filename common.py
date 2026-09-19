"""
Mental Health in Tech — Workplace Mental Health Intelligence
A glassmorphism analytics dashboard over the 2014 OSMI survey dataset.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------------------------
# DESIGN TOKENS
# ---------------------------------------------------------------------------
NAVY = "#0A0E1A"
NAVY_2 = "#0D1220"
GLASS_06 = "rgba(255,255,255,0.06)"
GLASS_08 = "rgba(255,255,255,0.08)"
GLASS_10 = "rgba(255,255,255,0.10)"
BORDER = "rgba(255,255,255,0.12)"
TEXT_PRIMARY = "#F4F6FA"
TEXT_SECONDARY = "#8B93A7"

BLUE = "#4C8DFF"
VIOLET = "#A78BFA"
TEAL = "#2DD4BF"
CORAL = "#FB7185"
PALETTE = [BLUE, VIOLET, TEAL, CORAL]
PALETTE_MUTED = ["#4C8DFF", "#7C9CFF", "#A78BFA", "#2DD4BF", "#5EEAD4", "#FB7185"]

NAV_ITEMS = [
    "01 — Executive Overview",
    "02 — Mental Health",
    "03 — Workplace Environment",
    "04 — Treatment & Support",
    "05 — Demographics",
    "06 — Interactive Explorer",
    "07 — Key Findings",
]

# ---------------------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------------------
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{background: transparent;}}

    .stApp {{
        background:
            radial-gradient(ellipse 900px 600px at 8% 8%, rgba(76,141,255,0.10), transparent 60%),
            radial-gradient(ellipse 800px 700px at 95% 15%, rgba(167,139,250,0.09), transparent 60%),
            radial-gradient(ellipse 900px 800px at 50% 100%, rgba(45,212,191,0.07), transparent 60%),
            linear-gradient(180deg, {NAVY} 0%, {NAVY_2} 100%);
        background-attachment: fixed;
        color: {TEXT_PRIMARY};
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(10,14,26,0.85);
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] > div {{padding-top: 1.2rem;}}

    .block-container {{padding-top: 1.6rem; max-width: 1400px;}}

    /* ---- Glass primitives ---- */
    .glass {{
        background: {GLASS_06};
        border: 1px solid {BORDER};
        border-radius: 20px;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }}
    .glass-strong {{
        background: {GLASS_10};
        border: 1px solid {BORDER};
        border-radius: 20px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.28);
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-in {{ animation: fadeInUp 0.5s ease both; }}

    @keyframes shimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 200% 50%; }}
    }}

    /* ---- Header ---- */
    .app-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 22px 30px;
        margin-bottom: 22px;
    }}
    .app-header .brand-title {{
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        line-height: 1.15;
        color: {TEXT_PRIMARY};
    }}
    .app-header .brand-sub {{
        font-size: 0.82rem;
        color: {TEXT_SECONDARY};
        margin-top: 4px;
        font-weight: 500;
    }}
    .app-header .meta-right {{
        text-align: right;
    }}
    .app-header .meta-label {{
        font-size: 0.72rem;
        letter-spacing: 1.2px;
        color: {TEXT_SECONDARY};
        text-transform: uppercase;
    }}
    .app-header .meta-value {{
        font-size: 1.0rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
    }}

    /* ---- Hero ---- */
    .hero {{
        padding: 46px 42px;
        margin-bottom: 26px;
    }}
    .hero h1 {{
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0 0 12px 0;
        color: {TEXT_PRIMARY};
        letter-spacing: -0.5px;
    }}
    .hero p {{
        font-size: 1.02rem;
        color: {TEXT_SECONDARY};
        max-width: 640px;
        margin: 0;
        line-height: 1.55;
    }}
    .hero-line {{
        height: 3px;
        width: 140px;
        margin-top: 26px;
        border-radius: 4px;
        background: linear-gradient(90deg, {BLUE}, {VIOLET}, {TEAL}, {CORAL}, {BLUE});
        background-size: 300% 100%;
        animation: shimmer 6s linear infinite;
    }}

    /* ---- KPI cards ---- */
    .kpi-card {{
        padding: 22px 22px 18px 22px;
        transition: transform 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
        height: 100%;
    }}
    .kpi-card:hover {{
        transform: translateY(-4px);
        background: {GLASS_10};
        box-shadow: 0 14px 40px rgba(0,0,0,0.35);
    }}
    .kpi-label {{
        font-size: 0.70rem;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        color: {TEXT_SECONDARY};
        font-weight: 600;
    }}
    .kpi-value {{
        font-size: 2.15rem;
        font-weight: 800;
        margin: 8px 0 4px 0;
        color: {TEXT_PRIMARY};
        line-height: 1.1;
    }}
    .kpi-desc {{
        font-size: 0.80rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 12px;
    }}
    .kpi-accent-line {{
        height: 3px;
        width: 36px;
        border-radius: 3px;
    }}

    /* ---- Section titles ---- */
    .section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin: 6px 0 2px 0;
    }}
    .section-sub {{
        font-size: 0.85rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 14px;
    }}

    /* ---- Chart container ---- */
    .chart-card {{
        padding: 20px 22px 8px 22px;
        margin-bottom: 22px;
    }}
    .chart-card-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin-bottom: 2px;
    }}
    .chart-card-sub {{
        font-size: 0.76rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 10px;
    }}

    /* ---- Insight card ---- */
    .insight-card {{
        padding: 18px 22px;
        margin-bottom: 16px;
        border-left: 3px solid {BLUE};
    }}
    .insight-label {{
        font-size: 0.68rem;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        color: {BLUE};
        font-weight: 700;
        margin-bottom: 6px;
    }}
    .insight-text {{
        font-size: 0.90rem;
        color: {TEXT_PRIMARY};
        line-height: 1.5;
    }}

    /* ---- Sidebar nav (radio restyle) ---- */
    section[data-testid="stSidebar"] .stRadio > label {{display: none;}}
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {{
        gap: 4px;
    }}
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {{
        background: transparent;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 2px;
        transition: background 0.2s ease, border-color 0.2s ease;
        border: 1px solid transparent;
        width: 100%;
    }}
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {{
        background: {GLASS_06};
    }}
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] {{
        background: rgba(76,141,255,0.12);
        border: 1px solid rgba(76,141,255,0.35);
        box-shadow: 0 0 18px rgba(76,141,255,0.15);
    }}
    section[data-testid="stSidebar"] .stRadio input {{display: none;}}

    /* ---- Filter panel widgets ---- */
    div[data-testid="stExpander"] {{
        background: {GLASS_06};
        border: 1px solid {BORDER};
        border-radius: 18px;
        backdrop-filter: blur(16px);
        margin-bottom: 20px;
    }}
    div[data-testid="stExpander"] summary {{
        font-weight: 600;
        color: {TEXT_PRIMARY};
    }}

    .filter-tag {{
        display: inline-block;
        background: {GLASS_10};
        border: 1px solid {BORDER};
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.76rem;
        color: {TEXT_PRIMARY};
        margin: 3px 6px 3px 0;
    }}
    .showing-text {{
        font-size: 0.82rem;
        color: {TEXT_SECONDARY};
        margin-top: 6px;
    }}

    hr.section-div {{
        border: none;
        height: 1px;
        background: {BORDER};
        margin: 30px 0;
    }}

    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-thumb {{ background: {GLASS_10}; border-radius: 8px; }}
    </style>
    """, unsafe_allow_html=True)


def plotly_theme(fig, height=380, show_legend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_SECONDARY, size=12),
        title_font=dict(color=TEXT_PRIMARY, size=14),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=11),
            orientation="h",
            yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
        hoverlabel=dict(bgcolor="#151A2C", font_color=TEXT_PRIMARY, bordercolor=BORDER),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False, color=TEXT_SECONDARY)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False, color=TEXT_SECONDARY)
    return fig


def chart_card(title, subtitle=""):
    st.markdown(f"""
    <div class="glass chart-card fade-in">
        <div class="chart-card-title">{title}</div>
        <div class="chart-card-sub">{subtitle}</div>
    """, unsafe_allow_html=True)


def chart_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def kpi_card(col, label, value, desc, accent):
    with col:
        st.markdown(f"""
        <div class="glass kpi-card fade-in">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-desc">{desc}</div>
            <div class="kpi-accent-line" style="background:{accent};"></div>
        </div>
        """, unsafe_allow_html=True)


def insight_card(text):
    st.markdown(f"""
    <div class="glass insight-card fade-in">
        <div class="insight-label">Key Insight</div>
        <div class="insight-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
MALE_TERMS = {'male', 'm', 'man', 'cis male', 'male-ish', 'maile', 'cis man', 'malr',
              'mal', 'make', 'msle', 'mail', 'guy (-ish) ^_^', 'male (cis)',
              'something kinda male?', 'male leaning androgynous',
              'ostensibly male, unsure what that really means'}
FEMALE_TERMS = {'female', 'f', 'woman', 'cis female', 'femake', 'female (cis)',
                'femail', 'cis-female/femme', 'female (trans)', 'trans woman',
                'trans-female'}


def clean_gender(g):
    g = str(g).strip().lower()
    if g in MALE_TERMS:
        return "Male"
    if g in FEMALE_TERMS:
        return "Female"
    return "Other"


@st.cache_data
def load_data():
    df = pd.read_csv("survey.csv")
    age_valid = df.loc[(df["Age"] >= 15) & (df["Age"] <= 80), "Age"]
    df.loc[(df["Age"] < 15) | (df["Age"] > 80), "Age"] = age_valid.median()
    df["Gender"] = df["Gender"].apply(clean_gender)
    df["work_interfere"] = df["work_interfere"].fillna("Not applicable")
    df["self_employed"] = df["self_employed"].fillna(df["self_employed"].mode()[0])
    return df


# ---------------------------------------------------------------------------
# FILTER PANEL
# ---------------------------------------------------------------------------
def filter_panel(df):
    with st.expander("Filters", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            countries = st.multiselect("Country", sorted(df["Country"].unique()), key="f_country")
            genders = st.multiselect("Gender", sorted(df["Gender"].unique()), key="f_gender")
        with c2:
            age_range = st.slider("Age range", int(df["Age"].min()), int(df["Age"].max()),
                                   (int(df["Age"].min()), int(df["Age"].max())), key="f_age")
            remote = st.selectbox("Remote work", ["All", "Yes", "No"], key="f_remote")
        with c3:
            tech = st.selectbox("Tech company", ["All", "Yes", "No"], key="f_tech")
            company_size = st.multiselect("Company size", sorted(df["no_employees"].unique()), key="f_size")
        with c4:
            treatment = st.selectbox("Treatment", ["All", "Yes", "No"], key="f_treatment")
            family = st.selectbox("Family history", ["All", "Yes", "No"], key="f_family")

        clear = st.button("Clear filters")
        if clear:
            for k in ["f_country", "f_gender", "f_remote", "f_tech", "f_size", "f_treatment", "f_family"]:
                st.session_state.pop(k, None)
            st.session_state.pop("f_age", None)
            st.rerun()

    mask = pd.Series(True, index=df.index)
    active = []
    if countries:
        mask &= df["Country"].isin(countries)
        active.append(f"Country: {', '.join(countries)}")
    if genders:
        mask &= df["Gender"].isin(genders)
        active.append(f"Gender: {', '.join(genders)}")
    if age_range != (int(df["Age"].min()), int(df["Age"].max())):
        mask &= df["Age"].between(age_range[0], age_range[1])
        active.append(f"Age: {age_range[0]}–{age_range[1]}")
    if remote != "All":
        mask &= df["remote_work"] == remote
        active.append(f"Remote work: {remote}")
    if tech != "All":
        mask &= df["tech_company"] == tech
        active.append(f"Tech company: {tech}")
    if company_size:
        mask &= df["no_employees"].isin(company_size)
        active.append(f"Company size: {', '.join(company_size)}")
    if treatment != "All":
        mask &= df["treatment"] == treatment
        active.append(f"Treatment: {treatment}")
    if family != "All":
        mask &= df["family_history"] == family
        active.append(f"Family history: {family}")

    filtered = df[mask]

    tag_html = "".join([f'<span class="filter-tag">{a}</span>' for a in active]) if active else \
        '<span class="filter-tag">No filters applied</span>'
    st.markdown(f"""
    <div style="margin: -6px 0 18px 2px;">
        {tag_html}
        <div class="showing-text">Showing {len(filtered):,} of {len(df):,} responses</div>
    </div>
    """, unsafe_allow_html=True)

    return filtered


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
def render_header():
    st.markdown(f"""
    <div class="glass app-header fade-in">
        <div>
            <div class="brand-title">MENTAL HEALTH<br/>IN TECH</div>
            <div class="brand-sub">Workplace Mental Health Intelligence</div>
        </div>
        <div class="meta-right">
            <div class="meta-label">Survey Dataset</div>
            <div class="meta-value">2014</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


