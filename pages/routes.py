import streamlit as st

DASHBOARD_PAGE = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/home:")
ACCOUNTS_PAGE = st.Page("pages/accounts.py", title="Accounts", icon=":material/account_circle:")
USERS_PAGE = st.Page("pages/users.py", title="Users", icon=":material/person:")
ORDERS_PAGE = st.Page("pages/orders.py", title="Orders", icon=":material/shopping_cart:")
AFFILIATES_PAGE = st.Page("pages/affiliates.py", title="Affiliates", icon=":material/groups:")
COUPONS_PAGE = st.Page("pages/coupons.py", title="Coupons", icon=":material/redeem:")
PAYOUTS_PAGE = st.Page("pages/payouts.py", title="Payouts", icon=":material/paid:")
PLANS_PAGE = st.Page("pages/plans.py", title="Plans", icon=":material/package_2:")
QUERY_PAGE = st.Page("pages/query.py", title="Custom Query", icon=":material/query_stats:")
LOGOUT = st.Page("pages/logout.py", title="Logout", icon=":material/logout:")

PAGES = [DASHBOARD_PAGE, ORDERS_PAGE, PAYOUTS_PAGE, ACCOUNTS_PAGE, USERS_PAGE, PLANS_PAGE, AFFILIATES_PAGE, COUPONS_PAGE, QUERY_PAGE, LOGOUT]