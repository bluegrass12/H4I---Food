import pandas as pd

file_name = input("Enter the Excel file name: ")

try:
    df = pd.read_excel(file_name)
    print("DataFrame successfully created from the Excel file.")
    ##print(df.head())  
except FileNotFoundError:
    print("File not found. Please make sure the file path is correct.")
except Exception as e:
    print("An error occurred:", e)