import string
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import allure


@allure.feature("Проверка ручки по регистрации пользователя")
class TestUserRegister(BaseCase):
    fields = [
        ('username'),
        ('password'),
        ('email'),
        ('firstName'),
        ('lastName')
    ]

    @allure.title("Успешная регистрация пользователя")
    def test_create_user_successfully(self):
        data = self.prepare_registration_user()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Регистрация пользователя с чужим email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_user(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.title("Регистрация пользователя с неправильным email")
    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_user(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('field', fields)
    @allure.title(f"Регистрация пользователя без параметра {fields}")
    def test_create_user_without_any_field(self, field):
        data = self.prepare_registration_user()
        del data[field]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", \
            f"Unexpected response content {response.content}"

    @allure.title("Регистрация пользователя с коротким username")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_user()
        data['username'] = 'a'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.title("Регистрация пользователя с длинным username")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_user()

        username = ''.join(random.choices(string.ascii_uppercase, k=251))
        data['username'] = username

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"
