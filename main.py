from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv
import os
import re


class HHru:
    def __init__(self, phone, proxy, password=None):
        self.url = "https://hh.ru/account/login"
        self.phone = phone
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        self.options_wire = {'proxy': {'https': proxy}}
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options,
                                       seleniumwire_options=self.options_wire)

    def auth_with_password(self):
        if self.password is not None:
            driver = self.driver
            driver.get(self.url)

            driver.find_element(By.NAME, "login").send_keys(self.phone)
            driver.find_element(By.CSS_SELECTOR, "button[data-qa='expand-login-by-password']").click()
            driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-input-password']").send_keys(self.password)
            driver.find_element(By.CSS_SELECTOR, "button[data-qa='account-login-submit']").click()
        else:
            print("В экземляре не объявлен пароль.")

    def auth_without_password(self):
        driver = self.driver
        driver.get(self.url)

        driver.find_element(By.NAME, "login").send_keys(self.phone)
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='account-signup-submit']").click()
        code = input("Введите код с SMS:")
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='otp-code-input']").send_keys(code)
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='otp-code-submit']").click()

    def get_cookie(self):
        driver = self.driver
        driver.get("https://hh.ru/applicant/resumes")

        for request in driver.requests:
            if request.url == f'https://hh.ru/api/fl/idgib-w-hh':
                if request.response.status_code == 200:
                    cookie = request.headers.get('cookie')
                    xsrf = re.search(r"(?<=_xsrf=)\w+", cookie).group()
                    hhtoken = re.search(r"(?<=hhtoken=)\w+", cookie).group()
                    return dict(xsrf=xsrf, hhtoken=hhtoken, status=True)
                else:
                    print(request.response.status_code)
        del driver.requests
        return dict(status=False)

    def tear_down(self):
        input("Quit browser? [ENTER]")
        self.driver.quit()


def show_info(dictionary):
    for key, value in dictionary.items():
        print(f"{key}: {value}")


load_dotenv()
hh = HHru(os.getenv("phone"), os.getenv("proxy"), os.getenv("password"))
hh.auth_with_password()
data = hh.get_cookie()
if data["status"]:
    show_info(data)
else:
    show_info(data)
hh.tear_down()
