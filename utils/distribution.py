import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, kstest, probplot

# Load the data (assuming 'data' is already a pandas DataFrame)
# Example: data = pd.read_csv('fpl_data.csv')

# List of features to check for normal distribution
features = ['goals_scored', 'assists', 'expected_goals', 'expected_assists', 'minutes', 'bps']


def distribution_check(data):
    # Plot histograms and Q-Q plots
    for feature in features:
        plt.figure(figsize=(12, 5))

        # Histogram
        plt.subplot(1, 2, 1)
        sns.histplot(data[feature], kde=True)
        plt.title(f'Histogram of {feature}')

        # Q-Q plot
        plt.subplot(1, 2, 2)
        probplot(data[feature], dist="norm", plot=plt)
        plt.title(f'Q-Q Plot of {feature}')

        plt.tight_layout()
        plt.show()

        plt.savefig(f'distribution_{feature}.png')

        # Shapiro-Wilk test
        shapiro_test = shapiro(data[feature])
        print(f'Shapiro-Wilk Test for {feature}: p-value = {shapiro_test.pvalue}')

        # Kolmogorov-Smirnov test against a normal distribution
        ks_test = kstest(data[feature], 'norm', args=(data[feature].mean(), data[feature].std()))
        print(f'Kolmogorov-Smirnov Test for {feature}: p-value = {ks_test.pvalue}\n')
