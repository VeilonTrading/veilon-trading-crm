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
            st.subheader(f"Custom Query", anchor=False)

def query_page():
    render_header()

    query_input = st.text_input(label="Custom Query Input", placeholder="SELECT * FROM accounts;")

    if query_input:
        custom_table = execute_query(
            query_input)
        
        st.dataframe(custom_table)

if __name__ == "__main__":
    query_page()