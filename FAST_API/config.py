import urllib.parse

# Encode special characters in password
username = "root"
password = urllib.parse.quote("shikhar@123")  # Encodes "@" correctly
db_name = "assignment3"
host = "localhost"
port = "3306"

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
