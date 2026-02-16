import pandas as pd
import os

# 1. Setup file paths
# Replace the folder path with your specific folder directory
input_file = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/raw/himawari_aws_clean-data.xlsx'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/intermediate'
output_file = os.path.join(output_folder, 'himawari_aws_10AM_to_4PM.xlsx')

# 2. Load the Excel file
# We specify the engine as 'openpyxl' for XLSX files
df = pd.read_excel(input_file, engine='openpyxl')

# 3. Ensure the datetime column is in the correct format
df['Timestamp PH Time'] = pd.to_datetime(df['Timestamp PH Time'])

# 4. Filter for 10 AM (10:00) to 4 PM (16:00)
# This includes all data points starting at 10:00:00 up until 16:59:59
filtered_df = df[df['Timestamp PH Time'].dt.hour.between(10, 16)]

# 5. Save the result as a new XLSX file
filtered_df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Done! Data extracted to: {output_file}")