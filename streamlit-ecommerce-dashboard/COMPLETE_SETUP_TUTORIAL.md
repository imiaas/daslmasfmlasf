# Complete E-commerce Dashboard Setup Tutorial

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Overview](#project-overview)
3. [Installation Guide](#installation-guide)
4. [Data Setup](#data-setup)
5. [Running the Dashboard](#running-the-dashboard)
6. [Using Excel Files](#using-excel-files)
7. [Using Google Sheets (Advanced)](#using-google-sheets-advanced)
8. [Customization Guide](#customization-guide)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, make sure you have the following installed on your computer:

### Required Software
- **Python 3.7 or higher** - Download from [python.org](https://python.org)
- **VS Code** (which you already have) - Great for editing code
- **Command Prompt/Terminal** - Built into Windows/Mac/Linux

### Checking Your Python Installation
Open Command Prompt (Windows) or Terminal (Mac/Linux) and type:
```bash
python --version
```
or
```bash
python3 --version
```

You should see something like `Python 3.11.0` or similar. If not, install Python first.

---

## Project Overview

This dashboard provides comprehensive e-commerce analytics including:

### Key Features
- **Sales Performance**: Revenue tracking, channel analysis, daily trends
- **Inventory Management**: Stock levels, low-stock alerts, inventory value
- **Customer Insights**: Geographic distribution, customer metrics
- **Shipping Analytics**: Carrier performance, delivery rates, delay tracking
- **Interactive Filters**: Date range selection, real-time updates
- **Data Integration**: Support for Excel files and Google Sheets

### Technical Stack
- **Streamlit**: Web framework for Python
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file handling
- **Python**: Core programming language

---

## Installation Guide

### Step 1: Create Project Directory
1. Open Command Prompt/Terminal
2. Navigate to where you want to create the project:
   ```bash
   cd Desktop
   ```
3. Create a new folder:
   ```bash
   mkdir ecommerce-dashboard
   cd ecommerce-dashboard
   ```

### Step 2: Install Required Libraries
Copy and paste this command (all on one line):
```bash
pip install streamlit pandas openpyxl
```

**If you get permission errors on Mac/Linux, try:**
```bash
pip3 install streamlit pandas openpyxl
```

**If you get permission errors, try:**
```bash
pip install --user streamlit pandas openpyxl
```

### Step 3: Verify Installation
Test if Streamlit is installed correctly:
```bash
streamlit hello
```

This should open a web page with Streamlit's demo. Close it when done.

---


## Data Setup

### Step 4: Download Project Files
1. Extract the provided project files to your `ecommerce-dashboard` folder
2. You should have these files:
   ```
   ecommerce-dashboard/
   ├── streamlit_dashboard.py          # Basic dashboard
   ├── interactive_dashboard.py        # Advanced interactive version
   ├── generate_dummy_data.py          # Data generator
   ├── dummy_data/
   │   └── ecommerce_data.xlsx         # Sample data file
   └── COMPLETE_SETUP_TUTORIAL.md      # This tutorial
   ```

### Step 5: Generate Sample Data
Run this command to create sample data:
```bash
python generate_dummy_data.py
```

You should see: `All dummy data generated successfully in ./dummy_data/ecommerce_data.xlsx`

### Step 6: Verify Data Structure
The Excel file contains 5 sheets matching your requirements:
- **customers**: Customer information (ID, name, contact, location)
- **vendors**: Vendor details (ID, name, contact, items)
- **inventory**: Product inventory (ID, vendor, pricing, availability)
- **transaction**: Sales transactions (ID, customer, product, revenue)
- **shipping**: Shipping information (ID, tracking, delivery status)

---

## Running the Dashboard

### Basic Dashboard (Simple Version)
```bash
streamlit run streamlit_dashboard.py
```

### Interactive Dashboard (Advanced Version)
```bash
streamlit run interactive_dashboard.py
```

**The dashboard will open automatically in your web browser at:**
- `http://localhost:8501` (Basic version)
- `http://localhost:8502` (Interactive version)

### First Time Setup
1. When you run the command, Streamlit may ask for email - you can skip this
2. Your default web browser should open automatically
3. If it doesn't open, manually go to the URL shown in the terminal

---

## Using Excel Files

### Method 1: Replace Sample Data
1. **Keep the same structure**: Your Excel file must have the same sheet names and column headers
2. **Replace the file**: Save your data as `dummy_data/ecommerce_data.xlsx`
3. **Refresh dashboard**: The dashboard will automatically reload

### Required Excel Structure:

#### Sheet 1: "customers"
| customerID | userName | name | phoneNumber | email | city | state | country |
|------------|----------|------|-------------|-------|------|-------|---------|
| CUST0001 | user1 | Customer 1 | +1-555-0001 | user1@example.com | New York | NY | USA |

#### Sheet 2: "vendors"
| vendorID | nameVendor | phoneNumber | email | nameItemVendor | inventoryID |
|----------|------------|-------------|-------|----------------|-------------|
| VEND001 | VendorA | +1-555-1001 | vendor1@example.com | Laptop | INV1001 |

#### Sheet 3: "inventory"
| inventoryID | vendorID | nameInventory | Brand | type | modal | Price | EstimatedPrice | incomingDate | dateSold | availability | status | picture |
|-------------|----------|---------------|-------|------|-------|-------|----------------|--------------|----------|--------------|--------|---------|
| INV0001 | VEND001 | Laptop | Dell | Electronics | Model1 | 999.99 | 1099.99 | 2024-01-01 | 2024-01-15 | In Stock | Active | url |

#### Sheet 4: "transaction"
| transactionID | customerID | inventoryID | totalSales | totalEarings | shippingFee | otherFee | ketFee | shippingID | soldBy | noInvoice | notes |
|---------------|------------|-------------|------------|--------------|-------------|----------|--------|------------|--------|-----------|-------|
| TRN00001 | CUST0001 | INV0001 | 999.99 | 899.99 | 25.00 | 5.00 | | SHIP00001 | Salesperson A | INV123456 | Website |

#### Sheet 5: "shipping"
| shippingID | Receiver | trackingNumber | from | destination | carrier | carrierService | customerID | delayFlag |
|------------|----------|----------------|------|-------------|---------|----------------|------------|-----------|
| SHIP00001 | Customer 1 | TRK123456789 | Warehouse A | City 1 | FedEx | Standard | CUST0001 | False |

### Method 2: Update Data Generator
If you want different sample data:
1. Open `generate_dummy_data.py` in VS Code
2. Modify the data generation functions
3. Run: `python generate_dummy_data.py`
4. Refresh your dashboard

---

## Using Google Sheets (Advanced)

### Prerequisites for Google Sheets Integration
```bash
pip install gspread google-auth
```

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API

### Step 2: Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name it "dashboard-service-account"
4. Create and download JSON key file
5. Save as `credentials.json` in your project folder

### Step 3: Create Google Sheets
1. Create a new Google Sheet
2. Create 5 sheets: customers, vendors, inventory, transaction, shipping
3. Add the column headers as shown in the Excel structure above
4. Share the sheet with your service account email (found in credentials.json)

### Step 4: Update Dashboard for Google Sheets
Create a new file `google_sheets_dashboard.py`:

```python
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/spreadsheets/',
          'https://www.googleapis.com/auth/drive']

@st.cache_data
def load_google_sheet(sheet_url, sheet_name):
    try:
        # Load credentials
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Open sheet
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.worksheet(sheet_name)
        
        # Get data
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {e}")
        return pd.DataFrame()

# In your dashboard, replace the Excel loading with:
SHEET_URL = "YOUR_GOOGLE_SHEET_URL_HERE"
df_customers = load_google_sheet(SHEET_URL, "customers")
df_vendors = load_google_sheet(SHEET_URL, "vendors")
# ... etc for other sheets
```

### Step 5: Run Google Sheets Dashboard
```bash
streamlit run google_sheets_dashboard.py
```

### Benefits of Google Sheets Integration:
- **Real-time Updates**: Data updates automatically
- **Collaborative**: Multiple people can update data
- **Cloud-based**: Access from anywhere
- **Version Control**: Built-in revision history
- **Easy Sharing**: Simple permission management

---

## Customization Guide

### Adding New KPIs
1. Open your dashboard file in VS Code
2. Find the KPI section (around line 80)
3. Add new columns and metrics:

```python
with col5:  # Add new column
    conversion_rate = (unique_customers / total_visits * 100) if total_visits > 0 else 0
    st.metric(
        label="🎯 Conversion Rate", 
        value=f"{conversion_rate:.2f}%",
        delta="vs last month"
    )
```

### Adding New Charts
1. Find the charts section
2. Add new visualization:

```python
# New chart example
st.subheader("📈 Monthly Revenue Trend")
monthly_data = filtered_data.groupby(filtered_data["transactionDate"].dt.to_period("M"))["totalSales"].sum()
st.line_chart(monthly_data)
```

### Changing Colors and Styling
1. Modify the CSS section at the top:

```python
st.markdown("""
<style>
    .metric-card {
        background-color: #your-color-here;
        # Add your custom styles
    }
</style>
""", unsafe_allow_html=True)
```

### Adding New Filters
1. Add filter in sidebar section:

```python
# New filter example
product_categories = ['All'] + list(df_inventory['type'].unique())
selected_category = st.sidebar.selectbox("📦 Product Category:", product_categories)
```

2. Apply filter in data processing:

```python
if selected_category != 'All':
    filtered_inventory = filtered_inventory[filtered_inventory['type'] == selected_category]
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "ModuleNotFoundError"
**Error**: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: 
```bash
pip install streamlit pandas openpyxl plotly
```

#### Issue 2: "Port already in use"
**Error**: `Port 8501 is already in use`
**Solution**: 
```bash
# Use different port
streamlit run dashboard.py --server.port 8502
```

#### Issue 3: "Excel file not found"
**Error**: `Excel file not found at ./dummy_data/ecommerce_data.xlsx`
**Solution**: 
```bash
# Generate sample data first
python generate_dummy_data.py
```

#### Issue 4: Dashboard shows empty data
**Problem**: All metrics show $0.00
**Solution**: 
1. Check if Excel file exists in `dummy_data/` folder
2. Verify sheet names match exactly: "customers", "vendors", "inventory", "transaction", "shipping"
3. Check column names match the required structure

#### Issue 5: Charts not displaying
**Problem**: Charts appear blank
**Solution**: 
```bash
# Install plotly for interactive charts
pip install plotly
```

#### Issue 6: Permission denied (Mac/Linux)
**Error**: `Permission denied` when installing packages
**Solution**: 
```bash
# Use --user flag
pip install --user streamlit pandas openpyxl plotly
```

#### Issue 7: Python command not found
**Error**: `'python' is not recognized`
**Solution**: 
- Windows: Use `python` or `py`
- Mac/Linux: Use `python3`
- Or add Python to your PATH environment variable

### Getting Help
1. **Check the terminal**: Error messages usually explain the problem
2. **Restart the dashboard**: Stop (Ctrl+C) and run again
3. **Clear cache**: Add `?clear_cache=true` to the URL
4. **Check file paths**: Ensure all files are in the correct locations

---

## Next Steps

### Deployment Options

#### Option 1: Streamlit Community Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click
5. Get a public URL to share

#### Option 2: Local Network Sharing
```bash
# Run on all network interfaces
streamlit run dashboard.py --server.address 0.0.0.0
```
Others on your network can access via: `http://YOUR-IP-ADDRESS:8501`

#### Option 3: Cloud Deployment
- **Heroku**: Easy deployment with git
- **AWS EC2**: Full control over server
- **Google Cloud Run**: Serverless container deployment
- **Azure Container Instances**: Microsoft cloud option

### Advanced Features to Add

#### Real-time Database Connection
```python
import psycopg2  # For PostgreSQL
import mysql.connector  # For MySQL
import sqlite3  # For SQLite

# Example: Connect to PostgreSQL
@st.cache_data
def load_from_database():
    conn = psycopg2.connect(
        host="your-host",
        database="your-db",
        user="your-user",
        password="your-password"
    )
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df
```

#### Automated Data Refresh
```python
# Add auto-refresh every 5 minutes
import time
if st.button("🔄 Auto-refresh (5 min)"):
    placeholder = st.empty()
    while True:
        with placeholder.container():
            # Your dashboard code here
            pass
        time.sleep(300)  # 5 minutes
```

#### User Authentication
```python
import streamlit_authenticator as stauth

# Add login system
authenticator = stauth.Authenticate(
    names=['Admin', 'User'],
    usernames=['admin', 'user'],
    passwords=['admin123', 'user123'],
    cookie_name='dashboard_auth',
    key='random_signature_key'
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show dashboard
    st.write(f'Welcome *{name}*')
    # Your dashboard code here
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

#### Email Reports
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_report():
    # Generate report
    report_data = generate_report_data()
    
    # Send email
    msg = MIMEMultipart()
    msg['From'] = 'dashboard@company.com'
    msg['To'] = 'executive@company.com'
    msg['Subject'] = 'Daily Dashboard Report'
    
    body = f"Daily sales: ${report_data['total_sales']}"
    msg.attach(MIMEText(body, 'plain'))
    
    # Send via SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email', 'your-password')
    server.send_message(msg)
    server.quit()
```

### Performance Optimization

#### Caching Strategies
```python
# Cache expensive operations
@st.cache_data(ttl=3600)  # Cache for 1 hour
def expensive_calculation(data):
    # Your heavy computation here
    return result

# Cache database connections
@st.cache_resource
def get_database_connection():
    return create_connection()
```

#### Data Optimization
```python
# Load only required columns
df = pd.read_excel('data.xlsx', usecols=['col1', 'col2', 'col3'])

# Use efficient data types
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].astype('category')
df['amount'] = pd.to_numeric(df['amount'], downcast='float')
```

### Security Best Practices

1. **Environment Variables**: Store sensitive data in `.env` files
2. **HTTPS**: Use SSL certificates for production
3. **Authentication**: Implement proper user authentication
4. **Data Validation**: Validate all user inputs
5. **Access Control**: Limit data access based on user roles

---

## Conclusion

Congratulations! You now have a fully functional, interactive e-commerce dashboard that rivals Power BI and Tableau capabilities. This dashboard provides:

✅ **Real-time Analytics**: Live data updates and filtering
✅ **Interactive Visualizations**: Clickable charts and drill-down capabilities  
✅ **Executive-friendly Interface**: Clean, professional design
✅ **Multi-source Data**: Excel and Google Sheets integration
✅ **Export Capabilities**: Download filtered data
✅ **Mobile Responsive**: Works on all devices
✅ **Cost-effective**: Completely free solution

The dashboard is now ready for production use and can be easily extended with additional features as your business grows.

**Remember**: This is just the beginning. Python and Streamlit offer unlimited possibilities for customization and enhancement. Keep experimenting and adding new features as needed!

---

*Created by Manus AI - Your AI Assistant for Business Intelligence*
*Last Updated: July 30, 2025*

