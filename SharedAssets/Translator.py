
class Translator:
    _stage = 'Translation'

    def __init__(self):
        self._allowed_values = []

    def validate_parameters(self, name, parameter, argument, valid_values):
        if not argument in valid_values:
            print(f"ERROR [{self._stage}] Allowed '{name}({parameter})' arguments: '{valid_values}'")
            sys.exit(1)

    def translate(self):
        new_dataset = []

def main():

    translate = Translator()

if __name__ == '__main__': main()
