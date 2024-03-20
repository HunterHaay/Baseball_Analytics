import pyodbc

# Specify the file path to the MS Access database
database_path = "C:/Users/wagnerbl20/Downloads/lahman_1871-2022.mdb"

try:
    # Connect to the MS Access database
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + database_path)
    cursor = conn.cursor()

    # SQL query to select necessary columns from the Batting table
    sql_query = """
        SELECT playerID, AB, BB, HBP, SF, SH
        FROM Batting;
    """

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all rows from the result set
    batting_data = cursor.fetchall()

    # Dictionary to store plate appearances for each player
    plate_appearances = {}

    # Calculate plate appearances for each player and update the dictionary
    for row in batting_data:
        player_id, ab, bb, hbp, sf, sh = row
        # Check for null values and replace them with 0
        ab = ab if ab is not None else 0
        bb = bb if bb is not None else 0
        hbp = hbp if hbp is not None else 0
        sf = sf if sf is not None else 0
        sh = sh if sh is not None else 0
        pa = ab + bb + hbp + sf + sh
        plate_appearances[player_id] = pa

    # Update the Batting table to add a new field named "PA" for plate appearances
    cursor.execute("ALTER TABLE Batting ADD COLUMN PA INTEGER")

    # Update the new "PA" field with the calculated plate appearances
    for player_id, pa in plate_appearances.items():
        cursor.execute(f"UPDATE Batting SET PA = ? WHERE playerID = ?", (pa, player_id))

    # Commit the transaction
    conn.commit()

    print("Plate appearances calculated and updated in the Batting table.")

except pyodbc.Error as e:
    print("Error connecting to the database:", e)

finally:
    # Close the database connection
    if conn:
        conn.close()
