import os
import pickle
import requests
from bs4 import BeautifulSoup
import sys
from credentials import creds

# email = 'jaqsoms43@gmail.com'
# password = 'dwedu229!@!$7238hd'
db = "temp"
collection_profile = "profile_data"
collection_search = "profile_search"
port = 27017
host = "localhost"


# waring : dont touch the code
class Login:

    def __init__(self):
        self.proxy = self._get_proxy()

    def _get_proxy(self):

        url = "http://credsnproxy/api/v1/proxy"
        try:
            creds = requests.get(url=url).json()

        except:
            return {"proxy_host": '5.39.20.153',
                    "proxy_port": '25567'}


    def loginmethod(self):
        try:
            if os.path.isfile('login.pickle'):
                with open('login.pickle', 'rb') as handle:
                    self.client = pickle.load(handle)
            else:
                self.client = requests.Session()

                HOMEPAGE_URL = 'https://www.linkedin.com'
                LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'

                html = self.client.get(HOMEPAGE_URL, proxies={"http": "//socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']}).content
                soup = BeautifulSoup(html, "html.parser")
                csrf = soup.find(id="loginCsrfParam-login")['value']
                login_information = {
                    'session_key': creds['email'],
                    'session_password': creds['password'],
                    'loginCsrfParam': csrf,
                }

                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                }

                self.client.post(LOGIN_URL, headers=headers, data=login_information)
                print(self.client)
                with open('login.pickle', 'wb') as handle:
                    pickle.dump(self.client, handle, protocol=pickle.HIGHEST_PROTOCOL)

        except:
            print("error>>loginmethod::", sys.exc_info()[1])


if __name__ == '__main__':
    obj = Login()
    obj.loginmethod()
