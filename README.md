# Business Card Extractor and Database Manager

This is a Streamlit-based web application that allows users to upload business card images, extract information using EasyOCR, and manage the extracted data in a MySQL database.

## Features

- **Upload Tab:**
  - Users can upload a business card image (in jpg or png format).
  - The application extracts information such as name, designation, company name, phone number, email, etc., using the EasyOCR library.
  - Extracted information is displayed in a DataFrame.
  - Users can save the extracted data to a MySQL database.

- **Modify Tab:**
  - Users can search for business card data based on email.
  - Retrieved data is displayed with options to edit and delete.
  - Data updates are reflected in the MySQL database.

## Prerequisites

- Python 3.x
- MySQL server
- Required Python libraries

## Installation

- Streamlit
- EasyOCR
- pandas
- PIL
- mysql.connector


