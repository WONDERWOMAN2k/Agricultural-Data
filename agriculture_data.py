# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Agricultural Data.csv')

# Clean column names by replacing spaces with underscores, removing parentheses, and converting to lowercase
df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.lower()

# Check the updated column names to confirm changes
print(df.columns)

# ----------- CORRELATION HEATMAP -----------
# Calculate the correlation matrix
correlation_matrix = df.corr()

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title("Correlation Heatmap of Agricultural Data")
plt.show()

# ----------- RICE AND WHEAT PRODUCTION OVER TIME -----------
# Plot rice and wheat production over time
plt.figure(figsize=(10, 6))
plt.plot(df['year'], df['rice_production_1000_tons'], label='Rice Production (1000 tons)', color='green')
plt.plot(df['year'], df['wheat_production_1000_tons'], label='Wheat Production (1000 tons)', color='orange')
plt.xlabel('Year')
plt.ylabel('Production (1000 tons)')
plt.title('Rice and Wheat Production Over Time')
plt.legend()
plt.show()

# ----------- TOP 5 STATES BY RICE PRODUCTION -----------
# Group by state and sum the rice production
top_states = df.groupby('state_name')['rice_production_1000_tons'].sum().nlargest(5)

# Plot the top 5 states
plt.figure(figsize=(10, 6))
top_states.plot(kind='bar', color='blue')
plt.xlabel('State')
plt.ylabel('Rice Production (1000 tons)')
plt.title('Top 5 States by Rice Production')
plt.xticks(rotation=45)
plt.show()

# ----------- RICE YIELD DISTRIBUTION -----------
# Plot the distribution of rice yield
plt.figure(figsize=(10, 6))
sns.histplot(df['rice_yield_kg_per_ha'], bins=20, kde=True, color='green')
plt.title('Rice Yield Distribution (Kg per ha)')
plt.xlabel('Rice Yield (Kg per ha)')
plt.ylabel('Frequency')
plt.show()

# ----------- RICE AND WHEAT AREA VS PRODUCTION -----------
# Plot rice area vs production
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['rice_area_1000_ha'], y=df['rice_production_1000_tons'], color='green')
plt.title('Rice Area vs Rice Production')
plt.xlabel('Rice Area (1000 ha)')
plt.ylabel('Rice Production (1000 tons)')
plt.show()

# Plot wheat area vs production
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['wheat_area_1000_ha'], y=df['wheat_production_1000_tons'], color='orange')
plt.title('Wheat Area vs Wheat Production')
plt.xlabel('Wheat Area (1000 ha)')
plt.ylabel('Wheat Production (1000 tons)')
plt.show()

# ----------- TOP 5 STATES BY WHEAT PRODUCTION -----------
# Group by state and sum the wheat production
top_wheat_states = df.groupby('state_name')['wheat_production_1000_tons'].sum().nlargest(5)

# Plot the top 5 states for wheat production
plt.figure(figsize=(10, 6))
top_wheat_states.plot(kind='bar', color='orange')
plt.xlabel('State')
plt.ylabel('Wheat Production (1000 tons)')
plt.title('Top 5 States by Wheat Production')
plt.xticks(rotation=45)
plt.show()

# ----------- MAIZE AREA AND PRODUCTION -----------
# Plot maize area vs production
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['maize_area_1000_ha'], y=df['maize_production_1000_tons'], color='yellow')
plt.title('Maize Area vs Maize Production')
plt.xlabel('Maize Area (1000 ha)')
plt.ylabel('Maize Production (1000 tons)')
plt.show()

# ----------- CROPS AREA AND PRODUCTION COMPARISON -----------
# Select relevant columns for different crops
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
