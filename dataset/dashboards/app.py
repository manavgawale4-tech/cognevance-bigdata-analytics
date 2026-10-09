# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configure the dashboard
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Find the project and dataset folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = PROJECT_DIR / "dataset"


# Load datasets
@st.cache_data
def load_data():
    orders = pd.read_csv(
        DATASET_DIR / "olist_orders_dataset.csv"
    )

    customers = pd.read_csv(
        DATASET_DIR / "olist_customers_dataset.csv"
    )

    order_items = pd.read_csv(
        DATASET_DIR / "olist_order_items_dataset.csv"
    )

    payments = pd.read_csv(
        DATASET_DIR / "olist_order_payments_dataset.csv"
    )

    products = pd.read_csv(
        DATASET_DIR / "olist_products_dataset.csv"
    )

    categories = pd.read_csv(
        DATASET_DIR / "product_category_name_translation.csv"
    )

    # Convert date columns to datetime
    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )

    return (
        orders,
        customers,
        order_items,
        payments,
        products,
        categories
    )


# Load data and handle errors
try:
    (
        orders,
        customers,
        order_items,
        payments,
        products,
        categories
    ) = load_data()

except Exception as error:
    st.error(
        "Unable to load the datasets. Check that all required "
        "CSV files are inside the dataset folder."
    )
    st.code(str(error))
    st.stop()


# Dashboard heading
st.title("🛒 E-Commerce Customer Analytics")
st.subheader("Big Data Analytics & Predictive Intelligence")

st.write(
    "Analyze sales, customer behavior, product categories, "
    "payments, and delivery performance."
)


# Prepare category information for filtering
category_data = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

category_data = category_data.merge(
    categories,
    on="product_category_name",
    how="left"
)

category_data["product_category_name_english"] = (
    category_data["product_category_name_english"]
    .fillna("Unknown")
)


# Date and category filters
st.markdown("---")
st.header("🔎 Dashboard Filters")

valid_purchase_dates = orders[
    "order_purchase_timestamp"
].dropna()

if valid_purchase_dates.empty:
    st.error("No valid purchase dates are available.")
    st.stop()

min_date = valid_purchase_dates.min().date()
max_date = valid_purchase_dates.max().date()

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_dates = st.date_input(
        "📅 Select Purchase Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

with filter_col2:
    available_categories = sorted(
        category_data["product_category_name_english"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        "🛍️ Select Product Categories",
        options=available_categories,
        default=available_categories
    )


# Apply the date filter
if len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = selected_dates[0]
    end_date = selected_dates[0]

if start_date > end_date:
    st.warning("Start date must be before end date.")
    st.stop()

date_mask = (
    orders["order_purchase_timestamp"].notna()
    & (
        orders["order_purchase_timestamp"].dt.date
        >= start_date
    )
    & (
        orders["order_purchase_timestamp"].dt.date
        <= end_date
    )
)

filtered_orders = orders[date_mask].copy()

# Get delivered orders for the selected date range
delivered_orders = filtered_orders[
    filtered_orders["order_status"] == "delivered"
].copy()

delivered_order_ids = delivered_orders["order_id"]

# Filter delivered product items
delivered_items = order_items[
    order_items["order_id"].isin(delivered_order_ids)
].copy()

# Apply product category filter
filtered_category_items = category_data[
    category_data["order_id"].isin(delivered_order_ids)
    & category_data["product_category_name_english"].isin(
        selected_categories
    )
].copy()


# Calculate business metrics
total_orders = filtered_orders["order_id"].nunique()

delivered_order_count = (
    delivered_orders["order_id"].nunique()
)

unique_customer_ids = filtered_orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

unique_customers = (
    unique_customer_ids["customer_unique_id"].nunique()
)

# Revenue for selected date range and selected categories
total_revenue = filtered_category_items["price"].sum()


# Calculate average delivery time
valid_delivery = delivered_orders.dropna(
    subset=[
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
).copy()

valid_delivery["delivery_days"] = (
    valid_delivery["order_delivered_customer_date"]
    - valid_delivery["order_purchase_timestamp"]
).dt.total_seconds() / 86400

valid_delivery = valid_delivery[
    valid_delivery["delivery_days"] >= 0
]

average_delivery = (
    valid_delivery["delivery_days"].mean()
    if not valid_delivery.empty
    else 0
)

# Calculate on-time delivery rate
on_time_mask = (
    valid_delivery["order_delivered_customer_date"]
    <= valid_delivery["order_estimated_delivery_date"]
)

on_time_rate = (
    on_time_mask.mean() * 100
    if not valid_delivery.empty
    else 0
)


# Display KPI cards
st.markdown("---")
st.header("📌 Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "Delivered Orders",
    f"{delivered_order_count:,}"
)

col3.metric(
    "Unique Customers",
    f"{unique_customers:,}"
)

col4.metric(
    "Product Revenue",
    f"R$ {total_revenue:,.2f}"
)

col5, col6 = st.columns(2)

col5.metric(
    "Average Delivery Time",
    f"{average_delivery:.2f} days"
)

col6.metric(
    "On-Time/Early Delivery Rate",
    f"{on_time_rate:.2f}%"
)

st.caption(
    "Revenue is based on selected categories and delivered product "
    "prices, excluding freight. Delivery metrics use delivered orders "
    "with valid delivery dates."
)


# Monthly sales analysis
st.markdown("---")
st.header("📈 Monthly Sales Analysis")

monthly_items = filtered_category_items.merge(
    filtered_orders[
        ["order_id", "order_purchase_timestamp"]
    ],
    on="order_id",
    how="left"
)

monthly_items = monthly_items.dropna(
    subset=["order_purchase_timestamp"]
)

monthly_items["month"] = (
    monthly_items["order_purchase_timestamp"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly_sales = (
    monthly_items.groupby("month")["price"]
    .sum()
    .reset_index()
)

if not monthly_sales.empty:
    fig_monthly = px.line(
        monthly_sales,
        x="month",
        y="price",
        markers=True,
        title="Monthly Product Revenue",
        labels={
            "month": "Month",
            "price": "Product Revenue (BRL)"
        }
    )

    st.plotly_chart(
        fig_monthly,
        width="stretch"
    )
else:
    st.info(
        "No sales data available for the selected filters."
    )


# Product category analysis
st.markdown("---")
st.header("🏆 Top 10 Product Categories")

category_revenue = (
    filtered_category_items
    .groupby("product_category_name_english")["price"]
    .sum()
    .reset_index()
    .sort_values("price", ascending=False)
    .head(10)
)

if not category_revenue.empty:
    fig_category = px.bar(
        category_revenue.sort_values("price"),
        x="price",
        y="product_category_name_english",
        orientation="h",
        title="Top Categories by Product Revenue",
        labels={
            "price": "Product Revenue (BRL)",
            "product_category_name_english": "Product Category"
        }
    )

    st.plotly_chart(
        fig_category,
        width="stretch"
    )
else:
    st.info(
        "No product categories match the selected filters."
    )


# Customer behavior analysis
st.markdown("---")
st.header("👥 Customer Behavior")

customer_orders = filtered_orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

delivered_customer_orders = customer_orders[
    customer_orders["order_status"] == "delivered"
]

customer_order_counts = (
    delivered_customer_orders
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

repeat_customers = int(
    (customer_order_counts > 1).sum()
)

single_order_customers = int(
    (customer_order_counts == 1).sum()
)

repeat_rate = (
    repeat_customers / len(customer_order_counts) * 100
    if len(customer_order_counts) > 0
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Single-Order Customers",
    f"{single_order_customers:,}"
)

col2.metric(
    "Repeat Customers",
    f"{repeat_customers:,}"
)

col3.metric(
    "Repeat Customer Rate",
    f"{repeat_rate:.2f}%"
)

st.caption(
    "Customer repeat rate is calculated using delivered orders "
    "within the selected date range."
)


# Payment analysis
st.markdown("---")
st.header("💳 Payment Methods")

filtered_payments = payments[
    payments["order_id"].isin(
        filtered_orders["order_id"]
    )
]

payment_data = (
    filtered_payments
    .groupby("payment_type")["order_id"]
    .nunique()
    .reset_index(name="order_count")
    .sort_values("order_count", ascending=False)
)

if not payment_data.empty:
    fig_payment = px.bar(
        payment_data,
        x="payment_type",
        y="order_count",
        title="Orders by Payment Method",
        labels={
            "payment_type": "Payment Method",
            "order_count": "Number of Orders"
        }
    )

    st.plotly_chart(
        fig_payment,
        width="stretch"
    )

    st.caption(
        "An order may use more than one payment method, "
        "so payment-method counts may overlap."
    )
else:
    st.info("No payment data available for the selected dates.")


# Delivery performance analysis
st.markdown("---")
st.header("🚚 Delivery Performance")

if not valid_delivery.empty:
    delivery_counts = pd.DataFrame({
        "Delivery Status": [
            "On Time or Early",
            "Late"
        ],
        "Orders": [
            int(on_time_mask.sum()),
            int((~on_time_mask).sum())
        ]
    })

    fig_delivery = px.pie(
        delivery_counts,
        names="Delivery Status",
        values="Orders",
        title="On-Time vs Late Deliveries"
    )

    st.plotly_chart(
        fig_delivery,
        width="stretch"
    )
else:
    st.info("No valid delivery records available.")


# Project information
st.markdown("---")
st.header("ℹ️ Project Information")

st.write("""
- **Dataset:** Brazilian E-Commerce Public Dataset by Olist
- **Tools:** Python, Pandas, Streamlit and Plotly
- **Analysis:** Sales, customers, product categories, payments and deliveries
- **Revenue definition:** Delivered product prices, excluding freight
- **Filters:** Purchase date range and product categories
""")

st.success(
    "E-Commerce Analytics Dashboard loaded successfully!"
)