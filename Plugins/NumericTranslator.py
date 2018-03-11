import csv
from Translator import Translator

class NumericTranslator(Translator):

    def __init__(self):
        self._allowed_values = [int, float, complex] # add numeric code as needed

    def translate(self, dataset=[], key='', format=int):
        new_dataset      = []

        super().validate_parameters(name='translate', parameter='format', argument=format, valid_values=self._allowed_values)

        try:
            for index, data in enumerate(dataset):
                new_dataset.append(data)
                try:
                    formatted_numeric = format(data[key])

                    data[key] = formatted_numeric
                except:
                    print(f"ERROR [{Translator._stage}] Unhandled data format: '[{index}][numeric]{data[key]}'")

                    continue

        except KeyError as err:
            print("ERROR [{Translator._stage}] Key value not found in collection:", err)
            sys.exit(1)

        return new_dataset

def main():
    dataset = []

    with open('../PyBank/raw_data/budget_data_1.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: dataset.append(row)

    numeric = NumericTranslator()
    dataset = numeric.translate(dataset, 'Revenue', float)

    for data in dataset:
        print(data)

if __name__ == '__main__': main()
