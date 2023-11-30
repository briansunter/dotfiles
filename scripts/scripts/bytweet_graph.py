#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load the dataset
    data_path = 'combined.csv'
    data = pd.read_csv(data_path)

    # Ensure the time column is in datetime format
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M %z')

    # Resample the data to sum up the metrics for each month
    data.set_index('time', inplace=True)
    monthly_data = data.resample('M').sum()

    # Plotting the metrics aggregated by month
    plot_metrics_by_month(monthly_data)

def plot_metrics_by_month(monthly_data):
    fig, axes = plt.subplots(5, 1, figsize=(12, 25))

    # Setting the x-axis labels as month-year format
    x_labels = monthly_data.index.strftime('%Y-%m')

    # Plot for each metric
    plot_bar_chart(axes[0], x_labels, monthly_data['impressions'], 'Monthly Impressions', 'Impressions')
    plot_bar_chart(axes[1], x_labels, monthly_data['engagements'], 'Monthly Engagements', 'Engagements')
    plot_bar_chart(axes[2], x_labels, monthly_data['retweets'], 'Monthly Retweets', 'Retweets')
    plot_bar_chart(axes[3], x_labels, monthly_data['replies'], 'Monthly Replies', 'Replies')
    plot_bar_chart(axes[4], x_labels, monthly_data['likes'], 'Monthly Likes', 'Likes')

    # Adjusting layout and saving the figure
    plt.tight_layout()
    plt.savefig('out/tweet_metrics.png')

def plot_bar_chart(ax, x_labels, y_values, title, ylabel):
    ax.bar(x_labels, y_values, color='orange')
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=10)

if __name__ == "__main__":
    main()
