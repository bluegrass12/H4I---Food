import json
import pandas as pd
import hashlib
import sys
import os

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_events(json_data):
    events = json_data.get('epcisBody', {}).get('eventList', [])
    extracted_events = []
    for event in events:
        # Extracting the event ID based on its format
        event_id = event.get('eventID', '')
        if event_id.startswith("urn:uuid:"):
            # For UUID event IDs, grab everything after last ':'
            event_id_value = event_id.split(":")[-1].replace("-", "")
        elif event_id.startswith("ni:///sha-256;"):
            # For hashed event IDs, extract the hash value
            hash_value = event_id.split(";")[-1].split("?")[0]
            event_id_value = hashlib.sha256(hash_value.encode()).hexdigest()
        else:
            # For other types of event IDs, pass through as is
            event_id_value = event_id

        # Format Error Reason
        error_reason = event.get('errorDeclaration', {}).get('reason', 'N/A')
        if error_reason != 'N/A':
            error_reason = ' '.join([word.capitalize() for word in error_reason.split('_')])

        extracted_event = {
            'Type': event.get('type', ''),
            'Event Time': event.get('eventTime', ''),
            'Event TimeZone Offset': event.get('eventTimeZoneOffset', ''),
            'Event ID': event_id_value,
            'Biz Step': event.get('bizStep', '').capitalize(),
            'Read Point': event.get('readPoint', {}).get('id', '').split(":")[-1],
            'Error Reason': error_reason
        }
        extracted_events.append(extracted_event)
    return extracted_events

def save_to_excel(extracted_events, excel_file_path):
    df = pd.DataFrame(extracted_events)
    df.to_excel(excel_file_path, index=False)
    print("Excel file saved successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_excel_converter.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    if not os.path.exists(json_file_path):
        print("Error: JSON file does not exist.")
        sys.exit(1)

    try:
        excel_file_path = os.path.splitext(json_file_path)[0] + ".xlsx"
        json_data = read_json_file(json_file_path)
        extracted_events = extract_events(json_data)
        save_to_excel(extracted_events, excel_file_path)
    except json.JSONDecodeError:
        print("Invalid JSON format. Please check the content of the file.")
    except Exception as e:
        print("An error occurred:", e)