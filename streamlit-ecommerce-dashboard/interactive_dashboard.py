import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta

# --- Configuration --- #
st.set_page_config(
    page_title="Interactive E-commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stSelectbox > div > div > select {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions to Load Data --- #
@st.cache_data
def load_data_from_excel(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        st.error(f"Error: Excel file not found at {file_path}. Please ensure dummy data is generated.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data from sheet '{sheet_name}': {e}")
        return pd.DataFrame()

# --- Load All DataFrames from a single Excel file --- #
dummy_data_dir = "./dummy_data"
excel_file = os.path.join(dummy_data_dir, "ecommerce_data.xlsx")

df_customers = load_data_from_excel(excel_file, "customers")
df_vendors = load_data_from_excel(excel_file, "vendors")
df_inventory = load_data_from_excel(excel_file, "inventory")
df_transactions = load_data_from_excel(excel_file, "transaction")
df_shipping = load_data_from_excel(excel_file, "shipping")

# --- Data Preprocessing --- #
if not df_transactions.empty:
    df_transactions["totalSales"] = pd.to_numeric(df_transactions["totalSales"], errors='coerce').fillna(0)
    df_transactions["totalEarings"] = pd.to_numeric(df_transactions["totalEarings"], errors='coerce').fillna(0)
    # Create a more realistic transaction date based on row index
    df_transactions["transactionDate"] = pd.date_range(start='2024-01-01', periods=len(df_transactions), freq='D')
    
    # Add more columns for better interactivity
    df_transactions["month"] = df_transactions["transactionDate"].dt.strftime('%Y-%m')
    df_transactions["day_of_week"] = df_transactions["transactionDate"].dt.day_name()

if not df_inventory.empty:
    df_inventory["Price"] = pd.to_numeric(df_inventory["Price"], errors='coerce').fillna(0)
    df_inventory["incomingDate"] = pd.to_datetime(df_inventory["incomingDate"], errors='coerce')

# Merge data for better analysis
if not df_transactions.empty and not df_customers.empty:
    df_sales_analysis = df_transactions.merge(df_customers[['customerID', 'city', 'state']], on='customerID', how='left')
else:
    df_sales_analysis = df_transactions.copy() if not df_transactions.empty else pd.DataFrame()

# --- Sidebar Filters --- #
st.sidebar.header("🎛️ Interactive Filters")

# Date Filter
st.sidebar.subheader("📅 Time Period")
filter_option = st.sidebar.selectbox(
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
    start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=90))
    end_date = st.sidebar.date_input("End Date", datetime.now())

# Additional Interactive Filters
if not df_sales_analysis.empty:
    # Channel Filter
    channels = ['All'] + list(df_sales_analysis['notes'].unique())
    selected_channel = st.sidebar.selectbox("📱 Sales Channel:", channels)
    
    # City Filter
    cities = ['All'] + list(df_sales_analysis['city'].dropna().unique())
    selected_city = st.sidebar.selectbox("🏙️ City:", cities)
    
    # State Filter
    states = ['All'] + list(df_sales_analysis['state'].dropna().unique())
    selected_state = st.sidebar.selectbox("🗺️ State:", states)

# Inventory Filter
if not df_inventory.empty:
    brands = ['All'] + list(df_inventory['Brand'].unique())
    selected_brand = st.sidebar.selectbox("🏷️ Brand:", brands)

# --- Apply Filters --- #
if not df_sales_analysis.empty:
    # Date filter
    filtered_data = df_sales_analysis[
        (df_sales_analysis["transactionDate"] >= pd.to_datetime(start_date))
        & (df_sales_analysis["transactionDate"] <= pd.to_datetime(end_date))
    ]
    
    # Channel filter
    if selected_channel != 'All':
        filtered_data = filtered_data[filtered_data['notes'] == selected_channel]
    
    # City filter
    if selected_city != 'All':
        filtered_data = filtered_data[filtered_data['city'] == selected_city]
    
    # State filter
    if selected_state != 'All':
        filtered_data = filtered_data[filtered_data['state'] == selected_state]
else:
    filtered_data = pd.DataFrame()

# Filter inventory
if not df_inventory.empty:
    filtered_inventory = df_inventory.copy()
    if selected_brand != 'All':
        filtered_inventory = filtered_inventory[filtered_inventory['Brand'] == selected_brand]
else:
    filtered_inventory = pd.DataFrame()

# --- Dashboard Title --- #
st.title("📊 Interactive E-commerce Executive Dashboard")
st.markdown("**Click on charts to interact • Use sidebar filters to drill down • Real-time data updates**")

# Show active filters
active_filters = []
if selected_channel != 'All':
    active_filters.append(f"Channel: {selected_channel}")
if selected_city != 'All':
    active_filters.append(f"City: {selected_city}")
if selected_state != 'All':
    active_filters.append(f"State: {selected_state}")
if selected_brand != 'All':
    active_filters.append(f"Brand: {selected_brand}")

if active_filters:
    st.info(f"🔍 Active Filters: {' | '.join(active_filters)}")

st.info(f"📅 Showing data from {start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date} to {end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date}")

# --- KPI Section with Interactive Metrics --- #
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_data["totalSales"].sum() if not filtered_data.empty else 0
    st.metric(
        label="💰 Total Sales", 
        value=f"${total_sales:,.2f}",
        delta=f"{len(filtered_data)} transactions"
    )

with col2:
    total_earnings = filtered_data["totalEarings"].sum() if not filtered_data.empty else 0
    profit_margin = (total_earnings / total_sales * 100) if total_sales > 0 else 0
    st.metric(
        label="💵 Total Earnings", 
        value=f"${total_earnings:,.2f}",
        delta=f"{profit_margin:.1f}% margin"
    )

with col3:
    unique_customers = filtered_data["customerID"].nunique() if not filtered_data.empty else 0
    avg_order_value = total_sales / len(filtered_data) if not filtered_data.empty else 0
    st.metric(
        label="👥 Active Customers", 
        value=unique_customers,
        delta=f"${avg_order_value:.2f} AOV"
    )

with col4:
    delayed_shipments = df_shipping[df_shipping["delayFlag"] == True].shape[0] if not df_shipping.empty else 0
    total_shipments = df_shipping.shape[0] if not df_shipping.empty else 1
    delay_rate = (delayed_shipments / total_shipments * 100) if total_shipments > 0 else 0
    st.metric(
        label="🚚 Delayed Shipments", 
        value=delayed_shipments,
        delta=f"{delay_rate:.1f}% delay rate"
    )

# --- Interactive Charts Section --- #
if not filtered_data.empty:
    
    # Row 1: Sales Performance Charts
    st.header("📊 Interactive Sales Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💹 Sales Trend Over Time")
        daily_sales = filtered_data.groupby(filtered_data["transactionDate"].dt.date)["totalSales"].sum().reset_index()
        daily_sales.columns = ['Date', 'Sales']
        
        fig_trend = px.line(
            daily_sales, 
            x='Date', 
            y='Sales',
            title="Daily Sales Performance",
            markers=True
        )
        fig_trend.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.subheader("📱 Sales by Channel")
        channel_sales = filtered_data.groupby("notes")["totalSales"].sum().reset_index()
        channel_sales.columns = ['Channel', 'Sales']
        
        fig_channel = px.pie(
            channel_sales,
            values='Sales',
            names='Channel',
            title="Revenue Distribution by Channel"
        )
        fig_channel.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_channel, use_container_width=True)
    
    # Row 2: Geographic and Customer Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Sales by Geography")
        geo_sales = filtered_data.groupby("state")["totalSales"].sum().reset_index()
        geo_sales.columns = ['State', 'Sales']
        geo_sales = geo_sales.sort_values('Sales', ascending=False)
        
        fig_geo = px.bar(
            geo_sales,
            x='State',
            y='Sales',
            title="Sales Performance by State",
            color='Sales',
            color_continuous_scale='Blues'
        )
        fig_geo.update_layout(xaxis_title="State", yaxis_title="Sales ($)")
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with col2:
        st.subheader("📅 Sales by Day of Week")
        dow_sales = filtered_data.groupby("day_of_week")["totalSales"].sum().reset_index()
        dow_sales.columns = ['Day', 'Sales']
        
        # Order days properly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_sales['Day'] = pd.Categorical(dow_sales['Day'], categories=day_order, ordered=True)
        dow_sales = dow_sales.sort_values('Day')
        
        fig_dow = px.bar(
            dow_sales,
            x='Day',
            y='Sales',
            title="Sales Pattern by Day of Week",
            color='Sales',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_dow, use_container_width=True)

# --- Interactive Inventory Management --- #
st.header("📦 Interactive Inventory Management")

if not filtered_inventory.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Inventory Status Distribution
        st.subheader("📊 Inventory Status Overview")
        status_counts = filtered_inventory['availability'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig_status = px.bar(
            status_counts,
            x='Status',
            y='Count',
            title="Items by Availability Status",
            color='Status',
            color_discrete_map={
                'In Stock': '#2E8B57',
                'Low Stock': '#FF8C00',
                'Out of Stock': '#DC143C'
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)
        
        # Show critical items
        critical_items = filtered_inventory[filtered_inventory['availability'].isin(['Low Stock', 'Out of Stock'])]
        if not critical_items.empty:
            st.warning(f"⚠️ {len(critical_items)} items need attention!")
            st.dataframe(
                critical_items[['nameInventory', 'Brand', 'availability', 'Price']].head(10),
                use_container_width=True
            )
    
    with col2:
        # Inventory Value by Brand
        st.subheader("💰 Inventory Value by Brand")
        brand_value = filtered_inventory.groupby('Brand')['Price'].sum().reset_index()
        brand_value.columns = ['Brand', 'Total_Value']
        brand_value = brand_value.sort_values('Total_Value', ascending=False)
        
        fig_brand = px.treemap(
            brand_value,
            path=['Brand'],
            values='Total_Value',
            title="Inventory Value Distribution by Brand"
        )
        st.plotly_chart(fig_brand, use_container_width=True)
        
        # Top 10 Most Valuable Items
        st.subheader("💎 Top 10 Most Valuable Items")
        top_items = filtered_inventory.nlargest(10, 'Price')[['nameInventory', 'Brand', 'Price', 'availability']]
        st.dataframe(top_items, use_container_width=True)

# --- Interactive Shipping Analytics --- #
if not df_shipping.empty:
    st.header("🚚 Interactive Shipping Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Shipments by Carrier")
        carrier_counts = df_shipping['carrier'].value_counts().reset_index()
        carrier_counts.columns = ['Carrier', 'Shipments']
        
        fig_carrier = px.pie(
            carrier_counts,
            values='Shipments',
            names='Carrier',
            title="Shipment Distribution by Carrier"
        )
        st.plotly_chart(fig_carrier, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Delivery Performance")
        performance_data = df_shipping.groupby('carrier')['delayFlag'].agg(['count', 'sum']).reset_index()
        performance_data.columns = ['Carrier', 'Total_Shipments', 'Delayed_Shipments']
        performance_data['On_Time_Rate'] = ((performance_data['Total_Shipments'] - performance_data['Delayed_Shipments']) / performance_data['Total_Shipments'] * 100).round(2)
        
        fig_performance = px.bar(
            performance_data,
            x='Carrier',
            y='On_Time_Rate',
            title="On-Time Delivery Rate by Carrier (%)",
            color='On_Time_Rate',
            color_continuous_scale='RdYlGn'
        )
        fig_performance.update_layout(yaxis_title="On-Time Rate (%)")
        st.plotly_chart(fig_performance, use_container_width=True)

# --- Data Export and Download --- #
st.header("📥 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    if not filtered_data.empty:
        csv_sales = filtered_data.to_csv(index=False)
        st.download_button(
            label="📊 Download Sales Data",
            data=csv_sales,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col2:
    if not filtered_inventory.empty:
        csv_inventory = filtered_inventory.to_csv(index=False)
        st.download_button(
            label="📦 Download Inventory Data",
            data=csv_inventory,
            file_name=f"inventory_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col3:
    if not df_shipping.empty:
        csv_shipping = df_shipping.to_csv(index=False)
        st.download_button(
            label="🚚 Download Shipping Data",
            data=csv_shipping,
            file_name=f"shipping_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# --- Footer --- #
st.markdown("---")
st.markdown("**💡 Pro Tip:** Use the sidebar filters to drill down into specific segments. Click on chart elements for more details!")

# Show data freshness
st.caption(f"📊 Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

