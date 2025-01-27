import pyodbc
import streamlit as st

# Database connection details
server = 'YOGESH-522099\YOGESH'
database = 'ID_INFO'

@st.cache_resource(show_spinner="Connecting to the database...")
def create_table_if_not_exists():
    """
    Creates the 'id_card_info' table in the database if it does not already exist.
    The table contains columns for face ID, name, gender, in-time, out-time, action, and duration.
    """
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes')
        cursor = conn.cursor()
        
        # Execute SQL query to create table if it does not exist
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='id_card_info' AND xtype='U')
            CREATE TABLE id_card_info (
                face_id NVARCHAR(50) PRIMARY KEY,
                name NVARCHAR(100),
                gender NVARCHAR(10),
                in_time DATETIME,
                out_time DATETIME NULL,
                action NVARCHAR(10),
                duration FLOAT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except pyodbc.Error as e:
        print("Error: Could not connect to database or execute query.")
        print(e)

def save_data_to_db(data_list, update=False):
    """
    Saves data to the 'id_card_info' table in the database.

    Parameters:
    - data_list (list of tuples): List containing data to be inserted or updated in the database.
    - update (bool): Flag indicating whether to update existing records (True) or insert new records (False).
    """
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes')
        cursor = conn.cursor()
        
        if update:
            # Update existing records in the database
            for data in data_list:
                cursor.execute("""
                    UPDATE id_card_info
                    SET name = ?, gender = ?, in_time = ?, out_time = ?, action = ?, duration = ?
                    WHERE face_id = ?
                """, data[1:] + (data[0],))
                print('Information updated successfully')
        else:
            # Insert new records into the database
            for data in data_list:
                cursor.execute("""
                    INSERT INTO id_card_info (face_id, name, gender, in_time, out_time, action, duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, data)
                print('Information inserted successfully')
        
        conn.commit()
        cursor.close()
        conn.close()
    except pyodbc.Error as e:
        print("Error: Could not connect to database or execute query.")
        print(e)

def fetch_all_data():
    """
    Fetches all records from the 'id_card_info' table in the database.

    Returns:
    - list of dicts: Each dictionary represents a row from the table with column names as keys.
    """
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes')
        cursor = conn.cursor()
        
        # Execute SQL query to fetch all records
        cursor.execute("SELECT * FROM id_card_info")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        
        # Convert rows to a list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        conn.close()
        return data
    except pyodbc.Error as e:
        print("Error: Could not connect to database or execute query.")
        print(e)
        return []
