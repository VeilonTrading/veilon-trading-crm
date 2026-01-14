import streamlit as st
from veilon_core.db import execute_query
from millify import millify

def render_header():
    with st.container(border=False, horizontal=True, vertical_alignment="center"):
        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ):
            st.subheader(f"Payouts", anchor=False)

        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="center",
        ):
            timeframe_selection = st.selectbox(
                key="timeframe-selection",
                label="Timeframe",
                options=("This Month", "Last Month", "Today", "This Week", "This Quarter", "This Year", "All Time"),
                width=150,
                label_visibility="hidden",
            )

def payouts_page():
    render_header()

    trader_payouts_tab, affiliate_payouts_tab = st.tabs(["Traders", "Affiliates"])

    with trader_payouts_tab:
        with st.container(border=False, horizontal=True, horizontal_alignment="center"):
                with st.container(border=True): 
                    st.metric("Total Payouts", millify(123456, 2))

                with st.container(border=True): 
                    st.metric("Forecasted Payouts", millify(12345, 2))
                
                with st.container(border=True): 
                    st.metric("Pending Payouts", millify(1234, 2))

    with affiliate_payouts_tab:
        with st.container(border=False, horizontal=True, horizontal_alignment="center"):
                with st.container(border=True): 
                    st.metric("Total Affiliate Payouts", millify(123456, 2))

                with st.container(border=True): 
                    st.metric("Forecasted Affiliate Payouts", millify(12345, 2))
                
                with st.container(border=True): 
                    st.metric("Pending Affiliate Payouts", millify(1234, 2))

if __name__ == "__main__":
    payouts_page()