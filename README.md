
Task 1: API Development (Task Management System)

Prerequisites:
1.	Start the Flask Server: Make sure your main.py is running in your terminal.
2.	Open Postman: Launch the Postman application.


Testing Steps:

1. Register a User:
•	Method: Select POST from the HTTP method dropdown.
•	URL: Enter http://127.0.0.1:5000/register in the URL field.
•	Headers:
o	Click the "Headers" tab.
o	In the "Key" column, type Content-Type.
o	In the "Value" column, type application/json.
•	Body:
o	Click the "Body" tab.
o	Select the "raw" radio button.
o	From the dropdown on the right, select "JSON".
o	In the text area, enter the following JSON:
JSON
{
    "username": "testuser1",
    "password": "securepassword"
}
•	Send: Click the "Send" button.
•	Verify:
o	Check the "Status" at the top of the response (it should be 201 Created).
o	Check the "Body" of the response (it should be {"message": "User created successfully"}).

2. Login and Get an Access Token:
•	Method: Select POST.
•	URL: Enter http://127.0.0.1:5000/login.
•	Headers: Set Content-Type to application/json.
•	Body: Enter the following JSON:
JSON
{
    "username": "testuser1",
    "password": "securepassword"
}
•	Send: Click "Send".
•	Verify:
o	Check the "Status" (it should be 200 OK).
o	In the "Body", you'll see {"access_token": "your_jwt_token"}.
o	Important: Copy the entire access_token value (the part inside the quotes). You'll need it for subsequent requests.


3. Create a Task:
•	Method: Select POST.
•	URL: Enter http://127.0.0.1:5000/tasks.
•	Headers:
o	Set Content-Type to application/json.
o	Set Authorization to Bearer your_jwt_token (replace your_jwt_token with the access token you copied).
•	Body: Enter the following JSON:
JSON
{
    "title": "My First Postman Task",
    "description": "Testing the API with Postman."
}
•	Send: Click "Send".
•	Verify:
o	Check the "Status" (201 Created).
o	Check the "Body" ({"message": "Task created successfully"}).


4. Get All Tasks:
•	Method: Select GET.
•	URL: Enter http://127.0.0.1:5000/tasks.
•	Headers: Set Authorization to Bearer your_jwt_token.
•	Send: Click "Send".
•	Verify: 
o	Check the "Status" (200 OK).
o	Check the "Body" (you should see a JSON array of tasks, including the one you just created).

5. Get a Specific Task:
•	Get Task ID: Look at the response from step 4. Find the id of the task you want to get.
•	Method: Select GET.
•	URL: Enter http://127.0.0.1:5000/tasks/{task_id} (replace {task_id} with the actual ID).
•	Headers: Set Authorization to Bearer your_jwt_token.
•	Send: Click "Send".
•	Verify: 
o	Check the "Status" (200 OK).
o	Check the "Body" (you should see the details of the specific task).


6. Update a Task:
•	Method: Select PUT.
•	URL: Enter http://127.0.0.1:5000/tasks/{task_id} (use the same task_id as in step 5).
•	Headers:
o	Set Content-Type to application/json.
o	Set Authorization to Bearer your_jwt_token.
•	Body: Enter the following JSON:
JSON
{
    "title": "Updated Task Title",
    "status": "completed"
}
•	Send: Click "Send".
•	Verify:
o	Check the "Status" (200 OK).
o	Check the "Body" ({"message": "Task updated successfully"}).


7. Delete a Task:
•	 Method: Select DELETE.
•	 URL: Enter http://127.0.0.1:5000/tasks/{task_id} (use the same task_id).
•	Headers: Set Authorization to Bearer your_jwt_token.
•	 Send: Click "Send".
•	 Verify: 
o	Check the "Status" (200 OK).
o	Check the "Body" ({"message": "Task deleted successfully"}).


8. Get Tasks with Pagination: 
•	Method: GET
•	URL: http://127.0.0.1:5000/tasks?page=2&per_page=5 (or any combination of page and per_page)
•	Headers: Include your Authorization header with the JWT token.
•	Send: Click "Send".


######################################################---- Task- 2 ##################################################

Task 2: Data Processing (Large CSV File Handling)


Overall Purpose:

This script is designed to automate the process of extracting, transforming, and loading (ETL) data from a local CSV file into a PostgreSQL database. It emphasizes production readiness through robust error handling, efficient processing, and persistent logging.

Key Theoretical Concepts:

1. ETL (Extract, Transform, Load):

Extract: The script extracts data from a CSV file.
Transform: It cleans and transforms the data (numeric conversions, boolean conversions, null handling, data validation).
Load: It loads the transformed data into a PostgreSQL database.

2. Chunking for Memory Management:

The script processes the CSV file in chunks. This is a crucial strategy for handling large datasets that might exceed the available RAM. By processing data in smaller, manageable portions, the script avoids memory overload and ensures it can handle very large files.

3. Data Transformation and Cleaning Principles:

The script applies a series of transformations to ensure data quality and consistency.
Data Type Enforcement: It enforces correct data types for numeric and boolean columns. This is essential for accurate analysis and database operations.
Null Value Handling: It addresses missing data by filling null values with appropriate defaults or removing incomplete records. This prevents errors and ensures data completeness.
Data Validation: The script performs basic data validation by removing rows with critical missing information.
These transformations are vital for producing reliable and consistent data.

4. Relational Database Integration (SQLAlchemy):

The script uses SQLAlchemy, an ORM (Object-Relational Mapper), to interact with the PostgreSQL database.
ORM Abstraction: SQLAlchemy abstracts away the complexities of direct SQL queries, allowing the script to interact with the database using Python objects and methods.
Schema Definition: The script defines the database table schema programmatically, ensuring that the database structure matches the data being loaded.
Database Sessions and Transactions: SQLAlchemy's session management ensures that database operations are performed within transactions. This guarantees data integrity by ensuring that either all operations within a transaction succeed or none do.

5. Production-Level Logging:

The script uses the Python logging module to record events and errors.
File-Based Logging: Logs are written to a file, providing a persistent record of the script's execution. This is essential for monitoring and debugging in production environments.
Detailed Logging: The script logs various events, including data processing progress, errors, and exceptions. This provides valuable insights for troubleshooting and performance analysis.

6. Exception Logging: The use of logging.exception to log full stack traces is very important.

7. Error Handling and Robustness:

The script incorporates robust error handling using try-except blocks.
File Existence Check: It verifies that the input CSV file exists before attempting to process it.
Data Transformation Error Handling: It handles potential errors during data transformation, such as missing columns or invalid data types.
Database Error Handling: It handles potential errors during database operations, such as connection issues or data insertion failures.

8. Transaction Rollback: If a database error occurs, the script rolls back the transaction, preventing partial data writes.

9. Performance Considerations:
Chunking: The use of pandas chunking is the largest performance consideration.
SQLAlchemy Efficiency: SQLAlchemy provides efficient mechanisms for database interaction.
Data Type Optimization: Choosing appropriate data types for database columns optimizes storage and query performance.

Technology Choices:
•	Pandas: Chosen for its powerful data manipulation capabilities and efficiency in handling tabular data.
•	SQLAlchemy: Selected for its flexibility, performance, and robust database interaction features.
•	Python 3.8+: The chosen Python version provides access to modern language features and libraries.



#####  Key parts to change for your PostgreSQL setup:

db_uri:

1. Replace "postgresql://user:password@host:port/database" with your actual PostgreSQL connection string.
   Example: "postgresql://myuser:mypassword@localhost:5432/mydatabase"
2. Make sure you have the psycopg2-binary package installed: pip install psycopg2-binary
3. Database Credentials:   Ensure that the user, password, host, port, and database name in the db_uri are correct.
                    The user must have the necessary permissions to create tables and insert data into the database.
4.Database Existence:The database that you are connecting to must already exist. This code will not create a database. It will only create the table within the database.

How to run:

1. Install psycopg2-binary: pip install psycopg2-binary
2. Update db_uri: Modify the db_uri in the script with your PostgreSQL connection details.
3. Run the script: python Task_2.py
4. Verify the data: Use a PostgreSQL client (e.g., psql, pgAdmin) to check the processed_data table in your database.


