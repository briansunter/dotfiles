#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load the dataset
    combined_data_path = 'combined.csv'
    bytime_data_path = 'combined_bytime.csv'
    combined_data = pd.read_csv(combined_data_path)
    bytime_data = pd.read_csv(bytime_data_path)

    # Format datetime columns
    bytime_data['Date'] = pd.to_datetime(bytime_data['Date'])
    combined_data['time'] = pd.to_datetime(combined_data['time']).dt.tz_convert(None)

    # Prepare data for plots
    monthly_tweet_count, monthly_data, combined_monthly_data = prepare_data(combined_data, bytime_data)

    # Plotting tweet quality metrics
    fig, axs = plt.subplots(3, 1, figsize=(14, 21))
    plot_tweets_per_month(monthly_tweet_count, axs[0])
    plot_engagement_rate(monthly_data['engagement_rate'][-12:], axs[1])
    plot_followers_per_tweet(combined_monthly_data, axs[2])
    plt.tight_layout()
    plt.savefig('out/tweet_quality.png')

    # Plotting growth over time
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    plot_follower_growth(bytime_data, axs[0])
    plot_engagements_over_time(combined_data, axs[1])
    plot_impressions_over_time(combined_data, axs[2])
    plt.tight_layout()
    plt.savefig('out/combined_plots.png')
    plt.close()

def prepare_data(combined_data, bytime_data):
    # Resample and prepare data for plots
    combined_data.set_index('time', inplace=True)

    monthly_tweet_count = combined_data.resample('M').size()
    monthly_data = combined_data.resample('M').sum()
    monthly_data['engagement_rate'] = monthly_data['engagements'] / monthly_data['impressions']

    monthly_follows = bytime_data.groupby(pd.Grouper(key='Date', freq='M')).agg({'follows': 'sum'})
    monthly_tweets_data = combined_data.resample('M').agg({'impressions': 'sum', 'engagements': 'sum'})
    monthly_tweets_data['tweets_count'] = combined_data.resample('M').size()
    combined_monthly_data = pd.merge(monthly_tweets_data, monthly_follows, left_index=True, right_index=True, how='inner')
    combined_monthly_data['followers_per_tweet'] = combined_monthly_data['follows'] / combined_monthly_data['tweets_count']
    return monthly_tweet_count, monthly_data, combined_monthly_data



def plot_engagement_rate(engagement_rate, ax):
    # Calculate the average for the latest 3 months
    avg_engagement_rate_3_months = engagement_rate[-3:].mean()

    # Calculate the average for the previous 3 months
    prev_avg_engagement_rate_3_months = engagement_rate[-6:-3].mean()

    # Calculate percentage difference
    diff_percent = ((avg_engagement_rate_3_months - prev_avg_engagement_rate_3_months) / prev_avg_engagement_rate_3_months) * 100

    # Choose color based on difference
    color = 'green' if diff_percent >= 0 else 'red'

    # Plot previous 3-month average
    ax.axhline(y=prev_avg_engagement_rate_3_months, color='gray', linestyle=':', linewidth=2)
    ax.text(engagement_rate.index[-6], prev_avg_engagement_rate_3_months, f' Prev Avg: {prev_avg_engagement_rate_3_months:.4f}', verticalalignment='bottom', fontsize=12)

    # Plot current 3-month average
    ax.axhline(y=avg_engagement_rate_3_months, color='gray', linestyle='--', linewidth=2)
    ax.text(engagement_rate.index[-3], avg_engagement_rate_3_months, f' Current Avg: {avg_engagement_rate_3_months:.4f}', verticalalignment='bottom', fontsize=12)

    # Plot percentage difference
    ax.text(engagement_rate.index[-1], avg_engagement_rate_3_months, f' Diff: {diff_percent:.2f}%', verticalalignment='top', color=color, fontsize=12)

    # Plot the line chart
    ax.plot(engagement_rate.index, engagement_rate, color='tab:red', marker='o', linestyle='-', markersize=8)

    # Set labels and title
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Engagement Rate', fontsize=14)
    ax.set_title('Engagement Rate per Month', fontsize=16)
    ax.grid(True)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)


def plot_horizontal_line_with_growth(data, ax, field, color, title, ylabel):
    # Calculate the average for the latest 3 months
    avg_last_3_months = data[field][-3:].mean()

    # Calculate the average for the previous 3 months
    avg_prev_3_months = data[field][-6:-3].mean()

    # Calculate percentage difference
    diff_percent = ((avg_last_3_months - avg_prev_3_months) / avg_prev_3_months) * 100

    # Choose color based on difference
    growth_color = 'green' if diff_percent >= 0 else 'red'

    # Plot previous 3-month average
    ax.axhline(y=avg_prev_3_months, color='darkgray', linestyle=':', linewidth=3)
    ax.text(data.index[-6], avg_prev_3_months, f' Prev Avg: {avg_prev_3_months:.2f}', verticalalignment='bottom', fontsize=14, fontweight='bold')

    # Plot current 3-month average
    ax.axhline(y=avg_last_3_months, color='darkgray', linestyle='-', linewidth=3)
    ax.text(data.index[-3], avg_last_3_months, f' Current Avg: {avg_last_3_months:.2f}', verticalalignment='bottom', fontsize=14, fontweight='bold')

    # Plot percentage difference
    ax.text(data.index[-1], avg_last_3_months, f' Diff: {diff_percent:.2f}%', verticalalignment='top', color=growth_color, fontsize=14, fontweight='bold')

    # Plot the bar chart
    ax.bar(data.index, data[field], color=color, width=20.0)

    # Set labels and title
    ax.set_xlabel('Month', fontsize=15)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_title(title, fontsize=18, fontweight='bold')
    ax.grid(True)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)



def plot_tweets_per_month(monthly_tweet_count, ax):
    # Convert the Series to a DataFrame and assign a column name
    monthly_tweet_count_df = monthly_tweet_count.to_frame('tweet_count')
    plot_horizontal_line_with_growth(monthly_tweet_count_df, ax, 'tweet_count', 'tab:blue', 'Number of Tweets per Month', 'Number of Tweets')

def plot_followers_per_tweet(combined_monthly_data, ax):
    plot_horizontal_line_with_growth(combined_monthly_data, ax, 'followers_per_tweet', 'tab:green', 'Followers per Tweet per Month', 'Followers per Tweet')

def plot_follower_growth(bytime_data, ax):
    new_followers_per_month = bytime_data.groupby(pd.Grouper(key='Date', freq='M')).agg({'follows': 'sum'})
    plot_horizontal_line_with_growth(new_followers_per_month, ax, 'follows', 'tab:purple', 'New Followers Per Month', 'New Followers')

def plot_engagements_over_time(combined_data, ax):
    monthly_engagements = combined_data.resample('M').agg({'engagements': 'sum'})
    plot_horizontal_line_with_growth(monthly_engagements, ax, 'engagements', 'tab:orange', 'Engagements Over Time', 'Total Engagements')

def plot_impressions_over_time(combined_data, ax):
    monthly_impressions = combined_data.resample('M').agg({'impressions': 'sum'})
    plot_horizontal_line_with_growth(monthly_impressions, ax, 'impressions', 'tab:blue', 'Impressions Over Time', 'Total Impressions')

main()