import json
import os
import argparse
import pandas as pd
from datetime import datetime

from converterEnums import CTEType, KDE

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
    def __init__(self, file_name, settings_path="settings.json"):
        self.file_name = file_name
        self.fake_URN = "urn:epc:id:gid:88888888.XXXXXX"
        self.settings_path = settings_path
        # This will be set by get_settings() or prompt_for_format()
        self.start_row = 0
        self.start_column = 1
        self.CTEs = []
        self.cur_format = None 
        # Get the settings
        self.CTE_settings = self.get_settings()
        # Create a format if no previous one exists
        if (len(self.CTE_settings) == 0):
            self.prompt_for_format()
            self.save_settings()

    def read_excel(self):
        # Read the raw data into a dataframe
        try:
            df = pd.read_excel(self.file_name)

        except FileNotFoundError:
            print("File not found. Please make sure the file path is correct.")
        except Exception as e:
            print("An error occurred:", e)
        
        # Parse the data, starting from the start row
        try:
            # sliced df is the df with the non data starting rows removed
            # the -2 is because start_row is 1-indexed and the 1st row is the header, meaning row 2 is actually index 0
            sliced_df = df.iloc[self.start_row-2:]
            # Grabs the first entry in the sliced df and converts it to a list, -1 froms start_column is because of 0 indexing
            firstEntry = sliced_df.iloc[[0]].values.tolist()[0][self.start_column-1:]
            testCTE = HarvestCTE(firstEntry)
            testCTE.addAllKDEs(firstEntry, self.CTE_settings[self.cur_format].format)
            self.CTEs.append(testCTE)
        except Exception as e:
            print("An error occurred while parsing the data:\n\t", e)

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

    def get_settings(self):
        # Return nothing if file doesn't exist
        if (not os.path.exists(self.settings_path)):
           print("No Default Settings Found")
           return {}
        # Otherwise, read the settings from the file
        with open(self.settings_path, "r") as json_file:
            raw_settings = json.load(json_file)
            settings = {format_name : CTEFormat.fromDict(format) for format_name, format in raw_settings["settings"].items()}
            self.cur_format = raw_settings["current_format"]
            self.start_row = settings[self.cur_format].start_row
            self.start_column = settings[self.cur_format].start_column

            return settings
   
    def prompt_for_format(self):
        print("\n -- Adding a new excel file format -- \n")
        # Get CTE Type
        CTETypes = list(CTEType)
        for i in range(len(CTETypes)):
            print(f"{i+1}. {CTETypes[i].value}")
        print("\nPlease enter the number corresponding to the type of event you would like to add:")
        event_type = CTETypes[int(input())-1]
        # Get start row
        print("Please enter the row number where the data starts:")
        start_row = int(input())
        print("Please enter the column number where the data starts:")
        start_column = int(input())
        # Get the format:
        KDE_format = {}
        for kde in CTEFormat.required_KDEs[event_type]:
            print(f"\nPlease enter the column number for {kde.value}:")
            KDE_format[kde] = int(input())-start_column # Start column works because it is 1-indexed, so effectively we are subtracting (start_column + 1)
        # Name the format
        print("\n\nPlease enter the name of this format")
        format_name = input()
        # Save the data
        self.CTE_settings[format_name] = CTEFormat(start_row, event_type, KDE_format)
        self.cur_format = format_name 

    def save_settings(self):
        serializable_settings = {key: format.toDict() for key, format in self.CTE_settings.items()}
        with open(self.settings_path, "w") as json_file:
            json.dump({"current_format": self.cur_format,"settings": serializable_settings}, json_file, indent=4)

    def change_to_format(self, format_name):
        if(format_name not in self.CTE_settings):
            print("Format not found")
            return
        self.cur_format = format_name
        self.start_row = self.CTE_settings[format_name].start_row
        self.start_column = self.CTE_settings[format_name].start_column
        self.save_settings()

class CTE:
    """This is a super class for all CTEs (critical tracking events)
        It is intended to be the state that CTEs are stored in during the program, between being read and being exported to some output

    Attributes:
        event_type (CTEType): The type of event that the CTE represents
        raw_data (list): A list of the values that the CTE contains
        KDEs (dict): A dictionary that maps each key data element to its corresponding value

    """
    def __init__(self, type, raw_data):
        self.event_type = type
        self.raw_data = raw_data
        self.KDEs = {}

    def add_KDE(self, key, value):
        self.KDEs[key] = value

    def convertToEPCIS(self):
        pass
    def convertToJSON(self):
        pass    

class HarvestCTE(CTE):

    """This class represents a Harvest CTE
    It is a subclass of the CTE class and is intended to be used to store and convert Harvest CTEs
    """
    # The KDEs that must be included for a valid Harvest CTE
    requiredKDEs = [KDE.SUBSEQUENT_RECIPIENT_NAME, KDE.SUBSEQUENT_RECIPIENT_ADDRESS, KDE.HARVEST_LOCATION_COMPANY_NAME, KDE.HARVEST_LOCATION_ADDRESS, KDE.QUANTITY_HARVESTED, KDE.UNIT_OF_MEASURE, KDE.HARVESTER_BUSINESS_NAME, KDE.RAC_COMMODITY_AND_VARIETY, KDE.HARVEST_DATE]

    def __init__(self, raw_data):
        super().__init__(CTEType.HARVEST.value, raw_data)

    def addAllKDEs(self, values, format):
        for event, index in format.items():
            self.KDEs[event] = values[index]
        

    def convertToJSON(self):
        return {
            "eventList": "ObjectEvent",
            "eventTime": self.KDEs[KDE.HARVEST_DATE].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "recordTime": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "eventTimeZoneOffset": "TO-DO",
            "eventID": "urn:epc:id:gid:88888888.XXXXXX",
            "action": "ADD",
            "biz-step": "creating_class_instance",
            "disposition": "active",
            "readPoint": {
                    "name": self.KDEs[KDE.HARVEST_LOCATION_COMPANY_NAME],
                    "extension": {
                        "address": self.KDEs[KDE.HARVEST_LOCATION_ADDRESS]
                    }
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
                        "quantity": self.KDEs[KDE.QUANTITY_HARVESTED],
                        "uom": self.KDEs[KDE.UNIT_OF_MEASURE]
                    }
            ]
            

        }

class CTEFormat:

    """ This is a simple class to store different ways excel files can be formatted.

    Attributes:
        [static] required_KDEs (dict): A dictionary that maps each CTEType to a list of KDEs that are required for that type
        start_row (int): The row where the data starts
        event_type (CTEType): The type of event that the data represents
        format (dict): A dictionary which maps each required KDE type to the corresponding column in the Excel file     

    """
 
    required_KDEs = {
        CTEType.HARVEST: [KDE.SUBSEQUENT_RECIPIENT_NAME, KDE.SUBSEQUENT_RECIPIENT_ADDRESS, KDE.HARVEST_LOCATION_COMPANY_NAME, KDE.HARVEST_LOCATION_ADDRESS, KDE.QUANTITY_HARVESTED, KDE.UNIT_OF_MEASURE, KDE.HARVESTER_BUSINESS_NAME, KDE.RAC_COMMODITY_AND_VARIETY, KDE.HARVEST_DATE,],
    }

    def __init__(self, start_row, event_type, format, start_column=1):
        self.format = format
        self.event_type = event_type
        self.start_row = start_row
        self.start_column = start_column

    def toDict(self):
        return {
            "start_row": self.start_row,
            "start_column": self.start_column,
            "event_type": self.event_type.value,
            "format": {event.value: index for event, index in self.format.items()}
        }
    
    @staticmethod
    def fromDict(format_dict):
        event_type = CTEType(format_dict["event_type"])
        format = {KDE(key): value for key, value in format_dict["format"].items()}
        return CTEFormat(format_dict["start_row"], event_type, format, format_dict["start_column"])



    
    



# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", metavar="FILE", type= str, help="The name of the Excel file to be converted")
    parser.add_argument("-f", "--format", type=str, help="The name of the format to be used")
    parser.add_argument("-a", "--add_format", action="store_true", help="Add a new format")
    args = parser.parse_args()
    converter = Converter(args.file_name)
    if(args.add_format):
        converter.prompt_for_format()
        converter.save_settings()
    if(args.format):
        converter.change_to_format(args.format)
    converter.read_excel()
    converter.output_json("test_output.json")