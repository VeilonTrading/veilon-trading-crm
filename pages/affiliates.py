import streamlit as st
from veilon_core.db import execute_query
import pandas as pd

def render_header():
    with st.container(border=False, horizontal=True, vertical_alignment="center"):
        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ):
            st.subheader(f"Affiliates", anchor=False)

def affiliates_page():
    render_header()

    
if __name__ == "__main__":
    affiliates_page()