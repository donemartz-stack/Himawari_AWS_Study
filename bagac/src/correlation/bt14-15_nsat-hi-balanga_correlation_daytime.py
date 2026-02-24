import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import r2_score, mean_squared_error

# --- 1. SETTINGS & DATA LOADING ---
file_path = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/balanga/data/intermediate/himawari_aws-balanga_data-clean_daytime.xlsx'
output_folder = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/balanga/outputs/figures correlation'
output_filename = 'bt14-15_nsat-hi_balanga_correlation_daytime.png'
df = pd.read_excel(file_path)

# Himawari vs AWS Pairs
pairs = [('Band 14 Brightness Temperature', 'Near Surface Air Temperature'), ('Band 15 Brightness Temperature', 'Near Surface Air Temperature'),
    ('Band 14 Brightness Temperature', 'Heat Index'),   ('Band 15 Brightness Temperature', 'Heat Index')]

# Abbreviations for plot titles
abbrev_map = {'Band 14 Brightness Temperature': 'Band 14 BT',
    'Band 15 Brightness Temperature': 'B15 BT',
    'Near Surface Air Temperature': 'NSAT',
    'Heat Index': 'HI'}

# --- 2. PLOTTING SETUP ---
fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # 2x2 grid for the 4 pairs
axes = axes.flatten()

for i, (x_col, y_col) in enumerate(pairs):
    # Drop NaNs for the specific pair to ensure valid calculations
    temp_df = df[[x_col, y_col]].dropna()
    x, y = temp_df[x_col], temp_df[y_col]
    
 # --- 3. COMPUTATION ---
    # Pearson correlation
    r = np.corrcoef(x, y)[0, 1]  
    # Line of best fit (y = mx + b)
    m, b = np.polyfit(x, y, 1)  
    # Predicted y values based on the line of best fit
    y_pred = m * x + b 
    # R2 and RMSE using the actual y vs the predicted y
    r2 = r2_score(y, y_pred) 
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
 # --- 4. SCATTER PLOTS ---
    sns.scatterplot(x=x, y=y, ax=axes[i], alpha=0.5, edgecolor=None)
    sns.regplot(x=x, y=y, ax=axes[i], scatter=False, color='red') # Add trendline
    
    stats_text = f'r: {r:.3f}\n$R^2$: {r2:.3f}\nRMSE: {rmse:.3f}'
    axes[i].annotate(stats_text, xy=(0.05, 0.82), xycoords='axes fraction', 
                     bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))
    
    x_abbrev = abbrev_map.get(x_col, x_col)
    y_abbrev = abbrev_map.get(y_col, y_col)
    axes[i].set_title(f'{x_abbrev} vs {y_abbrev}')
    axes[i].set_xlabel(x_col)
    axes[i].set_ylabel(y_col)

# --- 5. FINALIZE & SAVE ---
plt.tight_layout()
save_path = os.path.join(output_folder, output_filename)
plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"Analysis complete. Figure saved to: {save_path}")
plt.show()