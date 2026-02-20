import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import r2_score, mean_squared_error

# --- 1. SETTINGS & DATA LOADING ---
file_path = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/intermediate/himawari_aws_data-clean_10AM-4PM_0-min-delay_b14-temp-x.xlsx'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/outputs/figures correlation'
output_filename = 'bt14-15_nsat-hi_correlation_10AM-4PM_0-min-delay_b14-temp-20.png'

# Ensure the folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load data
df = pd.read_excel(file_path)

# Define the pairs to compare (Himawari vs AWS)
pairs = [
    ('Band 14 Brightness Temperature', 'Near Surface Air Temperature'), ('Band 15 Brightness Temperature', 'Near Surface Air Temperature'), ('Brightness Temperature Difference', 'Near Surface Air Temperature'),
    ('Band 14 Brightness Temperature', 'Heat Index'),   ('Band 15 Brightness Temperature', 'Heat Index'),   ('Brightness Temperature Difference', 'Heat Index')
]

# --- 2. PLOTTING SETUP ---
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for i, (x_col, y_col) in enumerate(pairs):
    # Drop NaNs for the specific pair to ensure valid calculations
    temp_df = df[[x_col, y_col]].dropna()
    x, y = temp_df[x_col], temp_df[y_col]
    
    
    # --- 3. COMPUTE METRICS ---
    # 1. Calculate the Pearson correlation
    r = np.corrcoef(x, y)[0, 1]
    
    # 2. Mathematically calculate the line of best fit (y = mx + b)
    m, b = np.polyfit(x, y, 1)
    
    # 3. Generate the predicted y values based on that line
    y_pred = m * x + b
    
    # 4. Calculate R2 and RMSE using the actual y vs the predicted y
    r2 = r2_score(y, y_pred) 
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    # --- 4. GENERATE SCATTER PLOTS ---
    sns.scatterplot(x=x, y=y, ax=axes[i], alpha=0.5, edgecolor=None)
    sns.regplot(x=x, y=y, ax=axes[i], scatter=False, color='red') # Add trendline
    
    # Annotate plot with metrics
    stats_text = f'r: {r:.3f}\n$R^2$: {r2:.3f}\nRMSE: {rmse:.3f}'
    axes[i].annotate(stats_text, xy=(0.05, 0.82), xycoords='axes fraction', 
                     bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))
    
    axes[i].set_title(f'{x_col.upper()} vs {y_col.upper()}')
    axes[i].set_xlabel(x_col)
    axes[i].set_ylabel(y_col)

# --- 5. FINALIZE & SAVE ---
plt.tight_layout()

# Save with high resolution (300 DPI)
save_path = os.path.join(output_folder, output_filename)
plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"Analysis complete. Figure saved to: {save_path}")
plt.show()