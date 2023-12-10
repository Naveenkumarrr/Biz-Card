# Business Card Extractor and Database Manager

This is a Streamlit-based web application that allows users to upload business card images, extract information using EasyOCR, and manage the extracted data in a MySQL database.

### Features

    - **Business Card Extraction:**
        - Upload business card images (in jpg or png format).
        - Utilize EasyOCR for accurate text extraction.
        - Extracted information includes name, designation, company name, phone number, email, etc.

    - **Database Management:**
        - Save extracted data to a MySQL database.
        - Search, edit, and delete business card details from the database.

 ### How to Use

    1. **Upload Tab:**
        - Navigate to the "Upload" tab.
        - Upload a business card image.
        - View the extracted information in a DataFrame.
        - Save the data to the MySQL database using the "Save Database" button.


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


