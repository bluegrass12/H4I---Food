# Traceability JSON - Excel Converter

A simple project which converts EPCIS 2.0 Formatted Excel files to formatted JSON files and vice versa

## Git Repository

[Link to Github Repository](https://github.com/bluegrass12/H4I---Food/)

## Set up steps

In the current dev state, this application relies on Python for the backend and Flutter (a Dart framework) for the frontend.
As such, you'll need both Python and Flutter installed on your local machine. 
[Link to official flutter install guide](https://flutter.dev/docs/get-started/install)
[Link to Python's site](https://www.python.org/downloads/)

### Running using the UI
Once the code is installed, you can run it simply by using the "flutter run" command from the console, 
or, if using an IDE by navigating to the main.dart file and clicking run/debug.

The front end was designed to be a windows application, but it can also be run of the web (such as through chrome)
or as an Android app. 

### Running using the command line
The application can also be ran using a command line interface. Running the code this way only requires Python to be installed.

To convert from Excel to JSON, run "python converter.py FILE_PATH -f format"
Run with the -a flag to run the command line prompt to add a format

To convert JSON to Excel, run "python json_to_excel_converter.py JSON_FILE_PATH"

## How the Code Works
### Backend
The backend of this application relies on python. It uses pandas to read excel files, parsing the columns according to formats. 
Formats are mappings of column numbers to KDEs, and are how the program knows which data is in which column.
They are saved to the settings.json file (so they can be re-used), and can be added using the -a flag when running converter.py.

The JSON to excel conversion part works similarly, except no format is needed because the files can be more easily parsed. 
A file is simply designated, read, and outputed into an excel file using Pandas' built in .toexcel() function.

### Frontend
The frontend is a simple flutter application, intended to be run with a Windows application as the target.
A format can be selected from the drop down, and clicking the button in the middle will open a file explorer allowing
you to select an Excel or JSON file. If the convert button is then selected, the appropriate python file (either converter.py or json_to_excel_converter.py)
is ran according to the selected file type. The output then appears in either the JsonConverter folder or SpreadsheetConverter folder. 

The python code is ran simply by running the python code in the console with the input folder specified. When running converter.py, the shell 
python file UI_converter_handler.py is actually called in order to condense all console inputs into initial run parameters.

## What Works and What Doesn't
The basic functionality of reading an Excel file and converting it to JSON, as well as reading a JSON file and converting it Excel, are functional. 
Furthermore, the UI is functional in serving as a visual interface for those tasks; and provides a file explorer for easy selection of files.

However, the add buttton on the UI, intended to link to an add_format which would provide a visual representation for creating a format, is 
not functional and currently does nothing. We simply didn't have enough time to add that feature. Furthermore, although the output JSON & Excel files
are roughly EPCIS 2.0 compliant, they are not 100% so, and no master data is incorporated into the program. Thus, this code serves more as a proof of
concept and as a potential starting point rather than a full-fledged solution.

## What to Work on Next
There are several obvious areas of improvement for this code.
For one, an add format screen should be added to the UI, which would provide the same functionality as the console add format process.
Secondly, more options in the UI to specify locations (eg. output locations or location of settings file) should be added.
Thirdly, the outputs, both JSON and Excel, should be fine tuned to be fully EPCIS compliant. This would likely involve incorporating EPCIS master data into the process.
Finally, the code should be expanded to convert more than a single Harvest event, it should be easily expanded to handle all CTE events as well as handle multiple at once. 