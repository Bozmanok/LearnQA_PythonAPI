from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.feature("Проверка ручки по редактированию пользователя")
class TestUserEdit(BaseCase):
    @allure.title("Редактирование только что созданного пользователя")
    def test_edit_just_created_user(self):
        # REGISTER
        register_user = BaseCase.registration_user(self)

        email = register_user["email"]
        password = register_user["password"]
        user_id = register_user["user_id"]

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.title("Редактирование пользователя без авторизации")
    def test_edit_user_not_auth(self):
        new_name = "Changed Name"
        response = MyRequests.put(
            f"/user/2",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

    @allure.title("Редактирование пользователя другим пользователем")
    def test_edit_user_auth_another_user(self):
        # REGISTER FIRST USER
        register_first_user = BaseCase.registration_user(self)

        first_user_id = register_first_user["user_id"]

        # REGISTER SECOND USER
        register_second_user = BaseCase.registration_user(self)

        second_user_email = register_second_user["email"]
        second_user_password = register_second_user["password"]

        # LOGIN
        data = {
            'email': second_user_email,
            'password': second_user_password
        }
        response = MyRequests.post("/user/login", data=data)

        second_user_auth_sid = self.get_cookie(response, "auth_sid")
        second_user_token = self.get_header(response, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)

    @allure.title("Редактирование пользователя с коротким email")
    def test_edit_user_wrong_email(self):
        # REGISTER
        register_user = BaseCase.registration_user(self)

        email = register_user["email"]
        password = register_user["password"]
        user_id = register_user["user_id"]

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = email.replace("@", "")
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response3.content}"

    @allure.title("Редактирование пользователя с длинным email")
    def test_edit_user_short_first_name(self):
        # REGISTER
        register_user = BaseCase.registration_user(self)

        email = register_user["email"]
        password = register_user["password"]
        user_id = register_user["user_id"]

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_first_name = "a"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert eval(response3.content.decode("utf-8"))['error'] == "Too short value for field firstName", \
            f"Unexpected response content {response3.content}"
