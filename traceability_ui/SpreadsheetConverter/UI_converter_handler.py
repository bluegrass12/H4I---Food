import argparse
from converter import Converter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", metavar="FILE", type= str, help="The path of the Excel file to be converted")
    parser.add_argument("output_path", metavar="OUT", type= str, help="The path of the output file")
    parser.add_argument("settings_path", metavar="SETTINGS", type= str, help="The path of the settings file")
    parser.add_argument("-f", "--format", type=str, help="The name of the format to be used")
    args = parser.parse_args()
    converter = Converter(args.file_path, args.settings_path)
    if args.format:
        converter.change_to_format(args.format)
    converter.read_excel()
    converter.output_json(args.output_path)



# python UI_converter_handler.py 