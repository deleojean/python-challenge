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

            with open(file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: new_dataset.append(row)

        else:
            print(f"ERROR [Collection] No such file or directory: '{file}'")
            print(f"ERROR [Collection] Fail csv data merge to dataset: '{file}'")

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
                    new_dataset.append(data)
                    break
                except ValueError:
                    if allowed_strftime.index(strftime) == len(allowed_strftime) - 1:
                        print(f"ERROR [Translation] Unhandled date format: '[{index}]{data[key]}'")
                        print(f"DEBUG [Translation] Data not added to dataset: '[{index}]{data}'")

                    continue

    except KeyError as err:
        print("ERROR [Translation] Key value not found in collection:", err)
        sys.exit(1)

    return new_dataset

def numeric_translator(dataset, key, format):
    allowed_numerics = [int, float, complex] # add numeric type as needed
    new_dataset      = []

    if not format in allowed_numerics:
        print(f"ERROR [Translation] Value not an allowed numeric data type: '{format} {type(format)}'")
        sys.exit(1)  # abort because of invalid numeric type

    try:
        for index, data in enumerate(dataset):
            try:
                formatted_numeric = format(data[key])

                data[key] = formatted_numeric
                new_dataset.append(data)
            except:
                print(f"ERROR [Translation] Unhandled numeric type: '[{index}]{data[key]}'")
                print(f"DEBUG [Translation] Data not added to dataset: '[{index}]{data}'")

                continue

    except KeyError as err:
        print("ERROR [Translation] Key value not found in collection:", err)
        sys.exit(1)

    return new_dataset

def numeric_validator(dataset, key, format):
    allowed_numerics = [int, float, complex] # add numeric type as needed
    metrics          = []
    counter          = 0
    pass_rate        = 0

    if not format in allowed_numerics:
        print(f"ERROR [Translation] Value not an allowed numeric data type: '{format} {type(format)}'")
        sys.exit(1)  # abort because of invalid numeric type

    try:
        for index, data in enumerate(dataset):
            try:
                format(data[key])

                counter += 1
            except ValueError:
                print(f"DEBUG [Validation] Date in invalid format: '[{index}]{data[key]}'")

                continue

        fail = len(dataset) - counter
        pass_rate = (counter / len(dataset)) * 100 if counter >= 0 else pass_rate
        metrics.extend([{'name': key, 'passfail': f"{counter}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

    except KeyError as err:
        print("ERROR [Validation] Key value not found in collection:", err)
        sys.exit(1)

    return metrics

def date_validator(dataset, key='Date', format='%b-%y'):
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    metrics          = []
    counter          = 0
    pass_rate        = 0

    if not format in allowed_strftime:
        print(f"ERROR [Validation] Value not an allowed strftime format: '{format}'")
        sys.exit(1)  # abort because of invalid strftime

    try:
        for index, data in enumerate(dataset):
            try:
                datetime.datetime.strptime(data[key], format)

                counter += 1
            except ValueError:
                print(f"DEBUG [Validation] Date in invalid format: '[{index}]{data[key]}'")

                continue

        fail = len(dataset) - counter
        pass_rate = (counter / len(dataset)) * 100 if counter >= 0 else pass_rate
        metrics.extend([{'name': key, 'passfail': f"{counter}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

    except KeyError as err:
        print("ERROR [Validation] Key value not found in collection:", err)
        sys.exit(1)

    return metrics

def metrics_table(*metrics):
    header_exist = False

    for metric in metrics:
        try:
            for data in metric: # validate keys
                name     = data['name']
                passfail = data['passfail']
                rate     = data['rate']

            if not header_exist:
                print("\n Data Name".ljust(27) + " Pass/Fail".ljust(20) + " Pass Rate".rjust(6)) # column headers
                print('-' * 60)
                header_exist = True

            row =  f" {name.title().ljust(25)}"
            row += f" {passfail.title().ljust(19)}"
            row += f" {rate.title().rjust(6)}"
            print(row)

        except:
            continue

    print('-' * 60)

# collection
budget_data = []
budget_data = csv_collector('raw_data/budget_data_1.csv', 'raw_data/budget_data_2.csv')

# translation
budget_data = date_translator(budget_data)
budget_data = numeric_translator(budget_data, 'Revenue', int)

# validation
date_metrics = date_validator(budget_data)
numeric_metrics = numeric_validator(budget_data, 'Revenue', int)

# metrics
metrics_table(date_metrics, numeric_metrics)

# for i, j in enumerate(budget_data):
#      print(f"{i}  {j}")
