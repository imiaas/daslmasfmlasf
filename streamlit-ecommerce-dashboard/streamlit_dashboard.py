import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- Configuration --- #
st.set_page_config(
    page_title="E-commerce Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions to Load Data --- #
import os
import pandas as pd
import streamlit as st

# --- Helper Functions to Load Data ---
import os
import pandas as pd
import streamlit as st

# --- Helper Functions to Load Data ---
@st.cache_data
def load_data_from_excel(local_path, github_url=None):
    try:
        if os.path.exists(local_path):
            df = pd.read_excel(local_path, engine="openpyxl")
            return df
        elif github_url:
            df = pd.read_excel(github_url, engine="openpyxl")
            return df
        else:
            st.error(f"File not found: {local_path}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading file '{local_path}': {e}")
        return pd.DataFrame()

# --- Base directory (lokal) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dummy_data_dir = os.path.join(BASE_DIR, "dummy_data")

# --- GitHub raw base URL ---
# Ganti USERNAME & REPO sesuai punyamu
github_base_url = "https://raw.githubusercontent.com/imiaas/daslmasfmlasf/streamlit-ecommerce-dashboard/dummy_data"

# --- Load each Excel file ---
df_customers = load_data_from_excel(
    os.path.join(dummy_data_dir, "customers.xlsx"),
    f"{github_base_url}/customers.xlsx"
)

df_vendors = load_data_from_excel(
    os.path.join(dummy_data_dir, "vendors.xlsx"),
    f"{github_base_url}/vendors.xlsx"
)

df_inventory = load_data_from_excel(
    os.path.join(dummy_data_dir, "inventory.xlsx"),
    f"{github_base_url}/inventory.xlsx"
)

df_transactions = load_data_from_excel(
    os.path.join(dummy_data_dir, "transaction.xlsx"),
    f"{github_base_url}/transaction.xlsx"
)

df_shipping = load_data_from_excel(
    os.path.join(dummy_data_dir, "shipping.xlsx"),
    f"{github_base_url}/shipping.xlsx"
)



# --- Data Preprocessing (if DataFrames are not empty) --- #
if not df_transactions.empty:
    df_transactions["totalSales"] = pd.to_numeric(df_transactions["totalSales"], errors='coerce').fillna(0)
    df_transactions["totalEarings"] = pd.to_numeric(df_transactions["totalEarings"], errors='coerce').fillna(0)
    # Create a simple transaction date based on row index (for demo purposes)
    df_transactions["transactionDate"] = pd.date_range(start='2024-01-01', periods=len(df_transactions), freq='D')

if not df_inventory.empty:
    df_inventory["Price"] = pd.to_numeric(df_inventory["Price"], errors='coerce').fillna(0)
    df_inventory["incomingDate"] = pd.to_datetime(df_inventory["incomingDate"], errors='coerce')

# --- Dashboard Title and Filters --- #
st.title("📊 E-commerce Executive Dashboard")
st.markdown("A quick overview of sales, inventory, customer, and shipping performance.")

# Date Filter
st.subheader("📅 Time Period Filter")
filter_option = st.selectbox(
    "Select Time Period:",
    ["Last 30 Days", "Last 60 Days", "Last 90 Days", "Custom Range"]
)

if filter_option == "Last 30 Days":
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
elif filter_option == "Last 60 Days":
    start_date = datetime.now() - timedelta(days=60)
    end_date = datetime.now()
elif filter_option == "Last 90 Days":
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
else:  # Custom Range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

st.info(f"Showing data from {start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date} to {end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date}")

# Filter transactions by date
if not df_transactions.empty:
    filtered_transactions = df_transactions[
        (df_transactions["transactionDate"] >= pd.to_datetime(start_date))
        & (df_transactions["transactionDate"] <= pd.to_datetime(end_date))
    ]
else:
    filtered_transactions = pd.DataFrame()

# --- KPI Section --- #
st.header("Key Performance Indicators")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

# Total Sales
with kpi_col1:
    total_sales = filtered_transactions["totalSales"].sum() if not filtered_transactions.empty else 0
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

# Total Earnings
with kpi_col2:
    total_earnings = filtered_transactions["totalEarings"].sum() if not filtered_transactions.empty else 0
    st.metric(label="Total Earnings", value=f"${total_earnings:,.2f}")

# Number of Customers
with kpi_col3:
    num_customers = df_customers["customerID"].nunique() if not df_customers.empty else 0
    st.metric(label="Total Customers", value=num_customers)

# Delayed Shipments
with kpi_col4:
    delayed_shipments = df_shipping[df_shipping["delayFlag"] == True].shape[0] if not df_shipping.empty else 0
    st.metric(label="Delayed Shipments", value=delayed_shipments)

# --- Sales Performance Section --- #
st.header("Sales Performance")

if not filtered_transactions.empty:
    # Sales by Channel
    st.subheader("Sales by Channel")
    sales_by_channel = filtered_transactions.groupby("notes")["totalSales"].sum().sort_values(ascending=False)
    st.bar_chart(sales_by_channel)

    # Sales Trends (Daily)
    st.subheader("Daily Sales Trend")
    daily_sales = filtered_transactions.groupby(filtered_transactions["transactionDate"].dt.date)["totalSales"].sum()
    st.line_chart(daily_sales)
else:
    st.info("No sales data available for the selected date range.")

# --- Inventory Management Section --- #
st.header("Inventory Management")

if not df_inventory.empty:
    # Total Inventory Value
    total_inventory_value = df_inventory[df_inventory["availability"] == "In Stock"]["Price"].sum()
    st.metric(label="Total Inventory Value (In Stock)", value=f"${total_inventory_value:,.2f}")

    # Low Stock / Out of Stock Items
    low_stock_items = df_inventory[df_inventory["availability"] == "Low Stock"]
    out_of_stock_items = df_inventory[df_inventory["availability"] == "Out of Stock"]

    st.subheader("Inventory Status")
    col_inv1, col_inv2 = st.columns(2)
    with col_inv1:
        st.warning(f"Low Stock Items: {low_stock_items.shape[0]}")
        if not low_stock_items.empty:
            st.dataframe(low_stock_items[["nameInventory", "Brand", "availability"]])
    with col_inv2:
        st.error(f"Out of Stock Items: {out_of_stock_items.shape[0]}")
        if not out_of_stock_items.empty:
            st.dataframe(out_of_stock_items[["nameInventory", "Brand", "availability"]])

    # Inventory by Type
    st.subheader("Inventory by Type")
    inventory_by_type = df_inventory.groupby("type")["inventoryID"].count().sort_values(ascending=False)
    st.bar_chart(inventory_by_type)

else:
    st.info("No inventory data available.")

# --- Customer Insights Section --- #
st.header("Customer Insights")

if not df_customers.empty:
    # Customers by City
    st.subheader("Customers by City")
    customers_by_city = df_customers.groupby("city")["customerID"].count().sort_values(ascending=False)
    st.bar_chart(customers_by_city)
else:
    st.info("No customer data available.")

# --- Shipping & Fulfillment Section --- #
st.header("Shipping & Fulfillment")

if not df_shipping.empty:
    # Shipments by Carrier
    st.subheader("Shipments by Carrier")
    shipments_by_carrier = df_shipping.groupby("carrier")["shippingID"].count().sort_values(ascending=False)
    st.bar_chart(shipments_by_carrier)

    # On-Time Delivery Rate
    total_shipments = df_shipping.shape[0]
    on_time_shipments = df_shipping[df_shipping["delayFlag"] == False].shape[0]
    on_time_rate = (on_time_shipments / total_shipments) * 100 if total_shipments > 0 else 0
    st.metric(label="On-Time Delivery Rate", value=f"{on_time_rate:.2f}%")

else:
    st.info("No shipping data available.")

# --- Raw Data View (Optional) --- #
st.header("Raw Data (for debugging)")

with st.expander("View Customers Data"):
    st.dataframe(df_customers)
with st.expander("View Vendors Data"):
    st.dataframe(df_vendors)
with st.expander("View Inventory Data"):
    st.dataframe(df_inventory)
with st.expander("View Transactions Data"):
    st.dataframe(df_transactions)
with st.expander("View Shipping Data"):
    st.dataframe(df_shipping)

