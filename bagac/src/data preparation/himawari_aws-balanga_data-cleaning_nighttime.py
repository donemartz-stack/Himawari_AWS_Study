import pandas as pd
import os
from datetime import time

# --- Configuration ---
# Folder paths and filenames
input_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/balanga/data/processed'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/balanga/data/intermediate'
input_filename = 'himawari_aws-balanga_data_combined_30-min-delay.xlsx'
output_filename = 'himawari_aws-balanga_data-clean_nighttime.xlsx'

# --- Load Data ---
input_path = os.path.join(input_folder, input_filename)
print(f"Loading data from: {input_path}")
df = pd.read_excel(input_path)

# --- Data Check ---
if 'Timestamp' in df.columns:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
else:
    # If the column name is different, print available columns to help debug
    print("Error: 'Timestamp' column not found. Available columns:", df.columns)
    exit()

# --- Apply Filters ---
# 1. Extract 12 AM to 4 AM data
start_time = time(0, 0, 0) # 12:00:00 AM
end_time = time(4, 0, 0)   # 4:00:00 AM
time_mask = (df['Timestamp'].dt.time >= start_time) & (df['Timestamp'].dt.time <= end_time)

# 2. Exclude Band 14 Brightness Temperature lower than 18
band14_mask = df['Band 14 Brightness Temperature'] >= 12

# 3. Exclude Temperature Difference above 3.0
temp_diff_mask = (df['Brightness Temperature Difference'] <= 3.0) & (df['Brightness Temperature Difference'] >= 0.0)

# 4. Exclude Humidity below 40% and above 85%
humidity_mask = (df['Humidity'] >= 20) & (df['Humidity'] <= 85)

# 4. Exclude NSAT above 50
nsat_mask = df['Near Surface Air Temperature'] <= 50

# Combine all filters using the '&' (AND) operator
final_mask = time_mask & band14_mask & temp_diff_mask & humidity_mask & nsat_mask
filtered_df = df[final_mask]

# --- Save Output ---
output_path = os.path.join(output_folder, output_filename)
filtered_df.to_excel(output_path, index=False)

print(f"Processing complete.")
print(f"Original rows: {len(df)}")
print(f"Filtered rows: {len(filtered_df)}")
print(f"File saved to: {output_path}")