FJ Kanban Web Application

The FJ Kanban Web Application is designed to streamline the process of submitting manufacturing data using Kanban principles.
It provides a simple user interface for inputting details such as wood species, size, dimensions, machine ID, and trolley number.
The application then generates a PDF document containing the submitted data along with QR code and barcode images for easy tracking and identification.


Setting up of ERPNext:

1. Enable API Access:
	- Log in to your ERPNext instance as an administrator.
	- Go to Settings > API and Integrations.
	- Enable API access if it's not already enabled.

2. Create an API Key:
	- Navigate to Settings > API and Integrations > API Access.
	- Create a new API Key with the necessary permissions to access the resources required by your Python script.

3. Configure Permissions:
	- Ensure that the user associated with the API Key has adequate permissions to access the resources
	  and perform the required actions (e.g., read, write, create, delete) on the FJ Kanban resource.

4. Get the API URL:
	- Determine the URL endpoint for accessing the FJ Kanban resource. This typically follows the format http://<your_erpnext_instance>/api/resource/FJ%20Kanban.

5. Update the Python Script:
	- Modify the get_from_erpnext() function in your Python script to use the correct API URL, headers, and authentication token:
---------------------------------------------------------------------------------------------------
import requests

def get_from_erpnext():
    url = 'http://<your_erpnext_instance>/api/resource/FJ%20Kanban?order_by=running_number%20desc'
    headers = {
        "Authorization": "Token <your_api_token>",
        "Content-Type": "application/json"
    }

    # Make a GET request to fetch data from ERPNext
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print('Data retrieved from ERPNext successfully')
        data = response.json()  # Convert response to JSON format
        return data
    else:
        print('Failed to retrieve data from ERPNext')
        print(f'Status code: {response.status_code}')
        print(f'Response text: {response.text}')
        return None
---------------------------------------------------------------------------------------------------

How to Use:

1. Install Python:
    - Download and install Python from the official website (https://www.python.org/downloads/) or from the Microsoft Store. Ensure that pip is included during installation.

2. Clone the repository to your local machine:
    git clone https://github.com/ProdITdept/Kanban

3. Navigate to the project directory:
    cd Kanban

4. Install the required dependencies using pip and the provided requirements.txt file:
    pip install -r dependencies.txt

5. Run the Flask application using the following command:
    python app.py

6. Access the web form through your preferred web browser at http://localhost:5000.
7. Fill out the form with the required details and click the "Submit" button.
8. The application will generate a PDF document containing the submitted data, along with QR code and barcode images for easy tracking and identification.

