import pandas as pd
import requests

df = pd.read_csv('demo.csv')

api_key = 'changethis'
api_endpoint = 'https://api.touchbase.report/api/report/'

r = requests.post(api_endpoint, json={
        'table': df.to_json(orient='records'),
        'report_path': ['Demo'],
        'report_name': 'Demo',
        'id_headers': ['Order'],
        'api_key': api_key
    })
print('Status: ' + str(r.status_code) + ', response: ' + str(r.text))
