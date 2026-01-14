import streamlit as st

def render_header():
    with st.container(border=False, horizontal=True, vertical_alignment="center"):
        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ):
            st.subheader(f"Coupons", anchor=False)

def coupons_page():
    render_header()

if __name__ == "__main__":
    coupons_page()