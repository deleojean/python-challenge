
class BasePlugin:

    def __init__(self):
        self._allowed_values = []

    def collect_metrics(self, **kwargs):
        metrics   = []
        pass_rate = 0

        fail = kwargs['total'] - kwargs['counter']
        pass_rate = (kwargs['counter'] / kwargs['total']) * 100 if kwargs['counter'] > 0 else pass_rate
        metrics.extend([{'name': kwargs['key'], 'passfail': f"{kwargs['counter']}/{fail}", 'rate': f"{round(pass_rate, 2)}%"}])

        return metrics

    def validate_parameters(self, **kwargs):
        if not kwargs['argument'] in kwargs['valid_values']:
            print(f"ERROR [{self._stage}] Allowed '{kwargs['name']}({kwargs['parameter']})' arguments: '{kwargs['valid_values']}'")
            sys.exit(1)

    def translate(self):
        new_dataset = []

def main():

    base = BasePlugin()

if __name__ == '__main__': main()
