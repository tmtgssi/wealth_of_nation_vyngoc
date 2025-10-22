import streamlit as st
import pandas as pd
import wbgapi as wb
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration: title and wide layout
st.set_page_config(page_title="Wealth of Nations", layout="wide")

# Main title of the dashboard
st.title("Wealth of Nations Dashboard")

# Description of the dashboard
st.write("""
Explore the relationship between GDP per capita and Life Expectancy across countries and years.
Data source: World Bank Open Data API - wbgapi
""")

# Cache the data loading function to avoid reloading on every interaction; cache expires every hour (3600 seconds)
@st.cache_data(ttl=3600)
def load_data(countries, start, end):
    # Fetch GDP per capita data from World Bank for selected countries and years; returns DataFrame
    gdp = wb.data.DataFrame('NY.GDP.PCAP.CD', countries, range(start, end + 1), labels=True).reset_index()
    # Fetch Life Expectancy data from World Bank for the same countries and years
    life_exp = wb.data.DataFrame('SP.DYN.LE00.IN', countries, range(start, end + 1), labels=True).reset_index()
    
    # Rename columns that start with 'YR' to remove 'YR' prefix (e.g., 'YR2000' -> '2000')
    gdp = gdp.rename(columns=lambda x: x[2:] if x.startswith('YR') else x)
    life_exp = life_exp.rename(columns=lambda x: x[2:] if x.startswith('YR') else x)
    
    # Convert wide-format DataFrame to long-format for GDP
    gdp_long = pd.melt(gdp, id_vars=['economy', 'Country'], var_name='Year', value_name='GDP_per_Capita')
    # Convert wide-format DataFrame to long-format for Life Expectancy
    life_exp_long = pd.melt(life_exp, id_vars=['economy', 'Country'], var_name='Year', value_name='Life_Expectancy')
    
    # Extract year number from 'Year' column (string) and convert to integer for GDP
    gdp_long['Year'] = gdp_long['Year'].str.extract('(\d+)').astype(int)
    # Convert Life Expectancy 'Year' column to integer type
    life_exp_long['Year'] = life_exp_long['Year'].astype(int)
    
    # Merge GDP and Life Expectancy dataframes on economy, Country, and Year columns
    merged = pd.merge(gdp_long, life_exp_long, on=['economy', 'Country', 'Year'])
    
    # Filter merged data to include only the selected year range
    merged = merged[(merged['Year'] >= start) & (merged['Year'] <= end)]
    
    return merged

# Sidebar header for filter options
st.sidebar.header("Filter Options")

# Load all countries data from World Bank API
all_countries = wb.economy.DataFrame()

# Extract country names for selection in sidebar
country_names = all_countries['name'].tolist()

# Multi-select widget to allow user to select multiple countries; default selected countries provided
selected_countries = st.sidebar.multiselect(
    "Select countries:",
    options=country_names,
    default=["United States", "China", "India", "Brazil"]
)

# Slider widget to select start year (between 2000 and 2020, default 2000)
start_year = st.sidebar.slider("Start year", 2000, 2020, 2000)

# Slider widget to select end year (between 2000 and 2020, default 2020)
end_year = st.sidebar.slider("End year", 2000, 2020, 2020)

# Load economies DataFrame again to map country names to their codes (WB uses codes to query)
economies = wb.economy.DataFrame()

# Map selected country names to their corresponding economy codes for querying WB data
selected_codes = [code for code, name in zip(economies.index, economies['name']) if name in selected_countries]

# Load the merged GDP and Life Expectancy data using cached function
data = load_data(selected_codes, start_year, end_year)

# Display a header describing the data shown below
st.header(f"Data for selected countries from {start_year} to {end_year}")

# Display the first 20 rows of the data in an interactive table
st.dataframe(data.head(20))

# Set seaborn style for plots
sns.set(style="whitegrid")

# Create the first plot: GDP per Capita over time
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=data, x='Year', y='GDP_per_Capita', hue='Country', marker="o", ax=ax)
ax.set_title("GDP per Capita Over Time")
ax.set_ylabel("GDP per Capita (current US$)")
ax.legend(title="Country", loc='upper left')
st.pyplot(fig)  # Show plot in Streamlit app

# Create the second plot: Life Expectancy over time
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=data, x='Year', y='Life_Expectancy', hue='Country', marker="o", ax=ax2)
ax2.set_title("Life Expectancy Over Time")
ax2.set_ylabel("Life Expectancy (years)")
ax2.legend(title="Country", loc='upper left')
st.pyplot(fig2)  # Show plot in Streamlit app
