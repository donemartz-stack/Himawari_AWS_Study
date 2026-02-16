import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import r2_score, mean_squared_error

# --- 1. SETTINGS & DATA LOADING ---
file_path = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/data/intermediate/himawari_aws_10AM_to_4PM.xlsx'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/outputs/figures'
output_filename = 'himawari_aws_daytime_correlation.png'

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
    r = np.corrcoef(x, y)[0, 1]
    r2 = r2_score(y, x) 
    rmse = np.sqrt(mean_squared_error(y, x))
    
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