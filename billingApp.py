import streamlit as st

# Title
st.title("Supermarket Billing App 🛒")

# Input: Customer Details
st.header("Customer Details")
customer_name = st.text_input("Customer Name")
customer_phone = st.text_input("Customer Phone Number")

# Input: Itemsss
st.header("Add Items")
num_items = st.number_input("How many different items?", min_value=1, max_value=50, value=1, step=1)

items = []
for i in range(int(num_items)):
    st.subheader(f"Item {i+1}")
    name = st.text_input(f"Item Name {i+1}", key=f"name{i}")
    qty = st.number_input(f"Quantity {i+1}", min_value=1, key=f"qty{i}")
    price = st.number_input(f"Price per unit {i+1}", min_value=0.0, key=f"price{i}")
    items.append({"name": name, "qty": qty, "price": price})

# Discount
discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0)

# Calculate Total
if st.button("Generate Bill"):
    st.header("Invoice 🧾")
    total_amount = 0
    for item in items:
        item_total = item['qty'] * item['price']
        total_amount += item_total
        st.write(f"{item['name']} - {item['qty']} x ₹{item['price']} = ₹{item_total}")

    discount_amount = (total_amount * discount) / 100
    net_total = total_amount - discount_amount

    st.write(f"**Total:** ₹{total_amount}")
    st.write(f"**Discount ({discount}%):** ₹{discount_amount}")
    st.write(f"**Net Total:** ₹{net_total}")

    st.success(f"Thank you {customer_name}! Your bill amount is ₹{net_total}")
