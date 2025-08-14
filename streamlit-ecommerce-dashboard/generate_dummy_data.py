
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_customers_data(num_customers=100):
    customer_data = []
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    states = ["NY", "CA", "IL", "TX", "AZ"]
    countries = ["USA"]
    for i in range(1, num_customers + 1):
        customer_id = f"CUST{i:04d}"
        username = f"user{i}"
        name = f"Customer {i}"
        phone_number = f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        email = f"user{i}@example.com"
        city = random.choice(cities)
        state = random.choice(states)
        country = random.choice(countries)
        customer_data.append([customer_id, username, name, phone_number, email, city, state, country])
    return pd.DataFrame(customer_data, columns=["customerID", "userName", "name", "phoneNumber", "email", "city", "state", "country"])

def generate_vendors_data(num_vendors=20):
    vendor_data = []
    vendor_names = ["VendorA", "VendorB", "VendorC", "VendorD", "VendorE"]
    item_names = ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam"]
    for i in range(1, num_vendors + 1):
        vendor_id = f"VEND{i:03d}"
        name_vendor = random.choice(vendor_names)
        phone_number = f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        email = f"vendor{i}@example.com"
        name_item_vendor = random.choice(item_names)
        inventory_id = f"INV{random.randint(1000,9999):04d}"
        vendor_data.append([vendor_id, name_vendor, phone_number, email, name_item_vendor, inventory_id])
    return pd.DataFrame(vendor_data, columns=["vendorID", "nameVendor", "phoneNumber", "email", "nameItemVendor", "inventoryID"])

def generate_inventory_data(num_inventory=200):
    inventory_data = []
    brands = ["Dell", "HP", "Lenovo", "Apple", "Samsung"]
    types = ["Electronics", "Peripherals", "Accessories"]
    item_types = ["Laptop", "Desktop", "Monitor", "Keyboard", "Mouse", "Headphones"]
    statuses = ["In Stock", "Low Stock", "Out of Stock"]
    for i in range(1, num_inventory + 1):
        inventory_id = f"INV{i:04d}"
        vendor_id = f"VEND{random.randint(1,20):03d}"
        name_inventory = random.choice(item_types)
        brand = random.choice(brands)
        item_type = random.choice(types)
        model = f"Model{random.randint(1,10)}"
        price = round(random.uniform(50, 1500), 2)
        estimated_price = round(price * random.uniform(0.9, 1.1), 2)
        incoming_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        date_sold = (datetime.now() - timedelta(days=random.randint(1, 365))) if random.random() > 0.2 else None
        availability = random.choice(statuses)
        status = random.choice(["Active", "Discontinued"])
        picture = f"http://example.com/inv{i}.jpg"
        inventory_data.append([inventory_id, vendor_id, name_inventory, brand, item_type, model, price, estimated_price, incoming_date, date_sold, availability, status, picture])
    return pd.DataFrame(inventory_data, columns=["inventoryID", "vendorID", "nameInventory", "Brand", "type", "modal", "Price", "EstimatedPrice", "incomingDate", "dateSold", "availability", "status", "picture"])

def generate_transactions_data(num_transactions=500, customer_ids=None, inventory_ids=None):
    transaction_data = []
    channels = ["Website", "Mobile App", "Retail Store", "Marketplace"]
    sold_by_options = ["Salesperson A", "Salesperson B", "Online System"]
    for i in range(1, num_transactions + 1):
        transaction_id = f"TRN{i:05d}"
        customer_id = random.choice(customer_ids) if customer_ids else f"CUST{random.randint(1,100):04d}"
        inventory_id = random.choice(inventory_ids) if inventory_ids else f"INV{random.randint(1,200):04d}"
        total_sales = round(random.uniform(10, 2000), 2)
        total_earnings = round(total_sales * random.uniform(0.7, 0.95), 2)
        shipping_fee = round(random.uniform(5, 50), 2) if random.random() > 0.3 else 0
        other_fee = round(random.uniform(0, 20), 2) if random.random() > 0.5 else 0
        ket_fee = ""
        shipping_id = f"SHIP{random.randint(10000,99999):05d}"
        sold_by = random.choice(sold_by_options)
        no_invoice = f"INV{random.randint(100000,999999):06d}"
        notes = random.choice(channels)
        transaction_data.append([transaction_id, customer_id, inventory_id, total_sales, total_earnings, shipping_fee, other_fee, ket_fee, shipping_id, sold_by, no_invoice, notes])
    return pd.DataFrame(transaction_data, columns=["transactionID", "customerID", "inventoryID", "totalSales", "totalEarings", "shippingFee", "otherFee", "ketFee", "shippingID", "soldBy", "noInvoice", "notes"])

def generate_shipping_data(num_shipping=500, customer_ids=None):
    shipping_data = []
    carriers = ["FedEx", "UPS", "DHL", "USPS"]
    carrier_services = ["Standard", "Express", "Priority"]
    delay_flags = [True, False]
    for i in range(1, num_shipping + 1):
        shipping_id = f"SHIP{i:05d}"
        receiver = f"Receiver {i}"
        tracking_number = f"TRK{random.randint(100000000,999999999)}"
        _from = random.choice(["Warehouse A", "Warehouse B"])
        destination = f"City {random.randint(1,10)}"
        carrier = random.choice(carriers)
        carrier_service = random.choice(carrier_services)
        customer_id = random.choice(customer_ids) if customer_ids else f"CUST{random.randint(1,100):04d}"
        delay_flag = random.choice(delay_flags)
        shipping_data.append([shipping_id, receiver, tracking_number, _from, destination, carrier, carrier_service, customer_id, delay_flag])
    return pd.DataFrame(shipping_data, columns=["shippingID", "Receiver", "trackingNumber", "from", "destination", "carrier", "carrierService", "customerID", "delayFlag"])

if __name__ == "__main__":
    output_dir = "./dummy_data"
    import os
    os.makedirs(output_dir, exist_ok=True)

    excel_file_path = os.path.join(output_dir, "ecommerce_data.xlsx")

    print("Generating dummy data...")

    df_customers = generate_customers_data()
    df_vendors = generate_vendors_data()
    df_inventory = generate_inventory_data()

    # Ensure customer and inventory IDs exist for transactions and shipping
    customer_ids = df_customers["customerID"].tolist()
    inventory_ids = df_inventory["inventoryID"].tolist()

    df_transactions = generate_transactions_data(customer_ids=customer_ids, inventory_ids=inventory_ids)
    df_shipping = generate_shipping_data(customer_ids=customer_ids)

    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df_customers.to_excel(writer, sheet_name='customers', index=False)
        df_vendors.to_excel(writer, sheet_name='vendors', index=False)
        df_inventory.to_excel(writer, sheet_name='inventory', index=False)
        df_transactions.to_excel(writer, sheet_name='transaction', index=False)
        df_shipping.to_excel(writer, sheet_name='shipping', index=False)

    print(f"All dummy data generated successfully in {excel_file_path}")


