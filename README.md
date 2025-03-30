# JOOR to Shopify Converter

This project converts JOOR "to size" Excel files into Shopify-ready CSV files.

## Files Overview

- **converter.py:** Contains the conversion logic to process JOOR Excel files.
- **app.py:** A Flask web application that exposes an endpoint to upload JOOR files and returns a Shopify CSV.
- **requirements.txt:** Lists all the Python dependencies required by the project.
- **.gitignore:** Specifies files to be ignored by Git.

## How to Use

### Locally
1. **Install Dependencies:**  
   Run:
   pip install -r requirements.txt
2. **Run the Flask App:**  
   Run:
   python app.py
3. **Test the Endpoint:**  
   Use a tool like Postman or cURL to POST a JOOR Excel file to:
   http://localhost:5000/convert  
   The converted Shopify CSV file will be returned for download.

### Deployment on Render
1. Push this repository to GitHub.
2. In Render, create a new Web Service connecting to this repository.
3. Set the **Build Command** to:
   pip install -r requirements.txt
4. Set the **Start Command** to:
   gunicorn app:app
5. Configure required environment variables (like folder IDs and OAuth credentials) in Render.
6. Deploy and test your service using the provided URL.

## Environment Variables (on Render)
- GOOGLE_DRIVE_JOOR_FOLDER_ID: Folder ID for JOOR input files.
- GOOGLE_DRIVE_SHOPIFY_OUTPUT_FOLDER_ID: Folder ID for Shopify CSV output.
- (Optional) GOOGLE_DRIVE_STOCKY_OUTPUT_FOLDER_ID: Folder ID for Stocky CSV output.
- GOOGLE_OAUTH_CREDENTIALS: Your OAuth credentials as a JSON string (if using Google Drive API).

Enjoy automating your workflow!
