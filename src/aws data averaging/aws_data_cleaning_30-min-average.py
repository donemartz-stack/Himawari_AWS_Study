import pandas as pd
import os

# --- Configuration ---
input_file = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/raw/aws_pag-asa-orani_data.xlsx' 
save_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/processed' 

def process_weather_data(input_path, output_folder): 
    # 1. Load the Excel file
    print("Reading Excel file...")
    try:
        # Using read_excel specifically for XLSX files
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Convert the timestamp column to datetime objects
    time_col = 'Time Stamp PH Time'
    
    if time_col not in df.columns:
        print(f"Error: Column '{time_col}' not found. Please check the column name in your Excel file.")
        return
        
    df[time_col] = pd.to_datetime(df[time_col])

    # 3. Set the timestamp as the index
    df.set_index(time_col, inplace=True)

    # 4. Resample to 30-minute intervals and calculate the average
    df_resampled = df.resample('30min').mean()

    # Reset index to bring the timestamp back as a column
    df_resampled.reset_index(inplace=True)

    # 5. Save the output
    output_filename = 'aws_pag-asa-orani_averaged_data_30min.xlsx'
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
        
    output_path = os.path.join(output_folder, output_filename)
    
    try:
        df_resampled.to_excel(output_path, index=False)
        print(f"Successfully processed and saved data to: {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# --- Run the Process ---
if __name__ == "__main__":
    process_weather_data(input_file, save_folder)