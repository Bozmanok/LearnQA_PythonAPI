from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_user()

        repsonse = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(repsonse, 200)
        Assertions.assert_json_has_key(repsonse, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_user(email)

        repsonse = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(repsonse, 400)
        assert repsonse.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {repsonse.content}"
