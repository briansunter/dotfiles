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

    # Resample the data to sum up the metrics for each week and count tweets per week
    combined_data.set_index('time', inplace=True)
    weekly_data = combined_data.resample('W').sum()
    weekly_tweet_count = combined_data.resample('W').size()

    # Calculate engagement rate per tweet as impressions to engagements
    weekly_data['engagement_rate'] = weekly_data['engagements'] / weekly_data['impressions']

    # Calculate the 6-week rolling average for the last 12 weeks for tweets and engagement rate
    avg_tweets_6_weeks = weekly_tweet_count[-12:].rolling(window=6).mean().iloc[-1]
    avg_engagement_rate_6_weeks = weekly_data['engagement_rate'][-12:].rolling(window=6).mean().iloc[-1]

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

    # Plotting number of tweets per week with 6-week average

    # Plotting engagement rate per week with 6-week average

    # Plotting followers per tweet
    fig, axs = plt.subplots(3, 1, figsize=(14, 21))

    # Plotting number of tweets per week with 6-week average
    plot_tweets_per_week(weekly_tweet_count[-12:], avg_tweets_6_weeks, axs[0])

    # Plotting engagement rate per week with 6-week average
    plot_engagement_rate(weekly_data['engagement_rate'][-12:], avg_engagement_rate_6_weeks, axs[1])

    # Plotting followers per tweet
    plot_followers_per_tweet(combined_monthly_data, average_followers_per_tweet_monthly, axs[2])

    # Save the figure
    plt.tight_layout()
    plt.savefig('out/tweet_quality.png')
    plt.close()

def plot_tweets_per_week(weekly_tweet_count, avg_tweets_6_weeks, ax):
    ax.bar(weekly_tweet_count.index, weekly_tweet_count, color='tab:blue')
    ax.axhline(y=avg_tweets_6_weeks, color='gray', linestyle='--', linewidth=2)
    ax.text(x=weekly_tweet_count.index[0], y=avg_tweets_6_weeks, s=f' Avg: {avg_tweets_6_weeks:.2f}', verticalalignment='bottom')
    ax.set_xlabel('Week')
    ax.set_ylabel('Number of Tweets')
    ax.set_title('Number of Tweets per Week with 6-week Average')
    plt.xticks(rotation=45)

def plot_engagement_rate(engagement_rate, avg_engagement_rate_6_weeks, ax):
    ax.plot(engagement_rate.index, engagement_rate, color='tab:red', marker='o', linestyle='-')
    ax.axhline(y=avg_engagement_rate_6_weeks, color='gray', linestyle='--', linewidth=2)
    ax.text(x=engagement_rate.index[0], y=avg_engagement_rate_6_weeks, s=f' Avg: {avg_engagement_rate_6_weeks:.4f}', verticalalignment='bottom')
    ax.set_xlabel('Week')
    ax.set_ylabel('Engagement Rate')
    ax.set_title('Engagement Rate per Week with 6-week Average')
    plt.xticks(rotation=45)

def plot_followers_per_tweet(combined_monthly_data, average_followers_per_tweet_monthly, ax):
    ax.bar(combined_monthly_data.index, combined_monthly_data['followers_per_tweet'], width=20, color='tab:green')
    ax.axhline(y=average_followers_per_tweet_monthly, color='gray', linestyle='--', linewidth=2)
    ax.text(x=combined_monthly_data.index[0], y=average_followers_per_tweet_monthly, s=f' Avg: {average_followers_per_tweet_monthly:.2f}', verticalalignment='bottom')
    ax.set_xlabel('Month')
    ax.set_ylabel('Followers per Tweet')
    ax.set_title('Monthly Followers per Tweet with Average')
    plt.xticks(rotation=45)

main()