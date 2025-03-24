import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# Load and clean the data
def load_data():
    df = pd.read_csv('agriculture_data.csv')
    st.write("Raw Data", df.head())

    # Handle missing values for numerical and categorical columns
    df.fillna(df.select_dtypes(include=['number']).median(), inplace=True)
    df.fillna(df.select_dtypes(include=['object']).mode().iloc[0], inplace=True)
    
    # Convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Print column names to debug if there's an issue
    st.write("Column names:", df.columns)
    
    return df

# Visualizations for the data
def visualize_data(df):
    st.title("Agricultural Data Visualizations")

    # Histogram of Rice Area
    if 'rice_area_(1000_ha)' in df.columns:
        st.subheader("Distribution of Rice Area")
        plt.figure(figsize=(10, 5))
        sns.histplot(df['rice_area_(1000_ha)'], bins=30, kde=True)
        plt.title("Distribution of Rice Area (1000 ha)")
        plt.xlabel("Rice Area (1000 ha)")
        plt.ylabel("Count")
        st.pyplot(plt)
    else:
        st.error("Column 'rice_area_(1000_ha)' not found!")

    # Boxplot for Rice Yield
    if 'rice_yield_(kg_per_ha)' in df.columns:
        st.subheader("Boxplot of Rice Yield")
        plt.figure(figsize=(8, 5))
        sns.boxplot(y=df['rice_yield_(kg_per_ha)'])
        plt.title("Boxplot of Rice Yield")
        plt.ylabel("Rice Yield (kg per ha)")
        st.pyplot(plt)
    else:
        st.error("Column 'rice_yield_(kg_per_ha)' not found!")

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap (Numerical Features)")
    st.pyplot(plt)

    # Trend of Rice and Wheat Production over the Years
    st.subheader("Rice and Wheat Production Over Time")
    if 'year' in df.columns and 'rice_production_(1000_tons)' in df.columns and 'wheat_production_(1000_tons)' in df.columns:
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='year', y='rice_production_(1000_tons)', data=df, label="Rice Production", marker="o")
        sns.lineplot(x='year', y='wheat_production_(1000_tons)', data=df, label="Wheat Production", marker="s")
        plt.title("Trend of Rice and Wheat Production Over the Years")
        plt.xlabel("Year")
        plt.ylabel("Production (1000 Tons)")
        plt.legend()
        st.pyplot(plt)
    else:
        st.error("Columns 'year', 'rice_production_(1000_tons)', or 'wheat_production_(1000_tons)' not found!")

    # Bar chart of Top 5 States by Rice Production
    st.subheader("Top 5 States by Rice Production")
    if 'state_name' in df.columns and 'rice_production_(1000_tons)' in df.columns:
        top_states = df.groupby('state_name')['rice_production_(1000_tons)'].sum().nlargest(5)
        plt.figure(figsize=(10, 5))
        top_states.plot(kind='bar', color='skyblue')
        plt.title("Top 5 States by Rice Production")
        plt.xlabel("State")
        plt.ylabel("Total Rice Production (1000 Tons)")
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.error("Columns 'state_name' or 'rice_production_(1000_tons)' not found!")

# Database connection to TiDB Cloud
def connect_to_database():
    conn = mysql.connector.connect(
        host="gateway01.us-west-2.prod.aws.tidbcloud.com",
        port=4000,
        user="2cG3MBTK8AjfDHM.root",
        password="dYaKCArJUfrmgU85",  # Replace with actual password
        database="AgriData"
    )
    return conn

# Fetch data from TiDB Cloud
def fetch_data_from_db(conn):
    query = "SELECT * FROM Crop_Production;"
    df = pd.read_sql(query, conn)
    return df

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
        st.write("Connected to TiDB Cloud!")
        df = fetch_data_from_db(conn)
        visualize_data(df)

if __name__ == "__main__":
    main()
