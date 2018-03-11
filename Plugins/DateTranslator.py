import csv
import datetime
from Translator import Translator

class DateTranslator(Translator):

    def __init__(self):
        self._allowed_values = ['%b-%y', '%b-%Y', '%y-%b'] # add strfttime code as needed

    def translate(self, dataset=[], key='Date', format='%b-%y'):
        new_dataset = []

        super().validate_parameters(name='translate', parameter='format', argument=format, valid_values=self._allowed_values)

        try:
            for index, data in enumerate(dataset):
                for strftime in self._allowed_values:
                    try:
                        formatted_date = datetime.datetime.strptime(data[key], strftime).strftime(format)

                        data[key] = formatted_date
                        break
                    except ValueError:
                        if self._allowed_values.index(strftime) == len(self._allowed_values) - 1:
                            print(f"ERROR [{Translator._stage}] Unhandled data format: '[{index}][date]{data[key]}'")

                        continue

                new_dataset.append(data)
        except KeyError as err:
            print("ERROR [{Translator._stage}] Key value not found in collection:", err)
            sys.exit(1)

        return new_dataset

def main():
    dataset = []

    with open('../PyBank/raw_data/budget_data_1.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: dataset.append(row)

    date = DateTranslator()
    dataset = date.translate(dataset)

    for data in dataset:
        print(data)

if __name__ == '__main__': main()
