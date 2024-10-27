import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

conn = sqlite3.connect('pumpkin.db')

stacked_area_measures = [
    'Area harvested',
    'Area planted',
    'Total production'
]

bar_chart_measure = 'Farm gate value'

output_dir = "charts"
os.makedirs(output_dir, exist_ok=True)

for measure in stacked_area_measures:
    query = f'''
    SELECT Reference_Date, Geography, SUM(Converted_Quantity) as Total_Production
    FROM Production
    WHERE Geography != 'Canada' AND Measure = "{measure}"
    GROUP BY Reference_Date, Geography
    ORDER BY Reference_Date
    '''
    
    df = pd.read_sql_query(query, conn)

    uom = 'hectares'
    if measure == 'Total production':
        uom = 'kilograms'
    
    # Convert 'Reference_Date' to a datetime object
    df['Reference_Date'] = pd.to_datetime(df['Reference_Date'], format='%Y')
    
    # Pivot the data to have provinces as columns and 'Reference_Date' as the index
    df_grouped = df.pivot(index='Reference_Date', columns='Geography', values='Total_Production').fillna(0)
    
    if df_grouped.empty:
        print(f"Skipping {measure}: No data available.")
        continue
    
    years = df_grouped.index.year
    provinces = df_grouped.columns

    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.stackplot(years, df_grouped.T, labels=provinces)
    
    ax.set_title(measure)  
    ax.set_xlabel('Year')
    ax.set_ylabel(f'Total Quantity ({uom})')
    
    ax.ticklabel_format(style='plain', axis='x')
    
    ax.set_xlim([years.min(), years.max()])
    
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    output_path = os.path.join(output_dir, f'stacked_area_{measure}.svg')
    plt.tight_layout()
    plt.savefig(output_path)
    
    plt.show()
    
# Generate bar chart for "Farm Gate Value (dollars)"
bar_query = f'''
SELECT Reference_Date, Geography, SUM(Converted_Quantity) as Total_Value
FROM Production
WHERE Geography != 'Canada' AND Measure = "{bar_chart_measure}"
GROUP BY Reference_Date, Geography
ORDER BY Reference_Date
'''

df_bar = pd.read_sql_query(bar_query, conn)

# Convert 'Reference_Date' to a datetime object
df_bar['Reference_Date'] = pd.to_datetime(df_bar['Reference_Date'], format='%Y')

# Separate Ontario from other provinces
df_bar_ontario = df_bar[df_bar['Geography'] == 'Ontario'].pivot(index='Reference_Date', columns='Geography', values='Total_Value').fillna(0)
df_bar_others = df_bar[df_bar['Geography'] != 'Ontario'].pivot(index='Reference_Date', columns='Geography', values='Total_Value').fillna(0)

# Skip if there's insufficient data
if not df_bar_others.empty and not df_bar_ontario.empty:
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot stacked bars for other provinces
    df_bar_others.plot(kind='bar', stacked=True, ax=ax, width=0.4, position=1)
    
    # Plot a separate bar for Ontario
    df_bar_ontario.plot(kind='bar', stacked=False, color='red', ax=ax, width=0.4, position=0)
    
    ax.set_title(bar_chart_measure)
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Value (dollars)')
   
    ax.set_xticklabels(df_bar_others.index.year, rotation=45, ha='right')

    handles_others, labels_others = ax.get_legend_handles_labels()
    filtered_handles = []
    filtered_labels = []
    seen_labels = set()

    for handle, label in zip(handles_others, labels_others):
        if label not in seen_labels:
            filtered_handles.append(handle)
            filtered_labels.append(label)
            seen_labels.add(label)
            
    # Update the legend
    ax.legend(filtered_handles, filtered_labels, loc='upper left', bbox_to_anchor=(1, 1))

    output_path_bar = os.path.join(output_dir, f'bar_chart_{bar_chart_measure}.svg')
    plt.tight_layout()
    plt.savefig(output_path_bar)
    
    plt.show()
