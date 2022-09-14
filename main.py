from authentication import HHru
from raise_resume import request_raise_resume
from status_code import status

import json
import os
from dotenv import load_dotenv

load_dotenv()
hh = HHru(os.getenv("phone"), os.getenv("proxy"), os.getenv("password"))
try:
    hh.auth_with_password()
    data = hh.get_cookie()
    if data["status"]:
        print(json.dumps(data, indent=4))
        code = request_raise_resume(data["hhtoken"], data["xsrf"], data["resume"]["QA Engineer"], {"http": os.getenv("proxy")})
        print(status(code))
    else:
        print(json.dumps(data, indent=4))
finally:
    hh.tear_down()
