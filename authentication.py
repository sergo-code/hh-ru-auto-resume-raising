from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import json
import os
import re


class HHru:
    def __init__(self, phone, proxy, password=None):
        self.url = "https://hh.ru/account/login"
        self.phone = phone
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        self.options_wire = {'proxy': {'https': proxy}}
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options,
                                       seleniumwire_options=self.options_wire)
        self.driver.implicitly_wait(5)

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
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa='mainmenu_myResumes']"))
        ).click()

        resumes = driver.find_elements(By.CSS_SELECTOR, "div[data-qa='resume']")
        resume_dict = dict()
        for resume in resumes:
            title = resume.get_attribute("data-qa-title")
            link = resume.find_element(By.CSS_SELECTOR, "a[data-qa='resume-title-link']").get_attribute("href")
            link = link.split("/")[4].split("?")[0]
            resume_dict[title] = link

        content = driver.find_element(By.CSS_SELECTOR, "meta[name='description']").get_attribute("content")
        city = content.split(".")[0] if content.split(".")[1] == "hh" else "spb"

        anonymous_cookie_url = [self.url, f"https://{city}.hh.ru/account/login"]
        cookie_url = [f'https://{city}.hh.ru/api/fl/idgib-w-hh', f'https://hh.ru/api/fl/idgib-w-hh']

        for request in driver.requests:
            referer = request.headers.get('referer')

            if request.url == cookie_url[0] or request.url == cookie_url[1]:
                if request.response.status_code == 200:
                    if referer != anonymous_cookie_url[0] and referer != anonymous_cookie_url[1]:
                        cookie = request.headers.get('cookie')
                        xsrf = re.search(r"(?<=_xsrf=).+?;", cookie).group()[:-1]
                        hhtoken = re.search(r"(?<=hhtoken=).+?;", cookie).group()[:-1]

                        return dict(xsrf=xsrf, hhtoken=hhtoken, resume=resume_dict,
                                    status=True, message="Данные успешно получены.")
                else:
                    print(request.response.status_code)
        del driver.requests
        return dict(status=False, message="Запрос не найден.")

    def tear_down(self):
        self.driver.quit()


if __name__ == "__main__":
    load_dotenv()
    hh = HHru(os.getenv("phone"), os.getenv("proxy"), os.getenv("password"))
    try:
        hh.auth_with_password()
        data = hh.get_cookie()
        if data["status"]:
            print(json.dumps(data, indent=4))
        else:
            print(json.dumps(data, indent=4))
    finally:
        hh.tear_down()
