# Import required libraries
import sqlite3  # SQLite library to interact with the database
import pandas as pd  # Pandas to read and handle the CSV file

# 1. Load the CSV data into a DataFrame
csv_file = 'Sales Performance - advertising.csv'  # Path to the CSV file
data = pd.read_csv(csv_file)  # Read CSV into a pandas DataFrame

# Normalize column names to lowercase for consistency
data.columns = data.columns.str.lower()

# Display first few rows to check data
print("Loaded Data:")
print(data.head())  # Display first 5 rows to confirm

# 2. Create and Connect to a SQLite Database
conn = sqlite3.connect('sales_performance.db')
cursor = conn.cursor()  # Create a cursor to execute SQL queries

# 3. Create the 'advertising_data' table in the SQLite database
cursor.execute('''
CREATE TABLE IF NOT EXISTS advertising_data (
    TV REAL,
    Radio REAL,
    Newspaper REAL,
    Sales REAL
);
''')
conn.commit()  # Commit the transaction to save the changes

# 4. Insert data from the pandas DataFrame into the SQLite database
for index, row in data.iterrows():
    cursor.execute('''
    INSERT INTO advertising_data (TV, Radio, Newspaper, Sales)
    VALUES (?, ?, ?, ?)
    ''', (row['tv'], row['radio'], row['newspaper'], row['sales']))

conn.commit()  # Commit to save the inserted rows into the database

# 5. Perform SQL Queries for Data Analysis

# Example 1: Get the total advertising spend and total sales
cursor.execute('''
SELECT 
    SUM(TV) AS total_tv_spend,
    SUM(Radio) AS total_radio_spend,
    SUM(Newspaper) AS total_newspaper_spend,
    SUM(Sales) AS total_sales
FROM advertising_data;
''')
total_spend_sales = cursor.fetchone()  # Fetch the result
print("\nTotal Advertising Spend and Sales:")
print(f"Total TV Spend: {total_spend_sales[0]:.2f} thousand")
print(f"Total Radio Spend: {total_spend_sales[1]:.2f} thousand")
print(f"Total Newspaper Spend: {total_spend_sales[2]:.2f} thousand")
print(f"Total Sales: {total_spend_sales[3]:.2f} thousand")

# Example 2: Calculate average spend for each medium and average sales
cursor.execute('''
SELECT 
    AVG(TV) AS avg_tv_spend,
    AVG(Radio) AS avg_radio_spend,
    AVG(Newspaper) AS avg_newspaper_spend,
    AVG(Sales) AS avg_sales
FROM advertising_data;
''')
avg_spend_sales = cursor.fetchone()  # Fetch the result
print("\nAverage Spend and Sales:")
print(f"Average TV Spend: {avg_spend_sales[0]:.2f} thousand")
print(f"Average Radio Spend: {avg_spend_sales[1]:.2f} thousand")
print(f"Average Newspaper Spend: {avg_spend_sales[2]:.2f} thousand")
print(f"Average Sales: {avg_spend_sales[3]:.2f} thousand")

# Example 3: Analyze sales and media spending relationship (TV vs Sales)
cursor.execute('''
SELECT TV, Sales 
FROM advertising_data
ORDER BY TV;
''')
tv_sales_data = cursor.fetchall()  # Get all rows from the query

print("\nTV Spend vs. Sales (Top 5 Entries):")
for row in tv_sales_data[:5]:
    print(f"TV Spend: {row[0]:.2f} | Sales: {row[1]:.2f}")

# Example 4: ROI Calculation (Return on Investment) for each medium
cursor.execute('''
SELECT 
    TV, Sales, 
    CASE WHEN TV != 0 THEN Sales / TV ELSE 0 END AS tv_roi,
    Radio, 
    CASE WHEN Radio != 0 THEN Sales / Radio ELSE 0 END AS radio_roi,
    Newspaper, 
    CASE WHEN Newspaper != 0 THEN Sales / Newspaper ELSE 0 END AS newspaper_roi
FROM advertising_data;
''')
roi_data = cursor.fetchall()  # Get all ROI data

print("\nSample ROI Data (TV, Radio, Newspaper vs Sales):")
for row in roi_data[:5]:  # Display first 5 results
    print(f"TV ROI: {row[2]:.2f}, Radio ROI: {row[4]:.2f}, Newspaper ROI: {row[6]:.2f} | Sales: {row[1]:.2f}")

# 7. Optionally, save processed data to a new CSV file
output_csv_file = "processed_sales_data.csv"
data.to_csv(output_csv_file, index=False)
print(f"\nProcessed data saved to {output_csv_file}")

# Execute queries from queries.sql file
with open("queries.sql", "r") as file:
    sql_script = file.read()

cursor.executescript(sql_script)

print("\nQueries from queries.sql executed successfully!")

cursor.execute("SELECT SUM(Sales) FROM advertising_data")
print("Total Sales:", cursor.fetchone()[0])

# 6. Close the connection to the database
conn.close()