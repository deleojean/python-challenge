import sys, os, csv
sys.path.append('../Plugins')
from DateTranslator    import DateTranslator
from DateValidator     import DateValidator
from NumericTranslator import NumericTranslator
from NumericValidator  import NumericValidator

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

validated_date_metrics    = date_validator.validate(budget_data, returns='metrics')
validated_numeric_metrics = numeric_validator.validate(budget_data, 'Revenue', int, returns='metrics')

# metrics
metrics_table(translated_date_metrics, translated_numeric_metrics, title='translation')
metrics_table(validated_date_metrics, validated_numeric_metrics, title='validation')

# for i, j in enumerate(budget_data):
#      print(f"{i}  {j}")
