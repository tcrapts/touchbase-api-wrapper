import pandas as pd
import requests
import os
from dotenv import load_dotenv
load_dotenv()

df = pd.read_csv('demo.csv')

endpoint = 'http://api.touchbase.report/api/report/'
access_key_id = os.getenv('ACCESS_KEY_ID')
access_key = os.getenv('ACCESS_KEY')
payload = {
    'id_headers': [],
    'table':df.to_json(orient='records'),
    'report_path': ['Demo'],
    'report_name': 'Demo'
}
headers = {'access_key_id': access_key_id, 'access_key': access_key}
r = requests.post(endpoint, json=payload, headers=headers)
print('Report pushed to Touchbase with status: ' + str(r.status_code) + '; ' + str(r.text))

