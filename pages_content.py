"""
Page render functions for the Mental Health in Tech dashboard.
Each function takes the already-filtered dataframe and renders one page.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from common import (
    plotly_theme, chart_card, chart_card_end, kpi_card, insight_card,
    BLUE, VIOLET, TEAL, CORAL, PALETTE, PALETTE_MUTED, TEXT_SECONDARY, TEXT_PRIMARY,
)

WORKPLACE_DIMENSIONS = {
    "Company size": "no_employees",
    "Mental health benefits": "benefits",
    "Care options awareness": "care_options",
    "Anonymity protection": "anonymity",
    "Ease of taking leave": "leave",
    "Remote work": "remote_work",
    "Family history": "family_history",
    "Gender": "Gender",
}


def pct(part, whole):
    return round(100 * part / whole, 1) if whole else 0.0


# ===========================================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ===========================================================================
def render_overview(df, full_df):
    st.markdown(f"""
    <div class="glass hero fade-in">
        <h1>Mental Health in the Tech Workplace</h1>
        <p>Exploring mental health experiences, workplace support, treatment patterns,
        and employee attitudes.</p>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    n = len(df)
    treated = (df["treatment"] == "Yes").sum()
    family = (df["family_history"] == "Yes").sum()
    remote = (df["remote_work"] == "Yes").sum()
    benefits_yes = (df["benefits"] == "Yes").sum()
    interfere_often = df["work_interfere"].isin(["Often", "Sometimes"]).sum()

    cols = st.columns(6)
    kpi_card(cols[0], "Total Responses", f"{n:,}", "Survey participants in current view", BLUE)
    kpi_card(cols[1], "Treatment Seeking", f"{pct(treated, n)}%", f"{treated:,} sought treatment", VIOLET)
    kpi_card(cols[2], "Family History", f"{pct(family, n)}%", "Report family history of illness", TEAL)
    kpi_card(cols[3], "Remote Workers", f"{pct(remote, n)}%", "Work remotely 50%+ of the time", CORAL)
    kpi_card(cols[4], "Mental Health Benefits", f"{pct(benefits_yes, n)}%", "Employer provides benefits", BLUE)
    kpi_card(cols[5], "Work Interference", f"{pct(interfere_often, n)}%", "Report it affects their work", VIOLET)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.6, 1])

    with left:
        chart_card("Workplace Mental Health Landscape",
                    "Treatment-seeking rate across a selectable workplace dimension")
        dim_label = st.selectbox("Dimension", list(WORKPLACE_DIMENSIONS.keys()),
                                  key="overview_dim", label_visibility="collapsed")
        dim_col = WORKPLACE_DIMENSIONS[dim_label]
        ct = pd.crosstab(df[dim_col], df["treatment"], normalize="index").mul(100)
        for c in ["Yes", "No"]:
            if c not in ct.columns:
                ct[c] = 0.0
        ct = ct.sort_values("Yes", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=ct.index, x=ct["Yes"], name="Sought treatment",
                              orientation="h", marker_color=BLUE))
        fig.add_trace(go.Bar(y=ct.index, x=ct["No"], name="Did not seek treatment",
                              orientation="h", marker_color="rgba(255,255,255,0.14)"))
        fig.update_layout(barmode="stack", xaxis_title="% of respondents")
        plotly_theme(fig, height=420)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    with right:
        chart_card("Support Snapshot", "Care options awareness across responses")
        care_counts = df["care_options"].value_counts()
        fig2 = go.Figure(data=[go.Pie(
            labels=care_counts.index, values=care_counts.values, hole=0.62,
            marker=dict(colors=PALETTE_MUTED), textinfo="percent",
        )])
        plotly_theme(fig2, height=200, show_legend=True)
        fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Company Size Mix", "Where respondents work")
        size_order = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
        size_counts = df["no_employees"].value_counts().reindex(
            [s for s in size_order if s in df["no_employees"].unique()])
        fig3 = go.Figure(go.Bar(x=size_counts.index, y=size_counts.values,
                                 marker_color=TEAL))
        plotly_theme(fig3, height=200, show_legend=False)
        fig3.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig3, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    c1, c2 = st.columns(2)
    with c1:
        top_country = df["Country"].value_counts().idxmax()
        top_country_pct = pct(df["Country"].value_counts().max(), n)
        insight_card(
            f"Among the filtered responses, {top_country_pct}% are based in {top_country}, "
            f"making it the largest single geography represented in the current view."
        )
    with c2:
        fam_yes_treat = pct((df[df["family_history"] == "Yes"]["treatment"] == "Yes").sum(),
                             max((df["family_history"] == "Yes").sum(), 1))
        fam_no_treat = pct((df[df["family_history"] == "No"]["treatment"] == "Yes").sum(),
                            max((df["family_history"] == "No").sum(), 1))
        insight_card(
            f"Respondents with a family history of mental illness sought treatment at "
            f"{fam_yes_treat}%, compared to {fam_no_treat}% among those without one."
        )


# ===========================================================================
# PAGE 2 — MENTAL HEALTH
# ===========================================================================
def render_mental_health(df):
    st.markdown('<div class="section-title fade-in">Mental Health</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Treatment status, family history, and work interference</div>',
                unsafe_allow_html=True)

    n = len(df)
    treated = (df["treatment"] == "Yes").sum()

    cols = st.columns(4)
    kpi_card(cols[0], "Treatment Rate", f"{pct(treated, n)}%", f"{treated:,} of {n:,} respondents", BLUE)
    kpi_card(cols[1], "Family History", f"{pct((df['family_history']=='Yes').sum(), n)}%",
              "Report family history", VIOLET)
    kpi_card(cols[2], "Frequent Interference", f"{pct(df['work_interfere'].isin(['Often']).sum(), n)}%",
              "Say it 'often' affects work", TEAL)
    kpi_card(cols[3], "Consequence Concern", f"{pct((df['mental_health_consequence']=='Yes').sum(), n)}%",
              "Expect negative consequences", CORAL)

    left, right = st.columns([1.5, 1])

    with left:
        chart_card("Treatment Status", "Have respondents sought treatment for a mental health condition?")
        tc = df["treatment"].value_counts()
        fig = go.Figure(go.Bar(x=tc.index, y=tc.values,
                                marker_color=[BLUE, "rgba(255,255,255,0.14)"]))
        plotly_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Work Interference", "Does a mental health condition interfere with work?")
        order = ["Not applicable", "Never", "Rarely", "Sometimes", "Often"]
        wc = df["work_interfere"].value_counts().reindex([o for o in order if o in df["work_interfere"].unique()])
        fig2 = go.Figure(go.Bar(x=wc.index, y=wc.values, marker_color=VIOLET))
        plotly_theme(fig2, height=320, show_legend=False)
        st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    with right:
        chart_card("Family History vs. Treatment", "Treatment-seeking rate by family history")
        ct = pd.crosstab(df["family_history"], df["treatment"], normalize="index").mul(100)
        fig3 = go.Figure()
        for i, col in enumerate(["Yes", "No"]):
            if col in ct.columns:
                fig3.add_trace(go.Bar(name=col, x=ct.index, y=ct[col],
                                       marker_color=PALETTE[i]))
        fig3.update_layout(barmode="group", yaxis_title="%")
        plotly_theme(fig3, height=300)
        st.plotly_chart(fig3, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Perceived Consequences", "Would disclosing a mental health issue have negative consequences?")
        mc = df["mental_health_consequence"].value_counts()
        fig4 = go.Figure(data=[go.Pie(labels=mc.index, values=mc.values, hole=0.6,
                                       marker=dict(colors=PALETTE_MUTED))])
        plotly_theme(fig4, height=280)
        st.plotly_chart(fig4, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    wi_often = df[df["work_interfere"] == "Often"]
    wi_often_treated = pct((wi_often["treatment"] == "Yes").sum(), max(len(wi_often), 1))
    insight_card(
        f"Among the filtered responses, {wi_often_treated}% of those who say their condition "
        f"'often' interferes with work have sought treatment — responses indicate work "
        f"interference is one of the strongest signals associated with treatment-seeking."
    )


# ===========================================================================
# PAGE 3 — WORKPLACE ENVIRONMENT
# ===========================================================================
def render_workplace(df):
    st.markdown('<div class="section-title fade-in">Workplace Environment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Benefits, care options, wellness programs, and anonymity</div>',
                unsafe_allow_html=True)

    n = len(df)
    cols = st.columns(4)
    kpi_card(cols[0], "Benefits Offered", f"{pct((df['benefits']=='Yes').sum(), n)}%",
              "Employer provides mental health benefits", BLUE)
    kpi_card(cols[1], "Know Care Options", f"{pct((df['care_options']=='Yes').sum(), n)}%",
              "Aware of employer's care options", VIOLET)
    kpi_card(cols[2], "Wellness Program", f"{pct((df['wellness_program']=='Yes').sum(), n)}%",
              "Discussed as part of wellness program", TEAL)
    kpi_card(cols[3], "Anonymity Protected", f"{pct((df['anonymity']=='Yes').sum(), n)}%",
              "Anonymity protected if using resources", CORAL)

    left, right = st.columns([1, 1])

    with left:
        chart_card("Mental Health Benefits", "Does your employer provide mental health benefits?")
        b = df["benefits"].value_counts()
        fig = go.Figure(go.Bar(x=b.index, y=b.values, marker_color=PALETTE_MUTED))
        plotly_theme(fig, height=280, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Wellness Program", "Has your employer discussed mental health as part of a wellness program?")
        w = df["wellness_program"].value_counts()
        fig2 = go.Figure(go.Bar(x=w.index, y=w.values, marker_color=PALETTE_MUTED))
        plotly_theme(fig2, height=280, show_legend=False)
        st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Resources to Seek Help", "Does your employer provide resources to learn about mental health?")
        s = df["seek_help"].value_counts()
        fig3 = go.Figure(go.Bar(x=s.index, y=s.values, marker_color=PALETTE_MUTED))
        plotly_theme(fig3, height=280, show_legend=False)
        st.plotly_chart(fig3, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    with right:
        chart_card("Care Options Awareness", "Do you know the options for mental health care your employer provides?")
        c = df["care_options"].value_counts()
        fig4 = go.Figure(go.Bar(x=c.index, y=c.values, marker_color=PALETTE_MUTED))
        plotly_theme(fig4, height=280, show_legend=False)
        st.plotly_chart(fig4, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Anonymity Protection", "Is your anonymity protected if you use mental health resources?")
        a = df["anonymity"].value_counts()
        fig5 = go.Figure(go.Bar(x=a.index, y=a.values, marker_color=PALETTE_MUTED))
        plotly_theme(fig5, height=280, show_legend=False)
        st.plotly_chart(fig5, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Ease of Taking Medical Leave", "How easy is it to take leave for a mental health condition?")
        order = ["Very easy", "Somewhat easy", "Don't know", "Somewhat difficult", "Very difficult"]
        l = df["leave"].value_counts().reindex([o for o in order if o in df["leave"].unique()])
        fig6 = go.Figure(go.Bar(x=l.index, y=l.values, marker_color=VIOLET))
        plotly_theme(fig6, height=280, show_legend=False)
        fig6.update_xaxes(tickangle=-15)
        st.plotly_chart(fig6, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    dont_know_benefits = pct((df["benefits"] == "Don't know").sum(), n)
    insight_card(
        f"Among the filtered responses, {dont_know_benefits}% of respondents don't know "
        f"whether their employer offers mental health benefits — responses indicate "
        f"communication of existing support may be as important as the support itself."
    )


# ===========================================================================
# PAGE 4 — TREATMENT & SUPPORT
# ===========================================================================
def render_treatment(df):
    st.markdown('<div class="section-title fade-in">Treatment & Support</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">How workplace support relates to treatment-seeking</div>',
                unsafe_allow_html=True)

    n = len(df)
    treated = (df["treatment"] == "Yes").sum()
    cols = st.columns(4)
    kpi_card(cols[0], "Overall Treatment Rate", f"{pct(treated, n)}%", f"{treated:,} respondents", BLUE)
    kpi_card(cols[1], "Comfortable w/ Coworkers", f"{pct((df['coworkers']=='Yes').sum(), n)}%",
              "Willing to discuss with coworkers", VIOLET)
    kpi_card(cols[2], "Comfortable w/ Supervisor", f"{pct((df['supervisor']=='Yes').sum(), n)}%",
              "Willing to discuss with supervisor", TEAL)
    kpi_card(cols[3], "Observed Consequences", f"{pct((df['obs_consequence']=='Yes').sum(), n)}%",
              "Witnessed negative consequences", CORAL)

    left, right = st.columns([1.3, 1])

    with left:
        chart_card("Treatment Rate by Support Factor", "How workplace support correlates with treatment-seeking")
        factor_label = st.selectbox("Support factor", ["Benefits", "Care options", "Anonymity", "Leave difficulty"],
                                     key="support_factor", label_visibility="collapsed")
        factor_map = {"Benefits": "benefits", "Care options": "care_options",
                      "Anonymity": "anonymity", "Leave difficulty": "leave"}
        col = factor_map[factor_label]
        ct = pd.crosstab(df[col], df["treatment"], normalize="index").mul(100)
        if "Yes" not in ct.columns:
            ct["Yes"] = 0.0
        ct = ct.sort_values("Yes")
        fig = go.Figure(go.Bar(x=ct["Yes"], y=ct.index, orientation="h", marker_color=BLUE))
        fig.update_layout(xaxis_title="% who sought treatment")
        plotly_theme(fig, height=360, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Mental vs. Physical Health", "Is mental health taken as seriously as physical health?")
        mvp = df["mental_vs_physical"].value_counts()
        fig2 = go.Figure(go.Bar(x=mvp.index, y=mvp.values, marker_color=PALETTE_MUTED))
        plotly_theme(fig2, height=280, show_legend=False)
        st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    with right:
        chart_card("Comfort Discussing with Coworkers", "")
        cw = df["coworkers"].value_counts()
        fig3 = go.Figure(data=[go.Pie(labels=cw.index, values=cw.values, hole=0.6,
                                       marker=dict(colors=PALETTE_MUTED))])
        plotly_theme(fig3, height=250)
        st.plotly_chart(fig3, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Comfort Discussing with Supervisor", "")
        sv = df["supervisor"].value_counts()
        fig4 = go.Figure(data=[go.Pie(labels=sv.index, values=sv.values, hole=0.6,
                                       marker=dict(colors=PALETTE_MUTED))])
        plotly_theme(fig4, height=250)
        st.plotly_chart(fig4, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Would Discuss in an Interview", "Mental_health_interview responses")
        mhi = df["mental_health_interview"].value_counts()
        fig5 = go.Figure(go.Bar(x=mhi.index, y=mhi.values, marker_color=CORAL))
        plotly_theme(fig5, height=220, show_legend=False)
        st.plotly_chart(fig5, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    obs_yes = df[df["obs_consequence"] == "Yes"]
    obs_yes_treated = pct((obs_yes["treatment"] == "Yes").sum(), max(len(obs_yes), 1))
    obs_no = df[df["obs_consequence"] == "No"]
    obs_no_treated = pct((obs_no["treatment"] == "Yes").sum(), max(len(obs_no), 1))
    insight_card(
        f"Among the filtered responses, {obs_yes_treated}% of those who have observed negative "
        f"consequences for coworkers sought treatment themselves, versus {obs_no_treated}% "
        f"among those who haven't observed such consequences."
    )


# ===========================================================================
# PAGE 5 — DEMOGRAPHICS
# ===========================================================================
def render_demographics(df):
    st.markdown('<div class="section-title fade-in">Demographics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Age, gender, geography, and company profile of respondents</div>',
                unsafe_allow_html=True)

    n = len(df)
    cols = st.columns(4)
    kpi_card(cols[0], "Median Age", f"{int(df['Age'].median())}", "Years old", BLUE)
    kpi_card(cols[1], "Countries Represented", f"{df['Country'].nunique()}", "Distinct countries in view", VIOLET)
    kpi_card(cols[2], "Tech Company", f"{pct((df['tech_company']=='Yes').sum(), n)}%",
              "Work at a tech company", TEAL)
    kpi_card(cols[3], "Remote Work", f"{pct((df['remote_work']=='Yes').sum(), n)}%",
              "Remote 50%+ of the time", CORAL)

    left, right = st.columns([1.3, 1])

    with left:
        chart_card("Age Distribution", "Distribution of respondent age")
        fig = px.histogram(df, x="Age", nbins=25, color_discrete_sequence=[BLUE])
        plotly_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Top Countries", "Top 10 countries by respondent count")
        tc = df["Country"].value_counts().head(10).sort_values()
        fig2 = go.Figure(go.Bar(x=tc.values, y=tc.index, orientation="h", marker_color=TEAL))
        plotly_theme(fig2, height=340, show_legend=False)
        st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    with right:
        chart_card("Gender Distribution", "Standardized gender categories")
        g = df["Gender"].value_counts()
        fig3 = go.Figure(data=[go.Pie(labels=g.index, values=g.values, hole=0.6,
                                       marker=dict(colors=PALETTE_MUTED))])
        plotly_theme(fig3, height=280)
        st.plotly_chart(fig3, width="stretch", config={"displayModeBar": False})
        chart_card_end()

        chart_card("Company Size", "Number of employees at respondent's company")
        order = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
        s = df["no_employees"].value_counts().reindex([o for o in order if o in df["no_employees"].unique()])
        fig4 = go.Figure(go.Bar(x=s.index, y=s.values, marker_color=VIOLET))
        plotly_theme(fig4, height=300, show_legend=False)
        fig4.update_xaxes(tickangle=-20)
        st.plotly_chart(fig4, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    top_c = df["Country"].value_counts().idxmax()
    top_c_pct = pct(df["Country"].value_counts().max(), n)
    insight_card(
        f"Among the filtered responses, {top_c_pct}% are from {top_c}, and the sample skews "
        f"toward respondents in their late 20s to mid-30s — findings should be read as most "
        f"representative of that demographic."
    )


# ===========================================================================
# PAGE 6 — INTERACTIVE EXPLORER
# ===========================================================================
EXPLORABLE_COLS = [
    "Gender", "Country", "no_employees", "remote_work", "tech_company", "benefits",
    "care_options", "wellness_program", "seek_help", "anonymity", "leave",
    "mental_health_consequence", "phys_health_consequence", "coworkers", "supervisor",
    "mental_health_interview", "phys_health_interview", "mental_vs_physical",
    "obs_consequence", "family_history", "work_interfere", "treatment",
]


def render_explorer(df):
    st.markdown('<div class="section-title fade-in">Interactive Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Build your own cross-tabulation and inspect the filtered data</div>',
                unsafe_allow_html=True)

    n = len(df)
    cols = st.columns(3)
    kpi_card(cols[0], "Rows in View", f"{n:,}", "After current filters", BLUE)
    kpi_card(cols[1], "Columns Available", f"{len(EXPLORABLE_COLS)}", "Explorable survey variables", VIOLET)
    kpi_card(cols[2], "Treatment Rate", f"{pct((df['treatment']=='Yes').sum(), n)}%",
              "Within current selection", TEAL)

    chart_card("Custom Cross-Tabulation", "Pick any two variables to compare")
    c1, c2 = st.columns(2)
    with c1:
        var_x = st.selectbox("Row variable", EXPLORABLE_COLS,
                              index=EXPLORABLE_COLS.index("no_employees"), key="explorer_x")
    with c2:
        remaining = [c for c in EXPLORABLE_COLS if c != var_x]
        var_y = st.selectbox("Column variable", remaining,
                              index=remaining.index("treatment") if "treatment" in remaining else 0,
                              key="explorer_y")

    ct = pd.crosstab(df[var_x], df[var_y], normalize="index").mul(100).round(1)
    fig = go.Figure()
    for i, col in enumerate(ct.columns):
        fig.add_trace(go.Bar(name=str(col), x=ct.index, y=ct[col],
                              marker_color=PALETTE_MUTED[i % len(PALETTE_MUTED)]))
    fig.update_layout(barmode="stack", yaxis_title="% of row total")
    plotly_theme(fig, height=400)
    fig.update_xaxes(tickangle=-15)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    chart_card_end()

    chart_card("Filtered Data Table", f"{n:,} rows matching current filters")
    st.dataframe(df.reset_index(drop=True), width="stretch", height=360)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv, "filtered_survey_data.csv", "text/csv")
    chart_card_end()

    insight_card(
        f"Among the filtered responses, cross-tabulating {var_x} against {var_y} shows how "
        f"treatment and workplace-support patterns shift across groups — use the selectors "
        f"above to test your own hypotheses about the data."
    )


# ===========================================================================
# PAGE 7 — KEY FINDINGS
# ===========================================================================
def render_findings(df, full_df):
    st.markdown('<div class="section-title fade-in">Key Findings</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Correlation structure and headline takeaways from the dataset</div>',
                unsafe_allow_html=True)

    corr_df = pd.DataFrame(index=df.index)
    corr_df["Age"] = df["Age"]
    corr_df["treatment"] = df["treatment"].map({"Yes": 1, "No": 0})
    corr_df["family_history"] = df["family_history"].map({"Yes": 1, "No": 0})
    corr_df["work_interfere"] = df["work_interfere"].map(
        {"Not applicable": -1, "Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3})
    corr_df["remote_work"] = df["remote_work"].map({"Yes": 1, "No": 0})
    corr_df["tech_company"] = df["tech_company"].map({"Yes": 1, "No": 0})
    corr_df["benefits"] = df["benefits"].map({"Yes": 1, "Don't know": 0.5, "No": 0})
    corr_df["care_options"] = df["care_options"].map({"Yes": 1, "Not sure": 0.5, "No": 0})
    corr_df["anonymity"] = df["anonymity"].map({"Yes": 1, "Don't know": 0.5, "No": 0})
    corr_df["obs_consequence"] = df["obs_consequence"].map({"Yes": 1, "No": 0})
    corr_df = corr_df.dropna()

    n = len(df)
    treated = (df["treatment"] == "Yes").sum()

    # Correlation is only meaningful with enough rows and actual variation in
    # each column. A narrow filter selection (e.g. "Treatment: Yes" alone, or
    # very few matching rows) can make a column constant, which makes its
    # correlation with everything else undefined (NaN) rather than wrong —
    # so we detect that case and explain it instead of crashing on it.
    MIN_ROWS_FOR_CORRELATION = 10
    varying_cols = [c for c in corr_df.columns if corr_df[c].nunique(dropna=True) > 1]
    can_correlate = (
        len(corr_df) >= MIN_ROWS_FOR_CORRELATION
        and "treatment" in varying_cols
        and len(varying_cols) > 1
    )

    cols = st.columns(4)
    kpi_card(cols[0], "Responses Analyzed", f"{n:,}", "In current filtered view", BLUE)
    kpi_card(cols[1], "Treatment Rate", f"{pct(treated, n)}%", "Sought treatment", VIOLET)

    if can_correlate:
        corr_all = corr_df[varying_cols].corr()
        ranked_full = corr_all["treatment"].drop("treatment").abs().dropna().sort_values(ascending=False)
        if len(ranked_full):
            top_corr = ranked_full.idxmax()
            top_corr_val = ranked_full.max()
            kpi_card(cols[2], "Strongest Correlate", top_corr.replace("_", " ").title(),
                      f"r = {top_corr_val:.2f} with treatment", TEAL)
        else:
            can_correlate = False
    if not can_correlate:
        kpi_card(cols[2], "Strongest Correlate", "N/A",
                  "Not enough variation in current filters", TEAL)
    kpi_card(cols[3], "Variables Compared", f"{len(varying_cols)}", "With variation in current view", CORAL)

    if not can_correlate:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        insight_card(
            "Correlation analysis needs both a reasonable number of responses and some "
            "variation in each variable. Your current filters have narrowed the data down "
            "too far for a meaningful correlation (often because a filter like Treatment or "
            "Family History pins a variable to a single value). Try removing a filter or two "
            "to see the correlation matrix and rankings."
        )
        return

    left, right = st.columns([1.3, 1])

    with left:
        chart_card("Correlation Matrix", "Encoded workplace and demographic variables vs. treatment")
        fig = go.Figure(data=go.Heatmap(
            z=corr_all.values, x=corr_all.columns, y=corr_all.columns,
            colorscale=[[0, CORAL], [0.5, "#151A2C"], [1, BLUE]],
            zmin=-1, zmax=1, text=corr_all.round(2).values, texttemplate="%{text}",
            colorbar=dict(tickfont=dict(color=TEXT_SECONDARY)),
        ))
        plotly_theme(fig, height=440, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    with right:
        chart_card("What Correlates with Treatment", "Absolute correlation strength, ranked")
        ranked = ranked_full.sort_values()
        fig2 = go.Figure(go.Bar(x=ranked.values, y=[c.replace("_", " ").title() for c in ranked.index],
                                 orientation="h", marker_color=PALETTE_MUTED))
        fig2.update_layout(xaxis_title="Absolute correlation with treatment")
        plotly_theme(fig2, height=440, show_legend=False)
        st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        chart_card_end()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    fam_yes = pct((df[df["family_history"] == "Yes"]["treatment"] == "Yes").sum(),
                  max((df["family_history"] == "Yes").sum(), 1))
    fam_no = pct((df[df["family_history"] == "No"]["treatment"] == "Yes").sum(),
                 max((df["family_history"] == "No").sum(), 1))
    insight_card(
        f"Among the filtered responses, family history shows one of the strongest links to "
        f"treatment-seeking: {fam_yes}% of respondents with a family history sought "
        f"treatment, versus {fam_no}% without one."
    )

    know_benefits = df[df["benefits"] == "Yes"]
    dont_know_benefits = df[df["benefits"] == "Don't know"]
    kb_rate = pct((know_benefits["treatment"] == "Yes").sum(), max(len(know_benefits), 1))
    dkb_rate = pct((dont_know_benefits["treatment"] == "Yes").sum(), max(len(dont_know_benefits), 1))
    insight_card(
        f"Responses indicate awareness matters: {kb_rate}% of respondents who know their "
        f"employer offers mental health benefits sought treatment, compared to {dkb_rate}% "
        f"among those unsure whether benefits exist at all."
    )

    size_rates = df.groupby("no_employees")["treatment"].apply(lambda s: pct((s == "Yes").sum(), len(s)))
    insight_card(
        f"Company size shows little relationship with treatment-seeking in the filtered data: "
        f"rates range narrowly from {size_rates.min():.1f}% to {size_rates.max():.1f}% across "
        f"company-size groups, suggesting headcount alone doesn't predict support outcomes."
    )
