import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    json_file_path = input("Enter the path to the JSON file: ")

    try:
        json_data = read_json_file(json_file_path)
        print("JSON data loaded successfully.")
        print("Converted Python data structure:")
        print(json_data)
        exit(json_data)  # Exits and passes the JSON data to the caller
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except json.JSONDecodeError:
        print("Invalid JSON format. Please check the content of the file.")