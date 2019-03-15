from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
from config import Config


from time import sleep


class LinkedinId:

    def _get_proxy(self):

        url = "http://credsnproxy/api/v1/proxy"
        try:
            creds = requests.get(url=url).json()
            return creds

        except:
            return {"proxy_host": '185.141.25.178',
                    "proxy_port": '22866'}

    def __init__(self):

        self.cred = self._get_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        # options.add_argument('--proxy-server=socks://' + self.cred['proxy_host'] + ':' + self.cred['proxy_port'])


        # self.driver = webdriver.Chrome(chrome_options=options)

        # remote webdriver
        self.driver = webdriver.Remote(
            command_executor='http://'+Config.SELENIUM_CONFIG['host']+':'+Config.SELENIUM_CONFIG['port']+'/wd/hub',
            desired_capabilities=options.to_capabilities(),
        )
        self.EMAILFIELD = (By.ID, "username")
        self.PASSWORDFIELD = (By.ID, "password")

    def id_check(self, id):

        # url = 'https://www.linkedin.com/uas/request-password-reset?session_redirect=&trk=uas-login-forgot-password-text'
        url = 'https://www.linkedin.com/uas/login'
        self.driver.get(url)
        sleep(0.1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EMAILFIELD)).send_keys(id)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PASSWORDFIELD)).send_keys('efknjkn@309')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PASSWORDFIELD)).send_keys(Keys.ENTER)

        sleep(0.1)
        # try:
        # pass_ = self.driver.find_element_by_id('session_password-login-error')
        pass_ = self.driver.find_element_by_id('error-for-password')
        txt = pass_.text
        # pwd = self.driver.find_element_by_xpath('//*[@id="session_key-login-error"]')
        pwd = self.driver.find_element_by_xpath('//*[@id="error-for-username"]')
        txt2 = pwd.text
        if txt.startswith("Hmm, that's not the right password"):
            self.driver.quit()
            return {'profileExists': True,
                    'profile': id}

        elif txt2.startswith("We don't recognize that email."):
            self.driver.quit()
            return {'profileExists': False,
                    'profile': id}

        elif txt2.startswith("Hmm, we don't recognize that email."):
            self.driver.quit()
            return {'profileExists': False,
                    'profile': id}


if __name__ == '__main__':
    obj = LinkedinId()
    print(obj.id_check('quality.slip2016@ydex.com'))


# pparkar549@gmail.com
# jaqsoms43@gmail.com
