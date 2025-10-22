# Import numpy for numerical operations
import numpy as np

# Import pandas for DataFrame handling
import pandas as pd

# Import stats module from scipy for statistical calculations
from scipy import stats

# Function to compute the Pearson correlation coefficient between two columns in a DataFrame
def compute_correlation(df: pd.DataFrame,
                        x_col: str,
                        y_col: str) -> float:
    # Select the two columns and drop any rows with missing values to ensure clean data
    clean = df[[x_col, y_col]].dropna()

    # If no data left after dropping NaNs, return NaN
    if clean.empty:
        return np.nan

    # Calculate Pearson correlation coefficient and p-value between x_col and y_col
    r, p_value = stats.pearsonr(clean[x_col], clean[y_col])

    # Print the correlation coefficient and p-value with 3 decimal places
    print(f"Pearson r = {r:.3f}, p‑value = {p_value:.3f}")

    # Return the correlation coefficient
    return r

# Function to compute yearly growth rate of a value column, grouped by country
def compute_yearly_growth(df: pd.DataFrame,
                          country_col: str,
                          year_col: str,
                          value_col: str) -> pd.DataFrame:
    # Sort the DataFrame by country and year to prepare for calculating change over time
    df = df.sort_values([country_col, year_col])

    # Calculate the percent change of the value column within each country group (year-over-year growth rate)
    df['growth_rate'] = df.groupby(country_col)[value_col].pct_change()

    # Return the DataFrame with the new 'growth_rate' column added
    return df

# Function to compute summary statistics (mean) for GDP per Capita and Life Expectancy by country
def compute_summary_stats(df):
    # List of required columns for the summary calculation
    required_cols = ['GDP_per_Capita', 'Life_Expectancy']

    # Check if all required columns are present in the DataFrame, raise error if any missing
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame missing required columns: {required_cols}")

    # Group data by 'Country' and compute the mean of the required columns, then reset index to flatten the result
    summary = df.groupby('Country')[required_cols].mean().reset_index()

    # Return the summary DataFrame containing average GDP per Capita and Life Expectancy per country
    return summary
