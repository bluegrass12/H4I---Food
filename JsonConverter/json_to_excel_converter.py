import json
import pandas as pd

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def flatten_events(events):
    flattened_events = []
    for event in events:
        flattened_event = {}
        flattened_event['type'] = event['type']
        flattened_event['eventTime'] = event['eventTime']
        flattened_event['eventTimeZoneOffset'] = event['eventTimeZoneOffset']
        flattened_event['eventID'] = event['eventID']
        flattened_event['bizStep'] = event.get('bizStep', '')
        flattened_event['readPoint'] = event.get('readPoint', {}).get('id', '')
        flattened_event.update(flatten_quantities(event.get('inputQuantityList', []), 'input'))
        flattened_event.update(flatten_quantities(event.get('outputQuantityList', []), 'output'))
        flattened_events.append(flattened_event)
    return flattened_events

def flatten_quantities(quantities, prefix):
    flattened_quantities = {}
    for i, quantity in enumerate(quantities):
        key_prefix = f'{prefix}{i+1}_'
        flattened_quantities[key_prefix + 'epcClass'] = quantity.get('epcClass', '')
        flattened_quantities[key_prefix + 'quantity'] = quantity.get('quantity', '')
        flattened_quantities[key_prefix + 'uom'] = quantity.get('uom', '')
    return flattened_quantities

def convert_to_excel(json_file_path, excel_file_path):
    # Read JSON data from file
    json_data = read_json_file(json_file_path)

    # Flatten event data
    event_list = json_data.get('epcisBody', {}).get('eventList', [])
    flattened_events = flatten_events(event_list)

    # Convert flattened data to DataFrame
    df = pd.DataFrame(flattened_events)

    # Convert DataFrame to Excel file
    df.to_excel(excel_file_path, index=False)
    print("Excel file created successfully.")

if __name__ == "__main__":
    json_file_path = input("Enter the path to the JSON file: ")
    excel_file_path = input("Enter the path to save the Excel file: ")

    try:
        convert_to_excel(json_file_path, excel_file_path)
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format. Please check the content of the file.")
    except Exception as e:
        print("An error occurred:", e)