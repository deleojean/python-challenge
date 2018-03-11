from BasePlugin import BasePlugin

class Translator(BasePlugin):

    _stage = 'Translation'

    def __init__(self):
        self._allowed_values = []

def main():

    translate = Translator()

if __name__ == '__main__': main()
