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
    new_dataset = []

    for file in files:
        if os.path.isfile(file): # validate file exist
            print(f"DEBUG [Collection] Collect csv data to dataset: '{file}'")

            with open(file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: new_dataset.append(row)
        else:
            print(f"ERROR [Collection] No such file or directory: '{file}'")

    return new_dataset

def date_translator(dataset, key='Date', format='%b-%y'):
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    new_dataset      = []

    if not format in allowed_strftime:
        print(f"ERROR [Translation] Value not an allowed strftime format: '{format}'")
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
                        print(f"ERROR [Translation] Unhandled date format: '{data[key]}'")

                        continue

            # print(f"{index}  {data[key]}")
            new_dataset.append(data)
    except KeyError as err:
        print("ERROR [Translation] Key value not found in collection:", err)

    return new_dataset

def date_validator(dataset, key='Date', format='%b-%y'):
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    metrics          = []
    counter          = 0

    if not format in allowed_strftime:
        print(f"ERROR [Validation] Value not an allowed strftime format: '{format}'")
        sys.exit(1)  # abort because of invalid strftime

    for index, data in enumerate(dataset):
        try:
            datetime.datetime.strptime(data[key], format)

            counter += 1
        except ValueError:
            print(f"DEBUG [Validation] Date in invalid format: '{data[key]}'")

            continue

    fail = len(dataset) - counter
    pass_rate = (counter / len(dataset)) * 100
    metrics.extend([{'name': key, 'passfail': f"{counter}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

    return metrics

def metrics_table(*metrics):
    print("\n\n Data Name".ljust(27) + " Pass/Fail".ljust(20) + " Pass Rate".rjust(6)) # column headers
    print('-' * 60)

    for metric in metrics: # dictionary in a list
        for data in metric:
            row =  f" {data['name'].title().ljust(25)}"
            row += f" {data['passfail'].title().ljust(19)}"
            row += f" {data['rate'].title().rjust(6)}"
            print(row)

    print('-' * 60)

budget_data = []
budget_data = csv_collector('raw_data/budget_data_1.csv', 'raw_data/budget_data_2.csv')
metrics = date_validator(budget_data)
budget_data = date_translator(budget_data)
metrics2 = date_validator(budget_data)
metrics_table(metrics, metrics2)

# for i, j in enumerate(budget_data):
#     print(f"{i}  {j}")
