from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.data_generator import data_generator


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed_name"

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
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrongname of the user after edit"
        )

    def test_edit_user_not_authorized(self):
        # EDIT
        new_name = "Ivan"

        response = MyRequests.put(
            f"/user/2",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "Auth token not supplied", f"Unexpected response content {response.content}"

    def test_edit_another_user(self):
        # NEW USER 1
        reg_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=reg_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

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

        # EDIT USER 1
        new_name = "Ivan"

        response4 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response4, 200)

    def test_edit_wrong_email(self):
        # NEW USER
        reg_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN USER
        login_data = {
            'email': reg_data['email'],
            'password': reg_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        # EDIT EMAIL USER
        new_name = "Ivan"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": data_generator.prepare_bad_email()}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == "Invalid email format", f"Unexpected response content {response3.content}"

    def test_edit_short_firstname(self):
        # NEW USER
        reg_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN USER
        login_data = {
            'email': reg_data['email'],
            'password': reg_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        # EDIT FIRSTNAME
        new_name = "Ivan"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": data_generator.generate_random_string(1)}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            f"Unexpected response content {response3.content}"
        )
