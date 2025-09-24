import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Simple Splitter", layout="centered")

st.title("💰 Splitwise-like Expense Splitter (Streamlit)")
st.write("Add people and their contributions — the app calculates who owes whom and provides a minimal set of settlement transactions.")

# --- Input area ---
st.header("1) Add Participants & Contributions")

with st.form("add_expense", clear_on_submit=True):
    name = st.text_input("Person name", key="name_input")
    amount = st.number_input("Contribution amount (₹)", min_value=0.0, format="%.2f", key="amt_input")
    desc = st.text_input("Optional note / description", key="desc_input")
    submitted = st.form_submit_button("Add / Save")

    if submitted:
        if not name:
            st.warning("Please enter a name.")
        else:
            # initialize session state
            if "data" not in st.session_state:
                st.session_state.data = []
            st.session_state.data.append(
                {"name": name.strip(), "amount": float(amount), "note": desc.strip()}
            )
            st.success(f"Added: {name} — ₹{amount:.2f}")

# Show current list
st.write("---")
st.subheader("Current Contributions (all entries)")
if "data" not in st.session_state or len(st.session_state.data) == 0:
    st.info("No contributions yet. Add people and their contribution amounts above.")
else:
    df = pd.DataFrame(st.session_state.data)
    df.index = range(1, len(df) + 1)
    st.dataframe(df.style.format({"amount": "₹{:.2f}"}), height=220)

    # --- Person-wise total ---
    totals = df.groupby("name", as_index=False)["amount"].sum()
    totals = totals.round(2)

    st.subheader("2) Person-wise Totals")
    st.dataframe(totals.style.format({"amount": "₹{:.2f}"}))

    # Overall totals
    total = totals["amount"].sum()
    n = len(totals)
    fair_share = total / n if n else 0.0
    balances = (totals.set_index("name")["amount"] - fair_share).round(2)

    st.write(f"**Overall total contributed:** ₹{total:.2f}")
    st.write(f"**Number of people:** {n}")
    st.write(f"**Fair share per person:** ₹{fair_share:.2f}")
    st.write("---")

    st.subheader("3) Net Balances (positive = should receive, negative = should pay)")
    bal_df = balances.reset_index()
    bal_df.columns = ["name", "balance"]
    st.dataframe(bal_df.style.format({"balance": "₹{:.2f}"}))

    # Settlement algorithm (greedy)
    st.subheader("4) Suggested Settlements (min transactions)")
    creditors = [(name, bal) for name, bal in balances.items() if bal > 0.009]
    debtors = [(name, bal) for name, bal in balances.items() if bal < -0.009]

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1])

    settlements = []
    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        cred_name, cred_amt = creditors[i]
        debt_name, debt_amt = debtors[j]
        transfer = min(cred_amt, -debt_amt)
        transfer = round(transfer, 2)
        settlements.append({"from": debt_name, "to": cred_name, "amount": transfer})
        creditors[i] = (cred_name, round(creditors[i][1] - transfer, 2))
        debtors[j] = (debt_name, round(debtors[j][1] + transfer, 2))
        if abs(creditors[i][1]) < 0.01:
            i += 1
        if abs(debtors[j][1]) < 0.01:
            j += 1

    if len(settlements) == 0:
        st.success("✅ All settled — no transfers needed.")
    else:
        settle_df = pd.DataFrame(settlements)
        settle_df.index = range(1, len(settle_df) + 1)
        st.table(settle_df.style.format({"amount": "₹{:.2f}"}))

    # Export CSV
    csv_buf = StringIO()
    out_df = pd.DataFrame(st.session_state.data)
    out_df.to_csv(csv_buf, index=False)
    st.download_button(
        "⬇️ Download contributions CSV",
        csv_buf.getvalue(),
        file_name="contributions.csv",
        mime="text/csv",
    )

    # Clear data button
    if st.button("🗑️ Clear all contributions"):
        del st.session_state.data
        st.experimental_rerun()

st.write("---")
st.info("Usage tips: Add each person's name and the amount they paid. "
        "Multiple expenses per person are supported — they will be combined automatically. "
        "The app assumes everyone shares costs equally.")
