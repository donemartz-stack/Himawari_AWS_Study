import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
input_file = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/bagac/data/raw/aws-bagac_averaged_data_10-min.xlsx' 
save_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/bagac/outputs/time series plots' 

def plot_weather_data(input_file, output_folder):

    # 1. Load the data
    print("Reading data file...")
    try:
        # Load the Excel file
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Prepare the data
    # Ensure the timestamp column is in datetime format
    time_col = 'Timestamp PH Time'
    if time_col not in df.columns:
        print(f"Error: Column '{time_col}' not found.")
        return
        
    df[time_col] = pd.to_datetime(df[time_col])
    
    # Identify the parameters to plot (all columns except the timestamp)
    parameters = [col for col in df.columns if col != time_col]
    num_params = len(parameters)

    # 3. Create the plots
    # Create a figure with a subplot for each parameter
    fig, axes = plt.subplots(nrows=num_params, ncols=1, figsize=(12, 4 * num_params), sharex=True)
    
    # If there's only one parameter, axes is not a list, so wrap it
    if num_params == 1:
        axes = [axes]

    # Iterate through parameters and plot each one
    for i, param in enumerate(parameters):
        ax = axes[i]
        
        # Plot the data
        ax.plot(df[time_col], df[param], label=param, color='tab:blue')
        
        # Formatting
        ax.set_title(f"{param} Over Time", fontsize=14)
        ax.set_ylabel(param, fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right')

    # Common X-label and layout adjustments
    plt.xlabel('Date Time', fontsize=12)
    plt.tight_layout()

    # 4. Save the plot
    output_filename = 'aws-bagac_data_clean_10-min_time-series.png'
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
        
    output_path = os.path.join(output_folder, output_filename)
    
    try:
        plt.savefig(output_path)
        print(f"Success! Plot saved to: {output_path}")
    except Exception as e:
        print(f"Error saving plot: {e}")
    finally:
        plt.close(fig) # Close the figure to free memory

# --- Run the Process ---
if __name__ == "__main__":
    plot_weather_data(input_file, save_folder)