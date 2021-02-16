import requests

with open('wsgi.py', 'rb') as f:
    r = requests.post('http://localhost:8000', files={'report.xls': f})