import pandas as pd
import os
from datetime import time

# --- Configuration ---
# 1. Specify the folder paths (Modify these lines)
input_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/processed'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/intermediate'

# 2. File names
input_filename = 'himawari_aws_data_combined_60-min-delay.xlsx'
output_filename = 'himawari_aws_data-clean_10AM-4PM_60-min-delay_b14-temp-x.xlsx'
'0-min-delay.xlsx'

# --- Load Data ---
input_path = os.path.join(input_folder, input_filename)
print(f"Loading data from: {input_path}")
df = pd.read_excel(input_path)

# Ensure 'Timestamp' is in datetime format
# Adjust column name if it's different in your file (e.g., 'Timestamp PH Time')
if 'Timestamp' in df.columns:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
else:
    # If the column name is different, print available columns to help debug
    print("Error: 'Timestamp' column not found. Available columns:", df.columns)
    exit()

# --- Apply Filters ---

# 1. Extract 10 AM to 4 PM data
# We access the .dt.time property to filter by time of day
start_time = time(10, 0, 0) # 10:00:00
end_time = time(16, 0, 0)   # 16:00:00
time_mask = (df['Timestamp'].dt.time >= start_time) & (df['Timestamp'].dt.time <= end_time)

# 2. Exclude Band 14 Brightness Temperature lower than 16 (Keep >= 16)
band14_mask = df['Band 14 Brightness Temperature'] >= 20

# 3. Exclude Temperature Difference above 4.0 (Keep <= 4.0)
temp_diff_mask = (df['Brightness Temperature Difference'] <= 3.0) & (df['Brightness Temperature Difference'] >= 0.0)

# 4. Exclude Humidity below 40% and above 85% (Keep between 40 and 85)
humidity_mask = (df['Humidity'] >= 20) & (df['Humidity'] <= 95)

# Combine all filters using the '&' (AND) operator
final_mask = time_mask & band14_mask & temp_diff_mask & humidity_mask
filtered_df = df[final_mask]

# --- Save Output ---
output_path = os.path.join(output_folder, output_filename)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save to Excel
filtered_df.to_excel(output_path, index=False)

print(f"Processing complete.")
print(f"Original rows: {len(df)}")
print(f"Filtered rows: {len(filtered_df)}")
print(f"File saved to: {output_path}")