import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import os

# -----------------------
# ✅ TiDB Cloud Config
# -----------------------
DB_CONFIG = {
    'user': '2cG3MBTK8AjfDHM.root',
    'password': 'GNrddcP3aTtbSHkp',
    'host': 'gateway01.us-west-2.prod.aws.tidbcloud.com',
    'port': 4000,
    'database': 'AgriData',
    'ssl_ca': os.path.join(os.path.dirname(__file__), 'ca.pem')  # Ensure ca.pem is uploaded to GitHub
}

# -----------------------
# ✅ Connect to TiDB
# -----------------------
def connect_db():
    try:
        if not os.path.exists(DB_CONFIG['ssl_ca']):
            st.error("❌ SSL CA file 'ca.pem' not found. Please upload it to the repo.")
            return None
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

# -----------------------
# ✅ Fetch Data Function (cached)
# -----------------------
@st.cache_data
def fetch_data(query):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()

# -----------------------
# ✅ Main Streamlit App
# -----------------------
def main():
    st.set_page_config(page_title="AgriData Explorer", layout="wide")
    st.title("🌾 AgriData Explorer - Powered by TiDB Cloud")

    tables = ["Crop_Production", "Weather_Data", "Soil_Quality"]
    table = st.selectbox("📋 Select a Table", tables)

    if table:
        query = f"SELECT * FROM {table} LIMIT 1000;"
        df = fetch_data(query)

        if not df.empty:
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

            st.subheader("🔍 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            # -----------------------
            # ✅ Filtering
            # -----------------------
            with st.expander("🔎 Filter Data"):
                if "state_name" in df.columns:
                    selected_state = st.selectbox("State", df["state_name"].dropna().unique())
                    df = df[df["state_name"] == selected_state]

                if "year" in df.columns and df["year"].notnull().any():
                    min_year, max_year = int(df["year"].min()), int(df["year"].max())
                    if min_year < max_year:
                        selected_years = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))
                        df = df[(df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1])]
                    else:
                        st.info(f"📅 Only data for the year {min_year} available.")

            # -----------------------
            # ✅ Summary & Visuals
            # -----------------------
            st.subheader("📈 Summary Statistics")
            st.write(df.describe())

            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                st.subheader("🔗 Correlation Heatmap")
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(numeric_df.corr(), annot=True, cmap="YlGnBu", fmt=".2f", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("⚠️ No numerical data available for correlation.")

            # -----------------------
            # 📊 Table-Specific Charts
            # -----------------------
            if table == "Crop_Production":
                if "year" in df.columns and "yield_kg_per_ha" in df.columns:
                    st.subheader("🌱 Yield Trend Over Years")
                    trend = df.groupby("year")["yield_kg_per_ha"].mean().reset_index()
                    st.line_chart(trend.set_index("year"))

            elif table == "Weather_Data":
                if "year" in df.columns and "rainfall" in df.columns:
                    st.subheader("🌧️ Rainfall Trend Over Years")
                    trend = df.groupby("year")["rainfall"].mean().reset_index()
                    st.line_chart(trend.set_index("year"))

            elif table == "Soil_Quality":
                if "ph_value" in df.columns:
                    st.subheader("🧪 Soil pH Distribution")
                    fig, ax = plt.subplots()
                    sns.histplot(df["ph_value"].dropna(), kde=True, ax=ax)
                    st.pyplot(fig)
        else:
            st.warning("⚠️ No data found or empty table.")

if __name__ == "__main__":
    main()
