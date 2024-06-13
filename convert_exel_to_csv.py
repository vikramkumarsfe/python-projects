import os
import pandas as pd

# Get the current working directory
current_directory = os.getcwd()

# Set the Excel file name
excel_file_name = 'workshop1.xlsx'

# Set the CSV file name for output
csv_file_name = 'workshop.csv'

# Set the columns you want to extract
columns_to_extract = ['Name', 'Email']

# Set the full paths
excel_file_path = os.path.join(current_directory, excel_file_name)
csv_file_path = os.path.join(current_directory, csv_file_name)

# Check if the Excel file exists
if os.path.exists(excel_file_path):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)

    # Select only the specified columns
    selected_columns = df[columns_to_extract]

    # Save the selected columns to a CSV file
    selected_columns.to_csv(csv_file_path, index=False)

    print(f'Columns {columns_to_extract} extracted and saved to {csv_file_path}')
else:
    print(f'Error: Excel file not found at {excel_file_path}')