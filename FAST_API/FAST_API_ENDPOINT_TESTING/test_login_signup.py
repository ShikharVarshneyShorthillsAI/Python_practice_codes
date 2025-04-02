import requests
import csv
import pytest

# Base URL of your FastAPI app (Adjust if running locally or deployed)
BASE_URL = "http://127.0.0.1:8000"

# CSV File to record test results
CSV_FILE = "test_results.csv"

# Sample test cases
test_cases = [
    {
        "test_case": "Signup - New User",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "testuser1","password": "Test@123"},
        "expected_output": {"result": "Signed up successfully"},
    },
    {
        "test_case": "Signup - Existing User",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "testuser1", "password": "Test@123"},
        "expected_output": {"result": "Username is already taken"},
    },
    {
        "test_case": "Login - Correct Credentials",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "testuser1", "password": "Test@123"},
        "expected_output": {"result": "Login Successful"},
    },
    {
        "test_case": "Login - Wrong Password",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "testuser1", "password": "WrongPassword"},
        "expected_output": {"result": "Password is incorrect"},
    },
    {
        "test_case": "Login - Non-Existent User",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "unknown_user", "password": "Random123"},
        "expected_output": {"result": "Username not found"},
    },
    {
        "test_case": "Signup - Missing Password",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "user1", "email": "user1@example.com"},
        "expected_output": {"result": "Password cannot be empty"},
    },
    {
        "test_case": "Login - SQL Injection Attempt",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "' OR 1=1 --", "password": "password"},
        "expected_output": {"result": "Username not found"},
    },
    {
    "test_case": "Signup - Missing Username",
    "endpoint": "/signup",
    "method": "post",
    "data": {"password": "Test@123"},
    "expected_output": {"result": "Username cannot be empty"},
    },
    {
        "test_case": "Signup - Weak Password",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "user2", "password": "123"},
        "expected_output": {"result": "Password is too weak"},
    },
    {
        "test_case": "Signup - Special Characters in Username",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "user@123", "password": "StrongPass@123"},
        "expected_output": {"result": "Invalid username format"},
    },
    {
        "test_case": "Signup - Long Username",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "a" * 51, "password": "StrongPass@123"},
        "expected_output": {"result": "Username exceeds character limit"},
    },
    {
        "test_case": "Login - Empty Username",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "", "password": "Test@123"},
        "expected_output": {"result": "Username cannot be empty"},
    },
    {
        "test_case": "Login - Empty Password",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "testuser1", "password": ""},
        "expected_output": {"result": "Password cannot be empty"},
    },
    {
        "test_case": "Login - Case Sensitivity Check",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "TestUser1", "password": "Test@123"},
        "expected_output": {"result": "Username not found"},
    },
    {
        "test_case": "Login - Excessively Long Password",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": "testuser1", "password": "A" * 101},
        "expected_output": {"result": "Password exceeds character limit"},
    },
    {
        "test_case": "Login - Username with Leading/Trailing Spaces",
        "endpoint": "/login",
        "method": "get",
        "data": {"name": " testuser1 ", "password": "Test@123"},
        "expected_output": {"result": "Username not found"},
    },
    {
        "test_case": "Signup - SQL Injection in Username",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "'; DROP TABLE users;--", "password": "password123"},
        "expected_output": {"result": "Invalid username format"},
    },
    {
        "test_case": "Signup - HTML Injection in Username",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "<script>alert('Hacked')</script>", "password": "password123"},
        "expected_output": {"result": "Invalid username format"},
    },
    {
        "test_case": "Signup - Duplicate Username with Different Case",
        "endpoint": "/signup",
        "method": "post",
        "data": {"name": "TestUser1", "password": "Test@123"},
        "expected_output": {"result": "Username is already taken"},
    }
    ]


def send_request(method, endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    if method == "post":
        response = requests.post(url, json=data)
    else:
        response = requests.get(url, json=data)
    
    return response.json()  # Get JSON response


@pytest.mark.parametrize("case", test_cases)
def test_api(case):
    # Send request
    actual_output = send_request(case["method"], case["endpoint"], case["data"])

    # Compare expected vs actual output
    status = "Pass" if actual_output == case["expected_output"] else "Fail"

    # Write result to CSV
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            case["test_case"],
            case["data"],
            case["expected_output"],
            actual_output,
            status
        ])

    # Assert test case result
    assert actual_output == case["expected_output"], f"Failed: {case['test_case']}"


# Create CSV file with headers before running tests
def setup_csv():
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test Case", "Input Data", "Expected Output", "Actual Output", "Status"])


# Run setup before tests
setup_csv()
