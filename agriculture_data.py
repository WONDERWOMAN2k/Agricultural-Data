# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files  # Only necessary in Google Colab

# Upload the file (this will open a file picker)
uploaded = files.upload()

# Once uploaded, the file will be in the current directory
data_file_path = list(uploaded.keys())[0]  # This will get the uploaded file's name

# Load the dataset
try:
    df = pd.read_csv(data_file_path)
    print("Data loaded successfully!")
except FileNotFoundError:
    print(f"Error: The file '{data_file_path}' was not found.")
    exit()

# Clean column names by replacing spaces with underscores, removing parentheses, and converting to lowercase
df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.lower()

# Check the updated column names to confirm changes
print("Updated Column Names:")
print(df.columns)

# Check the first few rows of the dataframe to ensure data is correct
print("Data Preview:")
print(df.head())

# ----------- CORRELATION HEATMAP ----------- 
# Calculate the correlation matrix
correlation_matrix = df.corr()

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title("Correlation Heatmap of Agricultural Data")
plt.show()

# ----------- RICE AND WHEAT PRODUCTION OVER TIME ----------- 
# Check if columns exist before plotting
if 'year' in df.columns and 'rice_production_1000_tons' in df.columns and 'wheat_production_1000_tons' in df.columns:
    plt.figure(figsize=(10, 6))
    plt.plot(df['year'], df['rice_production_1000_tons'], label='Rice Production (1000 tons)', color='green')
    plt.plot(df['year'], df['wheat_production_1000_tons'], label='Wheat Production (1000 tons)', color='orange')
    plt.xlabel('Year')
    plt.ylabel('Production (1000 tons)')
    plt.title('Rice and Wheat Production Over Time')
    plt.legend()
    plt.show()
else:
    print("Error: Missing necessary columns for Rice and Wheat production over time.")

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
    plt.show()
else:
    print("Error: Missing necessary columns for Top 5 States by Rice Production.")

# ----------- RICE YIELD DISTRIBUTION ----------- 
if 'rice_yield_kg_per_ha' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['rice_yield_kg_per_ha'], bins=20, kde=True, color='green')
    plt.title('Rice Yield Distribution (Kg per ha)')
    plt.xlabel('Rice Yield (Kg per ha)')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("Error: Missing necessary column for Rice Yield Distribution.")

# ----------- RICE AND WHEAT AREA VS PRODUCTION ----------- 
# Plot rice area vs production
if 'rice_area_1000_ha' in df.columns and 'rice_production_1000_tons' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['rice_area_1000_ha'], y=df['rice_production_1000_tons'], color='green')
    plt.title('Rice Area vs Rice Production')
    plt.xlabel('Rice Area (1000 ha)')
    plt.ylabel('Rice Production (1000 tons)')
    plt.show()

# Plot wheat area vs production
if 'wheat_area_1000_ha' in df.columns and 'wheat_production_1000_tons' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['wheat_area_1000_ha'], y=df['wheat_production_1000_tons'], color='orange')
    plt.title('Wheat Area vs Wheat Production')
    plt.xlabel('Wheat Area (1000 ha)')
    plt.ylabel('Wheat Production (1000 tons)')
    plt.show()

# ----------- MAIZE AREA AND PRODUCTION ----------- 
if 'maize_area_1000_ha' in df.columns and 'maize_production_1000_tons' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['maize_area_1000_ha'], y=df['maize_production_1000_tons'], color='yellow')
    plt.title('Maize Area vs Maize Production')
    plt.xlabel('Maize Area (1000 ha)')
    plt.ylabel('Maize Production (1000 tons)')
    plt.show()

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
    plt.show()
else:
    print("Error: Missing necessary columns for Crops Area and Production Comparison.")
