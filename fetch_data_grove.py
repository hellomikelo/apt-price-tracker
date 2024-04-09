from email import header
import pandas as pd
import datetime
import json
import requests


def send_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    return response


def process_response(response):
    # Check if the request was successful
    if response.status_code == 200:
        # Request was successful
        print('Got a response!')
        df = pd.DataFrame(response.json()['data']['units'])
        df = df[['unit_number', 'area', 'price', 'available_on', 'display_lease_term']]
        df['display_lease_term'] = df['display_lease_term'].str.replace(r'[a-zA-Z\s]', '', regex=True).astype(int)
        # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # df['insert_time'] = current_time
        df.head()
    else:
        # Request failed
        print('Request failed with status:', response.status_code, response.reason)
    return df


def save_json(df):
    df.to_json('newest_prices_grove.json', orient='records')
    print('Done saving JSON.')

def save_csv(df):
    df.to_csv('newest_prices_grove.csv', header=True, index=False)
    print('Done saving CSV.')


if __name__ == '__main__':
    # API URL
    URL = 'https://sightmap.com/app/api/v1/4yjp202rwxl/sightmaps/2398'
    response = send_request(URL)
    df = process_response(response)
    save_csv(df)