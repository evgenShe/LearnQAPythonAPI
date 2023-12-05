from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import time
import allure


@allure.epic("User DELETE method cases")
class TestUserDelete(BaseCase):
    @allure.description("This test delete existing user vinkotov@example.com")
    def test_delete_existing_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    @allure.description("This test create, login and delete existing user")
    def test_delete_user(self):
        with allure.step("Create new user"):
            reg_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=reg_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = reg_data['email']
            password = reg_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login new user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Delete new user"):
            response3 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_code_status(response3, 200)
            time.sleep(3)

        with allure.step("Get user"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})
            Assertions.assert_code_status(response4, 404)
            assert response4.content.decode(
                "utf-8") == "User not found", f"Unexpected response content {response4.content}"

    @allure.description("This test delete another user")
    def test_delete_another_user(self):
        with allure.step("Create new user 1"):
            reg_data1 = self.prepare_registration_data()
            response1 = MyRequests.post("/user", data=reg_data1)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")
            username = reg_data1['username']

        with allure.step("Create new user 2"):
            reg_data2 = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=reg_data2)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

        with allure.step("Login user 2"):
            login_data = {
                'email': reg_data2['email'],
                'password': reg_data2['password']
            }
            response3 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        with allure.step("Delete user 1"):
            response3 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_code_status(response3, 200)

        with allure.step("Get user"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response4, 200)
            Assertions.assert_json_has_key(response4, "username")
            Assertions.assert_json_value_by_name(
                response4,
                "username",
                username,
                f"Unexpected response content {response3.content}"
            )
