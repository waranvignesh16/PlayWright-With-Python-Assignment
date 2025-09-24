import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Restaurant Order & Billing 🍔", layout="wide")

# --- Initialize session state ---
if "menu" not in st.session_state:
    st.session_state.menu = {
        "Burger": 120,
        "Pizza": 250,
        "Pasta": 180,
        "Sandwich": 100,
        "French Fries": 80,
        "Coke": 50,
    }

if "orders" not in st.session_state:
    st.session_state.orders = []

# Order statuses
status_flow = ["New", "Preparing", "Ready", "Served"]

# --- Sidebar navigation ---
st.sidebar.title("🍽 Restaurant System")
view = st.sidebar.radio(
    "Choose a View",
    ["Customer View", "Kitchen View", "Admin / Manager View"]
)

# ======================================================
# CUSTOMER VIEW
# ======================================================
if view == "Customer View":
    st.title("👨‍🍳 Customer Order Placement")

    # Customer Info
    st.subheader("👤 Customer Details")
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Name")
    with col2:
        customer_phone = st.text_input("Phone")

    order_items = {}
    st.subheader("🛒 Place Your Order")
    for item, price in st.session_state.menu.items():
        qty = st.number_input(f"{item} (₹{price})", min_value=0, step=1, key=f"cust_{item}")
        if qty > 0:
            order_items[item] = qty

    if st.button("✅ Confirm Order"):
        if customer_name and order_items:
            st.session_state.orders.append({
                "order_id": len(st.session_state.orders) + 1,
                "customer": customer_name,
                "phone": customer_phone,
                "items": order_items,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "New"
            })
            st.success("Order placed successfully! 🎉")
            st.rerun()
        else:
            st.error("Please fill customer name and select at least one item.")

    # Show latest bill
    if st.session_state.orders:
        st.subheader("🧾 Latest Bill")
        latest_order = st.session_state.orders[-1]
        bill_data = []
        subtotal = 0
        for item, qty in latest_order["items"].items():
            price = st.session_state.menu[item]
            total = qty * price
            subtotal += total
            bill_data.append({"Item": item, "Qty": qty, "Price": price, "Total": total})

        df = pd.DataFrame(bill_data)
        st.table(df)

        tax = round(subtotal * 0.05, 2)
        grand_total = subtotal + tax
        st.write(f"**Subtotal:** ₹{subtotal}")
        st.write(f"**Tax (5%):** ₹{tax}")
        st.success(f"Grand Total: ₹{grand_total}")

# ======================================================
# KITCHEN VIEW
# ======================================================
elif view == "Kitchen View":
    st.title("👨‍🍳 Kitchen Dashboard")

    if st.session_state.orders:
        df_orders = []
        for order in st.session_state.orders:
            for item, qty in order["items"].items():
                df_orders.append({
                    "Order ID": order["order_id"],
                    "Customer": order["customer"],
                    "Item": item,
                    "Qty": qty,
                    "Status": order["status"],
                    "Time": order["time"]
                })

        df = pd.DataFrame(df_orders)
        st.dataframe(df, use_container_width=True)

        # Update order status
        st.subheader("🔄 Update Order Status")
        order_ids = [o["order_id"] for o in st.session_state.orders]
        order_choice = st.selectbox("Select Order ID", order_ids)
        new_status = st.selectbox("Update Status", status_flow)

        if st.button("Update"):
            for o in st.session_state.orders:
                if o["order_id"] == order_choice:
                    o["status"] = new_status
            st.success(f"✅ Order {order_choice} updated to {new_status}")
            st.rerun()
    else:
        st.info("No active orders yet.")

# ======================================================
# ADMIN / MANAGER VIEW
# ======================================================
elif view == "Admin / Manager View":
    st.title("🛠 Admin / Manager Dashboard")

    st.subheader("📋 Menu Management")
    for item, price in list(st.session_state.menu.items()):
        new_price = st.number_input(f"{item} Price", min_value=10, max_value=2000, value=price, step=10, key=f"adm_{item}")
        st.session_state.menu[item] = new_price

    if st.button("Reset Orders"):
        st.session_state.orders = []
        st.success("All orders cleared!")
        st.rerun()

    st.subheader("📊 Sales Report")
    if st.session_state.orders:
        all_data = []
        for o in st.session_state.orders:
            for item, qty in o["items"].items():
                all_data.append({
                    "Order ID": o["order_id"],
                    "Customer": o["customer"],
                    "Item": item,
                    "Qty": qty,
                    "Price": st.session_state.menu[item],
                    "Total": qty * st.session_state.menu[item],
                    "Status": o["status"],
                    "Time": o["time"]
                })
        df = pd.DataFrame(all_data)
        st.dataframe(df, use_container_width=True)

        st.write("**Total Sales:** ₹", df["Total"].sum())
        best_item = df.groupby("Item")["Qty"].sum().idxmax()
        st.write("🏆 Best-selling Item:", best_item)

        # Export sales report
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Sales Report (CSV)",
            csv,
            "sales_report.csv",
            "text/csv"
        )
    else:
        st.info("No sales data yet.")
