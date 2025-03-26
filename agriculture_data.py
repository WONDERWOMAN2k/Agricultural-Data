import mysql.connector
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Function to connect to TiDB Cloud
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="gateway01.us-west-2.prod.aws.tidbcloud.com",
            port=4000,
            user="2cG3MBTK8AjfDHM.root",
            password="dYaKCArJUfrmgU85",  # Replace with actual password
            database="AgriData"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

# Function to fetch data from TiDB Cloud
def fetch_data_from_db(conn):
    try:
        query = "SELECT * FROM Crop_Production;"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Function to visualize data
def visualize_data(df):
    """Generates and displays data visualizations."""
    
    if df.empty:
        st.error("No data available for visualization.")
        return

    st.write("### Data Preview")
    st.write(df.head())

    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns

    if numeric_cols.empty:
        st.error("Error: No numerical data available for correlation heatmap.")
        return

    # Handle NaN values
    df_numeric = df[numeric_cols].dropna()

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    plt.figure(figsize=(12, 8))
    sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Correlation Heatmap of Agricultural Data")
    st.pyplot(plt)

    # Example Plot: Rice and Wheat Production Over Time
    required_columns = {'year', 'rice_production_1000_tons', 'wheat_production_1000_tons'}
    if required_columns.issubset(df.columns):
        plt.figure(figsize=(10, 6))
        plt.plot(df['year'], df['rice_production_1000_tons'], label='Rice Production (1000 tons)', color='green')
        plt.plot(df['year'], df['wheat_production_1000_tons'], label='Wheat Production (1000 tons)', color='orange')
        plt.xlabel('Year')
        plt.ylabel('Production (1000 tons)')
        plt.title('Rice and Wheat Production Over Time')
        plt.legend()
        st.pyplot(plt)
    else:
        st.warning("Missing necessary columns for Rice and Wheat production over time.")

# Main Streamlit app
def main():
    st.title
