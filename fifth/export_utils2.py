import os
import pandas as pd
from pylatex import Document, Tabular, Command
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape
from tables import Tables

# turning a single tests Tables() to CSV files
def tables_to_csv(tables_instance, output_dir):
    """
    Export all tables from a Tables instance to CSV files.
    
    Args:
        tables_instance: Tables object containing the generated tables
        output_dir: Directory path where CSV files will be saved
    
    Returns:
        List of created file paths
    """
    all_tables = tables_instance.get_all_tables()
    created_files = []
    table_info = []
    
    # Export each table as a separate CSV file
    for i, table in enumerate(all_tables, 1):
        filename = f"table{i}.csv"
        filepath = os.path.join(output_dir, filename)


        # Export table to CSV without headers
        table.to_csv(filepath, index=False, header=False)
        created_files.append(filepath)
        
        # Get table title from metadata
        title = table.attrs.get('title', f'Table {i}')
        table_info.append({'filename': filename, 'title': title})
    
    # Create tables.csv with filename and title information
    tables_df = pd.DataFrame(table_info)
    tables_csv_path = os.path.join(output_dir, 'tables.csv')
    tables_df.to_csv(tables_csv_path, index=False)
    
    print(f"Exported {len(all_tables)} tables to {output_dir}")
    print(f"Created tables.csv with table information")
    
    return created_files

# turning a single tests CSV files to LaTeX
    # inputs: csv folder path, output_dir
    # category_name/test_name/csv/
    # category_name/test_name/latex/



