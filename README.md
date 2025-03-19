
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
•	URL: http://127.0.0.1:8010/tasks?page=2&per_page=5 (or any combination of page and per_page)
•	Headers: Include your Authorization header with the JWT token.
•	Send: Click "Send".


######################################################---- Task- 2 ##################################################

Task 2: Data Processing (Large CSV File Handling)


Overview:
This Python script is designed to perform robust and efficient data processing of a large CSV file, transforming the data according to business requirements, and persisting the results into a relational database. It's built with production-level considerations, focusing on stability, performance, and maintainability.

Core Functionality:

1.	Data Ingestion and Chunking:
o	The script reads the CSV file in manageable chunks using Pandas, which is crucial for handling large datasets that exceed available memory. This chunking strategy prevents memory overload and ensures the script can process substantial amounts of data.

2.	Data Transformation and Cleaning:
o	The core of the script lies in its data transformation logic. It handles several critical tasks: 
	Data Type Conversion: It ensures that numeric columns are correctly converted to numeric types, handling potential errors and inconsistencies.
	Boolean Conversion: It correctly converts a column into boolean values.
	Null Value Handling: It addresses missing or null values by filling them with appropriate defaults or removing rows with critical missing information.
	Data Validation: It performs basic data validation by removing rows that do not contain critical data.
o	This step is essential for ensuring data quality and consistency before it's stored in the database.

3.	Database Persistence:
o	The script utilizes SQLAlchemy, a powerful Python SQL toolkit and ORM, to interact with the database.
o	It dynamically creates the database table schema based on the CSV file's structure, ensuring flexibility and adaptability.
o	The transformed data is then efficiently inserted into the database in chunks, leveraging SQLAlchemy's capabilities for optimized database operations.
o	The use of a primary key ensures data integrity.
o	The use of database sessions and transactions ensures that database operations are atomic, preventing partial data writes in case of errors.

4.	Error Handling and Logging:
o	Robust error handling is implemented throughout the script, using try-except blocks to catch and manage potential exceptions.
o	Comprehensive logging is employed to record events, errors, and performance metrics, providing valuable insights for monitoring and debugging.
o	Logging to a file ensures that information is preserved even after the script finishes execution.
o	The use of logging.exception ensures that full stack traces are captured, greatly aiding in debugging.


5.	Performance Optimization:
o	Chunking is the primary performance optimization technique, allowing the script to handle large datasets efficiently.
o	Pandas' vectorized operations are used for data transformation, leveraging the library's optimized data processing capabilities.
o	Database operations are optimized through the use of sqlalchemy.


6.	Production Readiness:
o	The script is designed with production considerations in mind, including: 
	File-based logging for persistent records.
	Robust error handling and logging for debugging.
	Clear and concise code for maintainability.
	Input file validation.

Technology Choices:
•	Pandas: Chosen for its powerful data manipulation capabilities and efficiency in handling tabular data.
•	SQLAlchemy: Selected for its flexibility, performance, and robust database interaction features.
•	Python 3.8+: The chosen Python version provides access to modern language features and libraries.


