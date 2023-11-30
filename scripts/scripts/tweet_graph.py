#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load the dataset from the uploaded CSV file
    data_path = 'combined.csv'
    data = pd.read_csv(data_path)

    # Convert 'Date' column to datetime and create 'Month-Year' for aggregation
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month-Year'] = data['Date'].dt.to_period('M')

    # Calculate the metrics
    data['Total Engagements'] = data['likes'] + data['replies'] + data['retweets']
    data['Weighted Engagement'] = (data['likes'] * 0.5 +
                                   data['retweets'] * 1 +
                                   data['replies'] * 27)

    # Aggregate the data month over month
    monthly_totals = data.drop(columns='Date').groupby('Month-Year').sum()
    # Extracting the 'Month-Year' periods for the x-axis in the correct order
    month_year_periods = monthly_totals.index.astype(str)

    # Plotting the figures
    plot_figures(month_year_periods, monthly_totals)

def plot_figures(month_year_periods, monthly_totals):
    # Creating the first figure for Tweets Published, Total Engagements, New Followers, and Impressions
    fig1, axes1 = plt.subplots(3, 1, figsize=(12, 20), sharex=True)
    # axes1[0].plot(month_year_periods, monthly_totals['Tweets published'], label='Tweets Published', color='brown')
    # axes1[0].set_title('Tweets Published over Time')
    # axes1[0].legend()

    axes1[0].plot(month_year_periods, monthly_totals['Total Engagements'], label='Total Engagements', color='magenta')
    axes1[0].set_title('Total Engagements over Time')
    axes1[0].legend()

    axes1[1].plot(month_year_periods, monthly_totals['follows'], label='New Followers', color='purple')
    axes1[1].set_title('New Followers over Time')
    axes1[1].legend()

    axes1[2].plot(month_year_periods, monthly_totals['impressions'], label='Impressions', color='orange')
    axes1[2].set_title('Impressions over Time')
    axes1[2].legend()

    for ax in axes1:
        for label in ax.get_xticklabels():
            label.set_rotation(90)

    fig1.tight_layout()
    fig1.savefig('out/figure_one.png')

    # Creating the second figure for Impressions, Weighted Engagements, Profile Views, and Combined Engagements
    fig2, axes2 = plt.subplots(4, 1, figsize=(12, 20), sharex=True)
    axes2[0].plot(month_year_periods, monthly_totals['impressions'], label='Impressions', color='orange')
    axes2[0].set_title('Impressions over Time')
    axes2[0].legend()

    axes2[1].plot(month_year_periods, monthly_totals['Weighted Engagement'], label='Weighted Engagement', color='teal')
    axes2[1].set_title('Weighted Engagement over Time')
    axes2[1].legend()

    axes2[2].plot(month_year_periods, monthly_totals['user profile clicks'], label='Profile Views', color='cyan')
    axes2[2].set_title('Profile Views over Time')
    axes2[2].legend()

    axes2[3].plot(month_year_periods, monthly_totals['likes'], label='Likes', color='red')
    axes2[3].plot(month_year_periods, monthly_totals['replies'], label='Replies', color='green')
    axes2[3].plot(month_year_periods, monthly_totals['retweets'], label='Retweets', color='blue')
    axes2[3].set_title('Combined Engagements over Time')
    axes2[3].legend()

    for ax in axes2:
        for label in ax.get_xticklabels():
            label.set_rotation(90)

    fig2.tight_layout()
    fig2.savefig('out/figure_two.png')

if __name__ == "__main__":
    main()
