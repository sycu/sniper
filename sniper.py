import matchers as matchers_module
import notifiers as notifiers_module
import requests
import yaml

from requests.exceptions import RequestException
from time import sleep


class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    urls = []
    for params in config['urls']:
        encoding = params['encoding'] if 'encoding' in params else config['default_encoding']
        matcher = getattr(matchers_module, params['matcher'])(*params['matcher_params'])
        urls.append((params['name'], params['url'], matcher, encoding))

    notifiers = []
    for params in config['notifiers']:
        notifier = getattr(notifiers_module, params['type'])(*params['params'])
        notifiers.append(notifier)

    headers = {
        'User-Agent': config['user_agent'],
    }

    delay = config['delay']
    stock = {}

    while True:
        for name, url, matcher, encoding in urls:
            try:
                html = requests.get(url, headers=headers)
            except RequestException as e:
                print(e)
                continue

            count = matcher.match(html.content.decode(encoding))

            if url not in stock:
                stock[url] = 0

            if stock[url] != count:
                print(f'{TerminalColors.OKBLUE}!!!!! STOCK CHANGED !!!!!{TerminalColors.ENDC}')
                for notifier in notifiers:
                    notifier.notify(name, url, count, stock[url])

            if count > 0:
                print(f'{TerminalColors.OKGREEN}!!! FOUND {count} results for {name} !!!{TerminalColors.ENDC} {url}')
            else:
                print(f'{TerminalColors.WARNING}No results for {name}{TerminalColors.ENDC}')

            stock[url] = count

        print(f'Cycle finished, waiting {delay} seconds...')
        sleep(delay)


if __name__ == '__main__':
    main()
