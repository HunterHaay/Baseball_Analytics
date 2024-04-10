import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# Get the user's downloads folder path
downloads_folder = os.path.expanduser('~') + '/Downloads/'

# Assuming the CSV file name is 'fangraphs-leaderboards 2.csv'
file_name = 'fangraphs-leaderboards.csv'

# Construct the file path
file_path = os.path.join(downloads_folder, file_name)

# Some CSV files may have encoding issues, so we try a different encoding if the default (utf-8) fails
try:
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
except Exception as e:
    # If there is an error, capture it for display
    print(e)
    data = None

if data is not None:
    # Rename the first entry in the columns
    data.columns.values[0] = 'Season'


# Assuming the data loaded successfully
if data is not None:
    # Function to find player stats for a given year
    def find_player_stats(player_name, year, df):
        # Filter the data for the player and the year
        player_data = df[(df['NameASCII'] == player_name) & (df['Season'] == year)]
       
        # Check if the player is found
        if player_data.empty:
            return None
        else:
            # Return the filtered data
            return player_data

    # User-provided player name and year
    player_name = "Ryan Braun"  # User-provided player name
    year = 2008                  # User-provided year

    # Search for the player and the year
    player_stats = find_player_stats(player_name, year, data)

    # If player stats are found, retrieve all years' wRC+ stats for that player
    if player_stats is not None:
        player_all_years_stats = data[data['NameASCII'] == player_name].sort_values(by='Season')
        wrc_plus_stats = player_all_years_stats[['Season', 'wRC+']].dropna()
       
        # Prepare the data for linear regression
        # Extract player's age for each season, assuming the player was 18 in their first season in 2016
        player_ages = wrc_plus_stats['Season'] 

        # Fit the linear regression model
        X = player_ages.values.reshape(-1, 1)  # Age needs to be 2D for the model
        y = wrc_plus_stats['wRC+'].values
        model = LinearRegression().fit(X, y)

        # Predict the wRC+ for the next age
        next_age = player_ages.iloc[-1] + 1
        predicted_wRC_plus = model.predict([[next_age]])

        # Create a scatter plot of the actual wRC+ values
        plt.scatter(player_ages, y, color='black', label='Actual wRC+')

        # Plot the linear regression line
        ages_range = np.linspace(player_ages.min(), next_age, 100).reshape(-1, 1)
        wrc_plus_fit = model.predict(ages_range)
        plt.plot(ages_range, wrc_plus_fit, color='blue', label='Regression Fit')

        # Mark the predicted wRC+ for the next season
        plt.scatter([next_age], predicted_wRC_plus, color='green', label='Predicted wRC+')

        # Add titles and labels
        plt.title('Aging Curve and wRC+ Linear Regression')
        plt.xlabel('Age')
        plt.ylabel('wRC+')
        plt.legend()

        # Save the figure
        plt_file_path = os.path.join(downloads_folder, 'aaron_judge_predicted_wrc_plus.png')
        plt.savefig(plt_file_path)

        # Show the plot
        plt.show()
else:
    print("Data could not be loaded.")
