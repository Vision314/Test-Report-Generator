from tables import Tables
import json

# Test data without table conditions
simple_data = {
    "basic_info": {
        "category": "Input",
        "test_name": "Simple Test"
    },
    "row_conditions": {
        "names": "Input Voltage, Input Current",
        "units": "V, A",
        "values": "99, 2.3"
    },
    "column_conditions": {
        "names": "Load",
        "units": "Ohm",
        "values": "10, 50"
    },
    "table_conditions": {
        "names": "",
        "units": "",
        "values": ""
    },
    "results": {
        "names": "Output Power",
        "units": "W"
    }
}

# Test data with table conditions
complex_data = {
    "basic_info": {
        "category": "Input",
        "test_name": "Complex Test"
    },
    "row_conditions": {
        "names": "Input Voltage, Input Current",
        "units": "V, A",
        "values": "99, 2.3"
    },
    "column_conditions": {
        "names": "Load",
        "units": "Ohm",
        "values": "10, 50"
    },
    "table_conditions": {
        "names": "Temperature, Ground Config",
        "units": "C, Config",
        "values": "25, 85"  # This creates 2 tables
    },
    "results": {
        "names": "Output Power",
        "units": "W"
    }
}

print("=== TEST 1: Simple Data (No Table Conditions) ===")
simple_tables = Tables(simple_data)
print(f"Number of tables: {simple_tables.get_table_count()}")
print("\nFirst table:")
print(simple_tables.get_table())
print()

print("=== TEST 2: Complex Data (With Table Conditions) ===")
complex_tables = Tables(complex_data)
print(f"Number of tables: {complex_tables.get_table_count()}")

for i, table in enumerate(complex_tables.get_all_tables()):
    print(f"\nTable {i}:")
    print(f"Title: {table.attrs['title']}")
    print(f"Table conditions: {table.attrs['table_conditions']}")
    print(table)
    print()
