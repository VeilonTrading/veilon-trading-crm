import streamlit as st
from streamlit_extras.switch_page_button import switch_page

@st.dialog("Logout", dismissible=False)
def logout_dialog():
    st.write("Are you sure you want to log out?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes", type="secondary", width="stretch"):
            st.logout()
    with col2:
        if st.button("No", type="secondary", width="stretch"):
            #st.rerun()
            switch_page("dashboard.py")

def logout_page():
    logout_dialog()

if __name__ == "__main__":
    logout_page()