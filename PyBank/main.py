import csv
import os

# The total number of months included in the dataset

# The total amount of revenue gained over the entire period

# The average change in revenue between months over the entire period

# The greatest increase in revenue (date and amount) over the entire period

# The greatest decrease in revenue (date and amount) over the entire period

def csv_collector(*files):
    collection = []

    for file in files:
        if os.path.isfile(file): # validate file exist
            print(f"FileFound: Merge csv data to dataset: '{file}'")

            with open(file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: collection.append(row)
        else:
            print(f"FileNotFoundError: No such file or directory: '{file}'")

    return collection

budget_data = []
budget_data = csv_collector('raw_data/budget_data_1.csv', 'raw_data/budget_data_2.csv')
