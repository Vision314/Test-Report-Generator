import os
import csv
import pandas as pd

structure = {
    "cover_page": [
        "equipment_used",
        "general_specifications",
        "product_information",
        "testing_and_review"
    ],
    "input": [
        "input_current",
        "no_load_input_power",
        "inrush_current",
        "efficiency",
        "power_factor"
    ],
    "output": [
        "turn_on_delay",
        "output_voltage_tolerance",
        "load_regulation",
        "line_regulation",
        "ripple",
        "transient_response",
        "startup_overshoot",
        "hold_up_time",
        "aux_output_voltage_regulation",
        "aux_output_current"
    ],
    "protections": [
        "over_voltage_protection",
        "over_current_protection",
        "short_circuit_protection"
    ],
    "safety": [
        "dielectric_withstand_voltage",
        "output_touch_current",
        "earth_leakage_current"
    ],
    "emc": [
        "conducted_emissions",
        "radiated_emissions",
        "electrostatic_discharge_immunity",
        "EFT_burst_immunity",
        "line_surge_immunity",
        "voltage_dip_immunity"
    ]
}

def create_csv_file(filepath):
    # make a csv
    df = pd.DataFrame({})
    df.to_csv(filepath, index=False)

def create_structure(base_path=r'Test-Report-Generator\the_two\TEMPLATE FORMAT'):
    for category, tests in structure.items():
        category_path = os.path.join(base_path, category)
        os.makedirs(category_path, exist_ok=True)

        for test in tests:
            test_path = os.path.join(category_path, test)
            os.makedirs(test_path, exist_ok=True)

            # Create subfolders
            csv_path = os.path.join(test_path, 'csv')
            images_path = os.path.join(test_path, 'images')
            latex_path = os.path.join(test_path, 'latex')

            os.makedirs(csv_path, exist_ok=True)
            os.makedirs(images_path, exist_ok=True)
            os.makedirs(latex_path, exist_ok=True)

            # Create real CSV files
            create_csv_file(os.path.join(csv_path, 'equipment_used.csv'))
            create_csv_file(os.path.join(csv_path, 'data.csv'))

if __name__ == "__main__":
    create_structure()
    print("Directory structure with real CSV files created successfully.")
