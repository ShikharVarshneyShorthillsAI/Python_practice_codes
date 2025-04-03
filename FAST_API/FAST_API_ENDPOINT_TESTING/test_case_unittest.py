import unittest
import requests
import csv

# Base URL of your FastAPI app (Adjust if running locally or deployed)
BASE_URL = "http://127.0.0.1:8000"

# CSV File to record test results
CSV_FILE = "test_results.csv"


def send_request(method, endpoint, data):
    """Send a request to the API and return the JSON response."""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "post":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url, json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def write_to_csv(test_case, data, expected_output, actual_output, status):
    """Write test case results to a CSV file."""
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([test_case, data, expected_output, actual_output, status])


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup CSV file before running tests."""
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Test Case", "Input Data", "Expected Output", "Actual Output", "Status"])

    def run_test_case(self, test_case, endpoint, method, data, expected_output):
        """General function to run a test case."""
        actual_output = send_request(method, endpoint, data)
        status = "Pass" if actual_output == expected_output else "Fail"
        write_to_csv(test_case, data, expected_output, actual_output, status)
        self.assertEqual(actual_output, expected_output, f"Failed: {test_case}")

    def test_signup_new_user(self):
        self.run_test_case(
            "Signup - New User",
            "/signup",
            "post",
            {"name": "testuser1", "password": "Test@123"},
            {"result": "Signed up successfully"},
        )

    def test_signup_existing_user(self):
        self.run_test_case(
            "Signup - Existing User",
            "/signup",
            "post",
            {"name": "testuser1", "password": "Test@123"},
            {"result": "Username is already taken"},
        )

    def test_login_correct_credentials(self):
        self.run_test_case(
            "Login - Correct Credentials",
            "/login",
            "get",
            {"name": "testuser1", "password": "Test@123"},
            {"result": "Login Successful"},
        )

    def test_login_wrong_password(self):
        self.run_test_case(
            "Login - Wrong Password",
            "/login",
            "get",
            {"name": "testuser1", "password": "WrongPassword"},
            {"result": "Password is incorrect"},
        )

    def test_login_non_existent_user(self):
        self.run_test_case(
            "Login - Non-Existent User",
            "/login",
            "get",
            {"name": "unknown_user", "password": "Random123"},
            {"result": "Username not found"},
        )

    def test_signup_missing_password(self):
        self.run_test_case(
            "Signup - Missing Password",
            "/signup",
            "post",
            {"name": "user1", "email": "user1@example.com"},
            {"result": "Password cannot be empty"},
        )

    def test_login_sql_injection_attempt(self):
        self.run_test_case(
            "Login - SQL Injection Attempt",
            "/login",
            "get",
            {"name": "' OR 1=1 --", "password": "password"},
            {"result": "Username not found"},
        )

    def test_signup_missing_username(self):
        self.run_test_case(
            "Signup - Missing Username",
            "/signup",
            "post",
            {"password": "Test@123"},
            {"result": "Username cannot be empty"},
        )

    def test_signup_weak_password(self):
        self.run_test_case(
            "Signup - Weak Password",
            "/signup",
            "post",
            {"name": "user2", "password": "123"},
            {"result": "Password is too weak"},
        )

    def test_signup_special_characters_in_username(self):
        self.run_test_case(
            "Signup - Special Characters in Username",
            "/signup",
            "post",
            {"name": "user@123", "password": "StrongPass@123"},
            {"result": "Invalid username format"},
        )

    def test_signup_long_username(self):
        self.run_test_case(
            "Signup - Long Username",
            "/signup",
            "post",
            {"name": "a" * 51, "password": "StrongPass@123"},
            {"result": "Username exceeds character limit"},
        )

    def test_login_empty_username(self):
        self.run_test_case(
            "Login - Empty Username",
            "/login",
            "get",
            {"name": "", "password": "Test@123"},
            {"result": "Username cannot be empty"},
        )

    def test_login_empty_password(self):
        self.run_test_case(
            "Login - Empty Password",
            "/login",
            "get",
            {"name": "testuser1", "password": ""},
            {"result": "Password cannot be empty"},
        )

    def test_login_case_sensitivity_check(self):
        self.run_test_case(
            "Login - Case Sensitivity Check",
            "/login",
            "get",
            {"name": "TestUser1", "password": "Test@123"},
            {"result": "Username not found"},
        )

    def test_login_excessively_long_password(self):
        self.run_test_case(
            "Login - Excessively Long Password",
            "/login",
            "get",
            {"name": "testuser1", "password": "A" * 101},
            {"result": "Password exceeds character limit"},
        )

    def test_login_username_with_spaces(self):
        self.run_test_case(
            "Login - Username with Leading/Trailing Spaces",
            "/login",
            "get",
            {"name": " testuser1 ", "password": "Test@123"},
            {"result": "Username not found"},
        )

    def test_signup_sql_injection_in_username(self):
        self.run_test_case(
            "Signup - SQL Injection in Username",
            "/signup",
            "post",
            {"name": "'; DROP TABLE users;--", "password": "password123"},
            {"result": "Invalid username format"},
        )

    def test_signup_html_injection_in_username(self):
        self.run_test_case(
            "Signup - HTML Injection in Username",
            "/signup",
            "post",
            {"name": "<script>alert('Hacked')</script>", "password": "password123"},
            {"result": "Invalid username format"},
        )

    def test_signup_duplicate_username_different_case(self):
        self.run_test_case(
            "Signup - Duplicate Username with Different Case",
            "/signup",
            "post",
            {"name": "TestUser1", "password": "Test@123"},
            {"result": "Username is already taken"},
        )


if __name__ == "__main__":
    unittest.main()
