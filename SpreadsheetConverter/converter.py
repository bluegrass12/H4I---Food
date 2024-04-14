import json
import pandas as pd
# from EPCPyYes.core.v1_2.CBV import business_steps
import sys
import os
from datetime import datetime

# Header ordering is fixed (for now)
# Subsequent recipient name, subsequent recipient address, harvest location company name, harvest location address, 
# Quantity harvested, Unit of measure, Reference document type, Reference document number, Harvester business name, 
# Harvester phone number, Rac commodity and variety, Container name or Equivalent (aquaculture), Harvest date,
# Harvest start time, Harvest end time, Harvest duration, Harvest location GPS latitude, Harvest location GPS longitude,

# Questions to consider:
# 1. Are we converting the entire Excel file or just a specific sheet?
# 2. What is the format of the data? Is it consistent?

# Steps:
# Develop list of what is needed for EPCIS JSON file
# Determine which columns in the Excel file correspond to each data point
# Read from excel, convert, and write to JSON


class Converter:
    def __init__(self, file_name, start_row):
        self.file_name = file_name
        self.start_row = start_row
        self.CTEs = []
        self.fake_URN = "urn:epc:id:gid:88888888.XXXXXX"

    def read_excel(self):
        try:
            df = pd.read_excel(self.file_name)

            # check if start_row is less than the number of rows in the Excel file
            if ((self.start_row - 2) > df.shape[0]):
                raise Exception('Number of first data row must not exceed number of rows in Excel file.')
            
            print("Excel file successfully read.")
        except FileNotFoundError:
            print("File not found. Please make sure the file path is correct.")
            print('Usage:', os.path.basename(__file__), '<Excel file name>',
              '<number of first data row>', '<JSON file name>')
            sys.exit(1)
        except Exception as e:
            print("An error occurred:", e)
            print('Usage:', os.path.basename(__file__), '<Excel file name>',
              '<number of first data row>', '<JSON file name>')
            sys.exit(1)
        
        # Parse the data, starting from the start row
        try:
            sliced_df = df.iloc[self.start_row-2:]
            firstEntry = sliced_df.iloc[[0]].values.tolist()[0][1:]
            testCTE = HarvestCTE("Harvest", firstEntry)
            testCTE.addAllKDEs(firstEntry)
            self.CTEs.append(testCTE)
        except Exception as e:
            print("An error occurred while parsing the data:\n\t", e)
            print('Usage:', os.path.basename(__file__), '<Excel file name>',
              '<number of first data row>', '<JSON file name>')
            sys.exit(1)

    def output_json(self, output_path):
        eventList = [] if len(self.CTEs) == 0 else [self.CTEs[0].convertToJSON()]
        data = {
            "@context": ["https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld"],
            "type": "EPCISDocument",
            "schemaVersion" : "2.0",
            "creationDate" : datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "epcisBody": {
                "eventList": eventList
            }
        }
        with open(output_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
            

class CTE:
    def __init__(self, type, value):
        self.event_type = type
        self.value = value
        self.KDEs = {}

    def add_KDE(self, key, value):
        self.KDEs[key] = value

    def convertToEPCIS(self):
        pass
    def convertToJSON(self):
        pass    

class HarvestCTE(CTE):
    def __init__(self, type, value):
        self.format = ["rName", "rAddr", "hLocName", "hLocAddr", "quantity", "unit", "refDocType", "refDocNum", "hBusName", "hPhoneNum", "racCommodity", "containerName", "hDate",]
        super().__init__(type, value)

    def addAllKDEs(self, values):
        for i in range(len(self.format)):
            self.KDEs[self.format[i]] = values[i]

    def convertToJSON(self):
        return {
            "eventList": "ObjectEvent",
            "eventTime": "TO-DO",
            "recordTime": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "eventTimeZoneOffset": "TO-DO",
            "eventID": "urn:epc:id:gid:88888888.XXXXXX",
            "action": "ADD",
            "biz-step": "creating_class_instance",
            "disposition": "active",
            "readPoint": {
                    "id": "https://id.gs1.org/414/9521234560005"
                },
            "bizLocation": {
                    "id": "https://id.gs1.org/414/9521234560005"
                },
            "bizTransactionList": [
                    {
                        "type": "prodorder",
                        "bizTransaction": "urn:epcglobal:cbv:bt:88888888:XXXXXX"
                    }
                ],
            "quantityList": [
                    {
                        "epcClass": "https://id.gs1.org/01/99521234561111/10/abc1234",
                        "quantity": self.KDEs["quantity"],
                        "uom": self.KDEs["unit"]
                    }
            ]
            

        }


if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print('Incorrect Arguments.')
        print('Must include Excel (xlsx) file.')
        print('Must indicate number of the first data row (do not include header or description rows).')
        print('Must include desired name of output JSON file')
        print('Usage:', os.path.basename(__file__), '<Excel file name>',
              '<number of first data row>', '<JSON file name>')
        sys.exit(1)

    try:
        firstRow = int(sys.argv[2])

        # n cannot be greater or less than the number of rows in CSV file
        if (firstRow < 1):
            raise ValueError

    except ValueError:
        print('Enter first data row as an integer. Must not exceed number of rows in Excel file or be less than 1')
        print('Usage:', os.path.basename(__file__), '<Excel file name>',
              '<number of first data row>', '<JSON file name>')
        sys.exit(1)

    output = sys.argv[3]
    if (len(output) < 6 or output[-5:] != '.json'):
        output += '.json'

    converter = Converter(sys.argv[1], firstRow)
    converter.read_excel()
    converter.output_json(output)



# other error handling to add: 
# - if firstRow is greater than the number of rows in the Excel file, raise ValueError