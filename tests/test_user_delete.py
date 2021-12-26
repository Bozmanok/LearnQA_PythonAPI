from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.feature("Проверка ручки по удалению пользователя")
class TestUserDelete(BaseCase):
    @allure.title("Удаление тестового пользователя")
    def test_delete_test_user(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    @allure.title("Успешное удаление пользователя")
    def test_delete_user_successfully(self):
        # REGISTER
        register_user = BaseCase.registration_user(self)

        email = register_user["email"]
        password = register_user["password"]
        user_id = register_user["user_id"]

        # LOGIN
        data = {
            'email': email,
            'password': password
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 200)

        # GET
        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response2.content}"

    @allure.title("Удаление пользователя другим пользователем")
    def test_delete_user_by_another_user(self):
        # REGISTER FIRST USER
        register_first_user = BaseCase.registration_user(self)

        first_user_id = register_first_user["user_id"]

        # REGISTER SECOND USER
        register_second_user = BaseCase.registration_user(self)

        second_user_email = register_second_user["email"]
        second_user_password = register_second_user["password"]

        # LOGIN SECOND USER
        data = {
            'email': second_user_email,
            'password': second_user_password
        }
        response1 = MyRequests.post("/user/login", data=data)

        second_user_auth_sid = self.get_cookie(response1, "auth_sid")
        second_user_token = self.get_header(response1, "x-csrf-token")

        # DELETE FIRST USER BY SECOND USER
        response2 = MyRequests.delete(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
