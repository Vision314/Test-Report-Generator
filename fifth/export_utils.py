import os
import pandas as pd
from pylatex import Document, Tabular, Command
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape
from tables import Tables

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

def csv_to_latex(csv_file_path, output_dir):
    """
    Convert a CSV file to LaTeX table format with merged cell handling.
    
    Args:
        csv_file_path: Path to the input CSV file
        output_dir: Directory path where the LaTeX file will be saved
    
    Returns:
        The generated LaTeX code as a string
    """
    # Read CSV file
    df = pd.read_csv(csv_file_path, header=None)
    
    # Generate LaTeX with merged cells
    latex_code = _generate_latex_with_merges(df)
    
    # Create output filename by replacing .csv with .tex
    csv_filename = os.path.basename(csv_file_path)
    tex_filename = csv_filename.replace('.csv', '.tex')
    output_path = os.path.join(output_dir, tex_filename)
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write(latex_code)
    
    print(f"Converted {csv_file_path} to LaTeX with merged cells: {output_path}")
    
    return latex_code

def _generate_latex_with_merges(df):
    """Generate LaTeX code with horizontal and vertical merges using PyLaTeX for commands"""
    rows, cols = df.shape
    
    # Track which cells are merged (to handle them appropriately)
    horizontal_merges = {}  # (row, col) -> span
    vertical_merges = {}    # (row, col) -> span
    skip_cells = set()      # Cells to skip entirely (part of horizontal merges)
    empty_cells = set()     # Cells that need empty content (part of vertical merges)
    
    def _should_merge(value):
        """Check if a cell value should be considered for merging"""
        value_str = str(value).strip()
        # Don't merge if it's "--" or a pure number
        if value_str == "--":
            return False
        # Check if it's a pure number (int or float)
        try:
            float(value_str)
            return False  # Don't merge numbers
        except ValueError:
            return True  # Merge text values
    
    def _detect_table_structure(df):
        """Detect table structure to determine midrule placement"""
        # With the updated structure, there are no title or table condition rows in the table itself
        # The table now starts directly with column condition headers or data rows
        
        has_table_conditions = False  # No longer in the table itself
        
        # Find where data rows start by looking for rows that start with row condition names
        # Data rows typically have specific values in first columns (not "--")
        data_start_row = rows  # Default to no data rows
        for i in range(rows):
            # Check if this row looks like a data row
            first_cell = str(df.iloc[i, 0]).strip()
            second_cell = str(df.iloc[i, 1]).strip() if cols > 1 else ""
            
            # Data rows typically have meaningful content in first two columns
            # and are not just repeated headers or "--"
            if (first_cell != "--" and 
                second_cell != "--" and 
                first_cell != "" and
                second_cell != ""):
                data_start_row = i
                break
        
        return has_table_conditions, data_start_row
    
    def _should_bold_cell(i, j, has_table_conditions, data_start_row):
        """Determine if a cell should be bold based on its position"""
        # Bold header rows (before data rows) - but only text, not numbers
        if i < data_start_row:
            cell_value = str(df.iloc[i, j]).strip()
            # Only bold if it's not a number and not "--"
            if cell_value != "--" and cell_value != "":
                try:
                    float(cell_value)
                    return False  # Don't bold numbers
                except ValueError:
                    return True  # Bold text
        # Bold first column in data rows (row names only)
        if i >= data_start_row and j == 0:
            cell_value = str(df.iloc[i, j]).strip()
            # Only bold if it's not a number and not "--"
            if cell_value != "--" and cell_value != "":
                try:
                    float(cell_value)
                    return False  # Don't bold numbers
                except ValueError:
                    return True  # Bold text like "Input Voltage (V)"
        return False
    
    # Detect table structure
    has_table_conditions, data_start_row = _detect_table_structure(df)
    
    # First pass: identify all merges
    for i in range(rows):
        for j in range(cols):
            if (i, j) in skip_cells or (i, j) in empty_cells:
                continue
                
            cell_value = str(df.iloc[i, j])
            
            if _should_merge(cell_value):
                # Check for horizontal merges first
                h_span = 1
                for k in range(j + 1, cols):
                    if str(df.iloc[i, k]) == cell_value and _should_merge(df.iloc[i, k]):
                        h_span += 1
                        skip_cells.add((i, k))
                    else:
                        break
                
                if h_span > 1:
                    horizontal_merges[(i, j)] = h_span
                else:
                    # Check for vertical merges only if no horizontal merge
                    v_span = 1
                    for k in range(i + 1, rows):
                        if str(df.iloc[k, j]) == cell_value and _should_merge(df.iloc[k, j]):
                            v_span += 1
                            empty_cells.add((k, j))
                        else:
                            break
                    
                    if v_span > 1:
                        vertical_merges[(i, j)] = v_span
    
    # Build LaTeX table manually but use PyLaTeX for commands
    latex_lines = []
    latex_lines.append(f"\\begin{{tabular}}{{{('c' * cols)}}}")
    
    # Second pass: generate LaTeX rows
    for i in range(rows):
        row_parts = []
        
        j = 0
        while j < cols:
            if (i, j) in skip_cells:
                # Skip this cell (part of horizontal merge)
                j += 1
                continue
            elif (i, j) in empty_cells:
                # Empty cell (part of vertical merge)
                row_parts.append("")
                j += 1
                continue
            
            cell_value = str(df.iloc[i, j]).strip()
            
            # Determine if this cell should be bold
            should_bold = _should_bold_cell(i, j, has_table_conditions, data_start_row)
            
            # Check if this cell has merges
            if (i, j) in horizontal_merges:
                h_span = horizontal_merges[(i, j)]
                # Apply bold formatting if needed
                if should_bold and cell_value != "--" and cell_value != "":
                    cell_value = f"\\textbf{{{cell_value}}}"
                # Use PyLaTeX's Command for multicolumn
                multicolumn_cmd = Command('multicolumn', arguments=[h_span, 'c', NoEscape(cell_value)])
                row_parts.append(multicolumn_cmd.dumps())
                j += h_span  # Skip the merged columns
            elif (i, j) in vertical_merges:
                v_span = vertical_merges[(i, j)]
                # Apply bold formatting if needed
                if should_bold and cell_value != "--" and cell_value != "":
                    cell_value = f"\\textbf{{{cell_value}}}"
                # Use PyLaTeX's Command for multirow
                multirow_cmd = Command('multirow', arguments=[v_span, '*', NoEscape(cell_value)])
                row_parts.append(multirow_cmd.dumps())
                j += 1
            else:
                # Regular cell
                # Apply bold formatting if needed
                if should_bold and cell_value != "--" and cell_value != "":
                    cell_value = f"\\textbf{{{cell_value}}}"
                row_parts.append(cell_value)
                j += 1
        
        # Join row parts and add to LaTeX
        latex_lines.append(" & ".join(row_parts) + " \\\\")
        
        # Add midrule before data rows start (after column headers)
        if i == data_start_row - 1 and data_start_row < rows:
            latex_lines.append("\\midrule")
    
    latex_lines.append("\\end{tabular}")
    
    return "\n".join(latex_lines)

def tables_to_complete_latex(tables_instance, base_output_dir, test_name=None, category=None):
    """
    Generate a LaTeX subsection with all tables from a Tables instance.
    Organizes output into the REAL_REPORT structure.
    
    Args:
        tables_instance: Tables object containing the generated tables
        base_output_dir: Base directory path (e.g., REAL_REPORT folder)
        test_name: Name of the test for the subsection title (if None, will try to extract from metadata)
        category: Test category ('input' or 'output', if None will try to extract from metadata)
    
    Returns:
        Dictionary with paths to created files
    """
    # Extract test information from metadata
    if test_name is None or category is None:
        basic_info = tables_instance.table_metadata.get('basic_info', {})
        if test_name is None:
            test_name = basic_info.get('test_name', 'Test Report')
        if category is None:
            category = basic_info.get('category', 'input').lower()
    
    # Create test-specific directory structure
    test_name_clean = test_name.lower().replace(' ', '_').replace('-', '_')
    test_dir = os.path.join(base_output_dir, 'tests', category, test_name_clean)
    
    # Create subdirectories
    csv_dir = os.path.join(test_dir, 'csv')
    latex_dir = os.path.join(test_dir, 'latex')
    images_dir = os.path.join(test_dir, 'images')
    
    for dir_path in [csv_dir, latex_dir, images_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Export CSV files to csv/ folder
    print(f"=== Exporting CSV files to {csv_dir} ===")
    csv_files = tables_to_csv(tables_instance, csv_dir)
    
    # Start building the LaTeX content (just the subsection, not full document)
    latex_content = []
    
    # Start with subsection and new page
    latex_content.extend([
        "\\newpage",
        f"\\subsection{{{test_name}}}",
        ""
    ])
    
    # Get all tables
    all_tables = tables_instance.get_all_tables()
    
    # Get table conditions for subsubsection titles
    table_conditions = tables_instance.table_conditions
    
    # Add each table to the document with subsubsections
    for i, table in enumerate(all_tables, 1):
        # Generate subsubsection title from table conditions
        if table_conditions and 'names' in table_conditions and 'values' in table_conditions:
            # Build condition string from table conditions
            condition_parts = []
            names = table_conditions['names']
            values = table_conditions['values']
            
            # Get the specific values for this table (table i-1 since we start from 1)
            if isinstance(values[0], list):  # Multi-dimensional
                table_values = [val[i-1] if i-1 < len(val) else val[0] for val in values]
            else:  # Single dimension
                table_values = [values[i-1] if i-1 < len(values) else values[0]]
            
            # Create condition string
            for name, value in zip(names, table_values):
                condition_parts.append(f"{name} = {value}")
            
            subsubsection_title = ", ".join(condition_parts)
        else:
            # Fallback title
            subsubsection_title = f"Table {i}"
        
        latex_content.extend([
            f"\\subsubsection{{{subsubsection_title}}}",
            ""
        ])
        
        # Export table to temporary CSV for processing
        temp_csv_path = os.path.join(csv_dir, f"temp_table{i}.csv")
        table.to_csv(temp_csv_path, index=False, header=False)
        
        # Read the CSV and generate LaTeX table
        df = pd.read_csv(temp_csv_path, header=None)
        table_latex = _generate_latex_with_merges(df)
        
        # Add the table with centering
        latex_content.extend([
            "\\begin{center}",
            table_latex,
            "\\end{center}",
            "",
            "\\vspace{1em}",  # Add some vertical space between tables
            ""
        ])
        
        # Clean up temporary CSV
        os.remove(temp_csv_path)
    
    # Write LaTeX file to latex/ folder
    latex_filename = f"{test_name_clean}_subsection.tex"
    latex_path = os.path.join(latex_dir, latex_filename)
    
    with open(latex_path, 'w') as f:
        f.write('\n'.join(latex_content))
    
    # Return information about created files
    result = {
        'latex_file': latex_path,
        'csv_files': csv_files,
        'csv_dir': csv_dir,
        'latex_dir': latex_dir,
        'images_dir': images_dir,
        'test_name': test_name,
        'category': category
    }
    
    print(f"Created LaTeX subsection: {latex_path}")
    print(f"CSV files exported to: {csv_dir}")
    print(f"Images directory ready: {images_dir}")
    print(f"Subsection contains {len(all_tables)} tables")
    print(f"Test: {test_name} (Category: {category})")
    
    return result

def generate_multiple_test_reports(test_metadata_list, base_output_dir):
    """
    Generate reports for multiple tests and organize them in the REAL_REPORT structure.
    
    Args:
        test_metadata_list: List of dictionaries containing test metadata
        base_output_dir: Base directory path (e.g., REAL_REPORT folder)
    
    Returns:
        Dictionary with information about all generated reports
    """
    all_results = {}
    
    print(f"=== Generating Multiple Test Reports ===")
    print(f"Base output directory: {base_output_dir}")
    print(f"Number of tests: {len(test_metadata_list)}")
    
    for i, test_metadata in enumerate(test_metadata_list, 1):
        print(f"\n--- Processing Test {i} ---")
        
        # Create Tables instance for this test
        tables_instance = Tables(table_metadata=test_metadata)
        
        # Extract test info
        basic_info = test_metadata.get('basic_info', {})
        test_name = basic_info.get('test_name', f'Test_{i}')
        category = basic_info.get('category', 'input').lower()
        
        print(f"Test: {test_name} (Category: {category})")
        
        # Generate the report
        try:
            result = tables_to_complete_latex(tables_instance, base_output_dir)
            all_results[test_name] = result
            print(f"✓ Successfully generated report for {test_name}")
        except Exception as e:
            print(f"✗ Error generating report for {test_name}: {str(e)}")
            all_results[test_name] = {'error': str(e)}
    
    print(f"\n=== Summary ===")
    print(f"Total tests processed: {len(test_metadata_list)}")
    print(f"Successful: {len([r for r in all_results.values() if 'error' not in r])}")
    print(f"Failed: {len([r for r in all_results.values() if 'error' in r])}")
    
    return all_results

# Import Tables class for the multiple reports function
from tables import Tables
