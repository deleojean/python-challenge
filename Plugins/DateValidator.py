import csv
import datetime
from Validator import Validator

class DateValidator(Validator):

    def __init__(self):
        self._allowed_strftime = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed
        self._allowed_returns  = ['metrics', 'dataset', 'all']

    def validate(self, dataset, key='Date', format='%b-%y', returns='dataset'):
        new_dataset   = []
        counter       = 0

        super().validate_parameters(name='validate', parameter='format', argument=format, valid_values=self._allowed_strftime)
        super().validate_parameters(name='validate', parameter='returns', argument=returns, valid_values=self._allowed_returns)

        try:
            for index, data in enumerate(dataset):
                try:
                    datetime.datetime.strptime(data[key], format)

                    counter += 1
                    new_dataset.append(data)
                except ValueError:
                    print(f"DEBUG [{Validator._stage}] Invalid data removed from dataset: '[{index}]{data}'")

                    continue

            metrics = super().collect_metrics(key=key, counter=counter, total=len(dataset))

        except KeyError as err:
            print("ERROR [{Validator._stage}] Key value not found in collection:", err)
            sys.exit(1)

        if returns == 'metrics': return metrics
        if returns == 'dataset': return new_dataset
        if returns == 'all'    : return new_dataset, metrics

def main():

    dataset = []

    with open('../PyBank/raw_data/budget_data_1.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: dataset.append(row)

    date = DateValidator()
    dataset = date.validate(dataset)

    for data in dataset:
        print(data)

if __name__ == '__main__': main()
