import pandas as pd
import sqlite3
import os
import sys

def process_csv_folder_to_sqlite(folder_path):
    conn = sqlite3.connect('pumpkin.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Production (
            Geography TEXT,
            Reference_Date TEXT,
            Measure TEXT,
            Unit_of_Measure TEXT,
            Quantity REAL,
            Measure_Type TEXT,
            Converted_Quantity REAL,
            Converted_UOM TEXT
        )
    ''')

    unit_conversion = {
        'kilograms': 1,           
        'pounds': 0.453592, 
        'tons': 907.185,
        'metric tonnes': 1000, 
        'acres': 0.404686,     
        'hectares': 1 
    }

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # Add a derived column to determine if the data is related to area, weight, or dollars
            def determine_measure_type(uom):
                uom = uom.lower()
                if uom in ['pounds', 'tons', 'metric tonnes', 'kilograms']:
                    return 'weight'
                elif uom in ['acres', 'hectares']:
                    return 'area'
                elif uom == 'dollars':
                    return 'dollars'
                else:
                    return 'unknown'

            df['Measure_Type'] = df['UOM'].apply(determine_measure_type)

            # Add a derived column to convert all quantities to a common unit
            def convert_quantity(row):
                uom = row['UOM'].lower()
                value = row['VALUE']
                if 'weight' in row['Measure_Type']:
                    if uom in unit_conversion:
                        return value * unit_conversion[uom]
                elif 'area' in row['Measure_Type']:
                    if uom in unit_conversion:
                        return value * unit_conversion[uom]
                elif 'dollars' in row['Measure_Type']:
                    return value * 1000
                return value 

            df['Converted_Quantity'] = df.apply(convert_quantity, axis=1)

            # Add a column for Converted_UOM (common unit after conversion)
            def determine_converted_uom(row):
                if row['Measure_Type'] == 'weight':
                    return 'kilograms'
                elif row['Measure_Type'] == 'area':
                    return 'hectares'
                elif row['Measure_Type'] == 'dollars':
                    return 'dollars'
                else:
                    return None

            df['Converted_UOM'] = df.apply(determine_converted_uom, axis=1)

            df_to_insert = df[['GEO', 'REF_DATE', 'Estimates', 'UOM', 'VALUE', 'Measure_Type', 'Converted_Quantity', 'Converted_UOM']]
            df_to_insert.columns = ['Geography', 'Reference_Date', 'Measure', 'Unit_of_Measure', 'Quantity', 'Measure_Type', 'Converted_Quantity', 'Converted_UOM']
            df_to_insert.to_sql('Production', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    folder_path = sys.argv[1]  # Folder path provided as the first argument
    process_csv_folder_to_sqlite(folder_path)
