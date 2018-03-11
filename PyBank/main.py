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
    function_name    = 'date_translator'
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    new_dataset      = []

    if not format in allowed_strftime:
        print(f"ERROR [Translation] Allowed '{function_name}(format)' arguments: '{allowed_strftime}'")
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
                        print(f"ERROR [Translation] Unhandled date format: '[{index}]{data[key]}'")

                    continue

            new_dataset.append(data)
    except KeyError as err:
        print("ERROR [Translation] Key value not found in collection:", err)
        sys.exit(1)

    return new_dataset

def numeric_translator(dataset, key, format):
    function_name    = 'numeric_translator'
    allowed_numerics = [int, float, complex] # add numeric type as needed
    new_dataset      = []

    if not format in allowed_numerics:
        print(f"ERROR [Translation] Allowed '{function_name}(format)' arguments: '{allowed_numerics}'")
        sys.exit(1)  # abort because of invalid strftime

    try:
        for index, data in enumerate(dataset):
            new_dataset.append(data)
            try:
                formatted_numeric = format(data[key])

                data[key] = formatted_numeric
            except:
                print(f"ERROR [Translation] Unhandled numeric type: '[{index}]{data[key]}'")

                continue

    except KeyError as err:
        print("ERROR [Translation] Key value not found in collection:", err)
        sys.exit(1)

    return new_dataset

def numeric_validator(dataset, key, format, returns='all'):
    function_name    = 'numeric_validator'
    allowed_numerics = [int, float, complex] # add numeric type as needed
    allowed_returns  = ['metrics', 'all']
    new_dataset      = []
    metrics          = []
    counter          = 0
    pass_rate        = 0

    if not returns in allowed_returns:
        print(f"ERROR [Validation] Allowed '{function_name}(returns) arguments: '{allowed_returns}'")
        sys.exit(1)  # abort because of invalid return value

    if not format in allowed_numerics:
        print(f"ERROR [Validation] Allowed '{function_name}(format)' arguments: '{allowed_numerics}'")
        sys.exit(1)  # abort because of invalid strftime

    try:
        for index, data in enumerate(dataset):
            if type(format(1)) == type(data[key]):
                counter += 1
                new_dataset.append(data)
            else:
                print(f"DEBUG [Validation] Invalid data removed from dataset: '[{index}]{data}'")

        fail = len(dataset) - counter
        pass_rate = (counter / len(dataset)) * 100 if counter > 0 else pass_rate
        metrics.extend([{'name': key, 'passfail': f"{counter}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

    except KeyError as err:
        print("ERROR [Validation] Key value not found in collection:", err)
        sys.exit(1)

    if returns == 'metrics': return metrics
    if returns == 'all'    : return new_dataset, metrics

def date_validator(dataset, key='Date', format='%b-%y', returns='all'):
    function_name    = 'date_validator'
    allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
    allowed_returns  = ['metrics', 'all']
    new_dataset      = []
    metrics          = []
    counter          = 0
    pass_rate        = 0

    if not returns in allowed_returns:
        print(f"ERROR [Validation] Allowed '{function_name}(returns) arguments: '{allowed_returns}'")
        sys.exit(1)  # abort because of invalid return value

    if not format in allowed_strftime:
        print(f"ERROR [Validation] Allowed '{function_name}(format)' arguments: '{allowed_strftime}'")
        sys.exit(1)  # abort because of invalid strftime

    try:
        for index, data in enumerate(dataset):
            try:
                datetime.datetime.strptime(data[key], format)

                counter += 1
                new_dataset.append(data)
            except ValueError:
                print(f"DEBUG [Validation] Invalid data removed from dataset: '[{index}]{data}'")

                continue

        fail = len(dataset) - counter
        pass_rate = (counter / len(dataset)) * 100 if counter > 0 else pass_rate
        metrics.extend([{'name': key, 'passfail': f"{counter}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

    except KeyError as err:
        print("ERROR [Validation] Key value not found in collection:", err)
        sys.exit(1)

    if returns == 'metrics': return metrics
    if returns == 'all'    : return new_dataset, metrics

def metrics_table(*metrics, title='required'):
    function_name = 'metrics_table'
    header_exist  = False

    if title == 'required':
        print(f"ERROR [Metrics] '{function_name}(title)' arguments: 'required'")
        sys.exit(1)

    for metric in metrics:
        try:
            for data in metric: # validate keys
                name     = data['name']
                passfail = data['passfail']
                rate     = data['rate']

            if not header_exist:
                print(f"\n {title.title()}".ljust(27) + " Pass/Fail".ljust(20) + " Pass Rate".rjust(6)) # column headers
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
budget_data, translated_date_metrics = date_validator(budget_data)
budget_data, translated_numeric_metrics = numeric_validator(budget_data, 'Revenue', int)

validated_date_metrics = date_validator(budget_data, returns='metrics')
validated_numeric_metrics = numeric_validator(budget_data, 'Revenue', int, returns='metrics')

# metrics
metrics_table(translated_date_metrics, translated_numeric_metrics, title='translation')
metrics_table(validated_date_metrics, validated_numeric_metrics, title='validation')

# for i, j in enumerate(budget_data):
#      print(f"{i}  {j}")
