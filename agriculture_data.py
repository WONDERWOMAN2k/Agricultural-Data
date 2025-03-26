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
        st.write(f"Error: {err}")
        return None
# Existing function in agriculture_data.py (around line 37)
def visualize_data(df):
    """Generates and displays data visualizations."""
    if df.empty:
        st.write("No data available for visualization.")
        return
    
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) == 0:
        st.write("Error: No numerical data available for correlation heatmap.")
        return
    
    # Drop non-numeric columns
    df_numeric = df[numeric_cols].copy()

    # Handle NaN values to avoid errors
    df_numeric = df_numeric.dropna()

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    st.pyplot(plt)

# Function to fetch data from TiDB Cloud
def fetch_data_from_db(conn):
    query = "SELECT * FROM Crop_Production;"
    df = pd.read_sql(query, conn)
    return df

# Function to visualize data
def visualize_data(df):
    st.write("Data Preview:")
    st.write(df.head())

    # Correlation Heatmap
    if df.select_dtypes(include=['number']).empty:
        st.write("Error: No numerical data available for correlation heatmap.")
    else:
        correlation_matrix = df.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title("Correlation Heatmap of Agricultural Data")
        st.pyplot(plt)

    # Example Plot: Rice and Wheat Production Over Time
    if 'year' in df.columns and 'rice_production_1000_tons' in df.columns and 'wheat_production_1000_tons' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(df['year'], df['rice_production_1000_tons'], label='Rice Production (1000 tons)', color='green')
        plt.plot(df['year'], df['wheat_production_1000_tons'], label='Wheat Production (1000 tons)', color='orange')
        plt.xlabel('Year')
        plt.ylabel('Production (1000 tons)')
        plt.title('Rice and Wheat Production Over Time')
        plt.legend()
        st.pyplot(plt)
    else:
        st.write("Error: Missing necessary columns for Rice and Wheat production over time.")

# Main Streamlit app
def main():
    st.title("Agricultural Data Exploration")

    # Upload CSV or connect to TiDB Cloud
    option = st.selectbox("Select Data Source", ["Upload CSV", "Connect to TiDB Cloud"])

    if option == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Data loaded successfully!")
            visualize_data(df)
    elif option == "Connect to TiDB Cloud":
        conn = connect_to_database()
        if conn is not None:
            st.write("Connected to TiDB Cloud!")
            df = fetch_data_from_db(conn)
            visualize_data(df)
            conn.close()  # Close the connection after fetching the data
        else:
            st.write("Failed to connect to TiDB Cloud.")

if __name__ == "__main__":
    main()

