import pandas as pd
import os

# 1. Setup file paths
# Replace the folder path with your specific folder directory
input_file = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/raw/himawari_ahi_data_Mar_Jun_2025_clean.xlsx'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/intermediate'
output_file = os.path.join(output_folder, 'himawari_ahi_data_Mar_Jun_2025_12PM_to_4PM_every_hour.xlsx')

# 2. Load the Excel file
# We specify the engine as 'openpyxl' for XLSX files
df = pd.read_excel(input_file, engine='openpyxl')

# 3. Ensure the datetime column is in the correct format
df['datetime'] = pd.to_datetime(df['datetime'])

# 4. Filter for Top-of-the-Hour data only
# hour.between(12, 16) captures 12, 13, 14, 15, 16
# minute == 0 ensures we skip 12:10, 12:20, etc.
filtered_df = df[(df['datetime'].dt.hour.between(12, 16)) & 
    (df['datetime'].dt.minute == 0)]
# 5. Save the result as a new XLSX file
filtered_df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Done! Data extracted to: {output_file}")