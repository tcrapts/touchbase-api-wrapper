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
        'foreign_key_headers': ['Product Number']
    },   
    {
        'path': 'files/sales_orders.xlsx',
        'report_name': 'Sales orders',
        'report_path': ['Sales'],
        'id_headers': ['Sales Order']
    },         
    {
        'path': 'files/sales_order_lines.xlsx',
        'report_name': 'Sales order lines',
        'report_path': ['Sales'],
        'id_headers': ['Sales Order', 'Sales Order Line'],
        'foreign_key_headers': ['Sales Order', 'Product Number']
    },
    {
        'path': 'files/suppliers.xlsx',
        'report_name': 'Suppliers',
        'report_path': ['Purchasing'],
        'id_headers': ['Supplier'],
    },    

]

tb_env = 'prd'
api = {
    'prd': {
        'endpoint': 'http://api.touchbase.report/api/report/',
        'access_key_id': os.getenv('ACCESS_KEY_ID'),
        'access_key': os.getenv('ACCESS_KEY')
    },
    'local': {
        'endpoint': 'http://localhost:3030/api/report/',
        'access_key_id': os.getenv('ACCESS_KEY_ID_LOCAL'),
        'access_key': os.getenv('ACCESS_KEY_LOCAL')
    }  
}

def push_report(payload: dict):
    headers = {'access_key_id': api[tb_env]['access_key_id'], 'access_key': api[tb_env]['access_key']}
    r = requests.post(api[tb_env]['endpoint'], json=payload, headers=headers)
    return r

def excel_to_df(path: str):
    df = pd.read_excel(path, engine='openpyxl', parse_dates=False)
    date_cols = df.select_dtypes(include=[np.datetime64])
    for col in date_cols:
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    return df

def push_files(files: list, foreign_key_headers_override: list = None):    
    for file in files:
        df = excel_to_df(path=file['path'])
        if foreign_key_headers_override is not None:
            foreign_key_headers = foreign_key_headers_override
        else:
            foreign_key_headers = file.get('foreign_key_headers')

        payload = {
            'id_headers': file['id_headers'],
            'table':df.to_json(orient='records'),
            'report_path': file['report_path'],
            'report_name': file['report_name'],
            'foreign_key_headers': foreign_key_headers 
        }
        r = push_report(payload=payload)
        print(f"Report \"{file['report_name']}\" pushed to Touchbase with status = {str(r.status_code)}; {str(r.text)}")
        print('**')        

push_standard = False
push_supplier = True

# Push all files without supplier
if push_standard:
    push_files(files = [f for f in files if f['path'] != 'files/suppliers.xlsx'])

# Also push suppliers
if push_supplier:
    push_files(files = [f for f in files if f['path'] == 'files/suppliers.xlsx'])
    push_files(files = [f for f in files if f['path'] == 'files/purchase_order_lines.xlsx'], foreign_key_headers_override=['Product Number','Supplier'])
    

