import sys, os, csv
sys.path.append('../Plugins')
from DateTranslator    import DateTranslator
from DateValidator     import DateValidator
from NumericTranslator import NumericTranslator
from NumericValidator  import NumericValidator

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

date_translator    = DateTranslator()
date_validator     = DateValidator()
numeric_translator = NumericTranslator()
numeric_validator  = NumericValidator()

# translation
budget_data = date_translator.translate(budget_data)
budget_data = numeric_translator.translate(budget_data, 'Revenue', int)

# validation
budget_data, translated_date_metrics    = date_validator.validate(budget_data, returns='all')
budget_data, translated_numeric_metrics = numeric_validator.validate(budget_data, 'Revenue', int, returns='all')

validated_budget_data, validated_date_metrics    = date_validator.validate(budget_data, returns='all')
validated_budget_data, validated_numeric_metrics = numeric_validator.validate(validated_budget_data, 'Revenue', int, returns='all')

# metrics
metrics_table(translated_date_metrics, translated_numeric_metrics, title='translation')
metrics_table(validated_date_metrics, validated_numeric_metrics, title='validation')

# for i, j in enumerate(budget_data):
#      print(f"{i}  {j}")

def extrema_amount(extrema, key1='Date', key2='Revenue'):
    valid_extrema = [min, max]
    month_amount  = {}

    try:
        amount = extrema([data[key2] for data in validated_budget_data])
        month  = [data[key1] for data in validated_budget_data if data[key2] == amount]
        month_amount = {key1: month, key2: amount}
    except TypeError:
        print(f"ERROR [] Allowed 'extrema_amount(extrema)' arguments: '{valid_extrema}'")
        sys.exit(1)
    except KeyError as err:
        print("ERROR [] Key value not found in collection:", err)
        sys.exit(1)

    return month_amount

def financial_table(**kwargs):
    dataset = {" Total Months:"                 : kwargs['months'],
               " Total Revenue:"                : f"${kwargs['revenue']}",
               " Average Revenue Change:"       : f"${kwargs['average']}",
               " Greatest Increase in Revenue:" : f"{kwargs['increase']}",
               " Greatest Decrease in Revenue:" : f"{kwargs['decrease']}"}

    print(f"\n {kwargs['title'].title()}") # column headers
    print('-' * 60)
    for key, value in dataset.items():
        try:
            print(f"{key} {value}")
        except:
            continue

    print("\n")

key1 = 'Date'
key2 = 'Revenue'

# The total number of months included in the dataset
months = [data[key1] for data in validated_budget_data]
total_months = len(set(months)) # set to unqiue values

# The total amount of revenue gained over the entire period
total_revenue = sum([data[key2] for data in validated_budget_data])

# The average change in revenue between months over the entire period
average_change = total_revenue // len(months) # integers

# The greatest increase in revenue (date and amount) over the entire period
greatest_increase = extrema_amount(max)
greatest_increase = f"{greatest_increase[key1]} $({greatest_increase[key2]})"

# The greatest decrease in revenue (date and amount) over the entire period
greatest_decrease = extrema_amount(min)
greatest_decrease = f"{greatest_decrease[key1]} $({greatest_decrease[key2]})"

print("\n")

financial_table(title='financial analysis', months=total_months, revenue=total_revenue, average=average_change, increase=greatest_increase, decrease=greatest_decrease)
