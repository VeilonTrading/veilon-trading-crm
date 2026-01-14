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
            st.subheader(f"Orders", anchor=False)

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

def orders_page():
    render_header()

    with st.container(border=False, horizontal=True, horizontal_alignment="center"):
            with st.container(border=True): 
                st.metric("Total Revenue", millify(123456, 2))

            with st.container(border=True): 
                st.metric("Total Refunds", millify(12345, 2))
            
            with st.container(border=True): 
                st.metric("Payment Success Rate", "90.12%")



    orders_table = execute_query(
        """
        SELECT 
            *
        FROM orders;
        """)
    
    st.dataframe(orders_table)

if __name__ == "__main__":
    orders_page()