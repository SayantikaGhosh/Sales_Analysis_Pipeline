import pandas as pd
import mysql.connector
from mysql.connector import Error

# MySQL connection config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin1234',  # 🔒 Replace with your actual password
    'database': 'sales_db'
}

CSV_PATH = 'dags/data/sales_data.csv'

try:
    # ✅ Read and preprocess CSV
    df = pd.read_csv(CSV_PATH)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')  # MySQL-friendly

    # ✅ Connect to MySQL
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # ✅ Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            product VARCHAR(255),
            category VARCHAR(100),
            quantity INT,
            revenue FLOAT,
            region VARCHAR(100),
            payment_method VARCHAR(100)
        );
    """)

    # ✅ Insert data row by row
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO sales_data (date, product, category, quantity, revenue, region, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))

    connection.commit()
    print("✅ Data loaded successfully into MySQL!")

except Error as e:
    print(f"❌ MySQL Error: {e}")
except Exception as ex:
    print(f"⚠️ Error: {ex}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
