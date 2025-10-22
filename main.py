# Import modules from the src package to load data, process it, analyze, and visualize
from src import data_loader, data_processing, analysis, visualization

# Define the main function which will run the core workflow
def main():
    # List of World Bank indicator codes for GDP per capita and life expectancy
    indicators = ['NY.GDP.PCAP.CD', 'SP.DYN.LE00.IN']
    
    # Specify countries to fetch data for; 'all' means all available countries
    countries = 'all'  # Alternatively, use a list like ['USA', 'CAN', 'BRA']
    
    # Define the range of years to collect data for (2000 to 2020 inclusive)
    years = range(2000, 2021)
    
    # Load raw data from World Bank API using the data_loader module
    df_raw = data_loader.load_world_bank_data(indicators, countries, years)
    
    # Transform raw data into a clean, pivoted format with indicators as columns
    df_clean = data_processing.pivot_data(df_raw)
    
    # Compute summary statistics such as average GDP per capita and life expectancy by country
    summary = analysis.compute_summary_stats(df_clean)
    
    # Print the first few rows of the summary DataFrame to console
    print(summary.head())
    
    # Visualize the relationship between GDP per capita and life expectancy using the visualization module
    visualization.plot_gdp_vs_life_expectancy(summary)

# If this script is run directly (not imported as a module), execute main()
if __name__ == "__main__":
    main()
