import pandas as pd
import numpy as np

# Create dummy data
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Count': [10, 20, 30, 40],
    'Cost': [100.5, 200.75, 150.0, 300.25],
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'City': ['NY', 'LA', 'Chicago', 'Houston'],
    'Age': [25, 32, 40, 29]
}

df = pd.DataFrame(data)

# Function to highlight columns starting with 'C'
def highlight_C_columns(col):
    if col.name.startswith('C'):
        return ['background-color: lightblue'] * len(col)
    else:
        return [''] * len(col)

# Apply the highlighting
styled_df = df.style.apply(highlight_C_columns)

