import requests


class TestHomeWorkCookie:
    def test_check_homework_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = response.cookies
        print(cookie)

        assert "HomeWork" in cookie.keys(), "Поле 'HomeWork' отсутствует в cookie"
        assert "hw_value" in cookie.values(), "Значение поля 'HomeWork' не соответствует значению 'hw_value'"
