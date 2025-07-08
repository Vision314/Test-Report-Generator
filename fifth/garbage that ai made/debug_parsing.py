#!/usr/bin/env python3

import json
from tables import Tables

# Test with the complex data to debug the parsing
with open('latex_generation_test001/test_descriptions.json', 'r') as f:
    complex_data = json.load(f)

print("=== DEBUGGING PARSED VALUES ===")
tables = Tables(complex_data)

print("Row conditions:", tables.row_conditions)
print("Column conditions:", tables.column_conditions)
print("Table conditions:", tables.table_conditions)
print("Results:", tables.results)
print("Specifications:", tables.specifications)
print("Calculations:", tables.calculations)

print(f"\nTotal columns calculated: {tables._calculate_total_columns()}")

# Get the first table and print its shape
first_table = tables.get_table(0)
print(f"First table shape: {first_table.shape}")
print("First table:")
print(first_table)
