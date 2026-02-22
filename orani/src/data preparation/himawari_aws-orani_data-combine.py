import pandas as pd
import os

# --- Configuration ---
# 1. Specify the folder paths (Modify these lines)
input_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/raw'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/processed'

# 2. File names
file1_name = 'aws_pag-asa-orani_averaged_data_10min.xlsx'
file2_name = 'himawari_aws_full-data.xlsx'
output_filename = 'himawari_aws_data_combined.xlsx'

# --- Load Data ---
print("Loading files...")
# Construct full paths
file1_path = os.path.join(input_folder, file1_name)
file2_path = os.path.join(input_folder, file2_name)

# Read the Excel files
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# --- Preprocessing ---
# Rename timestamp columns to a common name 'Timestamp'
# This handles the specific column names and the typo found in your data
if 'Time Stamp PH Time' in df1.columns:
    df1 = df1.rename(columns={'Time Stamp PH Time': 'Timestamp'})

if 'Timestamp PH Tine' in df2.columns: # Handling the typo "Tine"
    df2 = df2.rename(columns={'Timestamp PH Tine': 'Timestamp'})
elif 'Timestamp PH Time' in df2.columns:
    df2 = df2.rename(columns={'Timestamp PH Time': 'Timestamp'})

# Convert to datetime objects to ensure accurate matching
df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])
df2['Timestamp'] = pd.to_datetime(df2['Timestamp'])

# --- Merging ---
print("Merging data...")
# Merge based on the 'Timestamp' column
# how='inner' keeps only rows with timestamps that exist in BOTH files
merged_df = pd.merge(df1, df2, on='Timestamp', how='inner')

# --- Save Output ---
output_path = os.path.join(output_folder, output_filename)

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Save to Excel
merged_df.to_excel(output_path, index=False)

print(f"Success! Combined file saved to: {output_path}")
print(f"Total rows matched: {len(merged_df)}")