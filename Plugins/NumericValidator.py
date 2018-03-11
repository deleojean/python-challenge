import csv
from Validator import Validator

class NumericValidator(Validator):

    def __init__(self):
        self._allowed_numerics = [int, float, complex] # add numeric type as needed
        self._allowed_returns  = ['metrics', 'dataset', 'all']

    def validate(self, dataset=[], key='', format=int, returns='dataset'):
        new_dataset      = []
        counter          = 0

        super().validate_parameters(name='validate', parameter='format', argument=format, valid_values=self._allowed_numerics)
        super().validate_parameters(name='validate', parameter='returns', argument=returns, valid_values=self._allowed_returns)

        try:
            for index, data in enumerate(dataset):
                if type(format(1)) == type(data[key]):
                    counter += 1
                    new_dataset.append(data)
                else:
                    print(f"DEBUG [Validation] Invalid data removed from dataset: '[{index}]{data}'")

            metrics = super().collect_metrics(key=key, counter=counter, total=len(dataset))

        except KeyError as err:
            print("ERROR [Validation] Key value not found in collection:", err)
            sys.exit(1)

        if returns == 'metrics': return metrics
        if returns == 'dataset': return new_dataset
        if returns == 'all'    : return new_dataset, metrics

def main():

    dataset = []

    with open('Test/budget_data_1.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: dataset.append(row)

    numeric = NumericValidator()
    dataset = numeric.validate(dataset, key='Revenue')

    for data in dataset:
        print(data)

if __name__ == '__main__': main()
