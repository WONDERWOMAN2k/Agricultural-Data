import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload your Agricultural Data CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load the dataset
        df = pd.read_csv(uploaded_file)
        st.write("Data loaded successfully!")

        # Display column names and check for missing values
        st.write("Column Names:", df.columns)  # Show column names
        st.write("Missing Values:", df.isnull().sum())  # Check for missing values in each column

        # Clean column names by replacing spaces with underscores, removing parentheses, and converting to lowercase
        df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.lower()

        # Display updated column names
        st.write("Updated Column Names:")
        st.write(df.columns)

        # Check the first few rows of the dataframe
        st.write("Data Preview:")
        st.write(df.head())

        # ----------- CORRELATION HEATMAP ----------- 
        correlation_matrix = df.corr()

        # Plot the heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title("Correlation Heatmap of Agricultural Data")
        st.pyplot(plt)

        # ----------- RICE AND WHEAT PRODUCTION OVER TIME ----------- 
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

        # ----------- TOP 5 STATES BY RICE PRODUCTION ----------- 
        if 'state_name' in df.columns and 'rice_production_1000_tons' in df.columns:
            top_states = df.groupby('state_name')['rice_production_1000_tons'].sum().nlargest(5)

            # Plot the top 5 states
            plt.figure(figsize=(10, 6))
            top_states.plot(kind='bar', color='blue')
            plt.xlabel('State')
            plt.ylabel('Rice Production (1000 tons)')
            plt.title('Top 5 States by Rice Production')
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.write("Error: Missing necessary columns for Top 5 States by Rice Production.")

        # ----------- RICE YIELD DISTRIBUTION ----------- 
        if 'rice_yield_kg_per_ha' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(df['rice_yield_kg_per_ha'], bins=20, kde=True, color='green')
            plt.title('Rice Yield Distribution (Kg per ha)')
            plt.xlabel('Rice Yield (Kg per ha)')
            plt.ylabel('Frequency')
            st.pyplot(plt)
        else:
            st.write("Error: Missing necessary column for Rice Yield Distribution.")

        # ----------- RICE AND WHEAT AREA VS PRODUCTION ----------- 
        if 'rice_area_1000_ha' in df.columns and 'rice_production_1000_tons' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=df['rice_area_1000_ha'], y=df['rice_production_1000_tons'], color='green')
            plt.title('Rice Area vs Rice Production')
            plt.xlabel('Rice Area (1000 ha)')
            plt.ylabel('Rice Production (1000 tons)')
            st.pyplot(plt)

        if 'wheat_area_1000_ha' in df.columns and 'wheat_production_1000_tons' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=df['wheat_area_1000_ha'], y=df['wheat_production_1000_tons'], color='orange')
            plt.title('Wheat Area vs Wheat Production')
            plt.xlabel('Wheat Area (1000 ha)')
            plt.ylabel('Wheat Production (1000 tons)')
            st.pyplot(plt)

        # ----------- MAIZE AREA AND PRODUCTION ----------- 
        if 'maize_area_1000_ha' in df.columns and 'maize_production_1000_tons' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=df['maize_area_1000_ha'], y=df['maize_production_1000_tons'], color='yellow')
            plt.title('Maize Area vs Maize Production')
            plt.xlabel('Maize Area (1000 ha)')
            plt.ylabel('Maize Production (1000 tons)')
            st.pyplot(plt)

        # ----------- CROPS AREA AND PRODUCTION COMPARISON ----------- 
        if 'year' in df.columns and 'state_name' in df.columns and 'rice_area_1000_ha' in df.columns:
            crops_data = df[['year', 'state_name', 'rice_area_1000_ha', 'wheat_area_1000_ha', 'maize_area_1000_ha', 
                             'rice_production_1000_tons', 'wheat_production_1000_tons', 'maize_production_1000_tons']]

            # Plot crops area vs production for each crop
            plt.figure(figsize=(12, 8))
            plt.subplot(2, 2, 1)
            plt.scatter(crops_data['rice_area_1000_ha'], crops_data['rice_production_1000_tons'], color='green')
            plt.title('Rice Area vs Rice Production')
            plt.xlabel('Rice Area (1000 ha)')
            plt.ylabel('Rice Production (1000 tons)')

            plt.subplot(2, 2, 2)
            plt.scatter(crops_data['wheat_area_1000_ha'], crops_data['wheat_production_1000_tons'], color='orange')
            plt.title('Wheat Area vs Wheat Production')
            plt.xlabel('Wheat Area (1000 ha)')
            plt.ylabel('Wheat Production (1000 tons)')

            plt.subplot(2, 2, 3)
            plt.scatter(crops_data['maize_area_1000_ha'], crops_data['maize_production_1000_tons'], color='yellow')
            plt.title('Maize Area vs Maize Production')
            plt.xlabel('Maize Area (1000 ha)')
            plt.ylabel('Maize Production (1000 tons)')

            plt.tight_layout()
            st.pyplot(plt)
    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please upload a CSV file to proceed.")
