#!/usr/bin/env python3
import pandas as pd
import os
import argparse

def combine_csvs_in_folder(folder_path, output_file):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    combined_df = pd.DataFrame()

    for file in csv_files:
        df = pd.read_csv(os.path.join(folder_path, file))
        combined_df = pd.concat([combined_df, df], ignore_index=True)


    combined_df.to_csv(output_file, index=False)

def main():
    parser = argparse.ArgumentParser(description='Combine CSV files in a folder.')
    parser.add_argument('folder_path', type=str, nargs='?', default='.', help='Path to the folder containing CSV files (default: current directory)')
    parser.add_argument('output_file', type=str, nargs='?', default='combined.csv', help='File path for the output combined CSV (default: combined.csv in the current directory)')
    args = parser.parse_args()

    combine_csvs_in_folder(args.folder_path, args.output_file)

if __name__ == "__main__":
    main()