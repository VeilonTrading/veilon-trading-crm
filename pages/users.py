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
            st.subheader(f"Users", anchor=False)

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

def users_page():
    render_header()

    with st.container(border=False, horizontal=True, horizontal_alignment="center"):
            with st.container(border=True): 
                st.metric("Total Users", millify(1234, 2))

            with st.container(border=True): 
                st.metric("New Users", millify(123, 2))
            
            with st.container(border=True): 
                st.metric("Inactive Users", millify(453, 2))

    users_table = execute_query(
        """
        SELECT 
            *
        FROM users;
        """)
    
    st.dataframe(users_table)

if __name__ == "__main__":
    users_page()