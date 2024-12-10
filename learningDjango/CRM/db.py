import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the values from the environment
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Connect to MySQL using credentials from the .env file
database = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_password
)

# Create a cursor object
cursorObject = database.cursor()

# Create the database
cursorObject.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

print("Database Created Successfully")
