#!/usr/bin/env python3
import pandas as pd
import os
import argparse
import re

def combine_csvs_in_folder(folder_path, output_file):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    print(f"Found {len(csv_files)} CSV files in {folder_path}")
    
    dfs = []  # List to store DataFrames
    for file in csv_files:
        parts = file.split('_')
        date_part_1, date_part_2 = parts[5], parts[6]  # Split the 6th and 7th part on the underscore
        if len(parts) < 8 or not re.match(r'\s*\d{8}\s*', date_part_1) or not re.match(r'\s*\d{8}\s*', date_part_2):
            print(f"Skipping file {file} due to incorrect format")
            print(f"Failed part: {date_part_1} or {date_part_2}")
            continue  # Skip files that don't match the format

        df = pd.read_csv(os.path.join(folder_path, file))
        if df.empty:
            print(f"File {file} is empty or contains no valid data")
        else:
            df['start_date'] = date_part_1  # Add start_date column
            df['end_date'] = date_part_2  # Add end_date column
            dfs.append(df)  # Add DataFrame to list

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)  # Combine all DataFrames
        combined_df.to_csv(output_file, index=False)  # Write combined DataFrame to CSV
        print(f"Combined CSV written to {output_file}")
    else:
        print("No valid CSV files found to combine")

def main():
    parser = argparse.ArgumentParser(description='Combine all CSV files in a folder into one CSV file.')
    parser.add_argument('--folder_path', help='Path to folder containing CSV files', default=os.getcwd())
    parser.add_argument('--output_file', help='Path to output CSV file', default='combined.csv')
    args = parser.parse_args()

    if os.path.exists(args.output_file):
        os.remove(args.output_file)  # Remove the file if it exists

    combine_csvs_in_folder(args.folder_path, args.output_file)

if __name__ == '__main__':
    main()