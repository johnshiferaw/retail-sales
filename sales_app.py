import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide")
st.title("📈 Retail Sales Explorer")

# 2. Load Data Function
@st.cache_data
def load_data():
    conn = sqlite3.connect("retail.db")  # adjust path to your actual db location
    df = pd.read_sql("SELECT * FROM sales", conn)
    df['Order Date'] = pd.to_datetime(df['Order Date'])  # Let pandas infer  # Convert to datetime
    conn.close()
    return df

df = load_data()

# 3. Sidebar Filters
category = st.sidebar.selectbox("Category", df['Category'].unique())

# Get date range from data
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

# Date filter
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# 4. Build SQL Query
conn = sqlite3.connect("retail.db")  # adjust path to your actual db location

# Initialize result
result = pd.DataFrame()

# Add date filter if selected
if len(date_range) == 2:
    start_date = date_range[0].strftime('%Y-%m-%d')
    end_date = date_range[1].strftime('%Y-%m-%d')
    
    # Base query
    query = """
    SELECT "Product Name", SUM(Sales) AS Revenue 
    FROM sales 
    WHERE Category = ? AND DATE("Order Date") BETWEEN ? AND ?
    GROUP BY "Product Name" ORDER BY Revenue DESC
    """
    
    # Run the query
    result = pd.read_sql(query, conn, params=(category, start_date, end_date))
    conn.close()
else:
    st.warning("⚠️ Please select a valid start and end date.")

# 5. Visualization
if not result.empty:
    fig = px.bar(result, x="Product Name", y="Revenue", title=f"Revenue by Product in '{category}' Category")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found for the selected category and date range.")
