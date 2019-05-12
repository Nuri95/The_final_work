import pprint
import sys

import requests
import click


def make_request(**params):
    params = {key: value for key, value in params.items() if value is not None}
    try:
        response = requests.get('https://newsapi.org/v2/top-headlines', params=params)
#        pprint.pprint('responseJSON= ', response.json())

        for article in response.json()['articles']:

            print('title: ', article['title'])
            print('publishedAt: ', article['publishedAt'])
            print('url: ', article['url'])
    except ConnectionError as c:
        print(str(c))
    except ValueError as v:
        print(str(v))
    except AttributeError as a:
        print(str(a))


@click.command()
@click.option('--pagesize',
              '-ps',
              help='The number of results to return per page.')
@click.option('--page',
              '-p',
              help='Page number')
@click.option('--category',
              '-сtg',
              help='Possible options: business entertainment general health science sports technology')
@click.option('--country',
              '-с',
              help='The 2-letter ISO 3166-1 code of the country you want to get headlines for.')
@click.option('--keyword',
              '-k',
              help='Keywords or a phrase to search for. ')
def main(pagesize, page, category, country, keyword):
    try:
        with open('apiKey.txt', 'r') as fobj:
            key = fobj.read()
    except OSError:
        print('Ошибки с файлом')
        exit()
    make_request(category=category,
                 q=keyword,
                 country=country,
                 pageSize=pagesize,
                 page=page,
                 apiKey=key
                 )


if __name__ == '__main__':
    main()