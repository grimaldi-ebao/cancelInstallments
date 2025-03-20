import mysql.connector
import json

from bokeh.core.property.nullable import Nullable
from panel.layout.float import STATUS
from sqlalchemy.sql.operators import truediv


# Database connection configuration
def connect_database():
    return mysql.connector.connect(
        host="localhost",       # Example: "localhost"
        user="root",       # Database user
        password="12345678",  # User password
        database="ebao_default"   # Database name
    )

# Function to insert data into the database
def save_to_database(document_number, json_data, response, status):
    connection = connect_database()
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO cancel_payment (business_no, request, response, status)
        VALUES (%s, %s, %s, %s)
        """
        values = (document_number, json.dumps(json_data),response,status)
        cursor.execute(query, values)
        connection.commit()
        print("Data successfully inserted!")
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to retrieve data from the database using the document number
def fetch_from_database(business_no):
    connection = connect_database()
    try:
        cursor = connection.cursor(dictionary=True)  # Return results as dictionaries
        query = "SELECT business_no, request, response, status FROM cancel_payment WHERE business_no = %s"
        cursor.execute(query, (business_no,))
        result = cursor.fetchone()
        if result:
            result["request"] = json.loads(result["request"])  # Convert back to JSON
            return result
        else:
            print("No data found for the provided document number.")
            return None
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage
if __name__ == "__main__":
    # Example of inserting data
    document_number = "123456789"
    json_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    response = ""
    statis = True
    save_to_database(document_number, json_data,'',True)

    # Example of fetching data
    result = fetch_from_database('1236789')
    if result:
        print("Retrieved data:", result)
