from BasePlugin import BasePlugin

class Validator(BasePlugin):

    _stage = 'Validation'

    def __init__(self):
        self._allowed_values = []

    def validate(self):
        new_dataset   = []

def main():

    validate = Validator()

if __name__ == '__main__': main()
