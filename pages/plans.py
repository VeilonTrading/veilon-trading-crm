import streamlit as st
from veilon_core.db import execute_query

def render_header():
    with st.container(border=False, horizontal=True, vertical_alignment="center"):
        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ):
            st.subheader(f"Plans", anchor=False)

def plans_page():
    render_header()

    plans_table = execute_query(
        """
        SELECT 
            *
        FROM plans;
        """)
    
    st.dataframe(plans_table)

if __name__ == "__main__":
    plans_page()