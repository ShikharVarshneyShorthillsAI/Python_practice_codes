import multiprocessing
import requests
import random
import csv

BASE_URL = "http://127.0.0.1:8000"
CSV_FILE = "response_time_10.csv"

# Global lock (avoid passing it directly to Pool)
lock = None

def send_login_request(process_id):
    """Sends a login request and writes the response to a CSV file."""
    x = random.randint(0, 9)
    data = {"name": "shikhar", "password": f"shikhar@12{x}"}

    try:
        response = requests.get(BASE_URL + "/login", json=data)
        response_time = response.elapsed.total_seconds()  # Convert to seconds
        status_code = response.status_code

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_json = "Invalid JSON response"

    except requests.RequestException as e:
        response_time = None
        status_code = "Request failed"
        response_json = str(e)

    # Use global lock inside the process
    global lock
    with lock:
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([f"Process-{process_id}", response_time, status_code, response_json])

def setup_csv():
    """Creates the CSV file with headers."""
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Process Name", "Response Time (s)", "Status Code", "Response JSON"])

if __name__ == "__main__":
    multiprocessing.set_start_method("fork", force=True)  # Set method before creating any multiprocessing object

    num_requests = 100
    lock = multiprocessing.Lock()  # Initialize global lock inside main process

    setup_csv()  # Initialize CSV file

    with multiprocessing.Pool(processes=num_requests) as pool:
        pool.map(send_login_request, range(num_requests))  # No lock passed

    print("Load testing completed. Results saved in", CSV_FILE)
