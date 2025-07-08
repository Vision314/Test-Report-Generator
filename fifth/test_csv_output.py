#!/usr/bin/env python3

import json
from tables import Tables

# Test with the complex data to see CSV output
with open('latex_generation_test001/test_descriptions.json', 'r') as f:
    complex_data = json.load(f)

print("=== CSV OUTPUT TEST ===")
tables = Tables(complex_data)
print(f"Generated {tables.get_table_count()} tables")

# Get the first table and save it as CSV
first_table = tables.get_table(0)
print("\nFirst table (Temperature=25):")
print(first_table.to_string(index=False, header=False))

print("\nFirst table as CSV:")
csv_content = first_table.to_csv(index=False, header=False)
print(csv_content)

# Save to actual CSV file for inspection
first_table.to_csv('output_table_0.csv', index=False, header=False)
print("Saved first table to 'output_table_0.csv'")

# Also show the second table
second_table = tables.get_table(1)
print("\nSecond table (Temperature=85):")
print(second_table.to_string(index=False, header=False))

second_table.to_csv('output_table_1.csv', index=False, header=False)
print("Saved second table to 'output_table_1.csv'")
