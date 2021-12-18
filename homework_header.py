import requests


class TestHomeWorkHeader:
    def test_check_homework_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        header = response.headers
        print(header)

        assert "x-secret-homework-header" in header.keys(), "Поле 'x-secret-homework-header' отсутствует в headers"
        assert "Some secret value" in header.values(), \
            "Значение поля 'x-secret-homework-header' не соответствует значению 'Some secret value'"
