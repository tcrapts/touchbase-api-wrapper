import pandas as pd
import requests
import os
from dotenv import load_dotenv
import numpy as np
load_dotenv()

files = [
    {
        'path': 'files/products.xlsx',
        'report_name': 'Products',
        'report_path': ['Products'],
        'id_headers': ['Product Number']
    },
    {
        'path': 'files/purchase_order_lines.xlsx',
        'report_name': 'Purchase order lines',
        'report_path': ['Purchasing'],
        'id_headers': ['Purchase Order','Purchase Order Line'],
        'foreign_key_headers': [['Product Number']]
    },   
    {
        'path': 'files/sales_orders.xlsx',
        'report_name': 'Sales orders',
        'report_path': ['Sales'],
        'id_headers': ['Sales Order'],
        'foreign_key_headers': [['Product Number']]
    },         
    {
        'path': 'files/sales_order_lines.xlsx',
        'report_name': 'Sales order lines',
        'report_path': ['Sales'],
        'id_headers': ['Sales Order', 'Sales Order Line'],
        'foreign_key_headers': [['Sales Order'], ['Product Number']]
    },             
]


endpoint = 'http://api.touchbase.report/api/report/'
access_key_id = os.getenv('ACCESS_KEY_ID')
access_key = os.getenv('ACCESS_KEY')

for file in files:
    df = pd.read_excel(file['path'], engine='openpyxl', parse_dates=False)
    date_cols = df.select_dtypes(include=[np.datetime64])
    for col in date_cols:
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    payload = {
        'id_headers': file['id_headers'],
        'table':df.to_json(orient='records'),
        'report_path': file['report_path'],
        'report_name': file['report_name'],
        'foreign_key_headers': file.get('foreign_key_headers')
    }
    headers = {'access_key_id': access_key_id, 'access_key': access_key}
    r = requests.post(endpoint, json=payload, headers=headers)
    print('Report pushed to Touchbase with status: ' + str(r.status_code) + '; ' + str(r.text))