from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import time


class TestUserDelete(BaseCase):
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

    def test_delete_user(self):
        # NEW USER
        reg_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = reg_data['email']
        password = reg_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN USER
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE USER
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response3, 200)
        time.sleep(3)

        # GET USER
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode(
            "utf-8") == "User not found", f"Unexpected response content {response4.content}"

    def test_delete_another_user(self):
        # NEW USER 1
        reg_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=reg_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        username = reg_data1['username']

        # NEW USER 2
        reg_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=reg_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        # LOGIN USER 2
        login_data = {
            'email': reg_data2['email'],
            'password': reg_data2['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE USER 1
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response3, 200)
        # GET USER
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
