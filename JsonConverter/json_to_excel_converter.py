import json
import pandas as pd

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def convert_to_excel(json_data, excel_file_path):
    df = pd.DataFrame(json_data)
    df.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    json_file_path = input("Enter the path to the JSON file: ")
    excel_file_path = input("Enter the path to save the Excel file: ")

    try:
        # Read JSON data from file
        json_data = read_json_file(json_file_path)
        print("JSON data loaded successfully.")

        # Convert JSON data to Excel file
        convert_to_excel(json_data, excel_file_path)
        print("Excel file created successfully.")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format. Please check the content of the file.")
    except Exception as e:
        print("An error occurred:", e)