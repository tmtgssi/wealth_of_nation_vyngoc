# Import required libraries
import seaborn as sns                 # Seaborn for statistical data visualization
import matplotlib.pyplot as plt      # Matplotlib for creating static plots
import pandas as pd                  # Pandas for data manipulation and analysis

# Function to plot a time series line chart for a given indicator (e.g., GDP or Life Expectancy)
def plot_indicator_time_series(df: pd.DataFrame,
                               country_col: str,
                               year_col: str,
                               value_col: str,
                               countries: list,
                               title: str = ""):
    plt.figure(figsize=(10,6))  # Set the size of the figure (width=10, height=6 inches)

    # Filter the data for the selected countries and create a line plot
    sns.lineplot(data=df[df[country_col].isin(countries)],
                 x=year_col, y=value_col, hue=country_col)

    # Set the title and axis labels
    plt.title(title)            # Title of the plot
    plt.xlabel("Year")          # Label for the X-axis
    plt.ylabel(value_col)       # Label for the Y-axis (based on the data column)

    plt.legend(title=country_col)  # Show legend with country names
    plt.tight_layout()             # Adjust layout to prevent clipping
    plt.show()                     # Display the plot

# Function to create a scatter plot for two indicators in a specific year
def scatter_indicator(df: pd.DataFrame,
                      x_col: str,
                      y_col: str,
                      year: int,
                      country_col: str,
                      title: str = ""):
    # Filter the dataset to include only the specified year
    subset = df[df['year'] == year]

    plt.figure(figsize=(8,6))  # Set the figure size

    # Create a scatter plot with countries color-coded
    sns.scatterplot(data=subset, x=x_col, y=y_col, hue=country_col)

    # Set the plot title and axis labels
    plt.title(f"{title} ({year})")  # Include year in title
    plt.xlabel(x_col)               # X-axis label based on chosen column
    plt.ylabel(y_col)               # Y-axis label based on chosen column

    plt.tight_layout()              # Optimize layout
    plt.show()                      # Display the plot

# Function to compare average GDP per capita and life expectancy per country
def plot_gdp_vs_life_expectancy(summary_df):
    plt.figure(figsize=(10,6))  # Set figure size

    # Create a scatter plot with GDP per capita on X-axis and life expectancy on Y-axis
    sns.scatterplot(data=summary_df, x='GDP_per_Capita', y='Life_Expectancy')

    # Add title and axis labels
    plt.title('Average GDP per Capita vs Life Expectancy by Country')
    plt.xlabel('GDP per Capita (USD)')
    plt.ylabel('Life Expectancy (years)')

    plt.grid(True)  # Add a grid to the background for better readability
    plt.show()      # Display the plot
