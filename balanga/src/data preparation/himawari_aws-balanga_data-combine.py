import pandas as pd
import os

# --- Configuration ---
input_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/balanga/data/raw'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/balanga/data/processed'
file1_name = 'himawari-balanga_data_full.xlsx'
file2_name = 'aws-balanga_averaged_data_10-min.xlsx'
output_filename = 'himawari_aws-balanga_data_combined.xlsx'

# --- Load Data ---
print("Loading files...")
file1_path = os.path.join(input_folder, file1_name)
file2_path = os.path.join(input_folder, file2_name)
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# --- Preprocessing ---
# Rename df1 if needed
if 'Timestamp PH Time' in df1.columns:
    df1 = df1.rename(columns={'Timestamp PH Time': 'Timestamp'})

# Rename df2 if needed (Independent IF, not ELIF)
if 'Timestamp PH Time' in df2.columns:
    df2 = df2.rename(columns={'Timestamp PH Time': 'Timestamp'})

# Double-check if the columns actually exist now before converting
if 'Timestamp' not in df1.columns or 'Timestamp' not in df2.columns:
    print(f"Columns in df1: {df1.columns.tolist()}")
    print(f"Columns in df2: {df2.columns.tolist()}")
    raise KeyError("The 'Timestamp' column is missing from one of the files. Check the printout above for actual column names.")

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
merged_df.to_excel(output_path, index=False)

print(f"Success! Combined file saved to: {output_path}")
print(f"Total rows matched: {len(merged_df)}")