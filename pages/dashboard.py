import streamlit as st
import static.elements.metrics as metrics
from millify import millify
from numpy.random import default_rng as rng

changes = list(rng(4).standard_normal(20))
data = [sum(changes[:i]) for i in range(20)]
delta = round(data[-1], 2)


@st.dialog("Logout")
def logout_dialog():
    st.write("Are you sure you want to log out?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes", type="secondary", width="stretch"):
            st.logout()
    with col2:
        if st.button("No", type="secondary", width="stretch"):
            st.rerun()

def render_header():
    with st.container(border=False, horizontal=True, vertical_alignment="center"):
        # Left: welcome text
        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ):
            st.subheader(f"Welcome, {st.user.given_name}", anchor=False)

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


def dashboard_page():
    render_header()

    overview_tab, revenue_tab, payouts_tab = st.tabs(["Overview", "Revenue", "Payouts"])

    with overview_tab:
        with st.container(
                border=False,
                horizontal=True,
                horizontal_alignment="center"
            ):
                
                with st.container(
                    border=True,
                ): 
                    st.metric(
                        "New Users", 
                        millify(321),
                        delta=delta,
                        delta_color="off"
                        )

                with st.container(
                    border=True,
                ): 
                    st.metric(
                        "New Accounts", 
                        millify(198),
                        delta=delta,
                        delta_color="off"
                        )
                
                with st.container(
                    border=True,
                ): 
                    st.metric(
                        "New Accounts", 
                        millify(198),
                        delta=delta,
                        delta_color="off"
                        )
                    
        with st.container(
                border=False,
                horizontal=True,
                horizontal_alignment="center"
            ):
                with st.container(
                    border=True,
                ): 
                    st.metric(
                        "Revenue", 
                        millify(101250),
                        chart_data=data,
                        chart_type="line",
                        delta=delta,
                        delta_color="off"
                        )

                with st.container(
                    border=True,
                ): 
                    st.metric(
                        "Payouts", 
                        millify(32120),
                        chart_data=data,
                        chart_type="bar",
                        delta=delta,
                        delta_color="off"
                        )
        
if __name__ == "__main__":
    dashboard_page()