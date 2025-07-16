import pandas as pd
df = pd.read_csv("retail-sales/data/superstore.csv")
print(df.head())



import sqlite3
import pandas as pd

# 1. Load CSV
df = pd.read_csv("retail-sales/data/superstore.csv")

# 2. Convert Order_Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# 3. Create SQLite database
conn = sqlite3.connect("retail-sales/retail.db")  # adjust path to your actual db location


# 4. Load to SQL
df.to_sql("sales", conn, if_exists="replace", index=False)

# 5. Verify
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())  # Should show ['sales']



# Revenue by Category
query1 = """
SELECT Category, ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Category
ORDER BY Revenue DESC
"""
print(pd.read_sql(query1, conn))

# Monthly Sales Growth
query2 = """
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', "Order Date") AS Month,
        SUM(Sales) AS Revenue
    FROM sales
    GROUP BY Month
)
SELECT 
    Month,
    Revenue,
    ROUND((Revenue - LAG(Revenue) OVER (ORDER BY Month)) * 100.0 / LAG(Revenue) OVER (ORDER BY Month), 2) AS Growth_Pct
FROM monthly_sales
LIMIT 12;
"""


print(pd.read_sql(query2, conn))
conn.close()
