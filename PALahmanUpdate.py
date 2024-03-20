import pyodbc

# Specify the file path to the MS Access database
database_path = "C:/Users/wagnerbl20/Downloads/lahman_1871-2022.mdb"

try:
    # Connect to the MS Access database
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + database_path)
    cursor = conn.cursor()

    # Alter the Batting table to add a new column PA
    cursor.execute("ALTER TABLE Batting ADD COLUMN PA INTEGER")

    # Calculate plate appearances (PA) for each row in the Batting table and update the PA column
    cursor.execute("""
        UPDATE Batting 
        SET PA = AB + BB + HBP + SF + SH;
    """)

    # Commit the transaction
    conn.commit()

    print("Plate appearances calculated and updated in the Batting table.")

except pyodbc.Error as e:
    print("Error connecting to the database:", e)

finally:
    # Close the database connection
    if conn:
        conn.close()
