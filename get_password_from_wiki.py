import requests
from lxml import html


def get_passwords_from_wiki():
    response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

    tree = html.fromstring(response.text)

    locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
    passwords = tree.xpath(locator)

    list_passwords = []
    for password in passwords:
        password = str(password).strip()
        list_passwords.append(password)

    return list_passwords
