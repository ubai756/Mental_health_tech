"""
Mental Health in Tech — Workplace Mental Health Intelligence
A glassmorphism analytics dashboard over the 2014 OSMI survey dataset.
"""

import streamlit as st

st.set_page_config(
    page_title="Mental Health in Tech",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

from common import (
    inject_css, load_data, filter_panel, render_header, NAV_ITEMS, TEXT_SECONDARY,
)
import pages_content as pc


def main():
    inject_css()
    df = load_data()
    render_header()

    with st.sidebar:
        st.markdown(
            f'<div style="padding: 6px 10px 16px 10px; color:{TEXT_SECONDARY}; '
            f'font-size:0.72rem; letter-spacing:1.2px; text-transform:uppercase; font-weight:700;">'
            f'Navigation</div>', unsafe_allow_html=True)
        page = st.radio("nav", NAV_ITEMS, label_visibility="collapsed", key="nav_page")

    filtered = filter_panel(df)

    if filtered.empty:
        st.warning("No responses match the current filters. Try clearing a filter.")
        return

    if page == NAV_ITEMS[0]:
        pc.render_overview(filtered, df)
    elif page == NAV_ITEMS[1]:
        pc.render_mental_health(filtered)
    elif page == NAV_ITEMS[2]:
        pc.render_workplace(filtered)
    elif page == NAV_ITEMS[3]:
        pc.render_treatment(filtered)
    elif page == NAV_ITEMS[4]:
        pc.render_demographics(filtered)
    elif page == NAV_ITEMS[5]:
        pc.render_explorer(filtered)
    elif page == NAV_ITEMS[6]:
        pc.render_findings(filtered, df)


if __name__ == "__main__":
    main()
