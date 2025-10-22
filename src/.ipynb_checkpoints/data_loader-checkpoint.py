# Import pandas for data manipulation
import pandas as pd

# Import wbgapi to access World Bank data via API
import wbgapi as wb

# Function to fetch a single World Bank indicator (e.g., GDP, life expectancy) for a list of countries over time
def fetch_world_bank_indicator(indicator: str,
                               countries: list,
                               start_year: int,
                               end_year: int) -> pd.DataFrame:
    try:
        # Use wbgapi to download the indicator data for selected countries and years
        df = wb.data.DataFrame(indicator,
                               economy=countries,                  # List of country codes (e.g., ['USA', 'VNM'])
                               time=range(start_year, end_year+1)) # Time range as a list of years
    except Exception as e:
        # Raise a descriptive error if something goes wrong
        raise RuntimeError(f"Error fetching indicator {indicator}: {e}")

    # Reset the index to turn it into a standard DataFrame
    df = df.reset_index()

    # Rename the indicator column to a general name 'value' (e.g., the actual indicator code is replaced)
    df = df.rename(columns={indicator: 'value'})

    # Keep only relevant columns: country code, year, and value
    df = df[['economy', 'time', 'value']]

    # Rename columns to standardized names
    df = df.rename(columns={'economy': 'country', 'time': 'year'})

    # Return the cleaned and standardized DataFrame
    return df

# Function to load multiple World Bank indicators at once using their codes
def load_world_bank_data(indicators, countries, years):
    # This downloads data for multiple indicators with human-readable labels (e.g., indicator names and country names)
    df = wb.data.DataFrame(indicators,
                           countries,
                           time=years,
                           labels=True  # Adds readable country and series labels
                          ).reset_index()
    
    return df  # Return the DataFrame with indicators
