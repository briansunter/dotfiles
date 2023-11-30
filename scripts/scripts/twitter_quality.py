#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load the dataset
    combined_data_path = 'combined.csv'
    bytime_data_path = 'combined_bytime.csv'
    combined_data = pd.read_csv(combined_data_path)
    bytime_data = pd.read_csv(bytime_data_path)

    # Ensure the Date column is in datetime format
    bytime_data['Date'] = pd.to_datetime(bytime_data['Date'])

    # Ensure the time column is in datetime format
    combined_data['time'] = pd.to_datetime(combined_data['time']).dt.tz_convert(None)

    # Resample the data to sum up the metrics for each month and count tweets per month
    combined_data.set_index('time', inplace=True)
    monthly_data = combined_data.resample('M').sum()
    monthly_tweet_count = combined_data.resample('M').size()

    # Calculate engagement rate per tweet as impressions to engagements
    monthly_data['engagement_rate'] = monthly_data['engagements'] / monthly_data['impressions']

    # Calculate the 6-month rolling average for the last 12 months for tweets and engagement rate
    avg_tweets_6_months = monthly_tweet_count[-12:].rolling(window=6).mean().iloc[-1]
    avg_engagement_rate_6_months = monthly_data['engagement_rate'][-12:].rolling(window=6).mean().iloc[-1]

    # Group by 'Date' instead of 'start_date'
    monthly_follows = bytime_data.groupby(pd.Grouper(key='Date', freq='M')).agg({'follows': 'sum'})

    # Resampling combined_data to monthly for tweet counts
    monthly_tweets_data = combined_data.resample('M').agg({'impressions': 'sum', 'engagements': 'sum'})
    monthly_tweets_data['tweets_count'] = combined_data.resample('M').size()

    # Merging the datasets with the monthly 'follows' data
    combined_monthly_data = pd.merge(monthly_tweets_data, monthly_follows, left_index=True, right_index=True, how='inner')

    # Calculating followers per tweet rate using the monthly 'follows'
    combined_monthly_data['followers_per_tweet'] = combined_monthly_data['follows'] / combined_monthly_data['tweets_count']

    # Calculate average followers per tweet
    average_followers_per_tweet_monthly = combined_monthly_data['followers_per_tweet'].mean()

    # Plotting number of tweets per month with 6-month average
    # Plotting engagement rate per month with 6-month average
    # Plotting followers per tweet
    fig, axs = plt.subplots(3, 1, figsize=(14, 21))

    # Plotting number of tweets per month with 6-month average
    plot_tweets_per_month(monthly_tweet_count, axs[0])

    # Plotting engagement rate per month with 6-month average
    plot_engagement_rate(monthly_data['engagement_rate'][-12:], axs[1])
    # Plotting followers per tweet
    plot_followers_per_tweet(combined_monthly_data, axs[2])
    # Save the figure
    plt.tight_layout()
    plt.savefig('out/tweet_quality.png')
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Plotting follower growth over time
    plot_follower_growth(bytime_data, axs[0])

    # Plotting follower growth rate
    # Plotting engagements over time
    plot_engagements_over_time(combined_data, axs[1])

    plot_impressions_over_time(combined_data, axs[2])  # New plot for impressions


    # Save the figure
    plt.tight_layout()
    plt.savefig('out/combined_plots.png')
    plt.close()

def plot_tweets_per_month(monthly_tweet_count, ax):
    # Calculate the average for the latest 3 months
    avg_tweets_3_months = monthly_tweet_count[-3:].mean()

    # Calculate the average for the previous 3 months
    prev_avg_tweets_3_months = monthly_tweet_count[-6:-3].mean()

    # Calculate percentage difference
    diff_percent = ((avg_tweets_3_months - prev_avg_tweets_3_months) / prev_avg_tweets_3_months) * 100

    # Choose color based on difference
    color = 'green' if diff_percent >= 0 else 'red'

    # Plot previous 3-month average
    ax.axhline(y=prev_avg_tweets_3_months, color='gray', linestyle=':', linewidth=2)
    ax.text(monthly_tweet_count.index[-6], prev_avg_tweets_3_months, f' Prev Avg: {prev_avg_tweets_3_months:.2f}', verticalalignment='bottom', fontsize=12)

    # Plot current 3-month average
    ax.axhline(y=avg_tweets_3_months, color='gray', linestyle='--', linewidth=2)
    ax.text(monthly_tweet_count.index[-3], avg_tweets_3_months, f' Current Avg: {avg_tweets_3_months:.2f}', verticalalignment='bottom', fontsize=12)

    # Plot percentage difference
    ax.text(monthly_tweet_count.index[-1], avg_tweets_3_months, f' Diff: {diff_percent:.2f}%', verticalalignment='top', color=color, fontsize=12)

    # Plot the bar chart
    ax.bar(monthly_tweet_count.index, monthly_tweet_count, color='tab:blue', width=20.0)  # Increase width here

    # Set labels and title
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Number of Tweets', fontsize=14)
    ax.set_title('Number of Tweets per Month', fontsize=16)
    ax.grid(True)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

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

def plot_followers_per_tweet(combined_monthly_data, ax):
    # Calculate the average for the latest 3 months
    avg_followers_per_tweet_3_months = combined_monthly_data['followers_per_tweet'][-3:].mean()

    # Calculate the average for the previous 3 months
    prev_avg_followers_per_tweet_3_months = combined_monthly_data['followers_per_tweet'][-6:-3].mean()

    # Calculate percentage difference
    diff_percent = ((avg_followers_per_tweet_3_months - prev_avg_followers_per_tweet_3_months) / prev_avg_followers_per_tweet_3_months) * 100

    # Choose color based on difference
    color = 'green' if diff_percent >= 0 else 'red'

    # Plot previous 3-month average
    ax.axhline(y=prev_avg_followers_per_tweet_3_months, color='gray', linestyle=':', linewidth=2)
    ax.text(combined_monthly_data.index[-6], prev_avg_followers_per_tweet_3_months, f' Prev Avg: {prev_avg_followers_per_tweet_3_months:.2f}', verticalalignment='bottom', fontsize=12)

    # Plot current 3-month average
    ax.axhline(y=avg_followers_per_tweet_3_months, color='gray', linestyle='--', linewidth=2)
    ax.text(combined_monthly_data.index[-3], avg_followers_per_tweet_3_months, f' Current Avg: {avg_followers_per_tweet_3_months:.2f}', verticalalignment='bottom', fontsize=12)

    # Plot percentage difference
    ax.text(combined_monthly_data.index[-1], avg_followers_per_tweet_3_months, f' Diff: {diff_percent:.2f}%', verticalalignment='top', color=color, fontsize=12)

    # Plot the bar chart
    ax.bar(combined_monthly_data.index, combined_monthly_data['followers_per_tweet'], color='tab:green', width=20.0)

    # Set labels and title
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Followers per Tweet', fontsize=14)
    ax.set_title('Followers per Tweet per Month', fontsize=16)
    ax.grid(True)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

def plot_follower_growth(bytime_data, ax):
    # Calculate new followers per month
    new_followers_per_month = bytime_data.groupby(pd.Grouper(key='Date', freq='M')).agg({'follows': 'sum'})

    # Plotting the new followers per month
    ax.bar(new_followers_per_month.index, new_followers_per_month['follows'], color='tab:purple', width=20.0)  # Increase width here
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('New Followers', fontsize=14)
    ax.set_title('New Followers Per Month', fontsize=16)
    ax.grid(True)

def plot_engagements_over_time(combined_data, ax):
    # Calculate total engagements over time
    monthly_engagements = combined_data.resample('M').agg({'engagements': 'sum'})

    # Plotting engagements over time
    ax.bar(monthly_engagements.index, monthly_engagements['engagements'], color='tab:orange', width=20.0)  # Increase width here
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Total Engagements', fontsize=14)
    ax.set_title('Engagements Over Time', fontsize=16)
    ax.grid(True)

def plot_impressions_over_time(combined_data, ax):
    # Calculate total impressions over time
    monthly_impressions = combined_data.resample('M').agg({'impressions': 'sum'})

    # Plotting impressions over time
    ax.bar(monthly_impressions.index, monthly_impressions['impressions'], color='tab:blue', width=20.0)  # Increase width here
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Total Impressions', fontsize=14)
    ax.set_title('Impressions Over Time', fontsize=16)
    ax.grid(True)
main()