import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

# Updated TiDB Cloud Database Config
DB_CONFIG = {
    'user': '2cG3MBTK8AjfDHM.root',
    'password': 'Mi9z7bZhmQT5CXpY',
    'host': 'gateway01.us-west-2.prod.aws.tidbcloud.com',
    'port': 4000,
    'database': 'AgriData',
    'ssl_ca': 'ca.pem'  # Correct relative path for Streamlit Cloud
}


# Connect to TiDB Cloud
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

# Cached function to fetch data
@st.cache_data
def fetch_data(query):
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return pd.DataFrame(data)
    return None

# Streamlit App Logic
def main():
    st.set_page_config(page_title="AgriData Explorer", layout="wide")
    st.title("🌾 AgriData Explorer - Powered by TiDB Cloud")

    tables = ["Crop_Production", "Weather_Data", "Soil_Quality"]
    table = st.selectbox("📋 Select a Table", tables)

    if table:
        query = f"SELECT * FROM {table} LIMIT 1000;"
        df = fetch_data(query)

        if df is not None and not df.empty:
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

            st.subheader("🔍 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            with st.expander("🔎 Filter Data"):
                if "state_name" in df.columns:
                    selected_state = st.selectbox("State", df["state_name"].dropna().unique())
                    df = df[df["state_name"] == selected_state]

                if "year" in df.columns:
                    min_year, max_year = int(df["year"].min()), int(df["year"].max())
                    selected_years = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))
                    df = df[(df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1])]

            st.subheader("📈 Summary Statistics")
            st.write(df.describe())

            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                st.subheader("🔗 Correlation Heatmap")
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(numeric_df.corr(), annot=True, cmap="YlGnBu", fmt=".2f", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("No numerical data for correlation.")

            if "year" in df.columns and "yield_kg_per_ha" in df.columns:
                st.subheader("🌱 Yield Trend Over Years")
                trend = df.groupby("year")["yield_kg_per_ha"].mean().reset_index()
                st.line_chart(trend.set_index("year"))
        else:
            st.warning("⚠️ No data found or empty table.")

if __name__ == "__main__":
    main()
