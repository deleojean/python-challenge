import csv
import os
import datetime
import sys

# The total number of months included in the dataset

# The total amount of revenue gained over the entire period

# The average change in revenue between months over the entire period

# The greatest increase in revenue (date and amount) over the entire period

# The greatest decrease in revenue (date and amount) over the entire period

def csv_collector(*files):
    dataset = []

    for file in files:
        if os.path.isfile(file): # validate file exist
            print(f"FileFound: Collect csv data to dataset: '{file}'")

            with open(file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: dataset.append(row)
        else:
            print(f"FileNotFoundError: No such file or directory: '{file}'")

    return dataset

def date_translator(dataset, key='Date', format='%b-%y'):
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    new_dataset = []

    if not format in allowed_strftime:
        print(f"ArgumentError: Value not an allowed strftime format: '{format}'")
        sys.exit(1)  # abort because of invalid strftime

    try:
        for index, data in enumerate(dataset):
            for strftime in allowed_strftime:
                try:
                    formatted_date = datetime.datetime.strptime(data[key], strftime).strftime(format)

                    data[key] = formatted_date
                    break
                except ValueError:
                    if allowed_strftime.index(strftime) == len(allowed_strftime) - 1:
                        print(f"DateFormatFail: Unhandled date format: '{data[key]}'")

                        continue

            # print(f"{index}  {data[key]}")
            new_dataset.append(data)
    except KeyError as err:
        print("ArgumentError: Key value not found in collection:", err)

    return new_dataset

def date_validator(dataset, key='Date', format='%b-%y'):
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    metrics = []
    counter = 0

    if not format in allowed_strftime:
        print(f"ArgumentError: Value not an allowed strftime format: '{format}'")
        sys.exit(1)  # abort because of invalid strftime

    for index, data in enumerate(dataset):
        try:
            datetime.datetime.strptime(data[key], format)

            counter += 1
        except ValueError:
            print(f"DateFormatFail: Date in invalid format: '{data[key]}'")

            continue

    fail = len(dataset) - counter
    pass_rate = (counter / len(dataset)) * 100
    metrics.extend([{'name': key, 'passfail': f"{counter}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

    return metrics

budget_data = []
budget_data = csv_collector('raw_data/budget_data_1.csv', 'raw_data/budget_data_2.csv')
budget_data = date_translator(budget_data)
metrics = date_validator(budget_data)

# for i, j in enumerate(budget_data):
#     print(f"{i}  {j}")
