import json
import pandas as pd
import sys

def write_to_excel(data, excel_file_path):
    df = pd.DataFrame(data)
    df.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    # Receive JSON string from json_converter.py
    json_string = sys.stdin.read()
    try:
        # Convert JSON string to Python data structure
        python_data = json.loads(json_string)
    except json.JSONDecodeError:
        print("Invalid JSON format received from json_converter.py.")
        sys.exit(1)

    excel_file_path = input("Enter the path to save the Excel file: ")

    try:
        write_to_excel(python_data, excel_file_path)
        print("Excel file created successfully.")
    except Exception as e:
        print("An error occurred:", e)