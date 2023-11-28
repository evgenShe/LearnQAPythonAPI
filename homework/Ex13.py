import requests

from lib.assertions import Assertions
import pytest


class TestUserAgent:
    exclude_params = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) '
         'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
         'CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
         'Version/13.0.3 Mobile/15E148 Safari/604.1')
    ]

    @pytest.mark.parametrize("condition", exclude_params)
    def test_user_agent(self, condition):
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": condition}
        )
        platform = response.json()["platform"]
        browser = response.json()["browser"]
        device = response.json()["device"]
        print(platform)

        if condition == ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) '
                         'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'):
            Assertions.assert_json_value_by_name(
                response,
                "platform",
                'Mobile',
                f"User agent fail platform {platform}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'browser',
                'No',
                f"User agent fail browser {browser}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'device',
                'Android',
                f"User agent fail device {device}"
            )
        elif condition == ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                           'CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'):
            Assertions.assert_json_value_by_name(
                response,
                "platform",
                'Mobile',
                f"User agent fail platform {platform}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'browser',
                'Chrome',
                f"User agent fail browser {browser}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'device',
                'iOS',
                f"User agent fail device {device}"
            )
        elif condition == ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'):
            Assertions.assert_json_value_by_name(
                response,
                "platform",
                'Googlebot',
                f"User agent fail platform {platform}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'browser',
                'Unknown',
                f"User agent fail browser {browser}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'device',
                'Unknown',
                f"User agent fail device {device}"
            )
        elif condition == ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'):
            Assertions.assert_json_value_by_name(
                response,
                "platform",
                'Web',
                f"User agent fail platform {platform}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'browser',
                'Chrome',
                f"User agent fail browser {browser}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'device',
                'No',
                f"User agent fail device {device}"
            )
        elif condition == ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                           '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'):
            Assertions.assert_json_value_by_name(
                response,
                "platform",
                'Mobile',
                f"User agent fail platform {platform}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'browser',
                'No',
                f"User agent fail browser {browser}"
            )
            Assertions.assert_json_value_by_name(
                response,
                'device',
                'iPhone',
                f"User agent fail device {device}"
            )
