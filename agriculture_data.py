import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

# TiDB Cloud Database Credentials
DB_CONFIG = {
    "host": "gateway01.us-west-2.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "2cG3MBTK8AjfDHM.root",
    "password": "dYaKCArJUfrmgU85",  # Replace with actual password
    "database": "AgriData"
}

# Function to connect to the database
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Function to fetch data from TiDB Cloud
def fetch_data(query):
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return pd.DataFrame(data)
    return None

# Streamlit App
def main():
    st.title("🌾 AgriData Explorer - TiDB Cloud Integration")
    
    # Dropdown to select a table
    tables = ["crop_production", "farm_area", "yield_statistics"]
    table = st.selectbox("Select Table", tables)

    if table:
        query = f"SELECT * FROM {table} LIMIT 100;"
        df = fetch_data(query)
        
        if df is not None:
            st.subheader(f"📜 Data Preview - {table}")
            st.write(df.head())

            # Correlation Heatmap
            st.subheader("📊 Correlation Heatmap")
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                plt.figure(figsize=(10, 6))
                sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
                st.pyplot(plt)
            else:
                st.warning("No numerical columns available for correlation.")

if __name__ == "__main__":
    main()
