import os
from dotenv import load_dotenv
import requests

load_dotenv()

hhtoken = os.getenv("hhtoken")
_xsrf = os.getenv("_xsrf")
resume = os.getenv("resume")

boundary = "boundary"
url = "https://spb.hh.ru/applicant/resumes/touch"
headers = {
    'content-type': f'multipart/form-data; boundary={boundary}',
    'cookie': f'_xsrf={_xsrf}; hhtoken={hhtoken};',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36',
    'x-xsrftoken': f'{_xsrf}',
}

data = f'--{boundary}\r\nContent-Disposition: form-data; name="resume"\r\n\r\n{resume}\r\n--{boundary}\r\n' \
                       f'Content-Disposition: form-data; name="undirectable"\r\n\r\ntrue\r\n--{boundary}--\r\n'

response = requests.post(url=url, headers=headers, data=data)

assert response.status_code == 200, response.status_code
