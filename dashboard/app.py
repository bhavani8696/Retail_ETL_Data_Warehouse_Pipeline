import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Retail ETL Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------
def load_css():
    try:
        with open("assets/css/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# --------------------------------------------------
# MYSQL CONNECTION
# --------------------------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="retail_dw"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
query = """
SELECT
    f.sales,
    f.profit,
    f.quantity,
    f.discount,
    d.year,
    p.category,
    p.sub_category,
    p.product_name,
    c.customer_name,
    s.region,
    s.country,
    s.state,
    s.city
FROM fact_sales f
JOIN dim_customer c
ON f.customer_key = c.customer_key
JOIN dim_product p
ON f.product_key = p.product_key
JOIN dim_store s
ON f.store_key = s.store_key
JOIN dim_date d
ON f.date_key = d.date_key
"""

df = pd.read_sql(query, conn)
# -----------------------------------
# TITLE
# -----------------------------------
st.title("📊 Retail ETL Data Warehouse Dashboard")

st.success("🚀 Retail ETL Pipeline Loaded Successfully")

st.caption(
    "Advanced Retail Analytics Dashboard using Python • MySQL • Streamlit • Plotly"
)

st.divider()

# -----------------------------------
# KPI CARDS
# -----------------------------------
total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
total_orders = len(df)
total_customers = df["customer_name"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.0f}"
    )

with c2:
    st.metric(
        "📈 Total Profit",
        f"₹{total_profit:,.0f}"
    )

with c3:
    st.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

with c4:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

st.divider()

# -----------------------------------
# YEAR WISE SALES
# -----------------------------------
st.subheader("📈 Year Wise Sales")

sales_year = (
    df.groupby("year")["sales"]
      .sum()
      .reset_index()
)

fig = px.line(
    sales_year,
    x="year",
    y="sales",
    markers=True,
    title="Sales Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
# -----------------------------------
# CATEGORY & REGION CHARTS
# -----------------------------------
left, right = st.columns(2)

with left:

    st.subheader("🥧 Category Wise Sales")

    cat = (
        df.groupby("category")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        cat,
        names="category",
        values="sales",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🌍 Region Wise Sales")

    reg = (
        df.groupby("region")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        reg,
        x="region",
        y="sales",
        color="sales",
        title="Region Wise Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
# -----------------------------------
# TOP 10 PRODUCTS
# -----------------------------------
st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="sales",
    y="product_name",
    orientation="h",
    color="sales",
    title="Top 10 Products"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------------
# TOP 10 CUSTOMERS
# -----------------------------------
st.subheader("👑 Top 10 Customers by Sales")

top_customers = (
    df.groupby("customer_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="sales",
    y="customer_name",
    orientation="h",
    color="sales",
    title="Top 10 Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
st.divider()

st.subheader("💹 Profit Distribution")

fig = px.histogram(
    df,
    x="profit",
    nbins=50,
    title="Profit Distribution",
    color_discrete_sequence=["green"]
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DATA TABLE
# -----------------------------------
st.subheader("📄 Retail Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------------
# CLOSE DATABASE CONNECTION
# -----------------------------------
conn.close()
# -----------------------------------
# DOWNLOAD DATASET
# -----------------------------------
st.divider()

st.subheader("⬇ Download Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="Retail_ETL_Report.csv",
    mime="text/csv"
)

# -----------------------------------
# DATASET SUMMARY
# -----------------------------------
st.divider()

st.subheader("📊 Dataset Summary")

col1, col2 = st.columns(2)

with col1:
    st.write("### Numerical Statistics")
    st.dataframe(df.describe())

with col2:
    st.write("### Dataset Information")

    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(info)
    st.divider()

st.subheader("🎯 Discount vs Profit")

fig = px.scatter(
    df,
    x="discount",
    y="profit",
    color="category",
    size="sales",
    hover_data=["product_name"],
    title="Discount Impact on Profit"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("🏙️ Top 10 Cities by Sales")

city_sales = (
    df.groupby("city")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    city_sales,
    x="city",
    y="sales",
    color="sales"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("📦 Sub Category Sales")

sub = (
    df.groupby("sub_category")["sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    sub,
    x="sub_category",
    y="sales",
    color="sales"
)

st.plotly_chart(fig, use_container_width=True)
conn.close()