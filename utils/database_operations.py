import pyodbc
import streamlit as st

server = 'localhost'
database = 'ID_INFO'

@st.cache_resource(show_spinner="Connecting to the database...")
def create_table_if_not_exists():
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes')
        cursor = conn.cursor()
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
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes')
        cursor = conn.cursor()
        print('update',update)
        if update:      
            for data in data_list:
                cursor.execute("""
                    UPDATE id_card_info
                    SET name = ?, gender = ?, in_time = ?, out_time = ?, action = ?, duration = ?
                    WHERE face_id = ?
                """, data[1:] + (data[0],))
                print('information updated successsfully')
        else:
            for data in data_list:
                cursor.execute("""
                    INSERT INTO id_card_info (face_id, name, gender, in_time, out_time, action, duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, data)
                print('information inserted successsfully')
        
        conn.commit()
        cursor.close()
        conn.close()
    except pyodbc.Error as e:
        print("Error: Could not connect to database or execute query.")
        print(e)

def fetch_all_data():
    #data = [{'face_id': '3283b255-fd10-4b94-8b10-e8dd1bf090b2', 'name': 'Sandhiya B', 'gender': 'woman', 'in_time': datetime.datetime(2024, 7, 10, 17, 54, 11), 'out_time': datetime.datetime(2024, 7, 10, 17, 54, 48), 'action': 'out', 'duration': 37.0}, 
    #{'face_id': 'ff227d09-9c42-4499-8f5b-959bfb57fb36', 'name': 'Ajithkumar Velmurugan', 'gender': 'man', 'in_time': datetime.datetime(2024, 7, 10, 17, 57, 6), 'out_time': datetime.datetime(2024, 7, 10, 17, 57, 52), 'action': 'out', 'duration': 46.0}]
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM id_card_info")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        conn.close()
        return data
    except pyodbc.Error as e:
        print("Error: Could not connect to database or execute query.")
        print(e)
        return []
