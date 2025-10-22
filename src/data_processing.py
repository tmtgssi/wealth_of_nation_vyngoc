# Import pandas library for data manipulation
import pandas as pd

# Function to reshape raw World Bank data from wide format to long and then back to wide format
def pivot_data(df):
    # Identify all columns that start with 'YR' (e.g., 'YR2000', 'YR2001', ...)
    year_cols = [col for col in df.columns if col.startswith('YR')]

    # Reshape the DataFrame from wide to long format
    df_long = df.melt(id_vars=['economy', 'Country', 'series'],  # Keep these columns fixed
                      value_vars=year_cols,                     # Convert year columns into rows
                      var_name='Year',                          # New column name for years
                      value_name='Value')                       # New column name for values

    # Remove the 'YR' prefix and convert year to integer
    df_long['Year'] = df_long['Year'].str.replace('YR', '').astype(int)

    # Pivot the long-format DataFrame to a wide format
    df_wide = df_long.pivot_table(index=['economy', 'Country', 'Year'],  # Rows identified by these
                                  columns='series',                      # Each series becomes a column
                                  values='Value').reset_index()         # Flatten the index

    # Rename series codes to readable names
    df_wide = df_wide.rename(columns={
        'NY.GDP.PCAP.CD': 'GDP_per_Capita',        # GDP per capita
        'SP.DYN.LE00.IN': 'Life_Expectancy'        # Life expectancy
    })

    return df_wide  # Return the reshaped and renamed DataFrame

# Function to merge two DataFrames on specific keys (usually country and year)
def merge_indicators(df1: pd.DataFrame,
                     df2: pd.DataFrame,
                     how: str = 'inner',
                     on: list = ['country','year']) -> pd.DataFrame:
    # Merge the two DataFrames using pandas merge
    merged = pd.merge(df1, df2, how=how, on=on, suffixes=('_1', '_2'))

    return merged  # Return the merged result

# Function to remove rows with too many missing values
def clean_missing_values(df: pd.DataFrame,
                         threshold: float = 0.2) -> pd.DataFrame:
    # Drop rows where the number of non-NA values is less than the threshold
    df = df.dropna(thresh=int((1 - threshold) * df.shape[1]), axis=0)

    return df  # Return the cleaned DataFrame

# Function to rename columns to standard names for consistency
def clean_data(df):
    # Rename specific columns if the original codes exist
    df = df.rename(columns={
        'NY.GDP.PCAP.CD': 'GDP_per_Capita',
        'SP.DYN.LE00.IN': 'Life_Expectancy'
    })

    return df  # Return the DataFrame with renamed columns
