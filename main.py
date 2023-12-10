import streamlit as st
import cv2
import easyocr
import numpy as np
from PIL import Image
import re
import mysql.connector 
import pandas as pd
from mysql.connector import IntegrityError

# Connect to the MySQL server
isSave=False
con = mysql.connector.connect(
    host="localhost",
    user="username",  # Replace with your actual username
    password="password",  # Replace with your actual password
)

# Create a cursor object
cursor = con.cursor()

# Create the database "businesscard_db" if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS businesscard_db")

# Use the "businesscard_db" database
cursor.execute("USE businesscard_db")

# Create the table "bizcard" if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS bizcard (
    Name VARCHAR(255) NOT NULL,
    Designation VARCHAR(255) NOT NULL,
    Company_name VARCHAR(255) NOT NULL,
    Phone_Number VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) PRIMARY KEY NOT NULL,
    Website VARCHAR(255),
    Address VARCHAR(255),
    Pincode VARCHAR(10),
    City VARCHAR(255) NOT NULL,
    State VARCHAR(255) NOT NULL
);
"""
cursor.execute(create_table_query)

# Print confirmation message
print("Database 'businesscard_db' and table 'bizcard' created successfully!")

# Close the connection
con.close()


css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5Srem;
    width:150px
    }

</style>
'''

st.markdown(css, unsafe_allow_html=True)

col1, col2, col3 = st.tabs(["Home","Upload","Modify"])

with col1:

    st.title("Home")
    
    
    st.write("""
    ## Business Card Extractor and Database Manager

    Welcome to the Business Card Extractor and Database Manager! This Streamlit-based web application is designed to streamline the process of extracting information from business cards and managing the data efficiently.

    ### Features

    - **Business Card Extraction:**
        - Upload business card images (in jpg or png format).
        - Utilize EasyOCR for accurate text extraction.
        - Extracted information includes name, designation, company name, phone number, email, etc.

    - **Database Management:**
        - Save extracted data to a MySQL database.
        - Search, edit, and delete business card details from the database.
""")
      
with col2:

    st.write("Extract and Upload")

    con = mysql.connector.connect(
        host="localhost",
        user="username",  # Replace with your actual username
        password="password",  # Replace with your actual password
        database="businesscard_db"
    )
    # Upload an image file
    image_file = st.file_uploader("Upload a business card image", type=['jpg', 'png'])
    isShow=st.button('Show Database')

    if isShow:
        try:    
            query="""select * from bizcard;"""
            df=pd.read_sql(query,con=con)
            st.dataframe(df)
        except:
            st.warning("Something went wrong!")

    # Process the uploaded image if it exists
    if image_file is not None:
        # Read the image file as an OpenCV image
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image")

        image = Image.open(image_file)

        # Initialize reader 
        reader = easyocr.Reader(['en'])

        # Extract text 
        extracted_text = reader.readtext(np.array(image))
        text = []
       # print(extracted_text)

        def count_numbers(string):
            count = 0
            for char in string:
                if char.isdigit():
                    count += 1
            return count
        results={'Name': [], 'Designation': [], 'Company name': [], 'Phone Number': [], 'Email': [], 'Website': [],
               'Address': [], 'Pincode': [], 'City':[],'State':[]}
        companyname=""
        for idx,detection in enumerate(extracted_text):
            iscity=0
            iscompany=True
            if idx==0:
                results['Name'].append(detection[1])
            if idx==1:
                results['Designation'].append(detection[1])
            match1 = re.findall('.+St , ([a-zA-Z]+).+', detection[1])
            match2 = re.findall('.+St,, ([a-zA-Z]+).+', detection[1])
            match3 = re.findall('^[E].*', detection[1])
            iscity=len(match1)+len(match2)+len(match3)
            if "TamilNadu" in detection[1] and len(results['State'])==0:
                results["State"].append('TamilNadu')
            if match1:
                results["City"].append(match1[0])
            elif match2:
                results["City"].append(match2[0])
            elif match3:
                results["City"].append(match3[0])
            elif "@" in detection[1] and "." in detection[1]:
                results["Email"].append(detection[1])
                continue
            elif "-" in detection[1] and count_numbers(detection[1])>=9:
                results["Phone Number"].append(detection[1])
                continue
            if not detection[1].isalnum() and count_numbers(detection[1])!=0  and (count_numbers(detection[1])!=6 and count_numbers(detection[1])!=7):
                results["Address"].append(detection[1])
                continue

            elif (count_numbers(detection[1])==6 or count_numbers(detection[1])==7):
                if len(detection[1]) !=6:
                    results["Pincode"].append(detection[1].split()[1])              
                    continue
                else:
                    results["Pincode"].append(detection[1])
            elif "www " in  detection[1].lower() or "www." in  detection[1].lower():
                results["Website"].append(detection[1])
                continue
            elif "WWW" in  detection[1]:
                results["Website"].append(extracted_text[4][1] + "." + extracted_text[5][1])
                continue
            elif(detection[0][2][1]>460 and detection[0][3][1]>460 and 'St' not in detection[1] and iscity==0):
                companyname+=detection[1]+" "
            
            
        results["Company name"].append(companyname)
        data=[]
        for key,val in results.items():
            results[key]=','.join(val)
            data.append(','.join(val))
        df=pd.DataFrame(results,index=[1])
        st.dataframe(df)
        isSave=st.button('Save Database')
        
        
        if isSave:
            # Create a cursor object
            cursor = con.cursor()
            try:
                insert_query = """
                            INSERT INTO bizcard (Name, Designation, Company_name, Phone_Number, Email, Website, Address, Pincode, City, State)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                cursor.execute(insert_query, data)
                con.commit()
                # Print confirmation message
                st.success("Data inserted successfully!")
            except IntegrityError:
                st.warning("Duplicate entries are not allowed!")
            except:
                st.warning("Something went wrong!")
            finally:
                con.close()


with col3:  


    # Connect to the MySQL server
    con = mysql.connector.connect(
        host="localhost",
        user="username",  # Replace with your actual username
        password="password",  # Replace with your actual password
        database="businesscard_db",
    )

    # Create a cursor object
    cursor = con.cursor()

    # Define function to retrieve data based on email
    def get_data(email):
        query = """
        SELECT * FROM bizcard WHERE Email = %s;
        """
        cursor.execute(query, (email,))
        data = cursor.fetchone()
        if data:
            return dict(zip([column[0] for column in cursor.description], data))
        else:
            return None

    # Get email address from user input
    email = st.text_input("Enter the email address:")

    # Retrieve data using the email address
    data = get_data(email)

    # Check if data was retrieved
    if data:
        # Display retrieved data
        st.header("Business card details")

        with st.form(key="edit_form"):
            for key, value in data.items():
                if key != "Email":
                    data[key] = st.text_input(f"{key}:", value, key=key)

            email_input = st.text_input("Email:", email, key="Email", disabled=True)

            if st.form_submit_button("Edit"):
                # Update data form
                update_values = [data[key] for key in data if key != "Email"]
                update_values.append(data['Email'])

                # Update data in the database
                update_query = """
                UPDATE bizcard
                SET Name = %s, Designation = %s, Company_name = %s, Phone_Number = %s, Website = %s, Address = %s, Pincode = %s, City = %s, State = %s
                WHERE Email = %s;
                """
                cursor.execute(update_query, update_values)
                con.commit()
                st.success("Data updated successfully!")

                # Reload data after update
                data = get_data(email)


        # Delete functionality
        if st.button("Delete"):
            # Confirmation message
            
                # Delete data from the database
                delete_query = """
                DELETE FROM bizcard WHERE Email = %s;
                """
                cursor.execute(delete_query, (email,))
                con.commit()
                st.success("Data deleted successfully!")
                # Clear data from the page and form
                data = None
                email_input= ""
    else:
        st.warning("No data found for the given email address.")

    # Close the connection
    con.close()
