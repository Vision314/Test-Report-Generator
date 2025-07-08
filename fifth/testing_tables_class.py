from tables import Tables
import json

path = r"C:\Users\enfxm\Desktop\Python Testing\Test Report Template\Test-Report-Generator\fifth\latex_generation_test001\test_descriptions.json"


with open(path, 'r') as file:
    data = json.load(file)

test1_tables = Tables(table_metadata=data)


