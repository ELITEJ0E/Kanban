# FJ Kanban Web Application

The FJ Kanban Web Application is designed to streamline the process of submitting manufacturing data using Kanban principles.
It provides a simple user interface for inputting details such as wood species, size, dimensions, machine ID, and trolley number.
The application then generates a PDF document containing the submitted data along with QR code and barcode images for easy tracking and identification.


## ERPNext Doctype Setup:
- This guide provides step-by-step instructions on how to set up the FJ Kanban doctype in ERPNext, including adding the necessary fields and configuring field properties.

## Prerequisites
- Ensure you have ERPNext installed and running.
- You need administrator access to ERPNext to create and configure doctypes.

## Step-by-Step Setup
### 1. Create the FJ Kanban Doctype

**1. Log in to ERPNext:**
- Open your ERPNext instance and log in with your administrator credentials.

**2. Navigate to Doctype List:**
- Go to the ERPNext Desk.
- In the search bar, type "DocType List" and select it.

**3. Create a New Doctype:**

- Click the "New" button to create a new doctype.
- Fill in the following details:
	- Name: FJ Kanban
	- Module: Choose the relevant module (e.g., Manufacturing or Custom).
	- Naming: By "naming_series" field
- **Save the doctype.**

## 2. Add Fields to the Doctype
**Fields:** 
- Timestamp, Lot, Department, Barcode, Qr Code, 	***(set to hidden)***
- Size, Species, L x W x H, MC ID, Date, Trolley#, Status 	***(Mandatory)***
- Start Time, Paused Time, Resume Time, Stop Time 	***(set to read-only)***
![330292670-c3c2c9c9-1966-4af4-93f4-bf2551dd3c07](https://github.com/ELITEJ0E/Kanban/assets/155508356/2112930c-c9bf-4c24-83d1-4618abc48b23)


## 3. Configure Naming Series
**1. Open Naming Series:**
- In the search bar, type "Naming Series" and select it.
- Add a new naming series for the FJ Kanban doctype with the format YY.MM.DD.###.

**2. Assign Naming Series to Doctype:**
- Go back to the FJ Kanban doctype.
- Set the "Naming Series" field to the format you created (YY.MM.DD.###).

## 4. Finalize and Test
**1. Save and Publish:**
- Save the FJ Kanban doctype.
- Ensure there are no validation errors and the doctype is published.

**2. Test the Doctype:**
- Create a new FJ Kanban document to test the setup.
- Verify that all fields are present and correctly configured.
- Ensure the naming series is applied correctly.

## 5. Additional Configurations (Optional)
**Permissions:**
- Configure permissions to control who can create, read, update, and delete FJ Kanban documents.
**Custom Scripts:**
- Add custom scripts if you need additional automation or validations.

## Conclusion
By following these steps, you have successfully set up the FJ Kanban doctype in ERPNext with all required fields and configurations. Ensure to test thoroughly and adjust configurations as necessary to fit your specific workflow requirements.


## Getting API:

**1. Enable API Access:**
	- Log in to your ERPNext instance as an administrator.
	- Go to Settings > API and Integrations.
	- Enable API access if it's not already enabled.

**2. Create an API Key:**
	- Navigate to Settings > API and Integrations > API Access.
	- Create a new API Key with the necessary permissions to access the resources required by your Python script.

**3. Configure Permissions:**
	- Ensure that the user associated with the API Key has adequate permissions to access the resources
	  and perform the required actions (e.g., read, write, create, delete) on the FJ Kanban resource.

**4. Get the API URL:**
	- Determine the URL endpoint for accessing the FJ Kanban resource. This typically follows the format http://<your_erpnext_instance>/api/resource/FJ%20Kanban.

**5. Update the Python Script:**
	- Modify the get_from_erpnext() function in your Python script to use the correct API URL, headers, and authentication token:

![329983054-455d7594-5536-4504-a7c0-6cb769df6507](https://github.com/ELITEJ0E/Kanban/assets/155508356/afb7da5c-2eea-497d-b8e7-a38b573e546d)
![329982789-f1bb2545-5224-42a8-a643-22793dee7e5d](https://github.com/ELITEJ0E/Kanban/assets/155508356/6a35673e-0c99-4e1e-9cf7-dcbdf10a1c23)


## Installing Adobe Acrobat Reader:

**1. Visit the official Adobe Acrobat Reader download page at *https://get.adobe.com/reader/*.**

**2. Modify the directory to your own desired directories**
![329987175-be275948-7688-4ec1-969d-96b3841499c4](https://github.com/ELITEJ0E/Kanban/assets/155508356/9d6cfd47-2814-4329-8c32-c245c4f53f15)


## How to Use:

**1. Install Python:**
- Download and install Python from the official website (https://www.python.org/downloads/) or from the Microsoft Store. Ensure that pip is included during installation.

**2. Clone the repository to your local machine:**
- git clone https://github.com/ProdITdept/Kanban

**3. Navigate to the project directory:**
- cd Kanban

**4. Install the required dependencies using pip and the provided dependencies.txt file:**
- pip install -r dependencies.txt


**5. Run the Flask application using the following command:**
- python app.py
 
  ***If everything works up until this step, you should be seeing this:***
  
![329984953-c0ec210a-e69f-4928-8dfe-e94405385bbd](https://github.com/ELITEJ0E/Kanban/assets/155508356/4486a5ec-011d-49d9-b3f6-c6f441c71a17)

**6. Access the web form through your preferred web browser at http://localhost:5000.**

**7. Fill out the form with the required details and click the "Submit" button.**

**8. The application will generate a PDF document containing the submitted data, along with QR code and barcode images for easy tracking and identification.**


## Node-RED flow
- import the flow from **Kanban.json**

![330334210-b11d91b0-e7c3-4a15-bf5a-282a01db5fc9](https://github.com/ELITEJ0E/Kanban/assets/155508356/f4549722-83c3-4250-af53-a9f2646e22d8)

**- The flow should be able to change the status of the doctype**
![image](https://github.com/ELITEJ0E/Kanban/assets/155508356/f5b941f1-e901-4469-bb55-0821fc05ac2d)



*Author*
*Joel*
