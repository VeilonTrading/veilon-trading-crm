import streamlit as st
from veilon_core.db import execute_query
import veilon_core.accounts as am
from millify import millify

ALLOWED_ACTIONS_BY_STATUS = {
    "Phase 1": ["Close", "Disable", "Reset", "Set Balance", "Deposit/Withdraw"],
    "Funded": ["Close", "Disable", "Reset", "Set Balance", "Deposit/Withdraw"],
    "In Review": ["Approve", "Reject", "Close"],
    "Closed": ["Re-Open"],
    "Disabled": ["Enable", "Close", "Reset", "Set Balance", "Deposit/Withdraw"],
}

def get_timeframe_filter(timeframe: str, column: str = "created_at") -> str:
    """
    Returns a SQL WHERE clause fragment for a given timeframe.
    """
    if timeframe == "Today":
        return f"{column}::date = CURRENT_DATE"

    if timeframe == "This Week":
        return f"{column} >= date_trunc('week', CURRENT_DATE)"

    if timeframe == "This Month":
        return f"{column} >= date_trunc('month', CURRENT_DATE)"

    if timeframe == "Last Month":
        return f"""
            {column} >= date_trunc('month', CURRENT_DATE - INTERVAL '1 month')
            AND {column} < date_trunc('month', CURRENT_DATE)
        """

    if timeframe == "This Quarter":
        return f"{column} >= date_trunc('quarter', CURRENT_DATE)"

    if timeframe == "This Year":
        return f"{column} >= date_trunc('year', CURRENT_DATE)"

    # All Time
    return "TRUE"


@st.dialog("New Account", dismissible=True, width="medium")
def create_account_dialog():
    col1, col2 = st.columns(2)

    with col1:
        user_rows = execute_query("SELECT id, email FROM users ORDER BY email;")
        user_options = ["Select User"] + [row["email"] for row in user_rows]
        user_selection = st.selectbox("User", user_options, index=0)

    with col2:
        plan_rows = execute_query("SELECT id, name FROM plans ORDER BY name;")
        plan_options = ["Select Plan Type"] + [row["name"] for row in plan_rows]
        plan_selection = st.selectbox("Plan Type", plan_options, index=0)

    if user_selection == "Select User" or plan_selection == "Select Plan Type":
        st.info("Select a user and a plan to continue.")
        st.button("Create Account", icon=":material/add:", type="primary", disabled=True)
        return

    # Resolve IDs (parameterised)
    user_id_rows = execute_query(
        "SELECT id FROM users WHERE email = %s;",
        (user_selection,),
    )
    if not user_id_rows:
        st.error("User not found.")
        return
    user_id = user_id_rows[0]["id"]

    plan_id_rows = execute_query(
        "SELECT id FROM plans WHERE name = %s;",
        (plan_selection,),
    )
    if not plan_id_rows:
        st.error("Plan not found.")
        return
    plan_id = plan_id_rows[0]["id"]

    if st.button("Create Account", icon=":material/add:", type="primary"):
        try:
            
            created = am.account_create(user_id=user_id, plan_id=plan_id, is_enabled=True)
            st.success(f"Account created (id={created['id']}).")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to create account: {e}")


@st.dialog("Account Info", dismissible=True, width="large")
def account_info_dialog(account_id):

    st.subheader("Account Details", anchor=False, divider="gray")
    st.write("User: ")
    st.write("Plan")
    st.write("Status: ")
    st.write("Opened at: ")
    st.write("Closed at: ")
    st.write("Funded at: ")
    st.write("Notes")

    st.subheader("Payout History", anchor=False, divider="gray")
    st.dataframe(execute_query("SELECT * FROM payouts "))

    st.subheader("Trade History", anchor=False, divider="gray")
    st.dataframe(execute_query("SELECT * FROM trades"))

    st.subheader("Events", anchor=False, divider="gray")
    st.dataframe(execute_query("SELECT * FROM events"))


@st.dialog("Set Balance", width="small")
def set_balance_dialog():
    account_id = st.session_state["selected_account_ids"][0]

    new_balance = st.number_input(
        "New Balance",
        min_value=0.0
    )

    if st.button("Apply", type="primary"):
        try:
            updated = am.account_set_balance(account_id, new_balance)
            st.toast(f"Balance set to {updated['balance']}")
            st.rerun()
        except ValueError as e:
            st.error(str(e))


@st.dialog("Deposit/Widthdraw", width="small")
def adjust_balance_dialog():
    account_id = st.session_state["selected_account_ids"][0]

    balance_delta = st.number_input(
        "Adjustment",
    )

    if st.button("Apply", type="primary"):
        try:
            updated = am.account_adjust_balance(account_id, balance_delta)
            st.toast(f"Balance set to {updated['balance']}")
            st.rerun()
        except ValueError as e:
            st.error(str(e))


@st.dialog("Account Actions", width="medium")
def account_actions_dialog():
    account_id = st.session_state.get("selected_account_ids", [None])[0]
    if account_id is None:
        st.warning("No account selected.")
        return

    acct = am.account_get(account_id)

    status = am.derive_status(acct)
    actions = ALLOWED_ACTIONS_BY_STATUS.get(status, [])

    col1, col2 = st.columns(2, vertical_alignment="top")
    with col1:
        st.text_input("Account ID", value=str(account_id), disabled=True)

    with col2:
        action = st.selectbox("Action", options=actions)

    st.write("")

    # ---- Action panels ----
    if action == "Enable":
        if st.button("Enable", type="primary", width="stretch"):
            am.account_set_active(account_id, True)
            st.success("Account enabled.")
            st.rerun()

    elif action == "Disable":
        if st.button("Disable", type="primary", width="stretch"):
            am.account_set_active(account_id, False)
            st.success("Account disabled.")
            st.rerun()

    elif action == "Close":
        close_reason = st.text_input("Close reason (optional)")
        if st.button("Close account", type="primary", width="stretch"):
            am.account_close(account_id, close_reason=close_reason)
            st.success("Account closed.")
            st.rerun()

    elif action == "Re-Open":
        if st.button("Re-open account", type="primary", width="stretch"):
            am.account_reopen(account_id)
            st.success("Account reopened.")
            st.rerun()

    elif action == "Set Balance":
        new_balance = st.number_input("New balance", min_value=0.0, step=100.0)
        if st.button("Apply", type="primary", width="stretch"):
            am.account_set_balance(account_id, new_balance)
            st.success("Balance updated.")
            st.rerun()

    elif action == "Deposit/Withdraw":
        amount = st.number_input("Amount (positive = deposit, negative = withdraw)", step=100.0)
        if st.button("Apply", type="primary", width="stretch"):
            am.account_adjust_balance(account_id, amount)
            st.success("Balance adjusted.")
            st.rerun()

    elif action == "Reset":
        confirm = st.checkbox("I understand this will reset the account state.")
        if st.button("Reset", type="primary", disabled=not confirm, width="stretch"):
            am.account_reset_phase(account_id, reset_phase=1)
            st.success("Account reset.")
            st.rerun()

    elif action == "Approve":
        if st.button("Approve", type="primary", width="stretch"):
            am.account_set_in_review(account_id, False)
            st.success("Review approved.")
            st.rerun()

    elif action == "Reject":
        reject_reason = st.text_input("Reject reason (optional)")
        if st.button("Reject", type="primary", width="stretch"):
            am.account_set_in_review(account_id, False, resolution="rejected", reason=reject_reason)
            st.success("Review rejected.")
            st.rerun()


@st.dialog("Accounts Filter", width="small")
def account_filters_dialog():
    st.write("Filters")

def render_header():
    with st.container(border=False, horizontal=True, vertical_alignment="center"):
        with st.container(
            border=False,
            horizontal=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ):
            st.subheader(f"Accounts", anchor=False)

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

def accounts_page():
    render_header()
    timeframe = st.session_state.get("timeframe-selection", "All Time")

    time_filter = get_timeframe_filter(timeframe, "created_at")

    with st.container(border=False, horizontal=True, horizontal_alignment="center"):
        with st.container(border=True):

            rows = execute_query("""
                SELECT COUNT(*) AS total_accounts
                FROM accounts;
            """)

            st.metric("Total Accounts", millify(rows[0]["total_accounts"], 2))

        with st.container(border=True):
            rows = execute_query(f"""
                SELECT COUNT(*) AS new_accounts
                FROM accounts
                WHERE {time_filter};
            """)

            st.metric("New Accounts", millify(rows[0]["new_accounts"], 2))

        with st.container(border=True):

            rows = execute_query("""
                SELECT COALESCE(SUM(balance), 0) AS total_funded_capital
                FROM accounts
                WHERE funded_at IS NOT NULL
                AND closed_at IS NOT NULL;
            """)

            total_funded_capital = rows[0]["total_funded_capital"] if rows else 0
            st.metric("Total Funded Capital", millify(total_funded_capital, 2))

    # Ensure keys exist
    if "has_accounts_selection" not in st.session_state:
        st.session_state["has_accounts_selection"] = False
    
    if "selected_account_ids" not in st.session_state:
        st.session_state["selected_account_ids"] = []

    has_selection = st.session_state["has_accounts_selection"]
    actions_dropdown = not has_selection  # disabled when no selection

    # ---- Actions bar (above table) ----
    with st.container(border=False, horizontal=True, horizontal_alignment="right"):
        # Initialise filter state once
        st.session_state.setdefault("accounts_filter_user", "")
        st.session_state.setdefault("accounts_filter_status", None)
        st.session_state.setdefault("accounts_filter_plan_id", None)

        with st.popover(
            "",
            width=40,
            type="tertiary",
            icon=":material/filter_alt:",
        ):
            user_input = st.text_input(
                "User",
                placeholder="Email or User ID",
                value=st.session_state["accounts_filter_user"],
            )

            status_sel = st.selectbox(
                "Status",
                options=["All"] + ["Phase 1", "Funded", "In Review", "Closed", "Disabled"],
                index=0 if st.session_state["accounts_filter_status"] is None
                else (["All", "Phase 1", "Funded", "In Review", "Closed", "Disabled"].index(st.session_state["accounts_filter_status"])),
            )

            plan_rows = execute_query("SELECT id, name FROM plans ORDER BY name;")
            plan_name_to_id = {r["name"]: r["id"] for r in plan_rows}
            plan_options = ["All Plans"] + list(plan_name_to_id.keys())

            current_plan_id = st.session_state["accounts_filter_plan_id"]
            current_plan_name = "All Plans"
            if current_plan_id is not None:
                # reverse lookup for UI display
                for n, pid in plan_name_to_id.items():
                    if pid == current_plan_id:
                        current_plan_name = n
                        break

            plan_name = st.selectbox(
                "Plan",
                options=plan_options,
                index=plan_options.index(current_plan_name) if current_plan_name in plan_options else 0,
            )

            if st.button("Apply", type="primary", use_container_width=True):
                # Save raw user input; resolve to user_id below (outside popover is fine too, but this is simplest)
                st.session_state["accounts_filter_user"] = user_input.strip()

                st.session_state["accounts_filter_status"] = None if status_sel == "All" else status_sel
                st.session_state["accounts_filter_plan_id"] = None if plan_name == "All Plans" else plan_name_to_id[plan_name]

                st.rerun()

        if st.button(
            "",
            key="actions-button",
            width=40,
            type="tertiary",
            icon=":material/settings:",
            disabled=actions_dropdown,
        ):
            account_actions_dialog()

        if st.button(
            "",
            key="info-button",
            width=40,
            type="tertiary",
            icon=":material/info:",
            disabled=actions_dropdown,
        ):
            account_info_dialog(id)

        if st.button(
            "",
            key="add-button",
            width=40,
            type="tertiary",
            icon=":material/add_circle:",
        ):
            create_account_dialog()


    # ---- Resolve user_input -> user_id (optional) ----
    user_filter = st.session_state.get("accounts_filter_user", "").strip()
    user_id_filter = None

    if user_filter:
        if user_filter.isdigit():
            user_id_filter = int(user_filter)
        else:
            rows = execute_query("SELECT id FROM users WHERE email = %s;", (user_filter,))
            user_id_filter = rows[0]["id"] if rows else -1  # -1 yields no results (safe)

    # ---- Render table with filters ----
    am.accounts_table(
        user_id=user_id_filter,
        status=st.session_state.get("accounts_filter_status"),
        plan_id=st.session_state.get("accounts_filter_plan_id"),
    )


if __name__ == "__main__":
    accounts_page()